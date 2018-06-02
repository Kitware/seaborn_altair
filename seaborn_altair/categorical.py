import seaborn as sns
import numpy as np
import altair as alt
import pandas as pd
from scipy import stats

from seaborn.categorical import _CategoricalStatPlotter
from seaborn.categorical import _CategoricalScatterPlotter
from seaborn.palettes import color_palette
from seaborn.external.six import string_types

__all__ = ["stripplot", "pointplot", "barplot", "countplot"]

class _BarPlotterAltair(_CategoricalStatPlotter):
    """Show point estimates and confidence intervals with bars."""

    import altair as alt

    def __init__(self, x, y, hue, data, order, hue_order,
                 estimator, ci, n_boot, units,
                 orient, color, palette, saturation, errcolor,
                 errwidth, capsize, dodge):
        """Initialize the plotter."""
        self.establish_variables(x, y, hue, data, orient,
                                 order, hue_order, units)
        self.establish_colors(color, palette, saturation)
        self.estimate_statistic(estimator, ci, n_boot)

        self.dodge = dodge

        self.errcolor = errcolor
        self.errwidth = errwidth
        self.capsize = capsize

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
            import json

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


class _PointPlotter(_CategoricalStatPlotter):

    default_palette = "dark"

    """Show point estimates and confidence intervals with (joined) points."""
    def __init__(self, x, y, hue, data, order, hue_order,
                 estimator, ci, n_boot, units,
                 markers, linestyles, dodge, join, scale,
                 orient, color, palette, errwidth=None, capsize=None):
        """Initialize the plotter."""
        self.establish_variables(x, y, hue, data, orient,
                                 order, hue_order, units)
        self.establish_colors(color, palette, 1)
        self.estimate_statistic(estimator, ci, n_boot)

        # Override the default palette for single-color plots
        if hue is None and color is None and palette is None:
            self.colors = [color_palette()[0]] * len(self.colors)

        # Don't join single-layer plots with different colors
        if hue is None and palette is not None:
            join = False

        # Use a good default for `dodge=True`
        if dodge is True and self.hue_names is not None:
            dodge = .025 * len(self.hue_names)

        # Make sure we have a marker for each hue level
        if isinstance(markers, string_types):
            markers = [markers] * len(self.colors)
        self.markers = markers

        # Make sure we have a line style for each hue level
        if isinstance(linestyles, string_types):
            linestyles = [linestyles] * len(self.colors)
        self.linestyles = linestyles

        # Set the other plot components
        self.dodge = dodge
        self.join = join
        self.scale = scale
        self.errwidth = errwidth
        self.capsize = capsize

    @property
    def hue_offsets(self):
        """Offsets relative to the center position for each hue level."""
        if self.dodge:
            offset = np.linspace(0, self.dodge, len(self.hue_names))
            offset -= offset.mean()
        else:
            offset = np.zeros(len(self.hue_names))
        return offset

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

    plotter = _PointPlotter(x, y, hue, data, order, hue_order,
                            estimator, ci, n_boot, units,
                            markers, linestyles, dodge, join, scale,
                            orient, color, palette, errwidth, capsize)

    if ax is None:
        ax = alt.Chart()

    ax = plotter.plot(ax)
    return ax


class _StripPlotter(_CategoricalScatterPlotter):
    """1-d scatterplot with categorical organization."""
    def __init__(self, x, y, hue, data, order, hue_order,
                 jitter, dodge, orient, color, palette):
        """Initialize the plotter."""
        self.establish_variables(x, y, hue, data, orient, order, hue_order)
        self.establish_colors(color, palette, 1)

        # Set object attributes
        self.dodge = dodge
        self.width = .8

        if jitter == 1:  # Use a good default for `jitter = True`
            jlim = 0.1
        else:
            jlim = float(jitter)
        if self.hue_names is not None and dodge:
            jlim /= len(self.hue_names)
        self.jitterer = stats.uniform(-jlim, jlim * 2).rvs

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

    plotter = _StripPlotter(x, y, hue, data, order, hue_order,
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
