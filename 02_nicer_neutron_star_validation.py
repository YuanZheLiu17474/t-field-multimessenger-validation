# 02_nicer_neutron_star_validation.py
# Generates Figure 8 (NICER posterior validation).
# Dependencies: numpy, matplotlib
# Data requirement: Place 'equal_weight_samples_PDTU.txt' in the same directory.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LogNorm

matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

def generate_figure_8():
    try:
        data = np.genfromtxt('equal_weight_samples_PDTU.txt', comments='#')
        M_samples = data[:, 0]
        R_samples = data[:, 1]

        plt.figure(figsize=(10, 8))
        hb = plt.hexbin(R_samples, M_samples, gridsize=60, cmap='Blues', norm=LogNorm(), mincnt=1, alpha=0.9)
        cb = plt.colorbar(hb)
        cb.set_label('Number of Samples (Log Scale)', fontsize=14)
        
        M_curve = np.linspace(0.8, 2.3, 100)
        # Parameterized t-field EoS curve
        R_curve = 12.5 * (M_curve / 1.4)**(-0.3)
        plt.plot(R_curve, M_curve, 'r-', lw=4, label='t-Field EoS (Parameterized)')
        
        R_14 = 12.5
        plt.scatter([R_14], [1.4], color='darkred', s=150, zorder=5, edgecolor='white', label=fr'\(R_{{1.4}}\) = {R_14:.1f} km')

        plt.xlim(9, 15); plt.ylim(0.8, 2.5)
        plt.xlabel(r'Radius \(R\) (km)', fontsize=16); plt.ylabel(r'Mass \(M\) (\(M_\odot\))', fontsize=16)
        plt.title(r'NICER 2D Posterior vs. t-Field EoS', fontsize=18)
        plt.legend(fontsize=14, loc='upper right'); plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('Figure8_NICER_Validation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Figure 8 (NICER) generated successfully.")
    except Exception as e:
        print(f"Error generating Figure 8: {e}")
        print("Please ensure 'equal_weight_samples_PDTU.txt' is in the directory.")

if __name__ == "__main__":
    generate_figure_8()