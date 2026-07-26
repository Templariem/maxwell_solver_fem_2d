# Maxwell Project - 2D FEM Solver for Electromagnetism

This repository contains the source code for the electromagnetic solver based on the two-dimensional Finite Element Method (FEM), developed from scratch in Python by PhD student Giovanni Cocca-Guardia from Pontificia Universidad Católica de Valparaíso, Chile.

## Prerequisites

To run the experiments, you need to have Python 3.7 or higher installed on your system. It is recommended to use a virtual environment (`venv` or `conda`).

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
This experiment numerically validates the spatial precision of the solver (different meshing algorithms) and simulates the stationary, harmonic, and transient regimes of a conductive sphere and a high-voltage coil.
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
This script calibrates the spatial decay of the electric field using a hybrid analysis with empirical data from LED diodes at various distances.
```bash
python exp_3.py
```
> Here you will observe plots of the calibrated model spatially interpolated to equivalent dimensions in centimeters. Results will also go to `results/`.

## Additional Notes
- The routines for the main mathematical solver are located in `solver_fem_2d.py`.
- It is not necessary to modify the code to observe the results! Everything runs _out of the box_.
