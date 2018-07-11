import altair as alt
import seaborn as sns
from .util import size_chart, vega_palette
from .pyplot import fill_between, plot, scatter as pscatter

__all__ = ["regplot", "lmplot"]

def regplot(x, y, data=None, x_range=None, y_range=None,
            scatter=True, fit_reg=True, ci=95, n_boot=1000, units=None,
            order=1, logistic=False, lowess=False, robust=False, logx=False,
            color=None, scatter_kws={}, line_kws={}, ax=None,
            palette=None, size=None, aspect=1, color_scale=None):

    if x_range is None:
        x_raw_range = (data[x].min(), data[x].max())
        x_pad = 0.05*(x_raw_range[1] - x_raw_range[0])
        x_range = (x_raw_range[0] - x_pad, x_raw_range[1] + x_pad)

    def plot_regression(data, color):
        layers = []
        p = sns.regression._RegressionPlotter(data[x], data[y], n_boot=n_boot, units=units, ci=ci, order=order, logistic=logistic, lowess=lowess, robust=robust, logx=logx)
        grid, yhat, err_bands = p.fit_regression(x_range=x_range)
        layers.append(plot(grid, yhat, color=color, **line_kws))
        if err_bands is not None:
            area = fill_between(grid, *err_bands, color=color)
            area.encoding.opacity = alt.value(0.15)
            layers.append(area)
        return layers

    if color:
        if color_scale is None:
            val = data[color].unique()
            pal = sns.color_palette(palette)
            color_scale = alt.Scale(domain=list(val), range=vega_palette(pal))
        else:
            val = color_scale.domain

        color_map = {}
        for i in range(len(color_scale.domain)):
            color_map[color_scale.domain[i]] = color_scale.range[i % len(color_scale.range)]

        layers = []
        if scatter:
            layers.append(pscatter(x, y, data=data, color=alt.Color(color, scale=color_scale, **scatter_kws)))

        if fit_reg:
            for v in data[color].unique():
                part = data.loc[data[color] == v]
                layers += plot_regression(part, color_map[v])
    else:
        pal = sns.color_palette(palette)

        layers = []
        if scatter:
            layers.append(pscatter(x, y, data=data, color=pal[0], **scatter_kws))

        if fit_reg:
            layers += plot_regression(data, pal[0])

    for layer in layers:
        layer.mark = dict(type=layer.mark, clip=True)
        layer.encoding.x.scale=alt.Scale(domain=x_range, nice=False)
        if y_range is not None:
            layer.encoding.y.scale=alt.Scale(domain=y_range, nice=False)
        layer.config = alt.Undefined

    chart = alt.LayerChart(layer=layers)
    return chart


def lmplot(x, y, data, hue=None, col=None, row=None, palette=None,
           col_wrap=None, size=5, aspect=1,
           hue_order=None, col_order=None, row_order=None,
           scatter=True, fit_reg=True, ci=95, n_boot=1000,
           units=None, order=1, logistic=False, lowess=False, robust=False,
           logx=False, scatter_kws={}, line_kws={}):

    x_raw_range = (data[x].min(), data[x].max())
    x_pad = 0.05*(x_raw_range[1] - x_raw_range[0])
    x_range = (x_raw_range[0] - x_pad, x_raw_range[1] + x_pad)

    y_raw_range = (data[y].min(), data[y].max())
    y_pad = 0.05*(y_raw_range[1] - y_raw_range[0])
    y_range = (y_raw_range[0] - y_pad, y_raw_range[1] + y_pad)

    def unique_with_order(a, order):
        b = list(order) if order else []
        for i in a.unique():
            if i not in b:
                b.append(i)
        return b

    cols = unique_with_order(data[col], col_order) if col else [1]
    rows = unique_with_order(data[row], row_order) if row else [1]
    hues = unique_with_order(data[hue], hue_order) if hue else [1]

    pal = sns.color_palette(palette)
    color_scale = alt.Scale(domain=list(hues), range=vega_palette(pal))

    charts = []
    for r in rows:
        row_part = data.loc[data[row] == r] if row else data
        chart_row = []
        for c in cols:
            part = row_part.loc[row_part[col] == c] if col else row_part
            chart = regplot(
                data=part, x=x, y=y, color=hue, palette=palette, x_range=x_range, y_range=y_range,
                scatter=scatter, fit_reg=fit_reg, ci=ci, n_boot=n_boot, units=units,
                order=order, logistic=logistic, lowess=lowess, robust=robust, logx=logx,
                scatter_kws=scatter_kws, line_kws=line_kws, color_scale=color_scale,
            )
            size_chart(chart, size, aspect)
            chart.title = ("%s = %s" % (row, r) if row else "") + (" | " if row and col else "") + ("%s = %s" % (col, c) if col else "")
            chart_row.append(chart)
            if col_wrap is not None and len(chart_row) >= col_wrap:
                charts.append(chart_row)
                chart_row = []

        if len(chart_row) > 0:
            charts.append(chart_row)

    if len(charts) > 1 or len(charts[0]) > 1:
        chart_rows = []
        for chart_row in charts:
            chart_rows.append(alt.hconcat(*chart_row))
        facets = alt.vconcat(*chart_rows)
    else:
        facets = charts[0][0]

    return facets
