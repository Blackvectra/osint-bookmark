#!/usr/bin/env python3
"""Build a live, searchable single-page website from the bookmark collections.

Reads the Netscape-format bookmark files (security/security.html and
osint/osint.html), parses their nested folder structure, and renders a
self-contained docs/index.html: one HTML file with inline CSS/JS and the link
data embedded as JSON. No build step, no dependencies, no network needed to
view it — open it locally or serve it via GitHub Pages.

Run: python scripts/build_site.py
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

# Folder names that are structural wrappers, not real categories.
WRAPPERS = {
    "root", "bookmarks", "bookmarks bar", "osint bookmarks",
    "security & pentesting",
}

TOKEN_RE = re.compile(
    r'<DT><H3[^>]*>(?P<folder>.*?)</H3>'
    r'|<DT><A\s+HREF="(?P<url>[^"]+)"[^>]*>(?P<title>.*?)</A>'
    r'|(?P<close></DL>)',
    re.IGNORECASE | re.DOTALL,
)


def parse_collection(text: str) -> list[dict]:
    """Return links as {category, title, url}, category = first real folder."""
    stack = ["root"]
    links: list[dict] = []
    for m in TOKEN_RE.finditer(text):
        if m.group("folder") is not None:
            stack.append(html.unescape(re.sub(r"\s+", " ", m.group("folder")).strip()))
        elif m.group("close") is not None:
            if len(stack) > 1:
                stack.pop()
        else:
            url = m.group("url")
            if not url.startswith(("http://", "https://")):
                continue
            category = next(
                (f for f in stack if f.lower() not in WRAPPERS), "Other"
            )
            title = html.unescape(re.sub(r"\s+", " ", m.group("title")).strip()) or url
            links.append({"category": category, "title": title, "url": url})
    return links


def build_data(files: dict[str, Path]) -> list[dict]:
    """Build ordered collections: [{name, categories:[{name, links:[...]}]}]."""
    collections = []
    for name, path in files.items():
        if not path.is_file():
            continue
        links = parse_collection(path.read_text(encoding="utf-8", errors="replace"))
        cats: dict[str, list[dict]] = {}
        for link in links:
            cats.setdefault(link["category"], []).append(
                {"title": link["title"], "url": link["url"]}
            )
        collections.append({
            "name": name,
            "count": len(links),
            "categories": [
                {"name": c, "links": sorted(ls, key=lambda x: x["title"].lower())}
                for c, ls in cats.items()
            ],
        })
    return collections


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dogear — security & OSINT link library</title>
<meta name="description" content="A searchable, curated library of security, pentesting, and OSINT tools.">
<style>
  :root {
    --bg: #0d1117; --panel: #161b22; --panel2: #1c2430; --border: #2a3441;
    --text: #e6edf3; --muted: #8b949e; --accent: #2f81f7; --accent2: #3fb950;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  a { color: inherit; text-decoration: none; }
  header {
    position: sticky; top: 0; z-index: 10; background: rgba(13,17,23,.92);
    backdrop-filter: blur(8px); border-bottom: 1px solid var(--border);
    padding: 18px 20px 14px;
  }
  .wrap { max-width: 1100px; margin: 0 auto; }
  h1 { margin: 0 0 2px; font-size: 22px; letter-spacing: -.3px; }
  h1 .dot { color: var(--accent); }
  .tag { color: var(--muted); font-size: 13px; margin: 0 0 14px; }
  .controls { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
  #search {
    flex: 1 1 280px; min-width: 0; padding: 10px 14px; font-size: 15px;
    background: var(--panel); border: 1px solid var(--border); border-radius: 9px;
    color: var(--text); outline: none;
  }
  #search:focus { border-color: var(--accent); }
  .tabs { display: flex; gap: 6px; }
  .tab {
    padding: 9px 14px; border: 1px solid var(--border); border-radius: 9px;
    background: var(--panel); color: var(--muted); cursor: pointer; font-size: 14px;
    white-space: nowrap;
  }
  .tab.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .stats { color: var(--muted); font-size: 12.5px; margin-top: 10px; }
  main { max-width: 1100px; margin: 0 auto; padding: 22px 20px 60px; }
  .cat { margin-bottom: 30px; }
  .cat h2 {
    font-size: 14px; text-transform: uppercase; letter-spacing: .6px;
    color: var(--muted); margin: 0 0 12px; display: flex; align-items: center; gap: 8px;
  }
  .cat h2 .n { color: var(--accent2); font-weight: 600; }
  .grid { display: grid; gap: 10px; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }
  .card {
    display: block; padding: 12px 14px; background: var(--panel);
    border: 1px solid var(--border); border-radius: 10px; transition: .12s;
  }
  .card:hover { border-color: var(--accent); background: var(--panel2); transform: translateY(-1px); }
  .card .t { font-weight: 600; font-size: 14.5px; }
  .card .u { color: var(--muted); font-size: 12px; margin-top: 3px; overflow: hidden;
             text-overflow: ellipsis; white-space: nowrap; }
  .hidden { display: none !important; }
  .empty { color: var(--muted); padding: 40px 0; text-align: center; }
  mark { background: rgba(47,129,247,.35); color: inherit; border-radius: 3px; }
  footer { max-width: 1100px; margin: 0 auto; padding: 0 20px 40px; color: var(--muted); font-size: 12.5px; }
</style>
</head>
<body>
<header><div class="wrap">
  <h1>Dog<span class="dot">●</span>ear</h1>
  <p class="tag">A curated, searchable library of security, pentesting &amp; OSINT tools.</p>
  <div class="controls">
    <input id="search" type="search" placeholder="Search tools, e.g. burp, dns, hashcat…" autocomplete="off">
    <div class="tabs" id="tabs"></div>
  </div>
  <div class="stats" id="stats"></div>
</div></header>
<main id="content"></main>
<footer>
  Generated from the bookmark files in this repo — re-importable HTML lives in
  <code>security/</code> and <code>osint/</code>. Links are checked automatically every week.
</footer>
<script>
const DATA = __DATA__;
const $ = s => document.querySelector(s);
let activeTab = "All";

function esc(s){ return s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
function hostOf(u){ try { return new URL(u).hostname.replace(/^www\\./,''); } catch { return u; } }
function highlight(s, q){
  if(!q) return esc(s);
  const i = s.toLowerCase().indexOf(q);
  if(i < 0) return esc(s);
  return esc(s.slice(0,i)) + '<mark>' + esc(s.slice(i,i+q.length)) + '</mark>' + esc(s.slice(i+q.length));
}

function buildTabs(){
  const tabs = ["All", ...DATA.map(c => c.name)];
  $("#tabs").innerHTML = tabs.map(t =>
    `<button class="tab${t===activeTab?' active':''}" data-tab="${esc(t)}">${esc(t)}</button>`).join("");
  $("#tabs").querySelectorAll(".tab").forEach(b =>
    b.onclick = () => { activeTab = b.dataset.tab; buildTabs(); render(); });
}

function render(){
  const q = $("#search").value.trim().toLowerCase();
  const cols = DATA.filter(c => activeTab === "All" || c.name === activeTab);
  let shown = 0, html = "";
  for(const col of cols){
    for(const cat of col.categories){
      const matches = cat.links.filter(l =>
        !q || l.title.toLowerCase().includes(q) || l.url.toLowerCase().includes(q)
           || cat.name.toLowerCase().includes(q));
      if(!matches.length) continue;
      shown += matches.length;
      const label = activeTab === "All" ? col.name + " · " + cat.name : cat.name;
      html += `<section class="cat"><h2>${esc(label)} <span class="n">${matches.length}</span></h2><div class="grid">`;
      for(const l of matches){
        html += `<a class="card" href="${esc(l.url)}" target="_blank" rel="noopener">
          <div class="t">${highlight(l.title, q)}</div>
          <div class="u">${highlight(hostOf(l.url), q)}</div></a>`;
      }
      html += `</div></section>`;
    }
  }
  $("#content").innerHTML = html || `<div class="empty">No tools match “${esc(q)}”.</div>`;
  const total = DATA.reduce((n,c)=>n+c.count,0);
  $("#stats").textContent = q || activeTab !== "All"
    ? `Showing ${shown} of ${total} tools`
    : `${total} tools across ${DATA.length} collections — all links checked weekly`;
}

$("#search").addEventListener("input", render);
buildTabs(); render();
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="docs/index.html")
    args = parser.parse_args()

    data = build_data({
        "Security": Path("security/security.html"),
        "OSINT": Path("osint/osint.html"),
    })
    if not data:
        print("No bookmark files found — nothing to build.")
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    page = PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    out.write_text(page, encoding="utf-8")
    total = sum(c["count"] for c in data)
    cats = sum(len(c["categories"]) for c in data)
    print(f"Built {out} — {total} links, {cats} categories, {len(data)} collections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
