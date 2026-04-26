# dslr

Hogwarts house sorting via one-vs-all logistic regression trained from scratch on student course grades, with a custom dataset descriptor and three visualization tools.

## Installation

```bash
uv sync
```

## Usage

```bash
# Describe dataset statistics
uv run python src/data_analysis/describe.py datasets/dataset_train.csv

# Visualize grade distributions
uv run python src/data_analysis/histogram.py datasets/dataset_train.csv
uv run python src/data_analysis/scatter_plot.py datasets/dataset_train.csv
uv run python src/data_analysis/pairplot.py datasets/dataset_train.csv

# Train and predict
uv run python src/logistic_regression/logreg_train.py datasets/dataset_train.csv
uv run python src/logistic_regression/logreg_predict.py datasets/dataset_test.csv output/weights.json
```

## How it works

**Data description** — `describe.py` replicates pandas' `describe()` output (count, mean, std, min, 25th/50th/75th percentile, max) using only Python builtins. Percentiles are computed via linear interpolation on the sorted sample.

**Feature selection** — 10 of the 13 courses are used for training. Arithmancy, Defense Against the Dark Arts, and Care of Magical Creatures are excluded based on scatter plot analysis showing low inter-house discriminability.

**Training** — one-vs-all binary logistic regression, one classifier per house. Features are standardized (z-score) using training-set means and standard deviations before gradient descent. Missing grades are imputed as 0 post-standardization. Gradient descent runs for 1000 epochs at learning rate 0.1. Learned weights, means, and standard deviations are serialized to `output/weights.json`.

**Prediction** — the same standardization is applied at inference time using the saved training statistics. The predicted house is the argmax over the four classifier dot products.

## Files

```
src/
├── data_analysis/
│   ├── describe.py        # count, mean, std, min, percentiles, max
│   ├── histogram.py       # per-course grade distribution by house
│   ├── scatter_plot.py    # pairwise feature scatter
│   └── pairplot.py        # full pair plot matrix
├── logistic_regression/
│   ├── logreg_train.py    # gradient descent, weight serialization
│   └── logreg_predict.py  # inference, houses.csv output
└── utils/
    ├── constants.py       # course list, house colors, paths
    ├── data.py            # float conversion and course filtering
    └── csv_io.py          # CSV parsing
datasets/
├── dataset_train.csv
└── dataset_test.csv
output/
├── weights.json           # trained weights, means, stds
└── houses.csv             # predictions (Index, Hogwarts House)
plot/
├── histogram.png
├── scatter_plot.png
└── pair_plot.png
```

## Dependencies

NumPy, matplotlib. No scikit-learn or pandas.
