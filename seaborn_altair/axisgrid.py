import altair as alt
from IPython.display import display
import pandas as pd

from .util import size_chart

__all__ = ["FacetGrid"]

class FacetGrid():
    """Subplot grid for plotting conditional relationships."""

    def __init__(self, data, row=None, col=None, hue=None, palette=None, size=3, aspect=1):
        self.hue = hue
        self.palette = palette
        self.size = size
        self.aspect = aspect

        self.chart = alt.Chart(data).mark_point()

        facets = {}
        if col is not None:
            facets['column'] = col
        if row is not None:
            facets['row'] = row
        if len(facets):
            self.chart = self.chart.facet(**facets)

    def _ipython_display_(self):
        display(self.chart)

    def map(self, func, *args, **kwargs):
        raise ValueError('FacetGrid.map is not implemented. Use map_dataframe instead.')

    def map_dataframe(self, func, *args, **kwargs):
        plot_kwargs = dict(
            color=self.hue,
            palette=self.palette, size=self.size,
            aspect=self.aspect, data=self.chart.data
        )
        plot_kwargs.update(kwargs)

        single = func(*args, **plot_kwargs)

        if isinstance(self.chart, alt.FacetChart):
            if isinstance(single, alt.FacetChart):
                raise ValueError("Cannot facet a FacetChart")
            self.chart.config = single.config
            single.config = alt.Undefined
            single.data = alt.Undefined
            self.chart.spec = single
        else:
            self.chart = single

        return self
