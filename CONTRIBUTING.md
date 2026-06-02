# Contributing to OSINT Tools Directory

Thanks for helping keep this collection useful and current! Contributions of
new tools, corrections, and dead-link fixes are all welcome.

## Ways to contribute

- **Add a tool** you find valuable for OSINT research.
- **Fix or remove a dead link** flagged by the link checker.
- **Re-categorize** a tool that's filed in the wrong section.
- **Upgrade `http://` links to `https://`** where the site supports it.

## How the project is structured

There are two files that hold the link data:

- **`osint.html`** — the canonical, browser-importable bookmark file
  (Netscape format). This is the source of truth.
- **`README.md`** — a human-readable table of contents that mirrors the
  bookmark file for browsing on GitHub.

When you add or change a link, **update both files** so they stay in sync.

## Adding a link

1. Find the most appropriate category folder in `osint.html`.
2. Add a `<DT><A HREF="...">Tool Name</A>` entry alongside the others.
   - Prefer `https://` URLs.
   - Use a clear, recognizable tool name.
3. Mirror the addition under the matching section in `README.md`.
4. Open a pull request describing what the tool does and why it's useful.

## Link checking

A GitHub Action (`.github/workflows/check-links.yml`) validates every link:

- on each pull request that touches `osint.html` (only the links the PR
  *adds* are checked, so you aren't blocked by pre-existing rot),
- weekly on a schedule, where it also **auto-prunes dead links**.

You can run the checker locally before opening a PR:

```bash
python scripts/check_links.py osint.html
```

It needs only Python 3 (standard library, no extra packages) and exits
non-zero if any link is unreachable.

### Auto-pruning dead links

On the weekly schedule (and via `workflow_dispatch`), the checker removes
links with a **definitive** dead signal — HTTP `404`/`410` or a permanent
DNS failure — from both `osint.html` and `README.md`, then opens a pull
request with the removals for review. Links that merely time out, return a
`5xx`, or are rate-limited are **kept**, since those are usually transient;
they're listed in a `broken-links` tracking issue instead.

To prune locally (edits files in place — commit or discard as you like):

```bash
python scripts/check_links.py osint.html --prune
```

## Guidelines

- Only submit links to **publicly accessible** tools and resources.
- No paywalled-only or login-walled tools without a clear note.
- Keep entries factual — no affiliate links or promotional copy.
- One logical change per pull request keeps reviews easy.

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
