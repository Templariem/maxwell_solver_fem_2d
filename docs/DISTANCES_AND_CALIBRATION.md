# Distances and calibration

The five distances in Experiment III are surface-referenced LED activation observations. In the FEM terminal-height profile, a surface distance d corresponds to the coordinate x = Rs + d, where Rs = 2.25 cm; the units are converted to metres. Thus the updated `exp_3.py` correctly adds Rs once. This implementation is retained.

Experiment IV, whose implementation and dataset remain private, obtains an image scale s = 4.5/(2 Rpx) cm/pixel from the annotated sphere. The center-distance feature is r = s ||c_probe - c_sphere||. It already measures from the center, so no extra 2.25 cm is added. The FEM feature samples the terminal-height profile at (r/100, 0.1225) m; it is a radial-profile proxy rather than a full registered 3D FEM query.

Labels use d_surf: the nonnegative nearest distance from the probe centroid to either annotated conductor polygon, multiplied by s. Labels and the empirical slope use the same five-LED law V(d) = 6.019078473682064 (d/1 cm)^(-0.40580894137904955) V. This input–label dependence prevents high prediction scores from establishing independent field accuracy.

Figure 5 uses the same nearest-conductor surface-distance convention and image scale. The empirical profile is evaluated outside the conductor polygons; interiors show the photograph only. A half-source-pixel positive distance floor regularizes display near the boundary, but does not modify regression labels or queries. Hybrid displays multiply this profile by prediction(q)/profile(q), using bilinear sampling at the query. They are spatial visualizations of scalar predictions, not independent pixel-wise voltage estimates.

Figure 4(a) instead preserves FEM contour geometry: FEM magnitude along the documented terminal-height profile is associated with surface distance, then the five-LED law is applied to that distance. Figures 4(a) and 5 share the linear Turbo 0.1–8 V scale; only display colors saturate.

The October 3 center-distance correction refitted the physical ensemble and residual heads with unchanged labels, video groups, hyperparameters and seeds. The numerical release contains only the public FEM/calibration code.
