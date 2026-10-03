# Maxwell Solver FEM 2D: Solver, meshes, and reproduction material for Experiments I--III (CLAGTEE 2026)

This repository contains the source code for the electromagnetic solver based on the two-dimensional Finite Element Method (FEM), developed from scratch in Python by PhD student Giovanni Cocca-Guardia from Pontificia Universidad Católica de Valparaíso, Chile.

## Prerequisites

To run the experiments, you need to have Python 3.10 or higher installed on your system. It is recommended to use a virtual environment (`venv` or `conda`).

### Create Virtual Environment with Conda (Recommended)
To easily create and activate a conda environment named `electro`, run in your terminal:
```bash
conda create -n electro python=3.10
conda activate electro
```

### Project Setup
1. **Clone or download** this repository to your local computer.
2. Open a terminal and navigate to the directory:
   ```bash
   cd path/to/maxwell_solver_fem_2d
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(This will install numpy, scipy, matplotlib, pandas, openpyxl, and gmsh).*

## Execution Order

The code is prepared to run sequentially without needing to modify internal paths. Make sure to always execute the scripts from the `maxwell_solver_fem_2d` folder.

### 1. Mesh Generation (Optional but Recommended)
If you want to regenerate the structural meshes from scratch using the Gmsh API:
```bash
python mesh_generator.py
```
> This will create/overwrite the `.npz` files inside the `gmsh_meshes/` folder.

### 2. Experiment I - Geometric Precision and Dynamic Solver
This experiment numerically validates the spatial precision of the solver (different meshing algorithms) and simulates the stationary, harmonic, and transient regimes of a conductive sphere and a Tesla coil.
```bash
python exp_1.py
```
> The results, metrics, and animations from this test will be saved in the `results/` subfolder.

### 3. Experiment II - Faraday's Law and Magnetic Field
This experiment demonstrates the simulation of electromagnetic induction over a multiphysics domain (coil, capacitive dipoles, eddy current induction).
```bash
python exp_2.py
```
> The results will automatically be saved in the `results/` folder.

### 4. Experiment III - Experimental Calibration with LED Diodes
This script solves the Cartesian 2D coil prior and remaps its contour amplitudes with a single power law fitted to five manually observed LED activation distances and color-assigned voltages. These voltages are calibration-derived surrogates, not independent local-potential or field measurements.
```bash
python exp_3.py
```
> Results include the remapped grid, Figure 4(a) construction, Table III quantities, and a parameter/provenance record. Distances outside 5–17 cm are extrapolations. The five LED pairs are white (5 cm, 3.3 V), blue (6 cm, 3.1 V), green (6.5 cm, 2.5 V), yellow (12 cm, 2.1 V), and red (17 cm, 2.0 V); LED legs were 2 cm apart.

## Additional Notes
- The routines for the main mathematical solver are located in `solver_fem_2d.py`.
- It is not necessary to modify the code to observe the results! Everything runs _out of the box_.

## CLAGTEE 2026 release

The release tag `clagtee-2026-v1.0` identifies the solver, meshes and Experiments I–III associated with the revised manuscript. Experiment III retains the updated global five-LED fit; it has not been reverted to historical interpolation. The solver uses Cartesian integration, not an implemented axisymmetric 2πr weighting. The assumed 45 kV amplitude is an approximate breakdown-based estimate, not a measured terminal voltage.

Run the additional calibration sensitivity analysis with:

```sh
python calibration_sensitivity.py
```

This leaves out each LED pair in turn. The exponent ranges from 0.362 to 0.505; the largest change from the full fit over 5–17 cm is 9.56%. These are descriptive sensitivities, not measurement uncertainty intervals. The main experiment always retains all five pairs. Recorded results are in [docs/calibration_summary.json](docs/calibration_summary.json) and [docs/calibration_leave_one_LED_out.csv](docs/calibration_leave_one_LED_out.csv).

[The adapter-training procedure](docs/ADAPTER_TRAINING.md) documents the paper's physical ensemble and sequential visual residual. This release contains **no AI implementation, model weights, video dataset, annotations, or feature caches**. Consequently it reproduces the public FEM/calibration experiments, not the complete private machine-learning experiment. Downloading the pretrained backbones alone does not reproduce the trained adapters.

[Distance conventions](docs/DISTANCES_AND_CALIBRATION.md) distinguish center distance, surface distance, FEM remapping and image-profile visualization.
