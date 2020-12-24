#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 07-2019 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.rcsetup import cycler
from .plot_utils import lighten_color


def use(style_path, lighten_markers=None, scale=None):
    if style_path not in plt.style.available:
        wdir = Path(__file__).parent / 'stylesheets'
        style_path = str(wdir / f'{style_path}.mplstyle')
        print(f"Apply style {style_path}")
    plt.style.use(style_path)

    if lighten_markers is not None:
        set_color_cycle(colors=None, lighten=lighten_markers)

    if scale is not None and scale != 1:
        scale_style(scale)
    return style_path


def scale_style(scale):
    # scale numerical values
    print(f"Scaling numerical values by a factor {scale}")
    D = plt.rcParams.copy()
    figsize = plt.rcParams['figure.figsize']
    figsize = figsize[0] * scale, figsize[1] * scale
    nums = {k: v * scale for k, v in D.items() if not k.startswith('figure')
            and not isinstance(v, bool) and isinstance(v, (int, float))}
    nums['figure.figsize'] = figsize
    # print(nums)
    plt.rcParams.update(nums)


def set_palette(palette, lighten=0.4):
    cmap = palette.mpl_colormap
    set_colormap(cmap)
    colors = palette.mpl_colors
    set_color_cycle(colors, lighten=lighten)


def set_colormap(cmap):
    plt.register_cmap(cmap.name, cmap)
    plt.rcParams['image.cmap'] = cmap.name


def set_color_cycle(colors=None, lighten=0.4):
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    light_colors = [lighten_color(c, lighten) for c in colors]
    cc = cycler(color=colors, markerfacecolor=light_colors,
                markeredgecolor=colors)
    plt.rcParams['axes.prop_cycle'] = cc
