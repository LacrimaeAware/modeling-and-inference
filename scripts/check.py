"""Check the built site's local links, source images, and identity boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
import re
import hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set(); self.images=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.add(d['id'])
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if tag in ('img','script') and 'src' in d:self.links.append(d['src'])
        if tag=='link' and 'href' in d:self.links.append(d['href'])
        if tag=='img': self.images.append(d)
pages={}
for p in OUT.rglob('*.html'):
    parsed=Links();parsed.feed(p.read_text(encoding='utf-8'));pages[p.resolve()]=parsed
errors=[]
for p,parsed in pages.items():
    for target in parsed.links:
        u=urlsplit(target)
        if u.scheme or u.netloc:continue
        q=(p.parent/unquote(u.path)).resolve() if u.path else p
        if not q.exists():errors.append(f'Missing: {p.name}: {target}')
        if u.fragment and q in pages and u.fragment not in pages[q].ids:errors.append(f'Anchor: {p.name}: {target}')
    for im in parsed.images:
        if 'alt' not in im:errors.append(f'Missing alt: {p.name}')
    raw=p.read_text(encoding='utf-8')
    if re.search(r'C:[/\\]Users|PAPER_LEDGER',raw):errors.append(f'Private identity/context: {p.name}')
data=json.loads((OUT/'assets/study-data.json').read_text())
assert len(data['brightness'])==3 and all(len(s['samples'])==3 for s in data['brightness'])
assert data['benchmarks']['dream4']['count']==5 and data['benchmarks']['boolode']['count']==18
assert len(data['network']['rows'])==288
manifest=json.loads((ROOT/'data/manifest.json').read_text())
assert {r['file'] for r in manifest['files']}=={p.name for p in (ROOT/'data').iterdir() if p.is_file() and p.name!='manifest.json'},'Every included dataset must be recorded in the manifest.'
for row in manifest['files']:
    for folder in [ROOT/'data',OUT/'data']:
        assert hashlib.sha256((folder/row['file']).read_bytes()).hexdigest()==row['sha256'],row['file']
assert len(data['inputDesign']['traces'])==4
assert data['transfer']['trained_affine_group']['max']<.008
for p in (ROOT/'data').glob('*.json'):
    assert not re.search(r'C:[/\\]Users',p.read_text()),p.name
assert not errors,'\n'.join(errors)
print(f'{len(pages)} HTML pages: local links, anchors, image descriptions and identity checks passed.')
print(f"{len(manifest['files'])} data files match their recorded fingerprints.")
