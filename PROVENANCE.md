# Data provenance

The portfolio selects recorded evidence from three independent research projects. The published papers cited on the study pages supply model, method, and dataset context.

| Included data | Origin and meaning |
| --- | --- |
| input-design.json | Mechanistic model inference, experiment 10. Final selection counts from the wider-bound fit audit; nominal generating and refitted rival trajectories independently integrated with the second-order DOP853 formulation. Includes both nominal and basal-preserving count tables. |
| network-grid.csv | GRN experiment 28: nine shared-component weights, eight signal/noise levels, four methods, five seeds per cell, 100 genes. |
| benchmark-dream4.csv, benchmark-boolode.csv | GRN experiment 33: per-dataset average precision on common directed non-self reference edges. |
| response-scaling.csv, response-consistency.json | GRN experiment 42: modular-response controls and aggregate RPE1 split-half consistency. No raw cell measurements are included. |
| response-confound.csv | GRN experiment 41: response-strength control summary. |
| brightness-seed-*.json and .npz | Corrected structured-transform study: metrics and saved decoded outputs for three trained encoders, all three held-out bases per seed. |
| brightness-transfer.csv, brightness-transfer-parameters.json | Structured-transform transfer test: six multipliers, two starting brightness levels, 96 new bases, three trained and three random encoders. All 360 method cells and fitted action parameters. |
| color-discovery.csv | Original within-class discovery experiment 15, current saved quick-run scores: 40 requested pairs per shape, PCA 20, ICA 6. Shape labels enter discovery; color labels enter only the alignment score. This is a small exploratory result, not a held-out classification benchmark. |
| classification.json | Corrected structured-transform classification study: ten splits, independent and class-correlated blur, identity separation before transformations. |
| geometry-examples.npz | Seed 0 rerun of the corrected classification study, checked against its saved scores. First held-out 3, 5 and 8; traversals along training covariance directions. All three digit classes are present in fitting. |
| shape-actions.json | Ten-seed controlled brightness and color-rotation experiments. Fit on circles/squares; evaluate on triangles/crosses, including three-step composition. |
| shape-action-examples.npz | Regenerated seed 0 shape outputs, checked against the recorded single-step residuals. The displayed 90° color change composes the fitted 30° rule three times; the comparison adds the fitted average pixel change three times. Error maps share one absolute scale and use unclipped arrays. |

The input-design JSON contains plotted trajectories and aggregate counts. It does not contain every noisy fitting run. The image gallery contains saved model outputs; the trained checkpoints are maintained with the original project. Rebuilding these figures reproduces the selected presentation, rather than all original experiments.

The release includes a machine-readable [data manifest](data/manifest.json). The build check compares each included file against its SHA-256 fingerprint. Source changes should be reviewed in their relevant study before refreshing the manifest or numerical claims.

Evidence selection: 12 September 2026.

Math rendering uses KaTeX 0.18.7, distributed with its MIT license in `site/vendor/katex/LICENSE`. Scientific figures are generated from the included numerical arrays and tables by `scripts/generate.py`.
