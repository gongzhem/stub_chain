# -*- encoding: utf-8 -*-
"""
@File    :   fig04.py
@Time    :   2025/08/12 19:51:24
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :   This script is used to plot the spectral RHT between the right and left-end NPs of both A and B-type stub chains
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
datapath = proj_root / "data/fig04_spectral_rht_power.h5"
with h5py.File(datapath, "r") as hf:
    data1 = {}
    data5 = {}
    for key, val in hf["gamma1"].items():
        data1[key] = val[()]
    for key, val in hf["gamma5"].items():
        data5[key] = val[()]

# %% Plot
cm = 1e-2

fig, axs = plt.subplots(1, 2, gridspec_kw={"bottom": 0.2})
xdata = data5["wns"] * cm
(l1,) = axs[0].plot(
    xdata,
    data5["ht_a"] / cm,
    label="A-type Stub Chain",
    c="#b1283a",
)
(l2,) = axs[0].plot(
    xdata,
    data5["ht_b"] / cm,
    label="B-type Stub Chain",
    c="#006a8e",
)
xdata = data1["wns"] * cm
axs[1].plot(
    xdata,
    data1["ht_a"] / cm,
    label="A-type Stub Chain",
    c="#b1283a",
)
axs[1].plot(
    xdata,
    data1["ht_b"] / cm,
    label="B-type Stub Chain",
    c="#006a8e",
)

for ax in axs:
    ax.set(
        xlim=xdata[[0, -1]],
        ylabel=alias["ht_wn"],
        xlabel=alias["freq"],
        ylim=[0, None],
    )
axs[1].set(title=r"$\gamma$ = 1 cm$^{-1}$")
axs[0].set(title=r"$\gamma$ = 5 cm$^{-1}$")
fig.legend(
    handles=[l1, l2],
    loc="lower center",
    bbox_to_anchor=(0.5, 0),
    ncol=2,
)
