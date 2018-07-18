import altair as alt
from matplotlib.colors import to_rgba
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import six

def build_dataframe(fields):
    field_names = {}
    data = pd.DataFrame()
    for name, field in six.iteritems(fields):
        if isinstance(field, pd.Series):
            fname = field.name
        else:
            fname = name
        data[fname] = field
        field_names[name] = fname
    return data, field_names

def dtype_to_vega_type(t):
    if t == np.dtype('datetime64[ns]'):
        return 'temporal'
    if t == np.float64 or t == np.int64:
        return 'quantitative'
    return 'nominal'

def size_chart(chart, size, aspect):
    dpi = mpl.rcParams['figure.dpi']
    if size:
        if isinstance(chart, alt.FacetChart):
            chart = chart.spec
        chart.height = size*dpi
        chart.width = aspect*size*dpi

def vega_color(color):
    if isinstance(color, six.string_types) and (color.startswith('rgb(') or color.startswith('rgba(')):
        return color
    c = to_rgba(color)
    return "rgba(%s,%s,%s,%s)" % (c[0]*255, c[1]*255, c[2]*255, c[3])

def vega_palette(palette, color=None, saturation=1):
    if palette:
        pal = sns.color_palette(palette)
    elif color:
        pal = [color]
    else:
        pal = sns.color_palette()

    if saturation < 1:
        pal = sns.color_palette(pal, desat=saturation)

    pal = sns.color_palette(pal)
    return [vega_color(c) for c in pal]

# From seaborn.categorical
def infer_orient(x, y, orient=None):
    """Determine how the plot should be oriented based on the data."""
    orient = str(orient)

    def is_categorical(s):
        try:
            # Correct way, but does not exist in older Pandas
            try:
                return pd.api.types.is_categorical_dtype(s)
            except AttributeError:
                return pd.core.common.is_categorical_dtype(s) # pylint: disable=E1101
        except AttributeError:
            # Also works, but feels hackier
            return str(s.dtype) == "categorical"

    def is_not_numeric(s):
        try:
            np.asarray(s, dtype=np.float)
        except ValueError:
            return True
        return False

    no_numeric = "Neither the `x` nor `y` variable appears to be numeric."

    if orient.startswith("v"):
        return "v"
    elif orient.startswith("h"):
        return "h"
    elif x is None:
        return "v"
    elif y is None:
        return "h"
    elif is_categorical(y):
        if is_categorical(x):
            raise ValueError(no_numeric)
        else:
            return "h"
    elif is_not_numeric(y):
        if is_not_numeric(x):
            raise ValueError(no_numeric)
        else:
            return "h"
    else:
        return "v"
