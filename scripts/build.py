"""Build the static portfolio without a frontend framework."""
from pathlib import Path
import shutil
import json
import html
import re
import sys
import markdown
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
for path in SITE.iterdir():
    if path.is_file() and path.suffix!='.html': shutil.copyfile(path,OUT/path.name)
shutil.copytree(SITE/'assets',OUT/'assets',dirs_exist_ok=True)
shutil.copytree(SITE/'vendor',OUT/'vendor',dirs_exist_ok=True)
shutil.copytree(ROOT/'data',OUT/'data',dirs_exist_ok=True)
for name in ['README.md','DEVELOPMENT.md','PROVENANCE.md']:
    shutil.copyfile(ROOT/name,OUT/name)
titles={'index.html':'Modeling and Inference · LacrimaeAware','hidden-rates.html':'Biological mechanisms · Modeling and Inference',
        'gene-networks.html':'Gene-network recovery · Modeling and Inference','image-representations.html':'Image representations · Modeling and Inference',
        'methods.html':'Methods & data · Modeling and Inference','readme.html':'GitHub README · Modeling and Inference'}

def typeset(content):
    pattern=r'<(div|span) class="(math-block|math-inline)" data-tex="([^"]+)"></\1>'
    matches=list(re.finditer(pattern,content))
    if not matches: return content
    expressions=[{'tex':html.unescape(m[3]),'display':m[1]=='div'} for m in matches]
    rendered=json.loads(subprocess.run(['node',str(ROOT/'scripts/render-math.cjs')],
        input=json.dumps(expressions),text=True,encoding='utf-8',capture_output=True,check=True).stdout)
    for match,body in reversed(list(zip(matches,rendered))):
        content=content[:match.start()]+f'<{match[1]} class="{match[2]}">{body}</{match[1]}>'+content[match.end():]
    return content

def wrap(content,title,base):
    content=typeset(content)
    # Headline line breaks are hidden on phones; keep the words separated.
    content=re.sub(r'<br>(?=\S)', '<br> ', content)
    # Scientific figures can be opened at their original size on narrow screens.
    if re.search(r'<main class="[^\"]*\bnote\b',content):
        content=re.sub(r'(<figure>)(<img src="([^"]+)"[^>]*>)',r'\1<a href="\3" title="Open full-size figure">\2</a>',content)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Independent studies of biological parameter inference, gene-network recovery, and image representations, with interactive figures and reproducible measurements.">
<meta name="color-scheme" content="light"><title>{html.escape(title)}</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='20' fill='%23252e30'/%3E%3Ctext x='20' y='28' text-anchor='middle' font-family='Georgia' font-size='29' fill='%23f5f3ec'%3Em%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{base}vendor/katex/katex.min.css"><link rel="stylesheet" href="{base}style.css"><script type="module" src="{base}app.js"></script></head>
<body data-base="{base}"><a class="skip" href="#main">Skip to content</a>
<header class="mast"><div class="mast-inner wrap"><a class="brand" href="{base}index.html"><span class="brand-mark" aria-hidden="true">m</span>Modeling and Inference</a><nav aria-label="Main navigation"><a href="{base}index.html#rates">Studies</a><a href="{base}methods.html">Methods & data</a></nav></div></header>
{content}
<footer class="footer"><div class="footer-inner wrap"><div><strong>LacrimaeAware</strong><p>Independent research in modeling and inference.</p></div><div class="footer-right"><a href="{base}methods.html">Methods & credits</a><a href="{base}readme.html">GitHub README</a><p>Developed with AI assistance in implementation, analysis, and editing.<br>Unrefereed work. External priority is unestablished.</p></div></div></footer>
</body></html>'''

for path in SITE.glob('*.html'):
    if path.name=='readme.html': continue
    content=path.read_text(encoding='utf-8')
    (OUT/path.name).write_text(wrap(content,titles[path.name],'./'),encoding='utf-8')
(OUT/'studies').mkdir(exist_ok=True)
for path in (SITE/'studies').glob('*.html'):
    content=path.read_text(encoding='utf-8')
    (OUT/'studies'/path.name).write_text(wrap(content,titles[path.name],'../'),encoding='utf-8')
for source,target,title in [('README.md','readme.html','GitHub README'),('PROVENANCE.md','provenance.html','Data provenance'),('DEVELOPMENT.md','development.html','Build the portfolio')]:
    body=markdown.markdown((ROOT/source).read_text(encoding='utf-8-sig'),extensions=['tables','fenced_code'])
    body=body.replace('src="site/assets/','src="assets/')
    body=re.sub(r'href="https://lacrimaeaware.github.io/modeling-and-inference/([^"]*)"',lambda m:'href="'+(m[1] or 'index.html')+'"',body)
    for md,page in [('README.md','readme.html'),('PROVENANCE.md','provenance.html'),('DEVELOPMENT.md','development.html')]:
        body=body.replace(f'href="{md}"',f'href="{page}"')
    body=body.replace('<table>','<div class="table-scroll"><table>').replace('</table>','</table></div>')
    (OUT/target).write_text(wrap('<main class="note readme-content" id="main"><a class="back" href="index.html">← Portfolio overview</a>'+body+'</main>',title+' · Modeling and Inference','./'),encoding='utf-8')
(OUT/'.nojekyll').touch()
if '--pages' in sys.argv:
    target=ROOT/'docs'
    if target.is_symlink() or (target.exists() and not (target/'.nojekyll').is_file()):
        raise RuntimeError('Pages target must be a generated docs directory.')
    shutil.copytree(OUT,target,dirs_exist_ok=True)
print(f'Built {len(list(OUT.rglob("*.html")))} pages in dist.')
