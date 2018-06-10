import altair as alt
from IPython.display import display
import pandas as pd
import warnings

from .pyplot import mpl_color

__all__ = ["FacetGrid"]

class FacetGrid():
    """Subplot grid for plotting conditional relationships."""

    def __init__(self, data, row=None, col=None, hue=None, **kwargs):
        for key in kwargs:
            warnings.warn('FacetGrid.__init__ argument "%s" is not supported' % key)

        facets = {}
        if col is not None:
            facets['column'] = col
        if row is not None:
            facets['row'] = row
        self.hue = hue

        self.chart = alt.Chart(data).mark_point().properties(
            width=180,
            height=180
        ).facet(**facets)

    def _ipython_display_(self):
        display(self.chart)

    def map(self, func, *args, **kwargs):
        warnings.warn('FacetGrid.map is not implemented. Use map_dataframe instead.')
        return self

    def map_dataframe(self, func, *args, **kwargs):
        plot_kwargs = dict(kwargs)
        if self.hue:
            plot_kwargs["color"] = self.hue

        plot_args = [self.chart.data] + list(args)

        single = func(*plot_args, **plot_kwargs)

        self.chart.spec.mark = single.mark
        self.chart.spec.encoding = single.encoding
        self.chart = self.chart.interactive()
        return self

    def add_legend(self):
        warnings.warn('FacetGrid.add_legend is not implemented.')
        return self

    def set_axis_labels(self, *args, **kwargs):
        warnings.warn('FacetGrid.set_axis_labels is not implemented.')
        return self

    def set_titles(self, *args, **kwargs):
        warnings.warn('FacetGrid.set_titles is not implemented.')
        return self

    def set(self, *args, **kwargs):
        warnings.warn('FacetGrid.set is not implemented.')
        return self
