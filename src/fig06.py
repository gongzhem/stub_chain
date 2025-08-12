# -*- encoding: utf-8 -*-
"""
@File    :   fig06.py
@Time    :   2025/08/12 22:28:43
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :
"""

# %% Import packages
import os
import sys
from pathlib import Path
from typing import List

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
datapath = proj_root / "data/fig06-rht_scaling.h5"
dataset = {}
with h5py.File(datapath, "r") as hf:
    for key, val in hf.items():
        dataset[key] = val[()]


# %% Plot
N_xs = dataset["N_xs"]
fig, axs = plt.subplots(
    2,
    1,
    sharex=True,
    gridspec_kw={"hspace": 0, "height_ratios": [5, 2]},
)
lines = []
for idx, key in enumerate(["SA", "SB"]):
    axs[0].plot(
        N_xs,
        dataset[key],
        ls="--",
        markevery=slice(idx, None, 3),
        label=key,
    )
axs[1].axhline(
    1,
    ls=":",
    c="#a5aa99",
)
axs[1].plot(
    N_xs,
    np.array(dataset["SB"]) / np.array(dataset["SA"]),
    ls="--",
    c="#7f3c8d",
    markersize=3,
    marker="o",
)
axs: List[plt.Axes]
axs[0].set(yscale="log")
axs[0].legend(["A-type stub chain", "B-type stub chain"])
axs[0].set(ylabel=alias["ht"])
axs[1].set(
    xlabel="No. of Unit Cells",
    ylabel=r"$p_{\rm net}^B/p_{\rm net}^A$",
    xscale="log",
    xlim=N_xs[[0, -1]],
)

# An extra d^-2 line
xdata = N_xs[N_xs >= 10]
ydata = (xdata / 10) ** (-2) * 1e-18
axs[0].plot(
    xdata,
    ydata,
    ls="--",
    marker="none",
    c="gray",
)
axs[0].text(
    15,
    10**-19.5,
    "$l^{-2}$",
    fontdict={"color": "#a8a6a7"},
)

fig.tight_layout()
