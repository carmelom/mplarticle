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
import colorsys


def lighten_color(color, amount=0.5):
    """
    https://stackoverflow.com/a/49601444/11754331
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    try:
        c = mpc.cnames[color]
    except KeyError:
        c = color
    c = colorsys.rgb_to_hls(*mpc.to_rgb(c))
    c_light = colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
    return mpc.to_hex(c_light)


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


def label_subplots(fig=None, axes=None, xpos=-0.05, ypos=1.05, scale_text=1.15, letters=None, style='brackets', transform=None):
    if axes is None:
        fig = plt.gcf() if fig is None else fig
        axes = fig.axes
    size = plt.rcParams['font.size'] * scale_text
    letters = list(map(chr, range(97, 97 + len(axes)))
                   ) if letters is None else letters
    transform = ax.transAxes if transform is None else transform
    if style == 'brackets':
        labeltext = '({label:s})'
    else:
        labeltext = '{label:s}.'
    for ax, label in zip(axes, letters):
        ax.text(xpos, ypos, labeltext.format(label=label), ha='center', va='center',
                # family='sans-serif',
                # weight='bold',
                fontsize=size,
                transform=transform,
                )


def draw_ruler(ax, x, y, length, text='', lw=2, color='w', line_kwargs={}, text_kwargs={}):
    ax.plot([x, x + length], [y] * 2, color=color, lw=lw, **line_kwargs)
    ax.text(x, y, text, ha='left', va='bottom', color=color, **text_kwargs)


def ext_axes(ax, orig, lenx, leny, labelx='$x$', labely='$y$', scale_text=1.0):
    size = plt.rcParams['font.size'] * scale_text
    ax.annotate(labelx,
                xy=orig, xycoords='axes fraction',
                xytext=(orig[0] + lenx, orig[1]), textcoords='axes fraction',
                arrowprops=dict(arrowstyle="<-", color='k',
                                connectionstyle="arc3"),
                horizontalalignment='center',
                verticalalignment='center',
                color='k',
                fontsize=size)
    ax.annotate(labely,
                xy=orig, xycoords='axes fraction',
                xytext=(orig[0], orig[1] + leny), textcoords='axes fraction',
                arrowprops=dict(arrowstyle="<-", color='k',
                                connectionstyle="arc3"),
                horizontalalignment='center',
                verticalalignment='center',
                color='k',
                fontsize=size)


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
