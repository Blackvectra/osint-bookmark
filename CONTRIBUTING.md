# Contributing to Dogear

Thanks for helping keep these collections useful and current! Contributions of
new tools, corrections, and dead-link fixes are all welcome.

## Ways to contribute

- **Add a tool** you find valuable to the OSINT directory.
- **Fix or remove a dead link** flagged by the link checker.
- **Re-categorize** a tool that's filed in the wrong section.
- **Upgrade `http://` links to `https://`** where the site supports it.

## How the project is structured

```
osint/                  Curated OSINT tools directory
  osint.html              Canonical, browser-importable bookmark file (source of truth)
  README.md               Human-readable table of contents mirroring osint.html
security/               Curated security & pentesting directory (generated)
  security.html           Browser-importable bookmark file (generated)
  README.md               Table of contents (generated)
docs/
  index.html              Live, searchable website (generated)
favorites/              Your personal bookmarks
  inbox/                  Drop browser exports here
  favorites.html          Generated, organized bookmark file
scripts/
  build_security.py       Source of truth for the security catalog -> generates
                          security.html + security/README.md
  build_site.py           Generates the live site (docs/index.html)
  check_links.py          Link validator / dead-link pruner (scans every collection)
  organize.py             Hybrid bookmark categorizer
```

The two curated collections are maintained differently:

- **`security/`** is **generated**. The catalog lives in
  `scripts/build_security.py`; running it writes both `security.html` and
  `security/README.md`. Don't edit those two files by hand.
- **`osint/`** is **hand-maintained**. Its `osint.html` is the source of truth
  and `README.md` mirrors it, so changes go in both.

## Adding a tool to the security collection

1. Add a `("Tool Name", "https://…")` line to the right category in
   `scripts/build_security.py` (prefer `https://`; use a recognizable name).
2. Run `python scripts/build_security.py` to regenerate the HTML + README, then
   `python scripts/build_site.py` to refresh the live site.
3. Validate with `python scripts/check_links.py security/security.html`.
4. Open a pull request describing what the tool does and why it's useful.

## Adding a tool to the OSINT collection

1. Add a `<DT><A HREF="...">Tool Name</A>` entry to the right category folder in
   `osint/osint.html`, and mirror it under the matching section in
   `osint/README.md`.
2. Open a pull request describing what the tool does and why it's useful.

## Link checking

A GitHub Action (`.github/workflows/check-links.yml`) validates every link:

- on each pull request that touches `osint/osint.html` (only the links the PR
  *adds* are checked, so you aren't blocked by pre-existing rot),
- weekly on a schedule, where it also **auto-prunes dead links**.

You can run the checker locally before opening a PR:

```bash
python scripts/check_links.py osint/osint.html
```

It needs only Python 3 (standard library, no extra packages) and exits
non-zero if any link is unreachable.

### Auto-pruning dead links

On the weekly schedule (and via `workflow_dispatch`), the checker removes
links with a **definitive** dead signal — HTTP `404`/`410` or a permanent
DNS failure — from both `osint/osint.html` and `osint/README.md`, then opens
a pull request with the removals for review. Links that merely time out,
return a `5xx`, or are rate-limited are **kept**, since those are usually
transient; they're listed in a `broken-links` tracking issue instead.

To prune locally (edits files in place — commit or discard as you like):

```bash
python scripts/check_links.py osint/osint.html --prune
```

## Organizing your favorites

Drop a browser bookmark export into `favorites/inbox/` and the **Organize
favorites** Action (`.github/workflows/organize.yml`) regenerates
`favorites/favorites.html` and `favorites/README.md`, sorting every link into
categories. It uses domain/keyword rules first, then Claude for the rest when
an `ANTHROPIC_API_KEY` secret is set. Run it locally with:

```bash
python scripts/organize.py
```

## Guidelines

- Only submit links to **publicly accessible** tools and resources.
- No paywalled-only or login-walled tools without a clear note.
- Keep entries factual — no affiliate links or promotional copy.
- One logical change per pull request keeps reviews easy.

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
