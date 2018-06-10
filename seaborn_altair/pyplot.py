import altair as alt
import numpy as np
import warnings
from matplotlib.colors import to_rgba

def mpl_color(color):
    c = to_rgba(color)
    return "rgba(%s,%s,%s,%s)" % (c[0]*255, c[1]*255, c[2]*255, c[3])

def dtype_to_vega_type(t):
    if t == np.dtype('datetime64[ns]'):
        return 'temporal'
    if t == np.float64 or t == np.int64:
        return 'quantitative'
    return 'nominal'

def hist(data, x, color=None, **kwargs):
    for key in kwargs:
        warnings.warn('hist argument "%s" is not supported' % key)
    encodings = {
        "x": alt.X(bin=True, field=x, type="quantitative"),
        "y": alt.Y(aggregate="count", type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color)
        else:
            encodings["color"] = alt.Color(value=mpl_color(color))

    return alt.Chart(data).mark_bar().encode(**encodings)

def scatter(data, x, y, s=None, color=None, **kwargs):
    for key in kwargs:
        warnings.warn('scatter argument "%s" is not supported' % key)
    encodings = {
        "x": alt.X(field=x, type="quantitative"),
        "y": alt.Y(field=y, type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color, type="nominal")
        else:
            encodings["color"] = alt.Color(value=mpl_color(color))

    return alt.Chart(data).mark_circle().encode(**encodings)

def plot(data, x, y, s=None, color=None, **kwargs):
    for key in kwargs:
        warnings.warn('plot argument "%s" is not supported' % key)
    encodings = {
        "x": alt.X(field=x, type=dtype_to_vega_type(data[x].dtype)),
        "y": alt.Y(field=y, type="quantitative"),
    }
    if color:
        if color in list(data.columns):
            encodings["color"] = alt.Color(field=color, type="nominal")
        else:
            encodings["color"] = alt.Color(value=mpl_color(color))

    return alt.Chart(data).mark_line().encode(**encodings)
