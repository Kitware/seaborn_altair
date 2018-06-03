# seaborn_altair

Seaborn-compatible API for interactive Vega-Lite plots via Altair.

See the [interactive examples](https://kitware.github.io/seaborn_altair/) for current functionality and comparison to Seaborn.

## Installation

```
pip install seaborn_altair
```

Works in Jupyter lab or Jupyter notebooks.

## Usage

```python
import seaborn_altair as salt
import seaborn as sns

tips = sns.load_dataset("tips")

# Use salt as you would sns
salt.barplot(x="day", y="total_bill", data=tips)
```

## Limitations

This is only a proof of concept at this time.
Only `barplot`, `countplot`, `pointplot`, `stripplot` are currently available with limited support.

Contributions and suggestions welcome!

# Credit

Idea from [Jake VanderPlas](https://twitter.com/jakevdp/status/996041414596214784). [I](https://twitter.com/jeffbaumes) know Python and Vega-Lite reasonably well, so decided to give it a shot.
