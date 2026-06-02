# Favorites

Your personal bookmarks, organized into folders the way you want.

## How to use

1. Export your bookmarks from your browser as an HTML file.
2. Drop the file into [`inbox/`](inbox/) and push (or open a PR).
3. The **Organize favorites** GitHub Action runs
   [`scripts/organize.py`](../scripts/organize.py), sorts every link into
   folders, and regenerates:
   - `favorites.html` — a clean, foldered bookmark file you can re-import;
   - this `README.md` — a Markdown index of everything, by category.

Run it locally with `python scripts/organize.py`.

## Organize it your way

Copy [`organize.config.example.json`](organize.config.example.json) to
`organize.config.json` and edit it to control the output:

| Key | What it does |
| --- | --- |
| `categories` | Your folders, each mapped to a list of URL/title substrings that fill it. First match wins, in the order you list them. |
| `frequent` | Substrings that float a link into a top **★ Frequently Used** folder — your manual "most used" pin list. |
| `sort` | `name` (alphabetical) or `recent` (newest first by date added). |

Without a config, **security/pentest-flavored defaults** are used, so dumped
bookmarks sort straight into pentest buckets (Recon, Web App, Exploitation,
Active Directory, Threat Intel, Learning & CTF, …).

> **On "most used":** browser exports don't include visit counts, so true
> usage frequency can't be detected. Use `frequent` to pin your go-to sites,
> and `sort: recent` to surface what you bookmarked most recently.

## Categorization

Links are sorted by your rules first. Anything unrecognized is sent to
**Claude** for classification — but only if an `ANTHROPIC_API_KEY` repository
secret (or local env var) is set. Without a key, unmatched links go to an
"Uncategorized" folder, so the tool works fully offline. Set `ANTHROPIC_MODEL`
to override the model (defaults to `claude-haiku-4-5`).

_This file is regenerated on every run — the version here is a placeholder
until you add your first export._
