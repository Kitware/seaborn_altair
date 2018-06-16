import numpy as np
import altair as alt
import pandas as pd
from .util import infer_orient, size_chart, vega_color, vega_palette
from .axisgrid import FacetGrid

__all__ = ["boxplot", "factorplot", "stripplot", "pointplot", "barplot", "countplot"]

def _bar_encodings(x, y, xs, ys, hue, dodge, estimator):
    encodings = {
        ys: alt.Y(field=y, aggregate=estimator, type="quantitative", axis={"title": y}),
        "color": alt.Color(field=x ,type="nominal", legend=None)
    }

    if hue:
        legend = None if dodge else alt.Undefined
        encodings["color"] = alt.Color(field=hue ,type="nominal", legend=legend)

    xf = hue if hue and dodge else x
    encodings[xs] = alt.X(field=xf, type="nominal")
    return encodings

def _bar_ci_encodings(x, y, xs, ys, hue, dodge, estimator):
    encodings = {
        ys: alt.Y(field=y, aggregate="ci0", type="quantitative"),
        "%s2" % ys: alt.Y(field=y, aggregate="ci1", type="quantitative")
    }

    xf = hue if hue and dodge else x
    encodings[xs] = alt.X(field=xf, type="nominal")
    return encodings

def _point_encodings(x, y, xs, ys, hue, estimator):
    encodings = {
        ys: alt.Y(field=y, aggregate=estimator, type="quantitative"),
        "color": alt.Color(field="___" ,type="nominal", legend=None)
    }

    if hue:
        encodings["color"] = alt.Color(field=hue ,type="nominal")

    encodings[xs] = alt.X(field=x, type="nominal")
    return encodings

def _point_ci_encodings(x, y, xs, ys, hue, estimator):
    encodings = {
        ys: alt.Y(field=y, aggregate="ci0", type="quantitative"),
        "%s2" % ys: alt.Y(field=y, aggregate="ci1", type="quantitative")
    }

    encodings[xs] = alt.X(field=x, type="nominal")
    return encodings

def _validate_estimator(estimator, ci):
    if estimator in ["mean", np.mean]:
        estimator = "mean"
        if ci != 95 and ci is not None:
            raise ValueError("ci must be 95 for mean")
    elif estimator in ["median", np.median]:
        estimator = "median"
        if ci is not None:
            raise ValueError("ci not available for median")
    elif estimator in ["count", len]:
        estimator = "count"
        if ci is not None:
            raise ValueError("ci not available for median")
    else:
        raise ValueError("estimator must be mean or median")
    return estimator

def barplot(
    x=None, y=None, hue=None, data=None,
    estimator=np.mean, ci=95, size=None, aspect=1,
    orient=None, color=None, palette=None, saturation=.75, dodge=True
):
    xs, ys = "x", "y"
    orient = infer_orient(data[x], data[y], orient)
    if orient == "h":
        x, y = y, x
        xs, ys = ys, xs

    estimator = _validate_estimator(estimator, ci)

    encodings = _bar_encodings(x, y, xs, ys, hue, dodge, estimator)
    chart = alt.Chart(data).mark_bar().encode(**encodings)

    if ci:
        ci_encodings = _bar_ci_encodings(x, y, xs, ys, hue, dodge, estimator)
        ci_layer = alt.Chart().mark_rule().encode(**ci_encodings)
        chart.data = alt.Undefined
        chart = alt.LayerChart(data=data, layer=[chart, ci_layer])

    if hue and dodge:
        facet_dir = "column" if orient == "v" else "row"
        chart = chart.facet(**{facet_dir: "%s:N" % x})

    size_chart(chart, size, aspect)

    pal = vega_palette(palette, color, saturation)
    return chart.configure_range(category=pal)

def countplot(
    x=None, y=None, hue=None, data=None, size=None, aspect=1,
    orient=None, color=None, palette=None, saturation=.75, dodge=True
):
    estimator = len
    ci = None

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

    return barplot(
        x, y, hue, data,
        estimator=estimator, ci=ci, size=size, aspect=aspect,
        orient=orient, color=color, palette=palette, saturation=saturation,
        dodge=dodge,
    )

def pointplot(
    x=None, y=None, hue=None, data=None,
    estimator=np.mean, ci=95, join=True, size=None, aspect=1,
    orient=None, color=None, palette=None, saturation=.75
):
    xs, ys = "x", "y"
    orient = infer_orient(data[x], data[y], orient)
    if orient == "h":
        x, y = y, x
        xs, ys = ys, xs

    estimator = _validate_estimator(estimator, ci)

    encodings = _point_encodings(x, y, xs, ys, hue, estimator)
    chart = alt.Chart(data).mark_circle().encode(**encodings)
    layers = [chart]

    if join:
        layers.append(alt.Chart().mark_line().encode(**encodings))

    if ci:
        ci_encodings = _point_ci_encodings(x, y, xs, ys, hue, estimator)
        cfield = hue if hue else "___"
        ci_encodings["color"] = alt.Color(field=cfield, type="nominal", legend=None)
        layers.append(alt.Chart().mark_rule().encode(**ci_encodings))

    if len(layers) > 1:
        chart.data = alt.Undefined
        chart = alt.LayerChart(data=data, layer=layers)

    size_chart(chart, size, aspect)

    pal = vega_palette(palette, color, saturation)
    return chart.configure_range(category=pal)


def stripplot(
    x=None, y=None, hue=None, data=None, size=None, aspect=1,
    dodge=False, orient=None, color=None, palette=None, saturation=.75
):
    xs, ys = "x", "y"
    if data is None:
        data = pd.DataFrame({"x": x})
        x = "x"
        if y:
            data["y"] = y
            y = "y"

    if y:
        orient = infer_orient(data[x], data[y], orient)
    else:
        orient = "v"

    if orient == "h":
        x, y = y, x
        xs, ys = ys, xs

    encodings = {}

    if y:
        encodings[ys] = alt.Y(field=y, type="quantitative")
        xf = hue if hue and dodge else x
        encodings[xs] = alt.X(field=xf, type="nominal")
        encodings["color"] = alt.Color(field=x ,type="nominal", legend=None)
    else:
        encodings[xs] = alt.X(field=x, type="quantitative")

    if hue:
        legend = None if dodge else alt.Undefined
        encodings["color"] = alt.Color(field=hue ,type="nominal", legend=legend)

    chart = alt.Chart(data).mark_tick().encode(**encodings)

    if hue and dodge:
        facet_dir = "column" if orient == "v" else "row"
        chart = chart.facet(**{facet_dir: "%s:N" % x})

    size_chart(chart, size, aspect)

    pal = vega_palette(palette, color, saturation)
    return chart.configure_range(category=pal)

def boxplot(
    x=None, y=None, hue=None, data=None, size=None, aspect=1,
    orient=None, color=None, palette=None, saturation=.75, dodge=True
):
    xs, ys = "x", "y"
    if data is None:
        data = pd.DataFrame({"x": x})
        x = "x"
        if y:
            data["y"] = y
            y = "y"

    if x is None and y is None:
        # Make a box plot for each numeric column
        numeric_cols = [c for c in data if data[c].dtype in [np.float32, np.float64]]
        col = []
        val = []
        for c in numeric_cols:
            for v in data[c]:
                col.append(c)
                val.append(v)

        data = pd.DataFrame({"column": col, "value": val})
        x = "column"
        y = "value"
        if orient == "h":
            x, y = y, x

    if y:
        orient = infer_orient(data[x], data[y], orient)
    elif orient is None:
        orient = "h"

    if orient == "h":
        x, y = y, x
        xs, ys = ys, xs

    xf = hue if hue and dodge else x

    # Main bar
    encodings = {
        ys: alt.Y(field=y, aggregate="q1", type="quantitative", axis={"title": y}),
        "%s2" % ys: alt.Y(field=y, aggregate="q3", type="quantitative"),
        "color": alt.Color(field=x ,type="nominal", legend=None),
        xs: alt.X(field=xf, type="nominal")
    }
    if x is None:
        del encodings["color"]
        del encodings[xs]
    if hue:
        legend = None if dodge else alt.Undefined
        encodings["color"] = alt.Color(field=hue ,type="nominal", legend=legend)
    bar_layer = alt.Chart().mark_bar().encode(**encodings)

    # Min/max range line
    range_encodings = {
        ys: alt.Y(field=y, aggregate="min", type="quantitative"),
        "%s2" % ys: alt.Y(field=y, aggregate="max", type="quantitative"),
        xs: alt.X(field=xf, type="nominal")
    }
    if x is None:
        del range_encodings[xs]
    range_layer = alt.Chart().mark_rule().encode(**range_encodings)

    # Median line
    median_encodings = {
        ys: alt.Y(field=y, aggregate="median", type="quantitative"),
        xs: alt.X(field=xf, type="nominal")
    }
    if x is None:
        del median_encodings[xs]
    median_layer = alt.Chart().mark_tick(size=18, color="black").encode(**median_encodings)

    chart = alt.LayerChart(data=data, layer=[range_layer, bar_layer, median_layer])

    if hue and dodge:
        facet_dir = "column" if orient == "v" else "row"
        chart = chart.facet(**{facet_dir: "%s:N" % x})

    size_chart(chart, size, aspect)

    pal = vega_palette(palette, color, saturation)
    return chart.configure_range(category=pal)

def factorplot(
    x=None, y=None, hue=None, data=None, row=None, col=None,
    estimator=np.mean, ci=95, kind="point", size=None, aspect=1,
    orient=None, color=None, palette=None, facet_kws=None, **kwargs
):

    # Determine the plotting function
    try:
        plot_func = globals()[kind + "plot"]
    except KeyError:
        err = "Plot kind '{}' is not recognized".format(kind)
        raise ValueError(err)

    # Determine keyword arguments for the facets
    facet_kws = {} if facet_kws is None else facet_kws
    facet_kws.update(data=data, row=row, col=col, size=size, aspect=aspect)

    # Determine keyword arguments for the plotting function
    plot_kws = kwargs
    plot_kws.update(orient=orient, color=color, palette=palette)

    if kind in ["bar", "point"]:
        plot_kws.update(estimator=estimator, ci=ci)

    # Initialize the facets
    g = FacetGrid(**facet_kws)

    # Draw the plot onto the facets
    g.map_dataframe(plot_func, x, y, hue, **plot_kws)

    return g
