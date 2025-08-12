# -*- encoding: utf-8 -*-
"""
@File    :   fig02.py
@Time    :   2025/08/12 16:51:55
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :   This script is used to present the band structure and dipole moment distribution under open boundary conditions
"""

# %% Import Packages
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

with open(proj_root / "src/alias.yml") as f:
    alias = yaml.safe_load(f)

sns.set_theme("paper", style="ticks")

# %% Load data
datapath = proj_root / "data/fig02_band_structures_obc.h5"

dataset = {}
with h5py.File(datapath, "r") as hf:
    for key, val in hf.items():
        dataset[key] = val[()]

# %% Plot
## (a) bandstructures
xdata = np.arange(dataset["ws_z"].size)
ydata = dataset["ws_z"].real / 100
cdata = dataset["iprs_z"]
fig, ax = plt.subplots()
sc = ax.scatter(x=xdata, y=ydata, c=cdata)
cb = fig.colorbar(sc)
ax.set(title="OP Mode", xlabel=alias["sn"], ylabel=alias["eig_wn"])
cb.ax.set(title="IPR")
fig.tight_layout()

## (b-d) Eigenstates
state_nos = [6, 17, 30]
xdata, ydata, zdata = dataset["rlist"]
fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)
for idx, sn in enumerate(state_nos):
    ax: plt.Axes = axs[idx]
    vs = dataset["vs_z"][:, sn]
    ax.scatter(xdata, ydata, c=np.abs(vs))
    ax.set(
        aspect="equal",
        xticks=[],
        yticks=[],
        title=rf"{sn}th state, $\omega$ = {dataset['ws_z'].real[sn] / 100:.2f} cm$^{{-1}}$, IPR = {dataset['iprs_z'][sn]:.2f}",
    )
