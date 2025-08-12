# -*- encoding: utf-8 -*-
"""
@File    :   fig01.py
@Time    :   2025/08/12 16:31:45
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :   This script is used to present the IP and OP mode band structure under periodic boundary conditions
"""

# %% Packages import
import os
import sys
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sympy as sp
import yaml
from scipy.constants import pi

proj_root = Path(__file__).parents[1]

sns.set_theme("paper", style="ticks")
with open(proj_root / "src/alias.yml") as f:
    alias = yaml.safe_load(f)
# %% Load data and plot
datapath = proj_root / "data/fig01_band_structures_pbc.h5"
fig, axs = plt.subplots(1, 2, figsize=(6, 3), sharey=True)
# 1. QSNN Line plot
with h5py.File(datapath, "r") as hf:
    for i, mode in enumerate(["xy", "z"]):
        if mode == "xy":
            title = "IP mode"
        elif mode == "z":
            title = "OP mode"
        xdata = hf["/QSNN/kxs"][()]
        xdata = np.linspace(-pi, pi, xdata.size, endpoint=True)
        ydata = hf[f"/QSNN/w{mode}[cm^-1]"][()]
        lines = axs[i].plot(xdata, ydata.real, ls="--", c="#004488")
        axs[i].set(title=title)

# 2. Full Scatter plot
with h5py.File(datapath, "r") as hf:
    for i, mode in enumerate(["xy", "z"]):
        xdata = hf["/Full/kxs"][()]
        xdata = np.linspace(-pi, pi, xdata.size, endpoint=True)
        ydata = hf[f"/Full/w{mode}[cm^-1]"][()]
        # scatter plot
        for iband in range(ydata.shape[-1]):
            sc = axs[i].scatter(
                xdata[::4], ydata[::4, iband].real, s=3, c="#bb5566"
            )

# Setting title and labels
for i in range(2):
    axs[i].set(
        xlim=[-pi, pi],
        xticks=pi * np.arange(-1, 1.01, 0.5),
        xticklabels=[
            sp.latex(sp.pi / 2 * i, mode="inline") for i in range(-2, 3)
        ],
        xlabel=r"$k_x~d$",
    )
axs[0].set(ylabel=alias["freq"])
axs[1].legend(
    handles=[lines[0], sc], labels=["QSNN Approx.", "Full Calculation"]
)
fig.tight_layout()
