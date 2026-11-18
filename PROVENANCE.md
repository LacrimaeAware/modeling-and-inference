# Data sources

The figures use recorded simulation results, benchmark scores and saved image outputs.

| Included data | Origin and meaning |
| --- | --- |
| input-design.json | Model-selection counts and fitted protein trajectories under constant and pulsed inputs. A second comparison keeps basal transcription active during each pulse cycle. |
| network-grid.csv | Simulations of 100-gene networks at nine shared-component weights and eight signal-to-noise levels, with four methods and five seeds per setting. |
| benchmark-dream4.csv, benchmark-boolode.csv | Average precision for each method and dataset, scored against directed connections between distinct genes in the generating network. |
| benchmark-operator-scaling.csv | Per-dataset average precision for the same linear model under four preprocessing choices. Pair counts and a strictly increasing pseudotime comparison accompany the BoolODE results. |
| benchmark-time-direction.csv | Standardized linear fits in both observation orders, scored against the same directed edges. Each row gives average precision, its value after assigning both directions of a gene pair their mean forward score, and orientation counts for connections with only one known direction. |
| response-scaling.csv, response-consistency.json | Modular-response calculations on simulated networks and the agreement between two rankings obtained by splitting the measured RPE1 data. |
| response-confound.csv | Simulated perturbation responses with varying intervention strengths. |
| brightness-seed-*.json and .npz | Image metrics and decoded outputs for three trained encoders, with three held-out bases per seed. |
| brightness-transfer.csv, brightness-transfer-parameters.json | Structured-transform transfer test: six multipliers, two starting brightness levels, 96 new bases, three trained and three random encoders. All 360 method cells and fitted action parameters. |
| color-discovery.csv | Color and thickness alignment in one batch of synthetic shapes. The fit used 40 requested pairs per shape, 20 principal components and six independent components. Shape labels determined the pairs. Color labels were used to score alignment. |
| color-alignment-runs.csv | Color and thickness alignment in 20 runs per seed schedule. A stride of 192 gives disjoint rendering-seed ranges. A stride of 1 gives overlapping ranges. Both schedules include seed zero. |
| shape-pair-alignment.csv | Held-out color and stroke-width alignment across 20 paired comparisons. Each fit to 160 pairs uses the same images equally often on each side, with the same color and width transitions. Includes ungrouped fits, convergence flags and both iteration limits. |
| digit-variance-rules.csv | Classification accuracy and fitted weights from ten train/test splits per blur condition. The variance-weighting experiment compares distances to class means and regularized discriminant analysis on images of 3, 5 and 8. |
| digit-edit-transfer.csv | Squared displacement errors for thickness and slant on three held-out MNIST images in one split, relative to predicting zero displacement. A common vector and a kernel ridge predictor are evaluated on the same 39 steps per edit. |
| shape-transfer-alignment.csv | Raw-pixel alignment for five image changes, each transferred from three synthetic shapes to a fourth. |
| classification.json | Ten image splits with independent and class-correlated blur. Image identities are separated before transformations. |
| geometry-examples.npz | Seed 0 arrays for held-out images of digits 3, 5 and 8, moved along training covariance directions. All three digit classes are present in fitting. |
| shape-actions.json | Ten-seed controlled brightness and color-rotation experiments. Fit on circles/squares; evaluate on triangles/crosses, including three-step composition. |
| shape-action-examples.npz | Seed 0 shape outputs: a fitted 30° color rule applied three times, alongside three additions of the average pixel change. Error maps share one absolute scale and use unclipped arrays. |

[File checksums](data/manifest.json) · [Build instructions](DEVELOPMENT.md)
