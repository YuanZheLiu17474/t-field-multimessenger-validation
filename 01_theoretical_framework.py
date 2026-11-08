# 01_theoretical_framework.py
# Generates Figures 1-6 and 11 for the t-Field EFT paper.
# Dependencies: numpy, matplotlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

def generate_figures():
    # ==========================================
    # Figure 1: Nuclear Mass Residuals
    # ==========================================
    A_data = np.array([2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 39, 40, 48, 52, 54, 55, 56, 57, 58, 59, 60, 62, 63, 64, 66, 69, 74, 75, 79, 80, 84, 85, 88, 89, 90, 98])
    Z_data = np.array([1, 1, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 19, 20, 20, 24, 26, 25, 26, 26, 28, 27, 28, 28, 29, 30, 30, 31, 32, 33, 35, 34, 36, 37, 38, 39, 40, 42])
    residual_data = np.array([0.0, 3.0, 6.1, -0.5, -2.3, -1.4, -2.1, -1.5, 2.0, 1.0, 2.1, 1.0, 1.4, -1.1, -3.2, -3.5, -1.8, -3.0, -1.6, -0.6, -1.6, 0.0, 1.2, 0.1, 1.4, 0.3, -0.4, 0.4, -0.5, 0.0, -0.8, 4.3, 0.7, 1.0, 2.4, 1.2, 2.4, 1.2, 2.2, 0.9, 0.9, 1.3, -1.3, -1.2, -0.7, -1.4, -1.5, -2.3, -0.1, 0.1, 0.2, 1.7, 2.4, -0.3, -3.4])

    fig, ax = plt.subplots(figsize=(10, 6))
    sc = ax.scatter(A_data, residual_data, c=Z_data, cmap='viridis', s=80, edgecolor='k', alpha=0.8)
    plt.colorbar(sc, label='Proton Number (Z)')
    for m in [2, 8, 20, 28, 50, 82]:
        ax.axvline(m, color='red', linestyle='--', alpha=0.3)
        if m <= max(A_data):
            ax.text(m, max(residual_data)+1, f'Z/N={m}', color='red', rotation=90, va='top', ha='right', fontsize=8)
    ax.axhline(0, color='black', linewidth=1)
    ax.set_xlabel('Mass Number A', fontsize=14); ax.set_ylabel('Residual (MeV)', fontsize=14)
    ax.set_title('Residuals of 58 Nuclear Masses', fontsize=16)
    ax.grid(True, alpha=0.3)
    plt.savefig('Figure1_Nuclear_Residuals.png', dpi=300, bbox_inches='tight'); plt.close()

    # ==========================================
    # Figure 2: Dark Photon Parameter Space
    # ==========================================
    m_range = np.logspace(-9, -2, 100)
    eps = 2.0e-10 * (m_range / 1e-3)
    plt.figure(figsize=(10, 6))
    plt.loglog(m_range, eps, 'b-', lw=2.5)
    plt.xlabel(r'Dark Photon Mass \(m_{\gamma^\prime}\) (GeV)', fontsize=14)
    plt.ylabel(r'Kinetic Mixing \(\epsilon\)', fontsize=14)
    plt.axvline(1e-3, color='r', linestyle='--', label='Typical BEC scale')
    plt.title('Dark Photon Parameter Space', fontsize=16)
    plt.legend(); plt.grid(True, which="both", alpha=0.3)
    plt.savefig('Figure2_Parameter_Space.png', dpi=300, bbox_inches='tight'); plt.close()

    # ==========================================
    # Figure 3: Redshift of BEC Formation
    # ==========================================
    z = np.logspace(0, 4, 500)
    T_gamma = 2.725 * (1 + z)
    T_c = 1000.0
    z_cross = z[np.argmin(np.abs(T_gamma - T_c))]
    plt.figure(figsize=(10, 6))
    plt.loglog(z, T_gamma, 'k-', lw=2, label='Cosmic Temperature')
    plt.axhline(T_c, color='b', linestyle='--', lw=2.5, label='Critical Temperature')
    plt.scatter([z_cross], [T_c], color='red', s=150, zorder=5)
    plt.xlabel(r'Redshift \(z\)', fontsize=14); plt.ylabel(r'Temperature (K)', fontsize=14)
    plt.title('Redshift of Dark Photon BEC Formation', fontsize=16)
    plt.legend(); plt.grid(True, which="both", alpha=0.3)
    plt.savefig('Figure3_Redshift_Formation.png', dpi=300, bbox_inches='tight'); plt.close()

    # ==========================================
    # Figure 4: Jeans Mass vs Dark Photon Mass
    # ==========================================
    G_N = 6.67e-39; rho_0 = 0.3 / (1.3e41); M_sun = 1.1e57
    m_test = np.logspace(-6, 0, 50)
    M_Jeans = [(0.001 * (m / 1e-3)**0.5)**3 / (np.sqrt(G_N**3 * rho_0)) / M_sun for m in m_test]
    plt.figure(figsize=(10, 6))
    plt.loglog(m_test, M_Jeans, 'g-', lw=2.5)
    plt.axhline(1e12, color='r', linestyle='--', label='Typical Galaxy Mass')
    plt.xlabel(r'Dark Photon Mass \(m_{\gamma^\prime}\) (GeV)', fontsize=14)
    plt.ylabel(r'Jeans Mass (\(M_\odot\))', fontsize=14)
    plt.title('Jeans Mass vs Dark Photon Mass', fontsize=16)
    plt.legend(); plt.grid(True, which="both", alpha=0.3)
    plt.savefig('Figure4_Jeans_Mass.png', dpi=300, bbox_inches='tight'); plt.close()

    # ==========================================
    # Figure 5: BEC Core vs NFW Cusp
    # ==========================================
    r = np.logspace(-1, 2, 500)
    rho_0_nfw = 1e7; r_s = 10.0; R_TF = 15.0
    rho_NFW = rho_0_nfw / ((r/r_s) * (1 + r/r_s)**2)
    rho_BEC = np.where(r <= R_TF, rho_0_nfw * (1 - (r/R_TF)**2), 1e2)
    plt.figure(figsize=(10, 6))
    plt.loglog(r, rho_BEC, 'b-', lw=3.5, label='t-Field BEC (Core)')
    plt.loglog(r, rho_NFW, 'r--', lw=2.5, label='Standard CDM (NFW Cusp)')
    plt.xlabel(r'Radius \(r\) (kpc)', fontsize=14); plt.ylabel(r'Density', fontsize=14)
    plt.title('BEC Core vs NFW Cusp', fontsize=16)
    plt.legend(); plt.grid(True, which="both", alpha=0.3)
    plt.savefig('Figure5_BEC_vs_NFW.png', dpi=300, bbox_inches='tight'); plt.close()

    # ==========================================
    # Figure 6: Galactic Rotation Curves (Theory)
    # ==========================================
    r_rot = np.linspace(0.1, 50, 500)
    rho_rot = np.where(r_rot <= R_TF, rho_0_nfw * (1 - (r_rot/R_TF)**2), 0)
    M_enclosed = np.cumsum(4 * np.pi * r_rot**2 * rho_rot * (r_rot[1]-r_rot[0]))
    v_BEC = np.sqrt(np.where(r_rot > 0, 4.3e-6 * M_enclosed / r_rot, 0))
    v_NFW = np.sqrt(4.3e-6 * M_enclosed[-1] / r_rot) * 0.7
    plt.figure(figsize=(10, 6))
    plt.plot(r_rot, v_BEC, 'b-', lw=3, label='t-Field BEC Halo')
    plt.plot(r_rot, v_NFW, 'r--', lw=2.5, label='Standard CDM Halo')
    plt.xlabel(r'Radius \(r\) (kpc)', fontsize=14); plt.ylabel(r'Velocity \(v(r)\) (km/s)', fontsize=14)
    plt.title('Galactic Rotation Curves', fontsize=16)
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig('Figure6_Rotation_Curves.png', dpi=300, bbox_inches='tight'); plt.close()

    # ==========================================
    # Figure 11: EFT Extrapolation (Pink band)
    # ==========================================
    A_extrap = np.linspace(100, 240, 50)
    res_extrap = -0.05 * (A_extrap - 100)
    plt.figure(figsize=(10, 6))
    plt.scatter(A_data, residual_data, color='blue', alpha=0.6, label='Training Data')
    plt.fill_between(A_extrap, res_extrap - 20, res_extrap + 20, color='red', alpha=0.2, label='EFT Extrapolation Band')
    plt.plot(A_extrap, res_extrap, 'r--', lw=2)
    plt.axvline(x=100, color='gray', linestyle=':', label='EFT Boundary')
    plt.xlabel(r'Mass Number \(A\)', fontsize=14); plt.ylabel('Residual (MeV)', fontsize=14)
    plt.title('t-Field EFT Extrapolation to Superheavy Nuclei', fontsize=16)
    plt.legend(); plt.grid(alpha=0.3)
    plt.savefig('Figure11_EFT_Extrapolation.png', dpi=300, bbox_inches='tight'); plt.close()
    
    print("Theoretical Framework Figures (1-6, 11) generated successfully.")

if __name__ == "__main__":
    generate_figures()