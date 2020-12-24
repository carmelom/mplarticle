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


# def subplots_figsize(nrows, ncols):
#     w, h = plt.rcParams['figure.figsize']
#     return (w*ncols, h*nrows)


def subplots(nrows=1, ncols=1, *args, **kwargs):
    spp = {}
    gs_kw = kwargs.get('gridspec_kw', {})
    l, b, t, r, hs, ws = [gs_kw.get(name, plt.rcParams[f"figure.subplot.{name}"])
                          for name in ['left', 'bottom', 'top', 'right',
                                       'hspace', 'wspace']]
    spp['left'] = l / ncols
    spp['right'] = 1 - (1 - r) / ncols
    spp['bottom'] = b / nrows
    spp['top'] = 1 - (1 - t) / nrows
    spp.update(gs_kw)
    w, h = kwargs.get('figsize', plt.rcParams['figure.figsize'])
    nw = ncols * (r - l) / (ncols + r - l - 1) * (ncols + ws * (ncols - 1))
    nh = nrows * (t - b) / (nrows + t - b - 1) * (nrows + hs * (nrows - 1))
    fs = (w * nw, h * nh)
    kwargs.update({'figsize': fs, 'gridspec_kw': spp})
    return plt.subplots(nrows, ncols, *args, **kwargs)


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


def lighten_line2d(line, lighten=0.4):
    c = line.get_color()
    c_light = lighten_color(c, amount=lighten)
    line.set_markerfacecolor(c_light)
    # line.set_color(c)
    # line.set_markeredgecolor(c)
    return line


def lighten_plots(ax, lighten=0.4):
    for l in ax.get_lines():
        lighten_line2d(l, lighten=lighten)
    return ax


def get_linecolors(line):
    return {
        'color': line.get_color(),
        'markerfacecolor': line.get_markerfacecolor(),
        'markeredgecolor': line.get_markeredgecolor()
    }


def get_CN(n):
    cycle = plt.rcParams['axes.prop_cycle']
    cycle = cycle.simplify().by_key()
    return {k: cycle[k][n] for k in ['color', 'markerfacecolor', 'markeredgecolor']}


def label_subplots(fig=None, axes=None, xpos=-0.05, ypos=0.05, scale_text=1.15, letters=None, style='brackets', weight='normal'):
    """
    weight: [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight' ]
    style:  ['brackets' : '({x:s})',
             'dotted': '{x:s}.',
             or a custom string with the same format]
    """
    if axes is None:
        fig = plt.gcf() if fig is None else fig
        axes = fig.axes
    else:
        fig = axes[0].figure
    size = plt.rcParams['font.size'] * scale_text
    letters = list(map(chr, range(97, 97 + len(axes)))
                   ) if letters is None else letters
    if style == 'brackets':
        labeltext = '({x:s})'
    elif style == 'dotted':
        labeltext = '{x:s}.'
    else:
        labeltext = style
    for ax, label in zip(axes, letters):
        # place text wrt to upper left corner of the selected axis
        axis_to_figure = ax.transAxes + fig.transFigure.inverted()
        x, y = axis_to_figure.transform([0, 1])
        ax.text(x + xpos, y + ypos, labeltext.format(x=label), ha='center', va='center',
                # family='sans-serif',
                weight=weight,
                fontsize=size,
                transform=fig.transFigure,
                )


def draw_ruler(ax, x, y, length, text='', lw=2, color='w', line_kwargs={}, text_kwargs={}):
    ax.plot([x, x + length], [y] * 2, color=color, lw=lw, **line_kwargs)
    txt = dict(ha='center', va='bottom', color=color)
    txt.update(text_kwargs)
    xoffs = {'left': 0, 'center': length/2, 'right': length}
    ax.text(x + xoffs[txt['ha']], y, text, **txt)


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
    if not name.startswith('plot_'):
        raise ValueError(
            f"Check you script name! {name}\nIt must be named 'plot_<figure filename>.py'")
    else:
        return name


def savefig(fig=None, tag='', format='pdf', name=None):
    assert format in ['pdf', 'png', 'svg']
    fig = plt.gcf() if fig is None else fig
    name = check_scriptname() if name is None else name
    name = Path(name)
    # replace file extension and remove 'plot-' (5 chars)
    if tag:  # non-empty string
        tag = '-' + tag
    figurename = f"{name.stem[5:]}{tag}.{format}"
    figurepath = Path('..') / 'figures' / figurename
    fig.savefig(figurepath)  # ) bbox_inches=bbox_inches)
    print(f"Saved {figurepath}")
