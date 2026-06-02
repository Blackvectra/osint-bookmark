# Favorites

Your personal bookmarks, organized automatically.

## How to use

1. Export your bookmarks from your browser as an HTML file.
2. Drop the file into [`inbox/`](inbox/) and push (or open a PR).
3. The **Organize favorites** GitHub Action runs
   [`scripts/organize.py`](../scripts/organize.py), sorts every link into
   categories, and regenerates:
   - `favorites.html` — a clean, foldered bookmark file you can re-import
     into any browser;
   - this `README.md` — a Markdown index of everything, by category.

You can also run it locally:

```bash
python scripts/organize.py
```

## Categorization

Links are sorted by fast domain/keyword **rules** first. Anything the rules
don't recognize is sent to **Claude** for classification — but only if an
`ANTHROPIC_API_KEY` repository secret (or local env var) is set. Without a
key, unmatched links go to an "Uncategorized" folder, so the tool works fully
offline.

Set `ANTHROPIC_MODEL` to override the model (defaults to `claude-haiku-4-5`,
a cheap, fast choice for classification).

_This file is regenerated on every run — the version here is a placeholder
until you add your first export._
