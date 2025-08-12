# -*- encoding: utf-8 -*-
"""
@File    :   fig03.py
@Time    :   2025/08/12 18:44:58
@Author  :   Zhen Gong
@Version :   0.1
@Contact :   zhengong@sjtu.edu.cn
@Desc    :   This script is used for plot the eigenfrequency spectrum for A/B-type stub chain, and the dipole moment distribution of CLS
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

# %% (b)


# %% (e)


# %% (c)


# %% (f)
