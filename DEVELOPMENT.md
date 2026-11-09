# Build the portfolio

Public pages showcase questions, experiments and recorded results. Keep setup instructions here and detailed numerical checks on the methods page. Use one brief AI disclosure, linked from the footer, rather than repeating credits or ownership explanations throughout the site.

Requires Python 3.11 or later and Node.js 18 or later. From the repository root:

```sh
python -m pip install -r requirements.txt
python scripts/generate.py
python scripts/build.py
python scripts/check.py
node --check site/app.js
python -m http.server 4181 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4181/. The generator recreates the scientific figures and interactive data from the included results. It also checks the simple cascade against an independent ODE integration. The build renders the repository preview directly from README.md.

The presentation is plain HTML, CSS and JavaScript. Author pages in `site/`, figures in `scripts/generate.py`, and the repository front page in `README.md`. The generated `dist/` directory is ignored by Git. `python scripts/build.py --pages` also prepares `docs/` for GitHub Pages on the main branch.

Mathematics is typeset at build time using the bundled KaTeX library in `site/vendor/katex/`; the site needs no external script or font service.

Regenerating the presentation does not retrain the original encoders or rerun all biological experiments. Selected result tables and model outputs are included; the full working research projects remain separate. See [PROVENANCE.md](PROVENANCE.md) for the source of each dataset.
