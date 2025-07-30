# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 14:37:13 2025

@author: zaman
"""

# multi_viscosity_plot.py
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 15:00:00 2025

@author: zaman

Plot viscosity vs. shear rate for multiple compositions in one log–log figure.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === 1. Define your files and labels ===
files = {
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\100PEO_0CNC_4Sol\100PEO_0CNC_4Sol(1)_analyzed.csv": "100PEO_0CNC_4Sol",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\71PEO_29CNC_5.6Sol\71PEO_29CNC_5.6Sol_analyzed.csv": "71PEO_29CNC_5.6Sol",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\63PEO_37CNC_6.4Sol\63PEO_37CNC_6.4Sol_analyzed.csv": "63PEO_37CNC_6.4So",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\50PEO_50CNC_8Sol\50PEO_50CNC_8Sol_analyzed.csv": "50PEO_50CNC_8So",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\45PEO_55CNC_8.8Sol\45PEO_55CNC_8.8Sol_analyzed.csv": "45PEO_55CNC_8.8Sol",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\38PEO_62CNC_10.4Sol\38PEO_62CNC_10.4Sol_analyzed.csv": "38PEO_62CNC_10.4Sol",
 
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\70PEO_30CNC_2.9Sol\70PEO_30CNC_2.9Sol_analyzed.csv": "70PEO_30CNC_2.9Sol",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\55PEO_45CNC_3.6Sol\55PEO_45CNC_3.6Sol_analyzed.csv": "55PEO_45CNC_3.6Sol",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\50PEO_50CNC_4Sol\50PEO_50CNC_4Sol_analyzed.csv": "50PEO_50CNC_4So",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\35PEO_65CNC_5.7Sol\35PEO_65CNC_5.7Sol_analyzed.csv": "35PEO_65CNC_5.7Sol",
    #r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\30PEO_70CNC_6.7Sol\30PEO_70CNC_6.7Sol_analyzed.csv": "30PEO_70CNC_6.7Sol"
    
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\100PEO_0CNC_2Sol\100PEO_0CNC_2Sol(1)_analyzed.csv": "100PEO_0CNC_2Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\90PEO_10AHCNC_2.2Sol\90PEO_10AHCNC_2.2Sol_analyzed.csv": "90PEO_10AHCNC_2.2Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\80PEO_20AHCNC_2.5Sol\80PEO_20AHCNC_2.5Sol_analyzed.csv": "80PEO_20AHCNC_2.5Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\60PEO_40AHCNC_3.3Sol\60PEO_40AHCNC_3.3Sol_analyzed.csv": "60PEO_40AHCNC_3.3Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\50PEO_50AHCNC_4Sol\50PEO_50AHCNC_4Sol_analyzed.csv": "50PEO_50AHCNC_4Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\40PEO_60AHCNC_5Sol\40PEO_60AHCNC_5Sol(2)_analyzed.csv": "40PEO_60AHCNC_5Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\90PEO_10AHCNC_4.4Sol\90PEO_10AHCNC_4.4Sol_analyzed.csv": "90PEO_10AHCNC_4.4Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\80PEO_20AHCNC_5Sol\80PEO_20AHCNC_5Sol(1)_analyzed.csv": "80PEO_20AHCNC_5Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\70PEO_30AHCNC_5.7Sol\70PEO_30AHCNC_5.7Sol_analyzed.csv": "70PEO_30AHCNC_5.7Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\60PEO_40AHCNC_6.7Sol\60PEO_40AHCNC_6.7Sol_analyzed.csv": "60PEO_40AHCNC_6.7Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\50PEO_50AHCNC_8Sol\50PEO_50AHCNC_8Sol_analyzed.csv": "50PEO_50AHCNC_8Sol",
    r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Mohamad H. Zamani\Amir's Viscometry\results\40PEO_60AHCNC_10Sol\40PEO_60AHCNC_10Sol_analyzed.csv": "40PEO_60AHCNC_10Sol"
}

# === 2. User‐set axis limits ===
x_min, x_max = 0, 3e2    # [1/s]
y_min, y_max = 0, 30   # [Pa·s]

# === 3. Build the figure ===
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xscale('log')
ax.set_yscale('log')

for csv_file, label in files.items():
    # read and sort
    df = pd.read_csv(csv_file)
    sr   = df['IKA Rotavisc - Shear rate [1/s]'].values
    visc = df['IKA Rotavisc - Viscosity [Pa s]'].values
    idx  = np.argsort(sr)
    sr   = sr[idx]
    visc = visc[idx]

    # plot with filled blue markers
    ax.plot(
        sr,
        visc,
        marker='o',
        linestyle='-',
        markersize=5,
        linewidth=1.2,
        label=label,
        zorder=5
    )

# === 4. Decorate ===
ax.set_xlabel('Shear rate [1/s]', fontsize=12)
ax.set_ylabel('Viscosity [Pa·s]', fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=10)
#ax.set_title("Viscosity vs Shear Rate\nMultiple PDMS:Sylgard527 Compositions", pad=12)

# grid lines
ax.minorticks_on()
ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)
ax.grid(which='minor', linestyle=':',  linewidth=0.3, alpha=0.5)

# axis limits & legend
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.legend(loc='best', frameon=False, fontsize=6)

plt.tight_layout()

# === 5. Save figure ===
out_fig = os.path.join(
    os.path.dirname(list(files.keys())[0]),
    "viscosity_comparison.png"
)
fig.savefig(out_fig, dpi=600, bbox_inches='tight')
print(f"Saved figure to {out_fig}")

plt.show()
