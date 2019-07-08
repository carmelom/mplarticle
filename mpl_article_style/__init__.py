#!/usr/bin/env python

from pathlib import Path
import matplotlib.pyplot as plt

from .variables import *
from .plot_utils import *

wdir = Path(__file__).parent
style_path = str(wdir / 'aps_article.mplstyle')
print(f"Apply style {style_path}")
plt.style.use(style_path)


