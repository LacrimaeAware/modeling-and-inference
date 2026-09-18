# Modeling and Inference

Three computational studies of what measurements reveal about a model: biological mechanisms, gene networks and image representations. Built with Python, SciPy and PyTorch, with interactive figures and selected result data.

**[Explore the visual portfolio →](https://lacrimaeaware.github.io/modeling-and-inference/)** · [Studies and methods](https://lacrimaeaware.github.io/modeling-and-inference/methods.html)

[![Modeling and Inference: interactive studies of mechanisms, networks and image representations](site/assets/portfolio-preview.png)](https://lacrimaeaware.github.io/modeling-and-inference/)

A model can fit observations while leaving its explanation uncertain. These studies ask what an experiment needs to distinguish competing mechanisms, recover network structure, or reveal a reusable rule inside an image encoder.

| Study | Method and recorded result | Inspect |
| --- | --- | --- |
| Biological mechanisms | ODE simulation and parameter refitting. Three input pulses improve correct selection from **61–83 to 99–100 of 100 trials**, with equal duration, observations, total input and noise scale. | [Study](https://lacrimaeaware.github.io/modeling-and-inference/studies/hidden-rates.html) · [Counts and trajectories](data/input-design.json) |
| Gene-network recovery | SVD removal of shared activity and directed-edge ranking. At one simulated setting, normalized average precision rises from **0.24 to 0.63**. The full grid records the dependence on signal and noise. | [Study](https://lacrimaeaware.github.io/modeling-and-inference/studies/gene-networks.html) · [Simulation grid](data/network-grid.csv) |
| Image representations | Within-class PCA/ICA and fitted latent transforms. A brightness rule transfers to **96 new configurations and six multipliers**, across three trained encoders. | [Study](https://lacrimaeaware.github.io/modeling-and-inference/studies/image-representations.html) · [Transfer measurements](data/brightness-transfer.csv) |

## Approach and context

The work combines ODE models and parameter fitting in **Python/SciPy**, network simulations and comparative benchmarks, and **PyTorch** image encoders evaluated on separate fitting and test configurations. The portfolio includes interactive figures, saved measurements, and scripts that regenerate its plots.

The biological models come from [Ryzowicz & Yildirim (2023)](https://doi.org/10.1039/D2MO00222A). The network study connects to [BEELINE](https://doi.org/10.1038/s41592-019-0690-6) and [modular response analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC130547/); the representation study connects to [learning from paired changes](https://proceedings.mlr.press/v119/locatello20a.html).

The pulse and recovery-map results are simulations. Separate comparisons cover five DREAM4 networks, eighteen BoolODE datasets and real-cell response consistency. Image tests distinguish exploratory attribute discovery from held-out transform evaluation. Each study states its assumptions and baselines beside the result.

## Reproduce the presentation

```sh
python -m pip install -r requirements.txt
python scripts/generate.py
python scripts/build.py
python scripts/check.py
python -m http.server 4181 --bind 127.0.0.1 --directory dist
```

Python 3.11+ and Node.js 18+ are required. These commands regenerate the figures and site from included measurements. Original model training and full fitting runs are maintained in the source projects; [provenance](PROVENANCE.md) identifies what is included. The checker validates local links and the SHA-256 data manifest.

[Methods, data and references](https://lacrimaeaware.github.io/modeling-and-inference/methods.html) · [Data provenance](PROVENANCE.md) · [Build locally](DEVELOPMENT.md)

LacrimaeAware · AI-assisted implementation, analysis and editing, with human-directed research questions and review.
