# -*- coding: utf-8 -*-
"""
analyze_rheology.py

1) If the CSV header has <8 columns, skip the first 5 rows (metadata).
2) Then keep only rows where:
     • IKA Rotavisc - Percent [%] > 10
     • Viscosity, Shear stress, Shear rate are all > 0
3) For each shear rate, select the row with the highest viscosity
4) Plot Viscosity vs. Shear rate on log–log axes
   and display "X:Y" in the title, where
     • X is the number in parentheses after SE1700(…)
     • Y is the number in parentheses after Sylgard527(…)
5) Save analyzed data to `<original_name>_analyzed.csv`
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# 0. Path to your CSV
fn = r"C:\Users\zaman\OneDrive - The Pennsylvania State University\Kelly Brownstead\Viscometry Testing\Viscometry Tests Round 2\PDMS(82)_Silica(8)_Fe3O4_PEG30(10)_9_22_2024\PDMS(82)_Silica(8)_Fe3O4_PEG30(10)_9_22_2024.csv"

# 1. Peek at the header row only
preview = pd.read_csv(fn, nrows=0)
if len(preview.columns) < 8:
    df = pd.read_csv(fn, skiprows=5)
    print("Skipped first 5 rows (found fewer than 8 headers).")
else:
    df = pd.read_csv(fn)
    print("Loaded normally (≥8 headers detected).")

# 2. Normalize column names (strip whitespace, replace NBSPs)
df.columns = (
    df.columns
      .astype(str)
      .str.strip()
      .str.replace('\u00A0', ' ', regex=False)
)

# 3. Extract X and Y from filename
base = os.path.basename(fn)
x_m = re.search(r"SE1700\((\d+)\)", base)
y_m = re.search(r"Sylgard527\((\d+)\)", base)
if x_m and y_m:
    x_val = x_m.group(1)
    y_val = y_m.group(1)
    xy_label = f"{x_val}:{y_val}"
else:
    xy_label = "?"
    print("⚠️ Could not parse X and/or Y from filename – check the patterns.")

# 4. Identify your four target columns
visc_col   = "IKA Rotavisc - Viscosity [Pa s]"
stress_col = "IKA Rotavisc - Shear stress [Pa]"
shear_col  = "IKA Rotavisc - Shear rate [1/s]"
pct_col    = "IKA Rotavisc - Percent [%]"

# 5. Convert to numeric & filter
sub = df[[visc_col, stress_col, shear_col, pct_col]].apply(pd.to_numeric, errors="coerce")
sub = sub.dropna(subset=[visc_col, stress_col, shear_col, pct_col])
sub = sub[
    (sub[visc_col]   > 0) &
    (sub[stress_col] > 0) &
    (sub[shear_col]  > 0) &
    (sub[pct_col]    > 0)
]

# 6. For each shear rate, keep the measurement with the highest viscosity
idx = sub.groupby(shear_col)[visc_col].idxmax()
df_peak = sub.loc[idx].sort_values(by=shear_col)

# 7. Save the filtered peak points (optional fixed name)
df_peak.to_csv("filtered_peak_viscosity.csv", index=False)


# 8. Save to “<original_name>_analyzed.csv” in the same folder
orig_dir  = os.path.dirname(fn)
orig_base = os.path.basename(fn)
name, ext = os.path.splitext(orig_base)
out_path  = os.path.join(orig_dir, f"{name}_analyzed{ext}")
df_peak.to_csv(out_path, index=False)
print(f"Saved analyzed data to: {out_path}")

# 9. Plot Viscosity vs. Shear rate on log–log axes
fig, ax = plt.subplots(figsize=(7,5))
ax.scatter(df_peak[shear_col], df_peak[visc_col], s=60)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Shear rate [1/s]")
ax.set_ylabel("Viscosity [Pa·s]")

ax.set_xlim(0.1, 100)   # shear rate from 0.1 to 1000 1/s
ax.set_ylim(0.01, 1000)   # viscosity from 0.01 to 100 Pa·s

# Include X:Y in the title
ax.set_title(f"PDMS({xy_label})_Fe3O4(15)_PEG30", pad=15)


ax.grid(which='both', linestyle='--', linewidth=0.5)

# 10. Save the figure image as “<original_name>_analyzed.png”
out_png = os.path.join(orig_dir, f"{name}_analyzed.png")
fig.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"Saved plot image to: {out_png}")

plt.tight_layout()
plt.show()
