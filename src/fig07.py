# -*- encoding: utf-8 -*-
"""
@File    :   fig07.py
@Time    :   2025/08/13 10:40:47
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
datapath = proj_root / "data/fig07_temperoal_dynamics.h5"
dset = {}
with h5py.File(datapath, "r") as hf:
    for key, gp in hf.items():
        dset[key] = {}
        for sub_key, val in gp.items():
            dset[key][sub_key] = val[()]

# %% Plot
fig = plt.figure()
gs = fig.add_gridspec(2, 3)
axs = np.empty((2, 3), dtype="O")
labels = {
    "SA": "A-type stub chain",
    "SB": "B-type stub chain",
    "PA": "Periodic  chain",
}
# (a-c)
for idx, key in enumerate(["SA", "SB", "PA"]):
    if idx == 0:
        axs[0, idx] = fig.add_subplot(gs[0, idx])
    else:
        axs[0, idx] = fig.add_subplot(gs[0, idx], sharey=axs[0, 0])
    ax = axs[0, idx]
    ws = dset[key]["ws"]

    sc = ax.scatter(
        np.arange(ws.size),
        1 / ws,
        c=dset[key]["v_dest"],
    )
    ax.set(yscale="log", xlim=np.arange(ws.size)[[0, -1]], xlabel="State No.")
    fig.colorbar(sc)
axs[0, 0].set_ylabel(r"$\lambda^{-1}$ (s)")

# (d)
axs[1, 0] = fig.add_subplot(gs[1, 0])
ax_T_souce = axs[1, 0]
for key in ["SA", "SB", "PA"]:
    taus = dset[key]["taus"]
    ax_T_souce.plot(
        taus,
        (dset[key]["T_source"] - dset[key]["Tb"]),
        label=labels[key],
        ls="-" if "S" in key else "--",
    )
ax_T_souce.set(
    xscale="log",
    xlim=taus[[0, -1]],
    xlabel=r"$\tau-\tau_0$ (s)",
    ylabel=r"$\Delta T$ (K)",
)

# (e)
axs[1, 1] = fig.add_subplot(gs[1, 1])
ax = axs[1, 1]
for key in ["SA", "SB", "PA"]:
    ax.plot(
        taus,
        (dset[key]["T_dest"] - dset[key]["Tb"]),
        label=labels[key],
        ls="-" if "S" in key else "--",
    )
ax.set(
    xscale="log",
    xlabel=r"$\tau-\tau_0$ (s)",
    ylabel=r"$\Delta T$ (K)",
    xlim=[1e-7, 10],
    ylim=[-0.025, None],
)
ax: plt.Axes
ax_inset = ax.inset_axes([0.075, 0.475, 0.4, 0.4], transform=ax.transAxes)
for key in ["SA", "SB"]:
    ax_inset.plot(
        taus,
        (dset[key]["T_dest"] - dset[key]["Tb"]),
        label=labels[key],
        ls="-" if "S" in key else "--",
    )
ax_inset.set(xscale="log", xlim=[2e-4, 1e-2], ylim=[0, None])

# (f)
axs[1, 2] = fig.add_subplot(gs[1, 2])
ax = axs[1, 2]
ls = []
for key in ["SA", "SB", "PA"]:
    (l,) = ax.plot(
        taus,
        (dset[key]["T_dest"] - dset[key]["Tb"]),
        label=labels[key],
        ls="-" if "S" in key else "--",
    )
    ls.append(l)
ax.set(
    xscale="log",
    yscale="log",
    xlabel=r"$\tau-\tau_0$ (s)",
    ylabel=r"$\Delta T$ (K)",
    xlim=taus[[0, -1]],
)
fig.legend(handles=ls, ncols=3, loc="lower center")
fig.tight_layout()
