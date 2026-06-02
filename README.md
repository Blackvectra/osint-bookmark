# Dogear

A home for the links worth keeping — and the tooling to keep them tidy.

Dogear holds two bookmark collections, each in its own folder, and a set of
GitHub Actions that maintain them automatically:

| Folder | What's in it |
| --- | --- |
| [`osint/`](osint/) | A curated, categorized directory of OSINT (Open Source Intelligence) tools, importable into any browser. |
| [`favorites/`](favorites/) | Your personal bookmarks — drop a browser export in, and an Action organizes it for you. |

## `osint/` — curated OSINT tools

A hand-picked, browser-importable collection of ~200 OSINT tools across
company research, DNS/Whois, email/phone/people search, social media, and
more. See [`osint/README.md`](osint/README.md) for the full list and import
instructions.

**Kept healthy automatically** by a link checker
([`scripts/check_links.py`](scripts/check_links.py)) that:

- validates links on every pull request that touches the collection (only the
  links a PR *adds* are gated, so you're never blocked by pre-existing rot);
- runs weekly, **auto-removing genuinely dead links** (HTTP 404/410 or
  permanent DNS failure) via a reviewable pull request, while listing
  merely-flaky links (timeouts, 5xx) in a tracking issue rather than deleting
  them.

## `favorites/` — your bookmarks, auto-organized

1. Export bookmarks from your browser (an HTML file).
2. Drop it into [`favorites/inbox/`](favorites/inbox/) and push.
3. The **Organize favorites** Action sorts every link into categories and
   regenerates `favorites/favorites.html` (re-importable) plus a Markdown
   index.

Categorization is **hybrid**: fast domain/keyword rules first, then Claude
(via the API) for anything the rules don't catch — but only when an
`ANTHROPIC_API_KEY` repository secret is set. Without it, the rules still run
and unmatched links land in an "Uncategorized" folder, so it works fully
offline.

## How it's built

- **No runtime dependencies.** Everything is standard-library Python 3 plus
  GitHub Actions — no SDKs, no build step.
- **Reviewable automation.** Anything that deletes or rewrites content does so
  through a pull request you approve, not a silent push to `main`.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) to add tools or run the tooling
locally.
