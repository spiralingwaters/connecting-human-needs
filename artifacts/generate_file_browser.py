#!/usr/bin/env python3
"""Regenerate artifacts/file_browser.html from the current branch's tracked files.

Run this any time the repo's files change and you want the browser to catch up:

    python3 artifacts/generate_file_browser.py

It embeds every git-tracked file's contents plus the current branch name into a
single self-contained HTML page (artifacts/file_browser.html) with no server
or build step required to view it.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "artifacts" / "file_browser.html"
SELF_PATH = "artifacts/generate_file_browser.py"
OUTPUT_REL = "artifacts/file_browser.html"
OVERRIDES_REL = "artifacts/content_overrides.json"


def run(cmd):
    return subprocess.check_output(cmd, cwd=REPO_ROOT, text=True).strip()


def branch_name():
    try:
        name = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return name if name != "HEAD" else run(["git", "rev-parse", "--short", "HEAD"]) + " (detached)"
    except subprocess.CalledProcessError:
        return "(unknown branch)"


def tracked_files():
    paths = run(["git", "ls-files"]).splitlines()
    return [p for p in paths if p not in (SELF_PATH, OUTPUT_REL, OVERRIDES_REL)]


def group_for(path):
    parts = path.split("/")
    return parts[0] if len(parts) > 1 else "root"


# Optional per-file display overrides: an LLM-written markdown string per
# path, shown alongside the file's raw text (the browser gets a per-file
# Summary/Full text toggle whenever an override exists). The default style
# mirrors the file's own headers/sub-headers, with each section's content
# condensed into a short bullet list under its heading. This script
# contains no summarizing/rewriting logic of its own — it only reads
# whatever is here, bakes it into the HTML, and then resets this file to
# {} so a future run defaults back to raw-only unless something is
# written here again first.
OVERRIDES_PATH = REPO_ROOT / "artifacts" / "content_overrides.json"


def load_overrides():
    if not OVERRIDES_PATH.exists():
        return {}
    return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))


def clear_overrides():
    """Consume content_overrides.json: whatever was in it gets baked into
    this run's HTML, then the file is reset to empty so a future run (with
    nothing new written to it) defaults back to plain raw content."""
    OVERRIDES_PATH.write_text("{}\n", encoding="utf-8")


def build_file_map():
    overrides = load_overrides()
    files = {}
    for path in tracked_files():
        full = REPO_ROOT / path
        try:
            content = full.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            content = "(binary or unreadable file — not shown)"
        files[path] = {
            "group": group_for(path),
            "content": content,
            "override": overrides.get(path),
        }
    return files


TEMPLATE = """<title>Project File Browser</title>
<style>
:root{{
  --ground:#f6f4ef;
  --surface:#ffffff;
  --ink:#22231f;
  --ink-soft:#5b5c54;
  --line:#e1ddd0;
  --accent:#2f6f5e;
  --accent-soft:#e4efe9;
  --mono-tint:#f1efe6;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --ground:#191a17;
    --surface:#212220;
    --ink:#ece9de;
    --ink-soft:#a6a397;
    --line:#34352f;
    --accent:#7fc4ab;
    --accent-soft:#243330;
    --mono-tint:#26261f;
  }}
}}
:root[data-theme="dark"]{{
  --ground:#191a17;
  --surface:#212220;
  --ink:#ece9de;
  --ink-soft:#a6a397;
  --line:#34352f;
  --accent:#7fc4ab;
  --accent-soft:#243330;
  --mono-tint:#26261f;
}}

*{{box-sizing:border-box;}}
html,body{{margin:0;padding:0;}}
body{{
  background:var(--ground);
  color:var(--ink);
  font-family:'Source Serif 4', Georgia, 'Times New Roman', serif;
  min-height:100vh;
  display:flex;
  flex-direction:column;
}}

header{{
  padding:2rem clamp(1.25rem,4vw,3rem) 1.25rem;
  border-bottom:1px solid var(--line);
}}
header .eyebrow{{
  font-family:'IBM Plex Mono', ui-monospace, Menlo, monospace;
  font-size:0.72rem;
  letter-spacing:0.14em;
  text-transform:uppercase;
  color:var(--accent);
  display:flex;
  align-items:center;
  gap:0.6rem;
  flex-wrap:wrap;
}}
header .branch-pill{{
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  font-size:0.72rem;
  letter-spacing:0.02em;
  text-transform:none;
  background:var(--accent-soft);
  color:var(--accent);
  border:1px solid var(--accent);
  border-radius:999px;
  padding:0.15rem 0.6rem;
}}
header h1{{
  font-family:'Fraunces', 'Source Serif 4', Georgia, serif;
  font-weight:600;
  font-size:clamp(1.6rem,3.2vw,2.2rem);
  margin:0.35rem 0 0.15rem;
  text-wrap:balance;
}}
header p{{
  margin:0;
  color:var(--ink-soft);
  font-size:0.95rem;
  max-width:60ch;
}}
header .generated-at{{
  margin-top:0.4rem;
  color:var(--ink-soft);
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  font-size:0.75rem;
}}

main{{
  flex:1;
  display:grid;
  grid-template-columns:280px 1fr;
  min-height:0;
}}
@media (max-width:720px){{
  main{{grid-template-columns:1fr;}}
}}

nav{{
  border-right:1px solid var(--line);
  padding:1.25rem 0.75rem;
  overflow-y:auto;
}}
nav .group-label{{
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  font-size:0.68rem;
  letter-spacing:0.1em;
  text-transform:uppercase;
  color:var(--ink-soft);
  padding:0.6rem 0.65rem 0.35rem;
}}
nav ul{{
  list-style:none;
  margin:0 0 0.5rem;
  padding:0;
}}
nav button{{
  display:flex;
  align-items:baseline;
  gap:0.55rem;
  width:100%;
  text-align:left;
  background:none;
  border:none;
  border-radius:6px;
  padding:0.5rem 0.65rem;
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  font-size:0.86rem;
  color:var(--ink);
  cursor:pointer;
}}
nav button:hover{{background:var(--mono-tint);}}
nav button:focus-visible{{outline:2px solid var(--accent); outline-offset:1px;}}
nav button.active{{background:var(--accent-soft); color:var(--accent); font-weight:600;}}

section#viewer{{
  padding:1.75rem clamp(1.25rem,4vw,3rem) 3rem;
  overflow-y:auto;
}}
.file-head{{
  display:flex;
  align-items:baseline;
  gap:0.75rem;
  flex-wrap:wrap;
  border-bottom:1px solid var(--line);
  padding-bottom:0.85rem;
  margin-bottom:1.4rem;
}}
.file-head h2{{
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  font-size:1.05rem;
  margin:0;
  color:var(--ink);
}}
.view-toggle{{
  display:inline-flex;
  border:1px solid var(--line);
  border-radius:999px;
  overflow:hidden;
}}
.view-toggle button{{
  border:none;
  background:var(--surface);
  color:var(--ink-soft);
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  font-size:0.72rem;
  letter-spacing:0.04em;
  padding:0.3rem 0.75rem;
  cursor:pointer;
}}
.view-toggle button + button{{border-left:1px solid var(--line);}}
.view-toggle button.active{{background:var(--accent-soft); color:var(--accent); font-weight:600;}}
.view-toggle button:focus-visible{{outline:2px solid var(--accent); outline-offset:-2px;}}

.rendered{{
  max-width:66ch;
  font-size:1.02rem;
  line-height:1.65;
}}
.rendered h1,.rendered h2,.rendered h3{{
  font-family:'Fraunces','Source Serif 4',serif;
  font-weight:600;
  text-wrap:balance;
  margin-top:1.6em;
  margin-bottom:0.5em;
}}
.rendered h1{{font-size:1.5rem;}}
.rendered h2{{font-size:1.25rem;}}
.rendered h3{{font-size:1.08rem;}}
.rendered p{{margin:0.75em 0;}}
.rendered ul{{margin:0.6em 0; padding-left:1.3em;}}
.rendered li{{margin:0.3em 0;}}
.rendered code{{
  font-family:'IBM Plex Mono', ui-monospace, monospace;
  background:var(--mono-tint);
  padding:0.1em 0.35em;
  border-radius:4px;
  font-size:0.88em;
}}
.rendered .empty-file{{
  color:var(--ink-soft);
  font-style:italic;
}}

.placeholder{{
  color:var(--ink-soft);
  font-size:0.95rem;
  max-width:44ch;
}}

::-webkit-scrollbar{{width:10px; height:10px;}}
::-webkit-scrollbar-thumb{{background:var(--line); border-radius:6px;}}
</style>

<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">

<header>
  <div class="eyebrow">agentic-claude <span class="branch-pill">branch: {branch}</span></div>
  <h1>Project File Browser</h1>
  <p>Every tracked file in the repository on this branch. Click a name on the left to view it — raw content by default, or a custom style if one has been requested.</p>
  <div class="generated-at">Regenerated {generated_at} &middot; run <code>python3 artifacts/generate_file_browser.py</code> to refresh</div>
</header>

<main>
  <nav id="fileNav"></nav>
  <section id="viewer">
    <div class="file-head">
      <h2 id="fileTitle">No file selected</h2>
      <div class="view-toggle" id="viewToggle" style="display:none;">
        <button type="button" id="btnSummary" data-view="summary">Summary</button>
        <button type="button" id="btnFull" data-view="full">Full text</button>
      </div>
    </div>
    <div class="placeholder" id="placeholder">Pick a file from the list to view its contents.</div>
    <div class="rendered" id="rendered" style="display:none;"></div>
  </section>
</main>

<script id="file-data" type="application/json">{file_json}</script>
<script>
const files = JSON.parse(document.getElementById('file-data').textContent);

function mdToHtml(src){{
  if(!src.trim()) return '<p class="empty-file">(empty file)</p>';
  const lines = src.split('\\n');
  let html = '';
  let inList = false;
  for(const raw of lines){{
    const line = raw.replace(/\\s+$/,'');
    const inline = t => t.replace(/`([^`]+)`/g,'<code>$1</code>');
    if(/^###\\s+/.test(line)){{ if(inList){{html+='</ul>';inList=false;}} html += `<h3>${{inline(line.replace(/^###\\s+/,''))}}</h3>`; }}
    else if(/^##\\s+/.test(line)){{ if(inList){{html+='</ul>';inList=false;}} html += `<h2>${{inline(line.replace(/^##\\s+/,''))}}</h2>`; }}
    else if(/^#\\s+/.test(line)){{ if(inList){{html+='</ul>';inList=false;}} html += `<h1>${{inline(line.replace(/^#\\s+/,''))}}</h1>`; }}
    else if(/^-\\s+/.test(line)){{ if(!inList){{html+='<ul>';inList=true;}} html += `<li>${{inline(line.replace(/^-\\s+/,''))}}</li>`; }}
    else if(line.trim()===''){{ if(inList){{html+='</ul>';inList=false;}} }}
    else{{ if(inList){{html+='</ul>';inList=false;}} html += `<p>${{inline(line)}}</p>`; }}
  }}
  if(inList) html += '</ul>';
  return html;
}}

function escapeHtml(s){{
  return s.replace(/[&<>]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[c]));
}}

const groupOrder = [];
Object.values(files).forEach(f => {{ if(!groupOrder.includes(f.group)) groupOrder.push(f.group); }});
groupOrder.sort((a,b) => a === 'root' ? -1 : b === 'root' ? 1 : a.localeCompare(b));

const nav = document.getElementById('fileNav');
groupOrder.forEach(key => {{
  const entries = Object.entries(files).filter(([,v]) => v.group === key);
  if(!entries.length) return;
  const gLabel = document.createElement('div');
  gLabel.className = 'group-label';
  gLabel.textContent = key === 'root' ? 'Root' : key + ' /';
  nav.appendChild(gLabel);
  const ul = document.createElement('ul');
  entries.forEach(([path]) => {{
    const li = document.createElement('li');
    const btn = document.createElement('button');
    const name = path.split('/').pop();
    btn.dataset.path = path;
    btn.textContent = name;
    btn.addEventListener('click', () => selectFile(path));
    li.appendChild(btn);
    ul.appendChild(li);
  }});
  nav.appendChild(ul);
}});

function fullToHtml(path, content){{
  return path.endsWith('.md') ? mdToHtml(content) : `<pre style="white-space:pre-wrap;font-family:'IBM Plex Mono',monospace;font-size:0.88rem;">${{escapeHtml(content) || '(empty file)'}}</pre>`;
}}

let currentPath = null;
let currentView = 'summary';

function renderView(){{
  const {{content, override}} = files[currentPath];
  const rendered = document.getElementById('rendered');
  if(currentView === 'summary' && override){{
    rendered.innerHTML = mdToHtml(String(override));
  }} else {{
    rendered.innerHTML = fullToHtml(currentPath, content);
  }}
  document.getElementById('btnSummary').classList.toggle('active', currentView === 'summary');
  document.getElementById('btnFull').classList.toggle('active', currentView === 'full');
}}

document.getElementById('viewToggle').addEventListener('click', e => {{
  const btn = e.target.closest('button[data-view]');
  if(!btn || !currentPath) return;
  currentView = btn.dataset.view;
  renderView();
}});

function selectFile(path){{
  document.querySelectorAll('nav button').forEach(b => b.classList.toggle('active', b.dataset.path === path));
  document.getElementById('fileTitle').textContent = path;
  document.getElementById('placeholder').style.display = 'none';
  document.getElementById('rendered').style.display = 'block';
  currentPath = path;
  const hasOverride = !!files[path].override;
  const toggle = document.getElementById('viewToggle');
  toggle.style.display = hasOverride ? 'inline-flex' : 'none';
  currentView = hasOverride ? 'summary' : 'full';
  renderView();
}}
</script>
"""


def main():
    from datetime import datetime, timezone

    files = build_file_map()
    branch = branch_name()
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    file_json = json.dumps(files, indent=None).replace("</", "<\\/")
    html = TEMPLATE.format(
        branch=branch,
        generated_at=generated_at,
        file_json=file_json,
    )
    OUTPUT.write_text(html, encoding="utf-8")
    clear_overrides()
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)} for branch '{branch}' ({len(files)} files)")
    print(f"Reset {OVERRIDES_PATH.relative_to(REPO_ROOT)} — write new overrides before the next run if you want a custom view baked in again.")


if __name__ == "__main__":
    sys.exit(main())
