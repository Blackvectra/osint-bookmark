#!/usr/bin/env python3
"""Validate every link in osint.html and report (or prune) the dead ones.

Extracts all HREF URLs from the Netscape-format bookmark file, requests each
one concurrently (HEAD, falling back to GET), and prints a report. Exits with
a non-zero status if any link looks broken so CI can flag it.

With --prune, links with a *definitive* dead signal (HTTP 404/410 or a
permanent DNS failure) are removed from the bookmark files. Transient
failures (timeouts, 5xx, rate-limits) are reported but never deleted, since
those often recover.

No third-party dependencies — standard library only.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# A browser-like UA — many sites reject the default urllib agent with a 403.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
HREF_RE = re.compile(r'HREF="([^"]+)"', re.IGNORECASE)
# A bookmark entry line; only these are eligible for pruning.
ENTRY_RE = re.compile(r"<DT><A\s", re.IGNORECASE)
# Files whose embedded bookmark HTML should be kept in sync when pruning.
DEFAULT_PRUNE_FILES = ("osint/osint.html", "osint/README.md")
# Permanent DNS failures (name does not resolve). Substring match keeps this
# portable across platforms; note "Temporary failure in name resolution"
# (EAI_AGAIN) is intentionally excluded as it is transient.
DEAD_DNS_MARKERS = (
    "Name or service not known",
    "No address associated with hostname",
    "nodename nor servname",
)


def _hrefs(text: str) -> list[str]:
    """Ordered, de-duplicated http(s) URLs found in a blob of text."""
    seen: dict[str, None] = {}
    for url in HREF_RE.findall(text):
        if url.startswith(("http://", "https://")):
            seen.setdefault(url, None)
    return list(seen)


def extract_urls(html_path: Path) -> list[str]:
    """Return the ordered, de-duplicated list of http(s) URLs in the file."""
    return _hrefs(html_path.read_text(encoding="utf-8", errors="replace"))


def changed_urls(html_path: Path, base_ref: str) -> list[str]:
    """URLs introduced on added (+) diff lines relative to base_ref.

    Used by PR runs so contributors are gated only on the links they add,
    not on pre-existing link rot. The diff is taken across the whole PR with
    rename detection (path-limiting defeats rename detection — git would
    report a moved file as entirely new). Added lines are attributed to their
    file and collected only from `.html` bookmark files, so:
      - moving the bookmark file shows as a pure rename (no added lines), and
      - the markdown README mirror (which duplicates every link) is ignored.
    Falls back to a full scan if git fails.
    """
    try:
        diff = subprocess.run(
            ["git", "diff", "--unified=0", "--find-renames", f"{base_ref}...HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"::warning::diff vs {base_ref} failed ({exc}); scanning whole file.")
        return extract_urls(html_path)

    added: list[str] = []
    current = ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("+") and current.endswith(".html"):
            added.append(line[1:])
    return _hrefs("\n".join(added))


def _is_dead_dns(reason: object) -> bool:
    """True only for a permanent name-resolution failure (not a temporary one)."""
    return any(marker in str(reason) for marker in DEAD_DNS_MARKERS)


def check_url(url: str, timeout: float) -> tuple[str, bool, str, bool]:
    """Probe one URL. Returns (url, ok, detail, hard_dead).

    hard_dead is True only for a definitive dead signal (HTTP 404/410 or a
    permanent DNS failure) — the conservative set that is safe to auto-remove.
    """
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(
            url, method=method, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return url, True, f"{resp.status}", False
        except urllib.error.HTTPError as exc:
            # Some servers reject HEAD (405) but accept GET — retry with GET.
            if method == "HEAD" and exc.code in (403, 405, 501):
                continue
            # 401/403/429 means the host is alive but gated; treat as reachable.
            if exc.code in (401, 403, 429):
                return url, True, f"{exc.code} (reachable, gated)", False
            return url, False, f"HTTP {exc.code}", exc.code in (404, 410)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if method == "HEAD":
                continue  # retry with GET before giving up
            reason = getattr(exc, "reason", exc)
            return url, False, f"{type(exc).__name__}: {reason}", _is_dead_dns(reason)
        except Exception as exc:  # noqa: BLE001 - report anything unexpected
            return url, False, f"{type(exc).__name__}: {exc}", False
    return url, False, "unreachable", False


def prune_files(files: list[Path], dead_urls: set[str]) -> dict[Path, list[str]]:
    """Remove bookmark entry lines whose HREF is in dead_urls. Returns removals."""
    removed: dict[Path, list[str]] = {}
    for path in files:
        if not path.is_file():
            continue
        kept: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
            match = HREF_RE.search(line)
            if match and ENTRY_RE.search(line) and match.group(1) in dead_urls:
                removed.setdefault(path, []).append(match.group(1))
                continue
            kept.append(line)
        if path in removed:
            path.write_text("".join(kept), encoding="utf-8")
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        default="osint/osint.html",
        help="Bookmark HTML file to scan (default: osint/osint.html)",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument(
        "--diff-base",
        metavar="REF",
        help="Only check links added relative to this git ref (for PR runs).",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove hard-dead links (404/410 or permanent DNS failure) from "
        f"{', '.join(DEFAULT_PRUNE_FILES)}. Transient failures are kept.",
    )
    args = parser.parse_args()

    html_path = Path(args.file)
    if not html_path.is_file():
        print(f"::error::File not found: {html_path}", file=sys.stderr)
        return 2

    if args.diff_base:
        urls = changed_urls(html_path, args.diff_base)
        if not urls:
            print(f"No new links added vs {args.diff_base} — nothing to check.")
            return 0
        print(f"Checking {len(urls)} newly added link(s) vs {args.diff_base}...\n")
    else:
        urls = extract_urls(html_path)
        print(f"Checking {len(urls)} unique links in {html_path}...\n")

    dead: list[tuple[str, str]] = []  # hard-dead: 404/410 or permanent DNS
    transient: list[tuple[str, str]] = []  # broken but possibly temporary
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_url, u, args.timeout): u for u in urls}
        for fut in concurrent.futures.as_completed(futures):
            url, ok, detail, hard_dead = fut.result()
            if ok:
                continue
            (dead if hard_dead else transient).append((url, detail))
            print(f"{'DEAD   ' if hard_dead else 'BROKEN '} {url}  ->  {detail}")

    print(f"\n{'-' * 60}")
    print(
        f"Checked: {len(urls)}   Hard-dead: {len(dead)}   "
        f"Other broken: {len(transient)}"
    )

    if args.prune and dead:
        removed = prune_files(
            [html_path, *(Path(f) for f in DEFAULT_PRUNE_FILES if f != args.file)],
            {url for url, _ in dead},
        )
        print("\n### Removed hard-dead links\n")
        for path, urls_removed in removed.items():
            for url in urls_removed:
                print(f"- {url}  (from `{path}`)")
    elif dead:
        print("\n### Hard-dead links (safe to remove)\n")
        for url, detail in sorted(dead):
            print(f"- [ ] {url} — `{detail}`")

    if transient:
        print("\n### Other broken links (kept — may be transient)\n")
        for url, detail in sorted(transient):
            print(f"- [ ] {url} — `{detail}`")

    # After pruning, hard-dead links are gone; only unresolved breakage remains.
    remaining = transient if args.prune else dead + transient
    if remaining:
        return 1
    print("\nNo unresolved broken links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
