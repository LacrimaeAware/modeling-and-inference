# Data sources

The figures use recorded simulation results, benchmark scores and saved image outputs.

| Included data | Origin and meaning |
| --- | --- |
| input-design.json | Mechanistic model inference, experiment 10: selection counts and fitted trajectories for nominal and basal-preserving inputs. |
| network-grid.csv | GRN experiment 28: nine shared-component weights, eight signal/noise levels, four methods, five seeds per cell, 100 genes. |
| benchmark-dream4.csv, benchmark-boolode.csv | GRN experiment 33: per-dataset average precision on common directed non-self reference edges. |
| response-scaling.csv, response-consistency.json | GRN experiment 42: modular-response controls and aggregate RPE1 split-half consistency. |
| response-confound.csv | GRN experiment 41: response-strength control summary. |
| brightness-seed-*.json and .npz | Image metrics and decoded outputs for three trained encoders, with three held-out bases per seed. |
| brightness-transfer.csv, brightness-transfer-parameters.json | Structured-transform transfer test: six multipliers, two starting brightness levels, 96 new bases, three trained and three random encoders. All 360 method cells and fitted action parameters. |
| color-discovery.csv | Within-class discovery experiment 15: color and thickness alignment scores from one synthetic-data run, with 40 requested pairs per shape, PCA 20 and ICA 6. Shape labels enter discovery; color labels enter the alignment score. |
| classification.json | Ten image splits with independent and class-correlated blur. Image identities are separated before transformations. |
| geometry-examples.npz | Seed 0 arrays for held-out images of digits 3, 5 and 8, moved along training covariance directions. All three digit classes are present in fitting. |
| shape-actions.json | Ten-seed controlled brightness and color-rotation experiments. Fit on circles/squares; evaluate on triangles/crosses, including three-step composition. |
| shape-action-examples.npz | Seed 0 shape outputs: a fitted 30° color rule applied three times, alongside three additions of the average pixel change. Error maps share one absolute scale and use unclipped arrays. |

[File checksums](data/manifest.json) · [Build instructions](DEVELOPMENT.md)
