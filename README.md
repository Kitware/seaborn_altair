# seaborn_altair

Seaborn-compatible API for interactive Vega-Lite plots via Altair.

## Installation

    pip install seaborn_altair

Works in Jupyter lab or Jupyter notebooks.

## Usage

    import seaborn_altair as salt
    import seaborn as sns
    tips = sns.load_dataset("tips")

    # Use salt as you would sns
    salt.barplot(x="day", y="total_bill", data=tips)

![barplot](https://github.com/kitware/seaborn_altair/raw/master/img/visualization.png)

## API

This is only a proof of concept at this time. Only a subset of Seaborn plots (the ones with example links) are currently available with limited support.

### Axis grids
* [FacetGrid](http://kitware.github.io/seaborn_altair/facetgrid.html) Subplot grid for plotting conditional relationships.
* factorplot Draw a categorical plot onto a FacetGrid.
* lmplot Plot data and regression model fits across a FacetGrid.
* PairGrid Subplot grid for plotting pairwise relationships in a dataset.
* pairplot Plot pairwise relationships in a dataset.
* JointGrid Grid for drawing a bivariate plot with marginal univariate plots.
* jointplot Draw a plot of two variables with bivariate and univariate graphs.

### Categorical plots
* [stripplot](http://kitware.github.io/seaborn_altair/stripplot.html) Draw a scatterplot where one variable is categorical.
* swarmplot Draw a categorical scatterplot with non-overlapping points.
* [boxplot](http://kitware.github.io/seaborn_altair/boxplot.html) Draw a box plot to show distributions with respect to categories.
* violinplot Draw a combination of boxplot and kernel density estimate.
* lvplot Draw a letter value plot to show distributions of large datasets.
* [pointplot](http://kitware.github.io/seaborn_altair/pointplot.html) Show point estimates and confidence intervals using scatter plot glyphs.
* [barplot](http://kitware.github.io/seaborn_altair/barplot.html) Show point estimates and confidence intervals as rectangular bars.
* [countplot](http://kitware.github.io/seaborn_altair/countplot.html) Show the counts of observations in each categorical bin using bars.

### Distribution plots
* distplot Flexibly plot a univariate distribution of observations.
* kdeplot Fit and plot a univariate or bivariate kernel density estimate.
* rugplot Plot datapoints in an array as sticks on an axis.

### Regression plots
* regplot Plot data and a linear regression model fit.
* residplot Plot the residuals of a linear regression.

### Matrix plots
* heatmap Plot rectangular data as a color-encoded matrix.
* clustermap Plot a matrix dataset as a hierarchically-clustered heatmap.

### Timeseries plots
* tsplot Plot one or more timeseries with flexible representation of uncertainty.

### Miscellaneous plots
* palplot Plot the values in a color palette as a horizontal array.

### matplotlib.pyplot utilities
* [pyplot.hist](http://kitware.github.io/seaborn_altair/pyplot-hist.html)
* [pyplot.plot](http://kitware.github.io/seaborn_altair/pyplot-plot.html)
* [pyplot.scatter](http://kitware.github.io/seaborn_altair/pyplot-scatter.html)

## Credit

Idea from [Jake VanderPlas](https://twitter.com/jakevdp/status/996041414596214784). [I](https://twitter.com/jeffbaumes) know Python and Vega-Lite reasonably well, so decided to give it a shot.

Contributions and suggestions welcome!
