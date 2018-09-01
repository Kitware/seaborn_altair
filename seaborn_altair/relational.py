import numpy as np
import pandas as pd
from .pyplot import scatter
from .util import build_dataframe, dtype_to_vega_type

__all__ = ["scatterplot"]

def scatterplot(
    x=None, y=None, hue=None, style=None, size=None, data=None,
    palette=None, sizes=[10, 80]
):
    if data is None:
        data, names = build_dataframe({"x": x, "y": y, "hue": hue, "style": style, "size": size})
        x, y, hue, style, size = names["x"], names["y"], names["hue"], names["style"], names["size"]

    if x is None and y is None:
        plot_data = data.copy()
        x = getattr(data.index, "name", "x")
        plot_data.loc[:, x] = data.index
        plot_data = pd.melt(plot_data, x, var_name="series", value_name="y")
        y = "y"
        hue = "series"
        style = "series"
        data = plot_data

    x_type = dtype_to_vega_type(data[x].dtype)
    params = dict(x=x, x_type=x_type, y=y, color=hue, style=style, size_by=size, sizes=sizes, palette=palette, data=data)
    if hue is not None:
        params['color_type'] = dtype_to_vega_type(data[hue].dtype)
    if size is not None:
        params['size_type'] = dtype_to_vega_type(data[size].dtype)
    return scatter(**params)
