# Dogear

**A pentester's link library — and a place to organize your own.**

### 🔎 [**Browse the live, searchable site →**](https://blackvectra.github.io/osint-bookmark/)

Dogear is a curated, browser-importable library of security and
penetration-testing resources, kept healthy automatically, plus a tool that
organizes your *own* bookmark exports the way you want them.

The whole collection is also a **live website** you can search and filter in
the browser — 271 tools, instant search, no install. It's a single
self-contained page generated from this repo by
[`scripts/build_site.py`](scripts/build_site.py) and published via GitHub
Pages. (To enable: repo **Settings → Pages → Source: GitHub Actions** — one
click; or open [`docs/index.html`](docs/index.html) locally.)

| Folder | What's in it |
| --- | --- |
| [`security/`](security/) | **The library.** A categorized directory of security & pentesting tools — recon, web app, exploitation, Active Directory, forensics, threat intel, and CTF/practice labs. |
| [`osint/`](osint/) | A companion OSINT (Open Source Intelligence) collection — people/company/infrastructure research tools. |
| [`favorites/`](favorites/) | **Your** bookmarks — drop a browser export in, and an Action sorts it into folders the way you configure. |

> For lawful, authorized security testing and education only.

## `security/` — the pentesting library

A categorized, browser-importable directory of ~70 reputable tools and
resources across the kill chain:

- **Recon & OSINT** — Nmap, Shodan, Censys, Amass, SpiderFoot, Maltego…
- **Web app** — Burp Suite, OWASP ZAP, sqlmap, ffuf, Nuclei, WPScan
- **Exploitation & C2** — Metasploit, Exploit-DB, Impacket, Sliver
- **Passwords** — Hashcat, John, Hydra, Have I Been Pwned
- **Active Directory** — BloodHound, NetExec, Mimikatz, Responder, Certipy
- **Network/wireless**, **vuln intel** (CVE, NVD, CISA KEV, MITRE ATT&CK, OWASP)
- **Forensics & RE** — Ghidra, Volatility, CyberChef, radare2
- **Threat intel** — VirusTotal, urlscan, GreyNoise, MISP, OpenCTI
- **Learning & CTF** — Hack The Box, TryHackMe, PortSwigger Academy, picoCTF…
- **Cheat sheets** — HackTricks, PayloadsAllTheThings, GTFOBins, SecLists

Import [`security/security.html`](security/security.html) into any browser; see
[`security/README.md`](security/README.md) for the full list.

**Kept healthy automatically** by [`scripts/check_links.py`](scripts/check_links.py):

- **PRs** validate only the links a change *adds* (rename-aware — moving files
  isn't misread as new links), so you're never blocked by pre-existing rot.
- **Weekly**, it auto-removes genuinely dead links (HTTP 404/410 or permanent
  DNS failure) via a reviewable pull request, keeping the README mirror in
  sync, and lists merely-flaky links (timeouts, 5xx) in a tracking issue
  rather than deleting them.

The same checker covers the `osint/` collection too.

## `osint/` — companion OSINT collection

A curated set of ~200 OSINT tools (company research, DNS/Whois, email/phone/
people search, social media). See [`osint/README.md`](osint/README.md).

## `favorites/` — organize your own bookmarks

1. Export bookmarks from your browser (an HTML file).
2. Drop it into [`favorites/inbox/`](favorites/inbox/) and push.
3. The **Organize favorites** Action sorts every link into folders and
   regenerates `favorites/favorites.html` (re-importable) plus a Markdown index.

**Organize it your way.** Drop a `favorites/organize.config.json` (see
[`organize.config.example.json`](favorites/organize.config.example.json)) to
define your own categories, the rules that fill them, their folder order, a
`★ Frequently Used` pin list, and whether to sort by name or recency. Without
a config, security/pentest-flavored defaults are used — so your dumped
bookmarks sort straight into pentest buckets.

Categorization is **hybrid**: domain/keyword rules first, then Claude (via the
API) for anything the rules don't catch — but only when an `ANTHROPIC_API_KEY`
repository secret is set. Without it, the rules still run and unmatched links
land in an "Uncategorized" folder, so it works fully offline.

## How it's built

- **No runtime dependencies.** Standard-library Python 3 plus GitHub Actions —
  no SDKs, no build step. (The Claude categorizer calls the API over `urllib`.)
- **Reviewable automation.** Anything that deletes or rewrites content does so
  through a pull request you approve, not a silent push to `main`.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) to add tools or run the tooling
locally.
