#!/usr/bin/env python3
"""Organize a browser bookmark export into a clean, categorized collection.

Reads every Netscape-format bookmark HTML file under an input directory
(default: favorites/inbox/), extracts each link, sorts it into a category,
and regenerates a foldered bookmark file plus a README table of contents.

Categorization is **hybrid**:
  1. Rule-based — fast, free, deterministic domain/keyword matching.
  2. Claude API — anything the rules don't catch is sent to Claude for
     classification, but only when ANTHROPIC_API_KEY is set. Without a key,
     unmatched links fall back to "Uncategorized" so the tool still works
     fully offline.

The Claude call uses the standard library only (urllib) — no SDK dependency.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# --- Parsing -----------------------------------------------------------------

# Netscape bookmark entry: <DT><A HREF="url" ...>Title</A>
ENTRY_RE = re.compile(
    r'<DT><A\s+HREF="(?P<url>[^"]+)"[^>]*>(?P<title>.*?)</A>',
    re.IGNORECASE | re.DOTALL,
)


def extract_entries(html: str) -> list[tuple[str, str]]:
    """Return ordered (title, url) pairs for http(s) bookmarks in the HTML."""
    out: list[tuple[str, str]] = []
    for m in ENTRY_RE.finditer(html):
        url = m.group("url")
        if not url.startswith(("http://", "https://")):
            continue
        title = re.sub(r"\s+", " ", m.group("title")).strip() or url
        out.append((title, url))
    return out


# --- Rule-based categorization ----------------------------------------------

# The canonical category set. Claude is constrained to choose from these
# (plus "Other"); the rules below map known domains/keywords directly.
CATEGORIES = [
    "Development",
    "News & Reading",
    "Social & Communication",
    "Video & Media",
    "Shopping",
    "Finance",
    "Productivity & Tools",
    "Reference & Learning",
    "Design & Inspiration",
    "Travel",
]

# Substring (in host or full URL) -> category. First match wins.
DOMAIN_RULES: list[tuple[str, str]] = [
    ("github.com", "Development"),
    ("gitlab.com", "Development"),
    ("stackoverflow.com", "Development"),
    ("stackexchange.com", "Development"),
    ("npmjs.com", "Development"),
    ("pypi.org", "Development"),
    ("developer.mozilla.org", "Development"),
    ("news.ycombinator.com", "News & Reading"),
    ("medium.com", "News & Reading"),
    ("substack.com", "News & Reading"),
    ("nytimes.com", "News & Reading"),
    ("bbc.co", "News & Reading"),
    ("reddit.com", "Social & Communication"),
    ("twitter.com", "Social & Communication"),
    ("x.com", "Social & Communication"),
    ("linkedin.com", "Social & Communication"),
    ("facebook.com", "Social & Communication"),
    ("instagram.com", "Social & Communication"),
    ("mastodon", "Social & Communication"),
    ("slack.com", "Social & Communication"),
    ("discord.com", "Social & Communication"),
    ("youtube.com", "Video & Media"),
    ("youtu.be", "Video & Media"),
    ("vimeo.com", "Video & Media"),
    ("twitch.tv", "Video & Media"),
    ("netflix.com", "Video & Media"),
    ("spotify.com", "Video & Media"),
    ("amazon.", "Shopping"),
    ("ebay.", "Shopping"),
    ("etsy.com", "Shopping"),
    ("aliexpress.", "Shopping"),
    ("paypal.com", "Finance"),
    ("stripe.com", "Finance"),
    ("coinbase.com", "Finance"),
    ("notion.so", "Productivity & Tools"),
    ("trello.com", "Productivity & Tools"),
    ("docs.google.com", "Productivity & Tools"),
    ("drive.google.com", "Productivity & Tools"),
    ("calendar.google.com", "Productivity & Tools"),
    ("wikipedia.org", "Reference & Learning"),
    ("coursera.org", "Reference & Learning"),
    ("udemy.com", "Reference & Learning"),
    ("khanacademy.org", "Reference & Learning"),
    ("dribbble.com", "Design & Inspiration"),
    ("behance.net", "Design & Inspiration"),
    ("figma.com", "Design & Inspiration"),
    ("unsplash.com", "Design & Inspiration"),
    ("pinterest.com", "Design & Inspiration"),
    ("airbnb.com", "Travel"),
    ("booking.com", "Travel"),
    ("tripadvisor.com", "Travel"),
    ("expedia.com", "Travel"),
]

# Keyword (in title or URL, lowercased) -> category. Checked after domains.
KEYWORD_RULES: list[tuple[str, str]] = [
    ("docs", "Development"),
    ("api", "Development"),
    ("tutorial", "Reference & Learning"),
    ("course", "Reference & Learning"),
    ("blog", "News & Reading"),
    ("shop", "Shopping"),
    ("store", "Shopping"),
    ("invoice", "Finance"),
    ("bank", "Finance"),
]


def categorize_by_rule(title: str, url: str) -> str | None:
    """Return a category from the static rules, or None if no rule matches."""
    haystack = f"{title} {url}".lower()
    for needle, category in DOMAIN_RULES:
        if needle in url.lower():
            return category
    for needle, category in KEYWORD_RULES:
        if needle in haystack:
            return category
    return None


# --- Claude-backed categorization (stdlib only) ------------------------------

# Cheap classification task → Haiku 4.5 by default. Override with the
# ANTHROPIC_MODEL env var (e.g. claude-opus-4-8 for harder grouping).
DEFAULT_MODEL = "claude-haiku-4-5"
API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
BATCH_SIZE = 40

# Stable system prompt — the category taxonomy is the cacheable prefix.
SYSTEM_PROMPT = (
    "You are a bookmark categorizer. Each user message is a JSON array of "
    "bookmarks, each with an integer `i`, a `title`, and a `url`. Assign every "
    "bookmark to exactly one of these categories:\n"
    + "\n".join(f"- {c}" for c in CATEGORIES)
    + '\nUse "Other" only if none fit. Judge by the site and title, not by '
    "guessing page content."
)

# Structured-outputs schema — guarantees parseable JSON back.
_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "assignments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "i": {"type": "integer"},
                    "category": {"type": "string", "enum": CATEGORIES + ["Other"]},
                },
                "required": ["i", "category"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["assignments"],
    "additionalProperties": False,
}


def _classify_batch(
    batch: list[tuple[str, str]], model: str, api_key: str
) -> dict[int, str]:
    """Ask Claude to categorize one batch. Returns {index: category}."""
    user_payload = json.dumps(
        [{"i": i, "title": t, "url": u} for i, (t, u) in enumerate(batch)],
        ensure_ascii=False,
    )
    body = {
        "model": model,
        "max_tokens": 4000,
        # System prompt as a cacheable block (prefix caching). Note: caching
        # only engages once the prefix exceeds the model's minimum (~4096
        # tokens on Haiku/Opus); a short taxonomy simply won't be cached.
        "system": [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [{"role": "user", "content": user_payload}],
        "output_config": {"format": {"type": "json_schema", "schema": _RESPONSE_SCHEMA}},
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

    usage = data.get("usage", {})
    if usage.get("cache_read_input_tokens"):
        print(f"  (cache hit: {usage['cache_read_input_tokens']} tokens)")

    text = "".join(b["text"] for b in data["content"] if b.get("type") == "text")
    parsed = json.loads(text)
    return {a["i"]: a["category"] for a in parsed["assignments"]}


def classify_with_claude(
    items: list[tuple[str, str]], model: str, api_key: str
) -> dict[int, str]:
    """Categorize all items via Claude, in batches. Returns {global_index: cat}."""
    result: dict[int, str] = {}
    for start in range(0, len(items), BATCH_SIZE):
        batch = items[start : start + BATCH_SIZE]
        print(f"  classifying {start + 1}-{start + len(batch)} of {len(items)}...")
        try:
            local = _classify_batch(batch, model, api_key)
        except (urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
            print(f"::warning::Claude batch failed ({exc}); leaving as Uncategorized.")
            continue
        for local_i, category in local.items():
            result[start + local_i] = category
    return result


# --- Output generation -------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_bookmark_html(grouped: dict[str, list[tuple[str, str]]]) -> str:
    """Render a Netscape-format bookmark file with one folder per category."""
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
    ]
    for category in sorted(grouped):
        lines.append(f"    <DT><H3>{_esc(category)}</H3>")
        lines.append("    <DL><p>")
        for title, url in sorted(grouped[category], key=lambda x: x[0].lower()):
            lines.append(f'        <DT><A HREF="{_esc(url)}">{_esc(title)}</A>')
        lines.append("    </DL><p>")
    lines.append("</DL><p>")
    return "\n".join(lines) + "\n"


def render_readme(grouped: dict[str, list[tuple[str, str]]], total: int) -> str:
    """Render a Markdown table of contents mirroring the bookmark file."""
    lines = [
        "# Organized Bookmarks",
        "",
        f"_{total} links across {len(grouped)} categories, "
        "organized automatically._",
        "",
    ]
    for category in sorted(grouped):
        lines.append(f"## {category}")
        lines.append("")
        for title, url in sorted(grouped[category], key=lambda x: x[0].lower()):
            lines.append(f"- [{title}]({url})")
        lines.append("")
    return "\n".join(lines)


# --- Main --------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inbox", default="favorites/inbox")
    parser.add_argument("--out-html", default="favorites/favorites.html")
    parser.add_argument("--out-readme", default="favorites/README.md")
    args = parser.parse_args()

    inbox = Path(args.inbox)
    sources = sorted(inbox.glob("*.html")) if inbox.is_dir() else []
    if not sources:
        print(f"No bookmark files found in {inbox}/ — nothing to organize.")
        return 0

    # Collect + dedupe by URL.
    seen: dict[str, str] = {}
    for src in sources:
        for title, url in extract_entries(src.read_text(encoding="utf-8", errors="replace")):
            seen.setdefault(url, title)
    entries = [(title, url) for url, title in seen.items()]
    print(f"Found {len(entries)} unique links in {len(sources)} file(s).")

    grouped: dict[str, list[tuple[str, str]]] = {}
    leftovers: list[tuple[str, str]] = []
    for title, url in entries:
        category = categorize_by_rule(title, url)
        if category:
            grouped.setdefault(category, []).append((title, url))
        else:
            leftovers.append((title, url))

    print(f"Rules categorized {len(entries) - len(leftovers)}; "
          f"{len(leftovers)} need classification.")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if leftovers and api_key:
        model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
        print(f"Classifying leftovers with Claude ({model})...")
        assigned = classify_with_claude(leftovers, model, api_key)
        for i, (title, url) in enumerate(leftovers):
            category = assigned.get(i, "Uncategorized")
            category = category if category != "Other" else "Uncategorized"
            grouped.setdefault(category, []).append((title, url))
    elif leftovers:
        print("No ANTHROPIC_API_KEY set — leftovers go to Uncategorized.")
        grouped.setdefault("Uncategorized", []).extend(leftovers)

    Path(args.out_html).write_text(render_bookmark_html(grouped), encoding="utf-8")
    Path(args.out_readme).write_text(render_readme(grouped, len(entries)), encoding="utf-8")
    print(f"Wrote {args.out_html} and {args.out_readme} "
          f"({len(grouped)} categories).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
