"""
NeuralFoil Polar Generator
==========================
Generates aerodynamic polars using NeuralFoil (https://github.com/peterdsharpe/NeuralFoil)
for given airfoils and Reynolds numbers.

Output format: XFoil/xflr5-compatible polar format (fixed-width columns)
so the resulting .txt files can be directly loaded by xflr5 or compared
with XFoil outputs.

Usage:
  - Add airfoil names (without .dat) to foil_names list
  - Set dat_dir to the directory containing .dat files
  - Set Re_list to desired Reynolds numbers
  - Run: python NeuralFoil_Generate_Polars.py

Dependencies: neuralfoil, aerosandbox, numpy
  pip install neuralfoil aerosandbox numpy

Version: 1.1.0
"""

import neuralfoil as nf
import numpy as np
import os

__version__ = "1.1.0"

# ---------------------------------------------------------------------------
# User settings
# ---------------------------------------------------------------------------

# Airfoil names (without .dat extension).
# The script will look for <name>.dat in dat_dir for each name.
foil_names = [
    'JX-RS-Root',
    # 'TL54m3-h7-m1-h75-m0.5-h85-m1.5-r0.8',
    # 'E-N-2575',
    # 'E63',
    # 'NACA4412',
]

# Directory containing .dat airfoil files
dat_dir = "E:/Program Files/Aero/FlyingWing/Amokka-JX/CAD/Profile für SWX/JX-RS/"
# dat_dir = "E:/Program Files/Aero/FlyingWing/"

# Output directory for polar text files
output_dir = "./NeuralFoil_Data"

# Reynolds numbers to analyze
Re_list = [50000, 100000, 200000, 300000, 400000, 600000, 800000]

# Angle-of-attack sweep settings [degrees]
Alpha_Low = -20
Alpha_High = 20
Alpha_step = 0.5

# NeuralFoil model size: "xxsmall" | "xsmall" | "small" | "medium" |
#                        "large"  | "xlarge"  | "xxlarge" | "xxxlarge"
model_size = "xxxlarge"

# ---------------------------------------------------------------------------
# Output header (XFoil/xflr5 compatible)
# ---------------------------------------------------------------------------

def _header(foil_name, Re):
    Re_e6 = Re / 1e6
    return [
        "xflr5 v6.59\n",
        "\n",
        f" Calculated polar for: {foil_name}\n",
        "\n",
        " 1 1 Reynolds number fixed          Mach number fixed         \n",
        "\n",
        " xtrf =   1.000 (top)        1.000 (bottom)\n",
        f" Mach =   0.000     Re =     {Re_e6:.3f} e 6     Ncrit =   9.000\n",
        "\n",
        "  alpha     CL        CD       CDp       Cm    Top Xtr Bot Xtr   Cpmin    Chinge    XCp    \n",
        " ------- -------- --------- --------- -------- ------- ------- -------- --------- ---------\n",
    ]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

os.makedirs(output_dir, exist_ok=True)

for foil_name in foil_names:
    dat_path = os.path.join(dat_dir, foil_name + ".dat")

    if not os.path.exists(dat_path):
        print(f"  [SKIP]  {dat_path}  (file not found)")
        continue

    print(f"  [OK]    {foil_name}")

    for Re in Re_list:
        out_name = os.path.join(output_dir, f"{foil_name}_Re{Re/1e6:.3f}.txt")

        with open(out_name, 'w') as f:
            f.writelines(_header(foil_name, Re))

            for Alpha in np.arange(Alpha_Low, Alpha_High + Alpha_step, Alpha_step):
                aero = nf.get_aero_from_dat_file(
                    filename=dat_path,
                    alpha=Alpha,
                    Re=Re,
                    model_size=model_size,
                )
                CL = aero["CL"][0]
                CD = aero["CD"][0]
                Cm = aero["CM"][0]
                Top_Xtr = aero["Top_Xtr"][0]
                Bot_Xtr = aero["Bot_Xtr"][0]

                # alpha   CL        CD       CDp       Cm    Top Xtr Bot Xtr   Cpmin    Chinge    XCp
                f.write(
                    f"{Alpha:8.3f} {CL:8.4f} {CD:9.5f} {CD:9.5f} {Cm:8.4f}"
                    f" {Top_Xtr:7.4f} {Bot_Xtr:7.4f} {0.0:8.4f} {0.0:9.5f} {0.0:9.5f}\n"
                )
