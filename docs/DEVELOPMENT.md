# Build the portfolio

Requires Python 3.11 or later and Node.js 18 or later. From the repository root:

```sh
python -m pip install -r requirements.txt
python scripts/generate.py
python scripts/build.py
python scripts/check.py
node --check site/app.js
python -m http.server 4181 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4181/. The generator creates figures and interactive examples from `data/`. The build renders the pages and README. The check validates local links and file checksums.

The presentation is plain HTML, CSS and JavaScript. Author pages in `site/`, figures in `scripts/generate.py`, and the repository front page in `README.md`. The generated `dist/` directory is ignored by Git. `python scripts/build.py --pages` also prepares `docs/` for GitHub Pages on the main branch.

Mathematics is typeset at build time with KaTeX 0.18.7, bundled in
`site/vendor/katex/` with its [MIT license](https://lacrimaeaware.github.io/modeling-and-inference/vendor/katex/LICENSE).
