import altair as alt
import numpy as np
import warnings

from .util import size_chart, vega_color, vega_palette

def dtype_to_vega_type(t):
    if t == np.dtype('datetime64[ns]'):
        return 'temporal'
    if t == np.float64 or t == np.int64:
        return 'quantitative'
    return 'nominal'

def hist(x, color=None, data=None, palette=None, saturation=1, size=None, aspect=1):
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
    encodings = {
        "x": alt.X(field=x, type="quantitative"),
        "y": alt.Y(field=y, type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color, type="nominal")
        else:
            encodings["color"] = alt.Color(value=vega_color(color))

    chart = alt.Chart(data).mark_circle().encode(**encodings)
    size_chart(chart, size, aspect)
    pal = vega_palette(palette, None, saturation)
    return chart.configure_range(category=pal)

def plot(x, y, s=None, color=None, data=None, palette=None, saturation=1, size=None, aspect=1):
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
