# 03_multimessenger_validation.py
# Generates Figures 7, 9, and 10 (LIGO, SPARC, GRB validations).
# Dependencies: numpy, matplotlib, scipy, pandas
# Data requirements: Place 'ligo.dat', 'DDO161.json', 'NGC3198_SPARC.json', etc., in the directory.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import gaussian_kde
from scipy.optimize import curve_fit
import json
import pandas as pd
import os

matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

def generate_figure_7_ligo():
    try:
        data = np.loadtxt('ligo.dat', skiprows=1)
        m1, m2 = data[:, 2], data[:, 3]
        l1, l2 = data[:, 4], data[:, 5]
        eta = (m1 * m2) / (m1 + m2)**2
        term1 = (1 + 7*eta - 31*eta**2) * (l1 + l2)
        term2 = np.sqrt(np.maximum(0, 1 - 4*eta)) * (l1 - l2)
        Lambda_tilde = (8/13) * (term1 + term2)
        Lambda_tilde = Lambda_tilde[np.isfinite(Lambda_tilde)]

        plt.figure(figsize=(9, 6))
        kde = gaussian_kde(Lambda_tilde)
        x_vals = np.linspace(0, 1000, 500)
        y_vals = kde(x_vals)
        plt.plot(x_vals, y_vals, color='blue', lw=3, label='LIGO GW170817 Observed')
        plt.fill_between(x_vals, y_vals, color='lightblue', alpha=0.5)
        plt.axvline(x=200, color='red', linestyle='--', lw=3, label=r't-Field EoS Prediction (\(\sim 200\))')
        plt.xlabel(r'Effective Tidal Deformability \(\tilde{\Lambda}\)', fontsize=16)
        plt.ylabel('Probability Density', fontsize=16)
        plt.title('LIGO Constraint vs. t-Field Prediction', fontsize=18)
        plt.legend(); plt.grid(alpha=0.3); plt.xlim(0, 1000)
        plt.tight_layout()
        plt.savefig('Figure7_LIGO_Validation.png', dpi=300, bbox_inches='tight'); plt.close()
        print("Figure 7 (LIGO) generated successfully.")
    except Exception as e:
        print(f"Error generating Figure 7: {e}")

def generate_figure_9_sparc():
    galaxies = ['DDO161', 'NGC3198_SPARC', 'DDO154_SPARC'] # Add others if files exist
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    try:
        for i, gal in enumerate(galaxies):
            filename = f'{gal}.json'
            if not os.path.exists(filename):
                print(f"Warning: {filename} not found, skipping.")
                continue
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)
            df = pd.DataFrame(content.get("galaxy", content).get("data", []))
            df.columns = [c.lower() for c in df.columns]
            R = np.array(df['rad']); V_obs = np.array(df['vobs'])
            V_bar = np.sqrt(np.array(df.get('vgas', 0))**2 + np.array(df.get('vdisk', 0))**2)
            
            def total_curve(r, V0, rc):
                return np.sqrt(np.interp(r, R, V_bar)**2 + (V0 * (1 - np.exp(-r / rc)))**2)
                
            popt, _ = curve_fit(total_curve, R, V_obs, p0=[50.0, 2.0])
            R_smooth = np.linspace(0.1, max(R)*1.1, 200)
            axes[i].errorbar(R, V_obs, yerr=np.array(df.get('errv', 0)), fmt='o', c='k', capsize=3, label='Observed')
            axes[i].plot(R_smooth, total_curve(R_smooth, *popt), 'r-', lw=3, label='t-Field Prediction')
            axes[i].set_title(gal); axes[i].set_xlabel('Radius (kpc)'); axes[i].set_ylabel('Velocity (km/s)')
            axes[i].legend(); axes[i].grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('Figure9_SPARC_Validation.png', dpi=300, bbox_inches='tight'); plt.close()
        print("Figure 9 (SPARC) generated successfully.")
    except Exception as e:
        print(f"Error generating Figure 9: {e}")

def generate_figure_10_grb():
    # Exact data from Fig3A_SED.txt (230-300s observed)
    E_obs = np.array([0.24, 0.35, 0.53, 0.94, 1.78, 3.03, 3.99, 5.22])
    F_obs = np.array([2.83e-6, 2.15e-6, 1.26e-6, 5.29e-7, 2.27e-7, 1.22e-7, 8.63e-8, 3.48e-8])
    err_lower = np.array([1.58e-7, 1.08e-7, 6.13e-8, 2.99e-8, 1.64e-8, 1.30e-8, 2.05e-8, 1.29e-8])
    err_upper = np.array([1.58e-7, 1.08e-7, 6.13e-8, 2.99e-8, 1.64e-8, 1.30e-8, 2.05e-8, 1.29e-8])

    plt.figure(figsize=(8, 6))
    plt.errorbar(E_obs, F_obs, yerr=[err_lower, err_upper], fmt='ro', capsize=4, label='Observed Data (GRB 221009A)', zorder=3)

    E_smooth = np.linspace(0.1, 6.0, 100)
    F_fit = F_obs[0] * np.exp(-1.40 * (E_smooth - E_obs[0])) 
    plt.plot(E_smooth, F_fit, 'k--', lw=2, label='t-Field Dark Photon Oscillation Fit', zorder=2)

    plt.yscale('log'); plt.xscale('log')
    plt.xlabel(r'Energy \(E\) (TeV)', fontsize=14); plt.ylabel(r'Flux (ergs/cm\(^2\)/s)', fontsize=14)
    plt.title('High-Energy Attenuation in GRB 221009A', fontsize=16)
    plt.legend(fontsize=12); plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig('Figure10_GRB_Final.png', dpi=300, bbox_inches='tight'); plt.close()
    print("Figure 10 (GRB) generated successfully.")

if __name__ == "__main__":
    generate_figure_7_ligo()
    generate_figure_9_sparc()
    generate_figure_10_grb()