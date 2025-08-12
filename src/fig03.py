# -*- encoding: utf-8 -*-
"""
@File    :   fig03.py
@Time    :   2025/08/12 18:44:58
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :   This script is used for plot the eigenfrequency spectrum for A/B-type stub chain, and the dipole moment distribution of CLS
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

sns.set_theme("paper", style="ticks")
with open(proj_root / "src/alias.yml") as f:
    alias = yaml.safe_load(f)


# %% Load data
datapath = proj_root / "data/fig03_abtype_obc.h5"
dataset = {}
with h5py.File(datapath, "r") as hf:
    for key, gp in hf.items():
        dataset[key] = {}
        for key_sub, val in gp.items():
            dataset[key][key_sub] = val[()]

# %% Plot (b-f)
um = 1e-6
fig, axs = plt.subplots(2, 2, sharey="row")
chain_types = ["SA", "SB"]
stub_a = dataset["SA"]
stub_b = dataset["SB"]
# 1. Band structures
clim = [
    np.min(np.concat((stub_a["ipr_z"], stub_b["ipr_z"]))),
    np.max(np.concat((stub_a["ipr_z"], stub_b["ipr_z"]))),
]
for ax, key in zip(axs[0], chain_types):
    xdata = np.arange(dataset[key]["ipr_z"].size) + 1
    ydata = dataset[key]["w_z[cm^-1]"]
    cdata = dataset[key]["ipr_z"]
    sc = ax.scatter(
        xdata,
        ydata.real,
        c=cdata,
    )
    ax.set(
        title=f"Spectrum ({key[-1]}-type)",
        xlabel=alias["sn"],
        xlim=[0, xdata.size],
    )
    cb = fig.colorbar(sc)
    cb.ax.set(title="IPR")
axs[0, 0].set(ylabel=alias["eig_wn"])

# The dipole moment distribution
for ax, key in zip(axs[1], chain_types):
    rlist = dataset[key]["rlist"]
    xdata = rlist[0]
    Ntot = rlist.shape[1]
    Ncell = Ntot // 3 + 1
    sn = 70
    ydata = np.abs(dataset[key]["v_z"][:, sn])
    if key == "SA":
        idx_A = list(np.arange(Ncell) * 3)
        idx_B = list(np.arange(Ncell - 1) * 3 + 1)
        idx_C = list(np.arange(Ncell - 1) * 3 + 2) + [-1]
    elif key == "SB":
        idx_A = list(np.arange(Ncell - 1) * 3 + 1)
        idx_B = [0] + list(np.arange(Ncell - 1) * 3 + 2)
        idx_C = list(np.arange(Ncell - 1) * 3 + 3)
    markevery = 2
    ax.plot(
        xdata[idx_A] / um,
        ydata[idx_A],
        label="NP $A$",
        c="#a8a6a7",
        ls="--",
        marker="^",
        markevery=markevery,
    )
    ax.plot(
        xdata[idx_B] / um,
        ydata[idx_B],
        label="NP $B$",
        c="#b1283a",
        ls="--",
        marker="s",
        markevery=markevery,
    )
    ax.plot(
        xdata[idx_C] / um,
        ydata[idx_C],
        label="NP $C$",
        c="#006a8e",
        ls="--",
        marker="x",
        markevery=markevery,
    )
    ax.legend(
        ncol=3,
        fontsize="small",
        loc=9,
    )
    ax.set(
        xlim=[np.min(xdata) / um, np.max(xdata) / um],
        ylim=[0, 0.25],
        yticks=0.05 * np.arange(6),
        xlabel=r"x (um)",
        title=f"Dipole Moment Distribution ({key[-1]}-type)",
    )
axs[1, 0].set(ylabel="Nomalized Dipole Moment")
fig.tight_layout()
