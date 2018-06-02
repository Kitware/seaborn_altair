# seaborn_altair

Seaborn-compatible API for interactive Vega-Lite plots via Altair.

## Installation

```
pip install seaborn_altair
```

## Usage

```python
import seaborn_altair as salt
import seaborn as sns

tips = sns.load_dataset("tips")

# Use salt as you would sns
salt.barplot(x="day", y="total_bill", data=tips)
```

## Limitations

This is a proof of concept at this time.
Only `barplot`, `countplot`, `pointplot`, `stripplot` are currently supported with limited support.

Contributions and suggestions welcome!

