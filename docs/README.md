# Modeling and Inference

Experiments with biological models, gene networks and image representations.

**[Explore the experiments →](https://lacrimaeaware.github.io/modeling-and-inference/)** · [Methods and data](https://lacrimaeaware.github.io/modeling-and-inference/methods.html)

[![Modeling and Inference: interactive studies of mechanisms, networks and image representations](site/assets/portfolio-preview.jpg)](https://lacrimaeaware.github.io/modeling-and-inference/)

| Experiment | Recorded observation | Inspect |
| --- | --- | --- |
| Biological mechanisms | Three input pulses raise correct model selection from **61–83 to 99–100 of 100 simulated trials**, with equal duration, observations, total input and noise scale. | [Experiment](https://lacrimaeaware.github.io/modeling-and-inference/studies/hidden-rates.html) · [Counts and trajectories](data/input-design.json) |
| Gene-network recovery | Remove shared activity and compare recovered connections with a known simulated network. At one setting, the recovery score rises from **0.24 to 0.63**. | [Experiment](https://lacrimaeaware.github.io/modeling-and-inference/studies/gene-networks.html) · [Simulation grid](data/network-grid.csv) |
| Image representations | Fit a brightness rule inside an image model and test it on **96 new configurations and six multipliers**, across three trained encoders. | [Experiment](https://lacrimaeaware.github.io/modeling-and-inference/studies/image-representations.html) · [Transfer measurements](data/brightness-transfer.csv) |

## Approach and context

The biological models come from [Ryzowicz & Yildirim (2023)](https://doi.org/10.1039/D2MO00222A). The network study connects to [BEELINE](https://doi.org/10.1038/s41592-019-0690-6) and [modular response analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC130547/); the representation study connects to [learning from paired changes](https://proceedings.mlr.press/v119/locatello20a.html).

The pulse and recovery-map results use simulations. Separate comparisons cover DREAM4 and BoolODE datasets and measured cell responses. Image experiments distinguish finding an attribute from testing a fitted image change.

[Methods, data and references](https://lacrimaeaware.github.io/modeling-and-inference/methods.html) · [Data provenance](PROVENANCE.md) · [Build locally](DEVELOPMENT.md)

LacrimaeAware · [AI assistance](https://lacrimaeaware.github.io/modeling-and-inference/methods.html#ai-assistance).
