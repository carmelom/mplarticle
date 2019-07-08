#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 03-2019 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
import __main__ as main
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import colors as mpc


def set_mfalpha(line, alpha=0.4):
    # I like hollow data points
    c = line.get_color()
    line.set_markerfacecolor(mpc.to_rgba(c, alpha=alpha))
    line.set_markeredgecolor(c)
    return line


def ax_mfalpha(ax, alpha=0.4):
    for l in ax.get_lines():
        set_mfalpha(l, alpha)
    return ax


def label_subplots(fig=None, axes=None, xpos=-0.05, ypos=1.05, scale_text=1.15, letters=None):
    if axes is None:
        fig = plt.gcf() if fig is None else fig
        axes = fig.axes
    size = plt.rcParams['font.size'] * scale_text
    letters = list(map(chr, range(97, 97 + len(axes)))
                   ) if letters is None else letters
    for ax, label in zip(axes, letters):
        ax.text(xpos, ypos, f'{label}.', ha='center', va='center',
                # family='sans-serif',
                weight='bold', fontsize=size,
                transform=ax.transAxes,)


def check_scriptname():
    name = main.__file__
    if not name.startswith('plot-'):
        raise ValueError(
            f"Check you script name! {name}\nIt must be named 'plot-<figure filename>.py'")
    else:
        return name


def savefig(fig=None, tag='', format='pdf'):
    assert format in ['pdf', 'png', 'svg']
    fig = plt.gcf() if fig is None else fig
    name = Path(check_scriptname())
    # replace file extension and remove 'plot-' (5 chars)
    if tag:  # non-empty string
        tag = '-' + tag
    figurename = f"{name.stem[5:]}{tag}.{format}"
    figurepath = Path('..') / 'figures' / figurename
    fig.savefig(figurepath)  # ) bbox_inches=bbox_inches)
    print(f"Saved {figurepath}")
