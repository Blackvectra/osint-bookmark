#!/usr/bin/env python3
"""Validate every link in osint.html and report the dead ones.

Extracts all HREF URLs from the Netscape-format bookmark file, requests each
one concurrently (HEAD, falling back to GET), and prints a report. Exits with
a non-zero status if any link looks broken so CI can flag it.

No third-party dependencies — standard library only.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
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


def extract_urls(html_path: Path) -> list[str]:
    """Return the ordered, de-duplicated list of http(s) URLs in the file."""
    text = html_path.read_text(encoding="utf-8", errors="replace")
    seen: dict[str, None] = {}
    for url in HREF_RE.findall(text):
        if url.startswith(("http://", "https://")):
            seen.setdefault(url, None)
    return list(seen)


def check_url(url: str, timeout: float) -> tuple[str, bool, str]:
    """Probe one URL. Returns (url, ok, detail)."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(
            url, method=method, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return url, True, f"{resp.status}"
        except urllib.error.HTTPError as exc:
            # Some servers reject HEAD (405) but accept GET — retry with GET.
            if method == "HEAD" and exc.code in (403, 405, 501):
                continue
            # 401/403 means the host is alive but gated; treat as reachable.
            if exc.code in (401, 403, 429):
                return url, True, f"{exc.code} (reachable, gated)"
            return url, False, f"HTTP {exc.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            reason = getattr(exc, "reason", exc)
            if method == "GET":
                return url, False, f"{type(exc).__name__}: {reason}"
        except Exception as exc:  # noqa: BLE001 - report anything unexpected
            return url, False, f"{type(exc).__name__}: {exc}"
    return url, False, "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        default="osint.html",
        help="Bookmark HTML file to scan (default: osint.html)",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()

    html_path = Path(args.file)
    if not html_path.is_file():
        print(f"::error::File not found: {html_path}", file=sys.stderr)
        return 2

    urls = extract_urls(html_path)
    print(f"Checking {len(urls)} unique links in {html_path}...\n")

    broken: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_url, u, args.timeout): u for u in urls}
        for fut in concurrent.futures.as_completed(futures):
            url, ok, detail = fut.result()
            if not ok:
                broken.append((url, detail))
                print(f"BROKEN  {url}  ->  {detail}")

    print(f"\n{'-' * 60}")
    print(f"Checked: {len(urls)}   Broken: {len(broken)}")

    if broken:
        print("\n### Broken links\n")
        for url, detail in sorted(broken):
            print(f"- [ ] {url} — `{detail}`")
        return 1

    print("All links reachable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
