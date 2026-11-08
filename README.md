# t-Field EFT: Multi-Messenger Validation Code

This repository contains the Python code to generate all 11 figures for the paper: **"Phenomenological Analysis of Nuclear Mass Residuals and a Multi-Messenger Validation of the t-Field Dark Photon Condensate"**.

## Repository Structure

- `01_theoretical_framework.py`: Generates Figures 1-6 and 11 (Nuclear residuals, dark photon parameters, BEC physics).
- `02_nicer_neutron_star_validation.py`: Generates Figure 8 (NICER 2D posterior vs. TOV curve).
- `03_multimessenger_validation.py`: Generates Figures 7, 9, 10 (LIGO tidal deformability, SPARC rotation curves, GRB attenuation).

## Requirements & Data

Install dependencies:
```bash
pip install numpy matplotlib scipy pandas
Data files needed (must be placed in the root directory):

equal_weight_samples_PDTU.txt (for Fig 8)

ligo.dat (for Fig 7)

DDO161.json, NGC3198_SPARC.json, DDO154_SPARC.json (for Fig 9)

Note: Fig 10 uses hardcoded public data points from LHAASO/Fermi observations.

Usage
Run the scripts directly to generate the 300 DPI PNG figures:

bash
python 01_theoretical_framework.py
python 02_nicer_neutron_star_validation.py
python 03_multimessenger_validation.py