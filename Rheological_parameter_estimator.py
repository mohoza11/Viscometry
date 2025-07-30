# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 12:27:59 2025

@author: zaman
Rheological parameters estimation by curve fitting
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import os

# ─── 1. User-controllable axis limits ────────────────────────────────────────
x_min, x_max = 1e0, 3e2    # adjust as needed
y_min, y_max = 1e-1, 1e1   # adjust as needed

# ─── 2. Load your CSV ───────────────────────────────────────────────────────
file_path = r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\40PEO_60AHCNC_10Sol\40PEO_60AHCNC_10Sol_analyzed.csv"
df = pd.read_csv(file_path)
print(df.head())

shear_rate = df['IKA Rotavisc - Shear rate [1/s]'].values
viscosity  = df['IKA Rotavisc - Viscosity [Pa s]'].values

# ─── 3. Define models ───────────────────────────────────────────────────────
def power_law(sr, k, n):
    return k * sr**(n - 1)

def herschel_bulkley(sr, k, n, tau0):
    return k * sr**(n - 1) + tau0 / sr

def carreau_yasuda_fixed_a(sr, eta_inf, eta0, K, n):
    a = 10.0
    return eta_inf + (eta0 - eta_inf) / (1 + (K * sr)**a)**((1 - n) / a)

# ─── 4. Log–Log linear fit for Power-Law ────────────────────────────────────
log_sr   = np.log(shear_rate)
log_visc = np.log(viscosity)
slope, intercept = np.polyfit(log_sr, log_visc, 1)
n_pl = slope + 1
k_pl = np.exp(intercept)
popt_pl = [k_pl, n_pl]

# compute metrics for Power-Law
y_pred_pl = power_law(shear_rate, k_pl, n_pl)
ss_res_pl = np.sum((viscosity - y_pred_pl)**2)
ss_tot    = np.sum((viscosity - np.mean(viscosity))**2)
r2_pl     = 1 - ss_res_pl/ss_tot
rmse_pl   = np.sqrt(np.mean((viscosity - y_pred_pl)**2))

# ─── 5. Fit Herschel–Bulkley ────────────────────────────────────────────────
p0_hb = [1.0, 0.7, 0.1]
bnds_hb = ([0.0, 0.0, 0.0], [np.inf, 1.0, np.inf])
popt_hb, pcov_hb = curve_fit(herschel_bulkley, shear_rate, viscosity, p0=p0_hb, bounds=bnds_hb)

# ─── 6. Fit Carreau–Yasuda (a=10) ───────────────────────────────────────────
p0_cy = [viscosity.min(), viscosity.max(), 1.0, 0.5]  # [η∞, η₀, K, n]
bnds_cy = ([0.0,      0.0,         0.0, 0.01],
          [np.inf,  np.inf,       np.inf, 1.0])
popt_cy, pcov_cy = curve_fit(carreau_yasuda_fixed_a,
                             shear_rate,
                             viscosity,
                             p0=p0_cy,
                             bounds=bnds_cy)

# ─── 7. Metrics helper & print ──────────────────────────────────────────────
def metrics(model, popt, pcov):
    y_pred = model(shear_rate, *popt)
    ss_res = np.sum((viscosity - y_pred)**2)
    ss_tot = np.sum((viscosity - np.mean(viscosity))**2)
    r2     = 1 - ss_res/ss_tot
    se     = np.sqrt(np.diag(pcov))
    rmse   = np.sqrt(np.mean((viscosity - y_pred)**2))
    return r2, se, rmse

r2_hb, se_hb, rmse_hb = metrics(herschel_bulkley, popt_hb, pcov_hb)
r2_cy, se_cy, rmse_cy = metrics(carreau_yasuda_fixed_a, popt_cy, pcov_cy)

# print results
print("\n--- Power-Law (log–log) ---")
print(f" k={k_pl:.4f}, n={n_pl:.4f}, R²={r2_pl:.4f}, RMSE={rmse_pl:.4f}")

print("\n--- Herschel–Bulkley ---")
print(f" k={popt_hb[0]:.4f}, n={popt_hb[1]:.4f}, τ₀={popt_hb[2]:.4f}, R²={r2_hb:.4f}, RMSE={rmse_hb:.4f}")

print("\n--- Carreau–Yasuda ---")
print(f" η∞={popt_cy[0]:.4f}, η₀={popt_cy[1]:.4f}, K={popt_cy[2]:.4f}, n={popt_cy[3]:.4f}, R²={r2_cy:.4f}, RMSE={rmse_cy:.4f}")

# ─── 8. Plot on log–log with legend including the data ─────────────────────
shear_fit = np.logspace(np.log10(shear_rate.min()), np.log10(shear_rate.max()), 200)

fig, ax = plt.subplots()
ax.set_xscale('log')
ax.set_yscale('log')

ax.scatter(
    shear_rate,
    viscosity,
    label='Original data',
    marker='o',
    color='C0',
    zorder=5
)

ax.plot(shear_fit, power_law(shear_fit,        *popt_pl), label='Power-Law',            color='C1')
ax.plot(shear_fit, herschel_bulkley(shear_fit, *popt_hb), label='Herschel–Bulkley',     color='C2')
ax.plot(shear_fit, carreau_yasuda_fixed_a(shear_fit, *popt_cy),
        label='Carreau–Yasuda', color='C3')

ax.set_xlabel('Shear rate [1/s]')
ax.set_ylabel('Viscosity [Pa·s]')

#input the sample name
ax.set_title(f"40PEO_60AHCNC_10Sol", pad=15)

ax.legend(loc='best', frameon=False)
ax.set_xlim(1, 400)
ax.set_ylim(0, 10)

ax.minorticks_on()
ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.8)
ax.grid(which='minor', linestyle=':', linewidth=0.3, alpha=0.6)

plt.tight_layout()

# ─── 9. Save the figure next to the CSV ────────────────────────────────────
csv_dir, csv_file = os.path.split(file_path)
base, _          = os.path.splitext(csv_file)
out_png          = os.path.join(csv_dir, f"{base}.png")

fig.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"Figure saved to {out_png}")

plt.show()
