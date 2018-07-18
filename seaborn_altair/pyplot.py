import altair as alt
import numpy as np
import pandas as pd
import warnings

from .util import build_dataframe, dtype_to_vega_type, size_chart, vega_color, vega_palette


def fill_between(x, y1, y2, color=None, data=None, palette=None, saturation=1, size=None, aspect=1):
    if data is None:
        xname = x.name if isinstance(x, pd.Series) else "x"
        data = pd.DataFrame({xname: x})
        x = xname
        if y1 is not None:
            y1name = y1.name if isinstance(y1, pd.Series) else "y1"
            data[y1name] = y1
            y1 = y1name
        if y2 is not None:
            y2name = y2.name if isinstance(y2, pd.Series) else "y2"
            data[y2name] = y2
            y2 = y2name

    encodings = {
        "x": alt.X(field=x, type=dtype_to_vega_type(data[x].dtype)),
        "y": alt.Y(field=y1, type="quantitative"),
        "y2": alt.Y(field=y2, type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color, type="nominal")
        else:
            encodings["color"] = alt.Color(value=vega_color(color))

    chart = alt.Chart(data).mark_area().encode(**encodings)
    size_chart(chart, size, aspect)
    pal = vega_palette(palette, None, saturation)
    return chart.configure_range(category=pal)

def hist(x, color=None, data=None, palette=None, saturation=1, size=None, aspect=1):
    if data is None:
        data = pd.DataFrame({"x": x})
        x = "x"

    encodings = {
        "x": alt.X(bin=True, field=x, type="quantitative"),
        "y": alt.Y(aggregate="count", type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color)
        else:
            encodings["color"] = alt.Color(value=vega_color(color))

    chart = alt.Chart(data).mark_bar().encode(**encodings)
    size_chart(chart, size, aspect)
    pal = vega_palette(palette, None, saturation)
    return chart.configure_range(category=pal)

def scatter(x, y, s=None, color=None, data=None, palette=None, saturation=1, size=None, aspect=1):
    if data is None:
        data, fields = build_dataframe({"x": x, "y": y})
        x, y = fields["x"], fields["y"]

    encodings = {
        "x": alt.X(field=x, type="quantitative", axis={"title": x}),
        "y": alt.Y(field=y, type="quantitative", axis={"title": y}),
    }
    if color:
        if isinstance(color, alt.Color):
            encodings["color"] = color
        elif color in list(data.columns):
            encodings["color"] = alt.Color(field=color, type="nominal")
        else:
            encodings["color"] = alt.Color(value=vega_color(color))

    chart = alt.Chart(data).mark_circle().encode(**encodings)
    size_chart(chart, size, aspect)
    pal = vega_palette(palette, None, saturation)
    return chart.configure_range(category=pal)

def plot(x, y, s=None, color=None, data=None, palette=None, saturation=1, size=None, aspect=1):
    if data is None:
        data, fields = build_dataframe({"x": x, "y": y})
        x, y = fields["x"], fields["y"]

    encodings = {
        "x": alt.X(field=x, type=dtype_to_vega_type(data[x].dtype)),
        "y": alt.Y(field=y, type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color, type="nominal")
        else:
            encodings["color"] = alt.Color(value=vega_color(color))

    chart = alt.Chart(data).mark_line().encode(**encodings)
    size_chart(chart, size, aspect)
    pal = vega_palette(palette, None, saturation)
    return chart.configure_range(category=pal)
