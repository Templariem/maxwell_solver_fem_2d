# Adapter-training procedure for the CLAGTEE 2026 manuscript

This document describes the private Experiment IV method. The public release contains the FEM solver, meshes and Experiments I–III, together with this methodological description. AI implementation, images, annotations, feature caches and learned weights are not distributed. This document supports inspection and reimplementation; it does not make the private video experiment fully executable from this repository.

## Data and targets

The experiment contains 271 annotated keyframes from nine videos. Exclude all 107 frames lacking a localizable probe before fitting or scoring, leaving 128 development frames in Videos 1–7 and 36 holdout frames in Videos 8–9. Never replace a missing query with default coordinates or a 3.3 V target. Virtual queries used only to illustrate Figure 5 do not enter training or metrics.

The image scale is 4.5/(2 Rpx) cm/pixel. For the implemented geometry, polygon centroids and the mean annotated sphere radius are truncated to integer pixels. Let d be the nonnegative nearest distance from the probe centroid to either conductor polygon, converted to centimetres. The target is

Y = 6.019078473682064 (d/1 cm)^(-0.40580894137904955) V.

Only the five documented LED pairs define this law. Voltages are assigned by LED color; distances are manual activation observations with 2 cm LED-leg separation. No endpoint anchors or voltage clipping are used. The slope feature and target share this calibration; high agreement is not independent field validation.

Of the development/holdout frames, 71/15 are within 5–17 cm and 57/21 are extrapolated. Report both holdout domains separately. All retained query distances exceed the derivative half-step of 0.05 cm.

## Frozen backbones and image features

Obtain the official pretrained models through their model pages and complete any access or license steps required by the provider:

| Encoder | Official checkpoint | Exact revision used |
|---|---|---|
| DINOv3 ViT-S/16 | [facebook/dinov3-vits16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m) | `114c1379950215c8b35dfcd4e90a5c251dde0d32` |
| I-JEPA ViT-H/14 | [facebook/ijepa_vith14_1k](https://huggingface.co/facebook/ijepa_vith14_1k) | `f157467ea509bc356ff9f61fd3c0d840eec5e04e` |

These downloads provide the frozen feature extractors, **not the trained physical adapters, residual heads, PCA or scalers**. Those components must be fitted using the procedure below and a suitable annotated dataset. This repository does not require either backbone to execute its public FEM experiments.

Resize RGB images bilinearly to 224 × 224, rescale by 1/255, and normalize channels. DINOv3 uses means (0.485, 0.456, 0.406) and standard deviations (0.229, 0.224, 0.225); I-JEPA uses 0.5 for both. Keep both backbones frozen and in evaluation mode.

DINOv3 concatenates its 384-dimensional class token with a 384-dimensional local patch feature. Exclude its four register tokens from the 14 × 14 patch grid. I-JEPA concatenates the mean of its 16 × 16 patch tokens with a local feature, each 1280-dimensional. Local pooling uses a 3 × 3 neighborhood at the query: center/edge/corner weights 0.40/0.10/0.05 and clamped image-edge indices. Raw feature dimensions are therefore 768 and 2560.

Use one clean image and four ColorJitter variants for hybrid residual training, with brightness/contrast 0.20, saturation 0.15 and hue 0.03. No geometric augmentation is applied. Variant a = 1,…,4 of frame number i uses seed 42 + 1009a + i. Fit randomized PCA with 128 components and seed 42 on the expanded training fold only; fit a standard scaler on its PCA scores. Validation and holdout use clean features transformed by the training-fitted PCA and scaler.

## Physical ensemble

The five physical inputs are the FEM magnitude in volts, the negative centered derivative of the fitted law in V/cm, sphere-center distance in cm, and normalized image x/y coordinates. The derivative is [V(d−0.05) − V(d+0.05)]/0.10. The FEM feature samples the terminal-height profile at (r/100, 0.1225) m, where r is the image-plane center distance; **do not add the sphere radius to a distance already measured from its center**. See [distance conventions](DISTANCES_AND_CALIBRATION.md).

Fit physical standardization only on the clean training partition. Train three independently initialized adapters and average their predictions. Each adapter has this topology:

1. Linear 5→256, BatchNorm and SiLU.
2. Residual branch: Linear 256→256, BatchNorm, SiLU, dropout 0.15, Linear 256→256, BatchNorm. Add the identity branch and apply SiLU.
3. Residual branch: Linear 256→128, BatchNorm, SiLU, dropout 0.15, Linear 128→128, BatchNorm. Add a learned Linear 256→128 projection of the block input and apply SiLU.
4. Linear 128→1 output.

Use 180 epochs, shuffled minibatches of 32, AdamW with learning rate 0.005 and weight decay 0.0001, Smooth L1 loss with beta 0.5, and cosine annealing to 0.00001 over 180 epochs. There is no early stopping. Seed Python, NumPy, PyTorch and the minibatch generator. The implementation retains the final epoch, rather than selecting by holdout performance.

## Sequential residual fitting

Freeze the trained physical ensemble and compute its mean prediction on the clean training samples. Define the residual target as Y minus that prediction. Repeat the same residual target for the clean image and its four photometric variants. The residual is an in-sample physical residual, not an out-of-fold residual; preserve this distinction when reimplementing the method.

Fit the visual head to the standardized PCA-128 features: Linear 128→64, LayerNorm, SiLU, dropout 0.20, Linear 64→32, SiLU, Linear 32→1. Use 160 full-batch epochs, AdamW with learning rate 0.001 and weight decay 0.01, MSE loss and cosine annealing to 0.00001. Keep the physical ensemble and backbone frozen throughout. There is no early stopping.

At inference, return the physical ensemble mean plus 0.25 times the predicted visual residual. The 0.25 gate is fixed, is not fitted per frame, and does not scale the target during residual training. Save the physical scaler, three physical state dictionaries, PCA, visual scaler, residual state dictionary and gate together. Saved backbone weights alone cannot substitute for these fitted components.

## Cross-validation and final fit

Retain five validation video groups in this order: {6}, {4}, {2}, {1,5}, {3,7}. For fold k = 1,…,5, use the remaining development videos for training. Fit each physical scaler, PCA and visual scaler only within that fold; no development-validation or holdout features may enter their fitting.

The three physical seeds in fold k are 42 + 10k + j, j = 0,1,2; the residual seed is 170 + 100k. Average the three physical predictions before computing each fold score. CV means and sample standard deviations aggregate five fold scores, not fifteen independent seed scores. The final physical seeds are 42, 43 and 44, with residual seed 170; this final fit uses all 128 development frames. Score the 36 holdout frames together using conventional R², MSE and MAE, and additionally report the two calibration domains.

The hyperparameters were selected during initial DINOv3 development CV and transferred unchanged to I-JEPA. Selection was not nested within each reported fold. The previously examined holdout is a corrected reanalysis, not a fresh independent test. The center-distance correction retains labels, queries, video assignments and hyperparameters and refits physical and residual modules. Frozen feature caches remain applicable because their images and query locations are unchanged. Seed control does not guarantee bitwise identity across hardware.

The vision-only diagnostic has a different protocol: 14 variants plus the clean image, PCA-128 fitted within each expanded training fold, the physical-adapter optimizer and topology with input dimension 128, seeds 42–46, and an average of five fold models on holdout. It is not a matched residual ablation. Its saved five-LED results are unaffected by the correction of physical center-distance features.

## Inference timing

Measure the final fitted hybrids without training during timed passes. The recorded platform is Apple M4 Pro/MPS with four CPU threads, macOS 26.6.2, Python 3.14.6, PyTorch 2.13.0, torchvision 0.28.0, Transformers 5.14.1, NumPy 2.5.1, SciPy 1.18.0, scikit-learn 1.9.0, pandas 3.0.3, OpenCV 5.0.0.93 and Pillow 12.3.0. These are the observed run versions, not additional dependencies for the public solver.

Alternate encoder order over five passes per encoder. Load outside timing, warm up on five frames and then time the 36 clean holdout frames individually, with device synchronization. Include preprocessing, transfers, backbone extraction, local pooling, PCA, scalers and prediction heads. Exclude model loading, file decoding/acquisition, geometry extraction, the FEM solve and overlay rendering. Report mean latency and sample standard deviation across the five pass means, with FPS = 1000 / pooled mean latency in milliseconds. One session does not establish cross-device performance or complete application throughput.
