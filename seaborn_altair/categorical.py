import seaborn as sns
import numpy as np
import altair as alt
import pandas as pd
import warnings
from scipy import stats

from seaborn.categorical import (
    _BarPlotter,
    _BoxPlotter,
    _PointPlotter,
    _StripPlotter,
)
from seaborn.palettes import color_palette
from seaborn.external.six import string_types

__all__ = ["boxplot", "stripplot", "pointplot", "barplot", "countplot"]

class _BarPlotterAltair(_BarPlotter):
    """Show point estimates and confidence intervals with bars."""

    def draw_bars(self, ax, kws):
        """Draw the bars onto `ax`."""

        altx, alty = alt.X, alt.Y
        xprop, yprop = "x", "y"
        x, y = self.group_label, self.value_label

        if self.plot_hues is not None:
            hue_rng = range(len(self.hue_names))
            group = [g for g in self.group_names for h in hue_rng]
            stat = [s[h] for s in self.statistic for h in hue_rng]
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in c) for g in self.group_names for c in self.colors]
            hue_name = [h for g in self.group_names for h in self.hue_names]

            cols = {
                x: group,
                y: stat,
                self.hue_title: hue_name,
                "c": rgb_colors,
            }

            if self.confint.size:
                cols["ci0"] = [d[h][0] for d in self.confint for h in hue_rng]
                cols["ci1"] = [d[h][1] for d in self.confint for h in hue_rng]

            data = pd.DataFrame(cols)
        else:
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in c) for c in self.colors]
            cols = {
                x: self.group_names,
                y: self.statistic,
                "c": rgb_colors,
            }
            if self.confint.size:
                cols["ci0"] = [d[0] for d in self.confint]
                cols["ci1"] = [d[1] for d in self.confint]

            data = pd.DataFrame(cols)

        if self.orient == "h":
            altx, alty = alty, altx
            xprop, yprop = yprop, xprop

        xtitle = x

        if self.plot_hues is not None:
            column = x
            x = self.hue_title
            xtitle = ''

        encodings = {
            xprop: altx("%s:N" % x, axis=alt.Axis(title=xtitle), sort=None),
            yprop: alty("%s:Q" % y, axis=alt.Axis(title=y)),
            "color": alt.Color("c", scale=None)
        }

        if self.confint.size:
            chart = ax.mark_bar().encode(**encodings)
            error_bars = alt.Chart().mark_rule().encode(**{
                xprop: altx("%s:N" % x, axis=None, sort=None),
                yprop: "ci0:Q",
                "%s2" % yprop: "ci1:Q",
            })

            chart = alt.layer(chart, error_bars)
        else:
            chart = alt.Chart(data).mark_bar().encode(**encodings)

        if self.plot_hues is not None:
            facet_dir = "column" if self.orient == "v" else "row"
            chart = chart.facet(**{facet_dir: "%s:N" % column})

        if self.confint.size:
            chart.data = data

        chart = chart.interactive()

        return chart

    def plot(self, ax, bar_kws):
        """Make the plot."""
        return self.draw_bars(ax, bar_kws)


def barplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
               estimator=np.mean, ci=95, n_boot=1000, units=None,
               orient=None, color=None, palette=None, saturation=.75,
               errcolor=".26", errwidth=None, capsize=None, dodge=True,
               ax=None, **kwargs):

    plotter = _BarPlotterAltair(x, y, hue, data, order, hue_order,
                                estimator, ci, n_boot, units,
                                orient, color, palette, saturation,
                                errcolor, errwidth, capsize, dodge)

    if ax is None:
        ax = alt.Chart()

    ax = plotter.plot(ax, kwargs)
    return ax


def countplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
              orient=None, color=None, palette=None, saturation=.75,
              dodge=True, ax=None, **kwargs):

    estimator = len
    ci = None
    n_boot = 0
    units = None
    errcolor = None
    errwidth = None
    capsize = None

    if x is None and y is not None:
        orient = "h"
        x = y
    elif y is None and x is not None:
        orient = "v"
        y = x
    elif x is not None and y is not None:
        raise TypeError("Cannot pass values for both `x` and `y`")
    else:
        raise TypeError("Must pass values for either `x` or `y`")

    plotter = _BarPlotterAltair(x, y, hue, data, order, hue_order,
                                estimator, ci, n_boot, units,
                                orient, color, palette, saturation,
                                errcolor, errwidth, capsize, dodge)

    plotter.value_label = "count"

    if ax is None:
        ax = alt.Chart()

    ax = plotter.plot(ax, kwargs)
    return ax


class _PointPlotterAltair(_PointPlotter):

    def draw_points(self, ax):
        """Draw the main data components of the plot."""

        altx, alty = alt.X, alt.Y
        xprop, yprop = "x", "y"
        x, y = self.group_label, self.value_label

        if self.plot_hues is not None:
            hue_rng = range(len(self.hue_names))
            group = [g for g in self.group_names for h in hue_rng]
            stat = [s[h] for s in self.statistic for h in hue_rng]
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in c) for g in self.group_names for c in self.colors]
            hue_name = [h for g in self.group_names for h in self.hue_names]

            cols = {
                x: group,
                y: stat,
                self.hue_title: hue_name,
                "c": rgb_colors,
            }

            if self.confint.size:
                cols["ci0"] = [d[h][0] for d in self.confint for h in hue_rng]
                cols["ci1"] = [d[h][1] for d in self.confint for h in hue_rng]

            data = pd.DataFrame(cols)
        else:
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in c) for c in self.colors]
            cols = {
                x: self.group_names,
                y: self.statistic,
                "c": rgb_colors,
            }
            if self.confint.size:
                cols["ci0"] = [d[0] for d in self.confint]
                cols["ci1"] = [d[1] for d in self.confint]

            data = pd.DataFrame(cols)

        if self.orient == "h":
            altx, alty = alty, altx
            xprop, yprop = yprop, xprop

        xtitle = x

        encodings = {
            xprop: altx("%s:N" % x, axis=alt.Axis(title=xtitle), sort=None),
            yprop: alty("%s:Q" % y, axis=alt.Axis(title=y), scale={"zero": False}),
            "color": alt.Color("c", scale=None),
        }

        if self.confint.size:
            line_enc = dict(encodings)
            line = ax.mark_line(point=True).encode(**line_enc)
            error_bars = alt.Chart().mark_rule().encode(**{
                xprop: altx("%s:N" % x, axis=None, sort=None),
                yprop: "ci0:Q",
                "%s2" % yprop: "ci1:Q",
                "color": alt.Color("c", scale=None),
            })

            chart = alt.layer(line, error_bars)
        else:
            line = ax.mark_line().encode(**encodings)
            dot = ax.mark_point().encode(**encodings)
            chart = alt.layer(line, dot)

        if self.confint.size:
            chart.data = data

        chart = chart.interactive()
        return chart

    def plot(self, ax):
        """Make the plot."""
        return self.draw_points(ax)


def pointplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
              estimator=np.mean, ci=95, n_boot=1000, units=None,
              markers="o", linestyles="-", dodge=False, join=True, scale=1,
              orient=None, color=None, palette=None, errwidth=None,
              capsize=None, ax=None, **kwargs):

    plotter = _PointPlotterAltair(x, y, hue, data, order, hue_order,
                                  estimator, ci, n_boot, units,
                                  markers, linestyles, dodge, join, scale,
                                  orient, color, palette, errwidth, capsize)

    if ax is None:
        ax = alt.Chart()

    ax = plotter.plot(ax)
    return ax


class _StripPlotterAltair(_StripPlotter):
    """1-d scatterplot with categorical organization."""

    def draw_stripplot(self, ax, kws):
        """Draw the points onto `ax`."""

        altx, alty = alt.X, alt.Y
        xprop, yprop = "x", "y"
        x, y = self.group_label, self.value_label
        if not x:
            x = ""

        groups = self.group_names
        if not len(self.group_names):
            groups = [""]

        if self.plot_hues is not None:
            hues = {h: i for (i, h) in enumerate(self.hue_names)}
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in self.colors[hues[d]]) for g in self.plot_hues for d in g]
            hue_name = [d for g in self.plot_hues for d in g]
            cols = {
                x: [groups[i] for i in range(len(self.plot_data)) for d in self.plot_data[i]],
                y: [d for g in self.plot_data for d in g],
                self.hue_title: hue_name,
                "c": rgb_colors,
            }
            data = pd.DataFrame(cols)
        else:
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in self.colors[i]) for i in range(len(self.plot_data)) for d in self.plot_data[i]]
            cols = {
                x: [groups[i] for i in range(len(self.plot_data)) for d in self.plot_data[i]],
                y: [d for g in self.plot_data for d in g],
                "c": rgb_colors,
            }
            data = pd.DataFrame(cols)

        if self.orient == "h":
            altx, alty = alty, altx
            xprop, yprop = yprop, xprop

        xtitle = x

        encodings = {
            xprop: altx("%s:N" % x, axis=alt.Axis(title=xtitle), sort=None),
            yprop: alty("%s:Q" % y, axis=alt.Axis(title=y), scale={"zero": False}),
            "color": alt.Color("c:N", scale=None),
        }

        chart = ax.mark_circle().encode(**encodings)
        chart.data = data

        chart = chart.interactive()

        return chart

    def plot(self, ax, kws):
        """Make the plot."""
        return self.draw_stripplot(ax, kws)


def stripplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
              jitter=False, dodge=False, orient=None, color=None, palette=None,
              size=5, edgecolor="gray", linewidth=0, ax=None, **kwargs):

    if "split" in kwargs:
        dodge = kwargs.pop("split")
        msg = "The `split` parameter has been renamed to `dodge`."
        warnings.warn(msg, UserWarning)

    plotter = _StripPlotterAltair(x, y, hue, data, order, hue_order,
                                  jitter, dodge, orient, color, palette)
    if ax is None:
        ax = alt.Chart()

    kwargs.setdefault("zorder", 3)
    size = kwargs.get("s", size)
    if linewidth is None:
        linewidth = size / 10
    if edgecolor == "gray":
        edgecolor = plotter.gray
    kwargs.update(dict(s=size ** 2,
                       edgecolor=edgecolor,
                       linewidth=linewidth))

    ax = plotter.plot(ax, kwargs)
    return ax


class _BoxPlotterAltair(_BoxPlotter):

    def draw_boxplot(self, ax, kws):
        """Use Altair to draw a boxplot on an Axes."""

        altx, alty = alt.X, alt.Y
        xprop, yprop = "x", "y"
        x, y = self.group_label, self.value_label
        xtitle = x
        if not x:
            x = "group"
            xtitle = ""

        if self.plot_hues is not None:
            column = x
            x = self.hue_title
            xtitle = ""

        groups = self.group_names
        if not len(self.group_names):
            groups = [""]

        if self.plot_hues is not None:
            hues = {h: i for (i, h) in enumerate(self.hue_names)}
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in self.colors[hues[d]]) for g in self.plot_hues for d in g]
            hue_name = [d for g in self.plot_hues for d in g]
            cols = {
                column: [groups[i] for i in range(len(self.plot_data)) for d in self.plot_data[i]],
                y: [d for g in self.plot_data for d in g],
                x: hue_name,
                "c": rgb_colors,
            }
            data = pd.DataFrame(cols)
        else:
            rgb_colors = ["rgb(%s, %s, %s)" % tuple(comp*255 for comp in self.colors[i]) for i in range(len(self.plot_data)) for d in self.plot_data[i]]
            cols = {
                x: [groups[i] for i in range(len(self.plot_data)) for d in self.plot_data[i]],
                y: [d for g in self.plot_data for d in g],
                "c": rgb_colors,
            }
            data = pd.DataFrame(cols)

        if self.orient == "h":
            altx, alty = alty, altx
            xprop, yprop = yprop, xprop

        # Define aggregate fields
        lower_box = 'q1(%s):Q' % y
        lower_whisker = 'min(%s):Q' % y
        upper_box = 'q3(%s):Q' % y
        upper_whisker = 'max(%s):Q' % y

        xval = altx(x, axis=alt.Axis(title=xtitle), sort=None)

        # Compose each layer individually
        lower_plot = alt.Chart().mark_rule().encode(**{
            yprop: alty(lower_whisker, axis=alt.Axis(title=y)),
            "%s2" % yprop: lower_box,
            xprop: xval,
        })

        middle_plot = alt.Chart().mark_bar().encode(**{
            yprop: lower_box,
            "%s2" % yprop: upper_box,
            "color": alt.Color("c", scale=None),
            xprop: xval,
        })

        upper_plot = alt.Chart().mark_rule().encode(**{
            yprop: upper_whisker,
            "%s2" % yprop: upper_box,
            xprop: xval,
        })

        middle_tick = alt.Chart().mark_tick(
            size=18,
            color='black',
        ).encode(**{
            yprop: 'median(%s):Q' % y,
            xprop: xval,
        })

        chart = lower_plot + middle_plot + upper_plot + middle_tick

        if self.plot_hues is not None:
            facet_dir = "column" if self.orient == "v" else "row"
            chart = chart.facet(**{facet_dir: "%s:N" % column})
        chart.data = data
        chart = chart.interactive()

        return chart

    def plot(self, ax, boxplot_kws):
        """Make the plot."""
        return self.draw_boxplot(ax, boxplot_kws)


def boxplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
            orient=None, color=None, palette=None, saturation=.75,
            width=.8, dodge=True, fliersize=5, linewidth=None,
            whis=1.5, notch=False, ax=None, **kwargs):

    plotter = _BoxPlotterAltair(x, y, hue, data, order, hue_order,
                                orient, color, palette, saturation,
                                width, dodge, fliersize, linewidth)

    kwargs.update(dict(whis=whis, notch=notch))

    ax = plotter.plot(ax, kwargs)
    return ax
