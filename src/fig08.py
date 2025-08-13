# -*- encoding: utf-8 -*-
"""
@File    :   fig08.py
@Time    :   2025/08/13 11:25:47
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
from matplotlib import lines
from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import annotate, yticks
from numpy import spacing
from scipy.constants import pi

proj_root = Path(__file__).parents[1]

sns.set_theme("paper", style="ticks")
with open(proj_root / "src/alias.yml") as f:
    alias = yaml.safe_load(f)

# %% Load data
datapath = proj_root / "data/fig08_T_map.h5"
dset = {}
with h5py.File(datapath, "r") as hf:
    for key, gp in hf.items():
        dset[key] = gp[()]
data = dset


# 把两种情况绘制在一起组成一个 2*3 的组图
fig = plt.figure(figsize=(7, 4))
gs = GridSpec(1, 2, figure=fig, width_ratios=[20, 1], wspace=0.5)
subfig = fig.add_subfigure(gs[0])
cb_fig = fig.add_subfigure(gs[1])
axs = subfig.subplots(
    2,
    3,
    sharex="col",
    sharey="row",
    gridspec_kw={"hspace": 0, "wspace": 0},
)
ltypes = ["SA", "SB", "PA"]
labels = ["A-type stub chain", "B-type stub chain", "Periodic chain"]
# generate data
Tfield_set = data["Tfield_set"]
xlim = data["xlim"]
ylim = data["ylim"]
# 第一行, 初始温度场在 0 号位置
for i, ax in enumerate(axs.T.flat):
    ax: plt.Axes
    im = ax.imshow(
        Tfield_set[i] - 300,
        origin="lower",
        aspect="auto",
        extent=[*xlim, *ylim],
        clim=[0, 10],
        cmap="hot_r",
    )
    cs = ax.contour(
        np.linspace(xlim[0], xlim[1], Tfield_set[i].shape[1]),  # x坐标
        np.linspace(ylim[0], ylim[1], Tfield_set[i].shape[0]),
        Tfield_set[i] - 300,
        levels=[0.1],
        colors="#117733",
        linewidths=1,
        linestyles="dashed",
    )
cb = cb_fig.colorbar(im, cax=fig.add_subplot(gs[1]))
cb.ax.set_title(r"$\Delta T$ (K)")
axs[1, 1].set(xlabel="$x$ (um)")
for i in range(3):
    axs[0, i].set(title=labels[i])
for i in range(2):
    axs[i, 0].set(
        ylabel=r"$\tau$ - $\tau_0$ (s)",
    )
fig.subplots_adjust(
    top=0.925, bottom=0.11, left=0.09, right=0.955, hspace=0.2, wspace=0.2
)
