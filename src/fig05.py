# -*- encoding: utf-8 -*-
"""
@File    :   fig05.py
@Time    :   2025/08/12 22:29:00
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :
"""

# %% Import packages
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

# %% Load data
datapath = proj_root / "data/fig05_rht_along_chain.h5"
dataset = {"AType": {}, "BType": {}}
with h5py.File(datapath, "r") as hf:
    keys = list(dataset.keys())
    for key in keys:
        gp = hf[key]
        for key_sub, val in gp.items():
            dataset[key][key_sub] = val[()]

# %% Plot
um = 1e-6
markers = ["^", "o", "*"]
colors = sns.color_palette("muted")

fig, axs = plt.subplots(1, 2)
ax0, ax1 = axs
# A-type
for i, ptype in enumerate(["A", "B"]):
    xdata = dataset["AType"]["d"]
    ydata = dataset["AType"][f"ht_{ptype}"]
    ax0.scatter(
        xdata / um,
        ydata,
        label=f"NP ${ptype}$",
        marker=markers[i],
        facecolor="none",
        edgecolor=colors[i],
    )
ax0.set(
    yscale="log",
    xlabel="Interparticle Distance (um)",
)
ax0.legend()
# B-type
for i, ptype in enumerate(["A", "B"]):
    xdata = dataset["BType"]["d"]
    ydata = dataset["BType"][f"ht_{ptype}"]
    ax1.scatter(
        xdata / um,
        ydata,
        label=f"NP ${ptype}$",
        marker=markers[i],
        facecolor="none",
        edgecolor=colors[i],
    )
ax1.set(
    yscale="log",
    xlabel="Interparticle Distance (um)",
)
ax1.legend()
ax0.set(title="A-type stub chain", ylabel=alias["ht"])
ax1.set(title="B-type stub chain", ylabel=alias["ht"])
fig.tight_layout()
