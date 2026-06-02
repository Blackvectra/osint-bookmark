#!/usr/bin/env python3
"""Organize a browser bookmark export into a clean, categorized collection.

Reads every Netscape-format bookmark HTML file under an input directory
(default: favorites/inbox/), extracts each link, sorts it into a category,
and regenerates a foldered bookmark file plus a README table of contents.

Organize it **your way**: drop a `favorites/organize.config.json` next to your
inbox to define your own categories, the domain/keyword rules that fill them,
their folder order, and a "frequently used" pin list that floats to the top.
Without a config, security/pentest-flavored defaults are used.

Categorization is **hybrid**:
  1. Rule-based — fast, free, deterministic domain/keyword matching.
  2. Claude API — anything the rules don't catch is sent to Claude, but only
     when ANTHROPIC_API_KEY is set. Without a key, unmatched links fall back
     to "Uncategorized" so the tool still works fully offline.

The Claude call uses the standard library only (urllib) — no SDK dependency.

Note on "most used": browser bookmark exports do **not** include visit counts,
so usage frequency can't be detected automatically. Pin your most-used sites
via the config `frequent` list (they get their own top folder), and sort the
rest by `recent` (date added) or `name`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

# --- Parsing -----------------------------------------------------------------

# Netscape bookmark entry: <DT><A HREF="url" ADD_DATE="..." ...>Title</A>
ENTRY_RE = re.compile(
    r'<DT><A\s+HREF="(?P<url>[^"]+)"(?P<attrs>[^>]*)>(?P<title>.*?)</A>',
    re.IGNORECASE | re.DOTALL,
)
ADD_DATE_RE = re.compile(r'ADD_DATE="(\d+)"', re.IGNORECASE)

FREQUENT_FOLDER = "★ Frequently Used"  # ★


class Entry:
    """One bookmark: title, url, and the unix ADD_DATE (0 if absent)."""

    __slots__ = ("title", "url", "added")

    def __init__(self, title: str, url: str, added: int):
        self.title, self.url, self.added = title, url, added


def extract_entries(html: str) -> list[Entry]:
    """Return Entry objects for http(s) bookmarks in the HTML."""
    out: list[Entry] = []
    for m in ENTRY_RE.finditer(html):
        url = m.group("url")
        if not url.startswith(("http://", "https://")):
            continue
        title = re.sub(r"\s+", " ", m.group("title")).strip() or url
        date_m = ADD_DATE_RE.search(m.group("attrs"))
        out.append(Entry(title, url, int(date_m.group(1)) if date_m else 0))
    return out


# --- Configuration -----------------------------------------------------------

# Security/pentest-flavored defaults. Each category maps to a list of
# substrings matched (case-insensitively) against the URL or title; first
# category to match wins. Override any of this via organize.config.json.
DEFAULT_CONFIG: dict = {
    # "name" (alphabetical) or "recent" (newest first by date added).
    "sort": "name",
    # Substrings that float a link into the "Frequently Used" top folder —
    # this is your manual "most used" pin list (export data has no visit counts).
    "frequent": [],
    "categories": {
        "Recon & OSINT": ["nmap", "masscan", "shodan", "censys", "maltego",
                          "spiderfoot", "osintframework", "amass", "harvester",
                          "recon-ng", "virustotal", "urlscan"],
        "Web App Testing": ["portswigger", "burp", "zaproxy", "sqlmap", "nikto",
                            "ffuf", "gobuster", "nuclei", "wpscan"],
        "Exploitation & C2": ["metasploit", "exploit-db", "exploit-database",
                              "impacket", "sliver", "cobaltstrike"],
        "Passwords & Creds": ["hashcat", "openwall.com/john", "thc-hydra",
                             "haveibeenpwned", "crackstation", "hashes.com"],
        "Active Directory": ["bloodhound", "netexec", "crackmapexec", "mimikatz",
                            "responder", "certipy", "kerbrute"],
        "Network & Wireless": ["wireshark", "aircrack", "tcpdump", "tshark"],
        "Threat Intel": ["abuseipdb", "alienvault", "otx.", "greynoise", "misp",
                        "opencti", "threatfox"],
        "Forensics & RE": ["ghidra", "volatility", "autopsy", "cyberchef",
                          "rada.re", "radare", "cutter", "ghidra-sre"],
        "Learning & CTF": ["hackthebox", "tryhackme", "web-security", "picoctf",
                          "overthewire", "vulnhub", "root-me", "cyberdefenders",
                          "hackthissite"],
        "Cheat Sheets & Refs": ["hacktricks", "payloadsallthethings", "gtfobins",
                               "lolbas", "owasp", "seclists"],
        "Dev & Tooling": ["github.com", "gitlab.com", "stackoverflow", "pypi.org",
                         "npmjs"],
        "Reading": ["medium.com", "substack", "/blog", "news.ycombinator"],
    },
}


def load_config(path: Path) -> dict:
    """Load organize.config.json, falling back to defaults for missing keys."""
    config = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if path.is_file():
        user = json.loads(path.read_text(encoding="utf-8"))
        config.update({k: user[k] for k in ("sort", "frequent", "categories") if k in user})
        print(f"Using config: {path}")
    return config


def categorize_by_rule(entry: Entry, config: dict) -> str | None:
    """Return a category from the config rules, or None if nothing matches."""
    hay = f"{entry.title} {entry.url}".lower()
    for needle in config["frequent"]:
        if needle.lower() in hay:
            return FREQUENT_FOLDER
    for category, needles in config["categories"].items():
        if any(n.lower() in hay for n in needles):
            return category
    return None


# --- Claude-backed categorization (stdlib only) ------------------------------

DEFAULT_MODEL = "claude-haiku-4-5"  # cheap classification; override via ANTHROPIC_MODEL
API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
BATCH_SIZE = 40


def _system_prompt(categories: list[str]) -> str:
    return (
        "You are a bookmark categorizer. Each user message is a JSON array of "
        "bookmarks, each with an integer `i`, a `title`, and a `url`. Assign "
        "every bookmark to exactly one of these categories:\n"
        + "\n".join(f"- {c}" for c in categories)
        + '\nUse "Other" only if none fit. Judge by the site and title.'
    )


def _classify_batch(
    batch: list[Entry], categories: list[str], model: str, api_key: str
) -> dict[int, str]:
    user_payload = json.dumps(
        [{"i": i, "title": e.title, "url": e.url} for i, e in enumerate(batch)],
        ensure_ascii=False,
    )
    schema = {
        "type": "object",
        "properties": {
            "assignments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "i": {"type": "integer"},
                        "category": {"type": "string", "enum": categories + ["Other"]},
                    },
                    "required": ["i", "category"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["assignments"],
        "additionalProperties": False,
    }
    body = {
        "model": model,
        "max_tokens": 4000,
        # System prompt cached as a prefix (engages once it exceeds the model's
        # ~4096-token minimum; a short taxonomy simply won't be cached).
        "system": [
            {"type": "text", "text": _system_prompt(categories),
             "cache_control": {"type": "ephemeral"}}
        ],
        "messages": [{"role": "user", "content": user_payload}],
        "output_config": {"format": {"type": "json_schema", "schema": schema}},
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("usage", {}).get("cache_read_input_tokens"):
        print(f"  (cache hit: {data['usage']['cache_read_input_tokens']} tokens)")
    text = "".join(b["text"] for b in data["content"] if b.get("type") == "text")
    return {a["i"]: a["category"] for a in json.loads(text)["assignments"]}


def classify_with_claude(
    items: list[Entry], categories: list[str], model: str, api_key: str
) -> dict[int, str]:
    """Categorize all items via Claude, in batches. Returns {global_index: cat}."""
    result: dict[int, str] = {}
    for start in range(0, len(items), BATCH_SIZE):
        batch = items[start : start + BATCH_SIZE]
        print(f"  classifying {start + 1}-{start + len(batch)} of {len(items)}...")
        try:
            local = _classify_batch(batch, categories, model, api_key)
        except (urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
            print(f"::warning::Claude batch failed ({exc}); leaving as Uncategorized.")
            continue
        for local_i, category in local.items():
            result[start + local_i] = category
    return result


# --- Output generation -------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def order_categories(grouped: dict[str, list[Entry]], config: dict) -> list[str]:
    """Folder order: Frequently Used first, then config order, then extras."""
    order: list[str] = []
    if FREQUENT_FOLDER in grouped:
        order.append(FREQUENT_FOLDER)
    order += [c for c in config["categories"] if c in grouped]
    order += sorted(c for c in grouped if c not in order)
    return order


def _sorted_entries(entries: list[Entry], sort: str) -> list[Entry]:
    if sort == "recent":
        return sorted(entries, key=lambda e: e.added, reverse=True)
    return sorted(entries, key=lambda e: e.title.lower())


def render_bookmark_html(grouped: dict[str, list[Entry]], config: dict) -> str:
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
    ]
    for category in order_categories(grouped, config):
        lines.append(f"    <DT><H3>{_esc(category)}</H3>")
        lines.append("    <DL><p>")
        for e in _sorted_entries(grouped[category], config["sort"]):
            lines.append(f'        <DT><A HREF="{_esc(e.url)}">{_esc(e.title)}</A>')
        lines.append("    </DL><p>")
    lines.append("</DL><p>")
    return "\n".join(lines) + "\n"


def render_readme(grouped: dict[str, list[Entry]], config: dict, total: int) -> str:
    lines = [
        "# Organized Bookmarks",
        "",
        f"_{total} links across {len(grouped)} categories, "
        "organized automatically._",
        "",
    ]
    for category in order_categories(grouped, config):
        lines.append(f"## {category}")
        lines.append("")
        for e in _sorted_entries(grouped[category], config["sort"]):
            lines.append(f"- [{e.title}]({e.url})")
        lines.append("")
    return "\n".join(lines)


# --- Main --------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inbox", default="favorites/inbox")
    parser.add_argument("--config", default="favorites/organize.config.json")
    parser.add_argument("--out-html", default="favorites/favorites.html")
    parser.add_argument("--out-readme", default="favorites/README.md")
    args = parser.parse_args()

    inbox = Path(args.inbox)
    sources = sorted(inbox.glob("*.html")) if inbox.is_dir() else []
    if not sources:
        print(f"No bookmark files found in {inbox}/ — nothing to organize.")
        return 0

    config = load_config(Path(args.config))

    # Collect + dedupe by URL (keep the earliest-seen title/date).
    by_url: dict[str, Entry] = {}
    for src in sources:
        for e in extract_entries(src.read_text(encoding="utf-8", errors="replace")):
            by_url.setdefault(e.url, e)
    entries = list(by_url.values())
    print(f"Found {len(entries)} unique links in {len(sources)} file(s).")

    grouped: dict[str, list[Entry]] = {}
    leftovers: list[Entry] = []
    for e in entries:
        category = categorize_by_rule(e, config)
        if category:
            grouped.setdefault(category, []).append(e)
        else:
            leftovers.append(e)
    print(f"Rules categorized {len(entries) - len(leftovers)}; "
          f"{len(leftovers)} need classification.")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    categories = list(config["categories"].keys())
    if leftovers and api_key:
        model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
        print(f"Classifying leftovers with Claude ({model})...")
        assigned = classify_with_claude(leftovers, categories, model, api_key)
        for i, e in enumerate(leftovers):
            category = assigned.get(i, "Uncategorized")
            grouped.setdefault("Uncategorized" if category == "Other" else category, []).append(e)
    elif leftovers:
        print("No ANTHROPIC_API_KEY set — leftovers go to Uncategorized.")
        grouped.setdefault("Uncategorized", []).extend(leftovers)

    Path(args.out_html).write_text(render_bookmark_html(grouped, config), encoding="utf-8")
    Path(args.out_readme).write_text(render_readme(grouped, config, len(entries)), encoding="utf-8")
    print(f"Wrote {args.out_html} and {args.out_readme} ({len(grouped)} categories).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
