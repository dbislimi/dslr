#!/usr/bin/env python3
import sys
from typing import Callable

from utils import COURSES, EXPECTED_ARGC, parse_data

BASE_METRIC_WIDTH = 12
MIN_COLUMN_WIDTH = 14


def _count(values: list[float]) -> int:
    return len(values)


def _mean(values: list[float]) -> float:
    n = len(values)
    if n == 0:
        return float("nan")
    total = 0.0
    for x in values:
        total += x
    return total / n


def _std(values: list[float]) -> float:
    n = len(values)
    if n <= 1:
        return float("nan")
    mean = _mean(values)
    sum_sqd = 0.0
    for x in values:
        sum_sqd += (x - mean) ** 2
    return (sum_sqd / (n - 1)) ** 0.5


def _min(values: list[float]) -> float:
    min_value = float("inf")
    for x in values:
        min_value = min(min_value, x)
    if min_value == float("inf"):
        return float("nan")
    return min_value


def _percent(values: list[float], percent: int) -> float:
    n = len(values)
    if n == 0:
        return float("nan")
    if n == 1:
        return values[0]

    sorted_values = sorted(values)
    k = (percent / 100) * (n - 1)
    i_low = int(k)
    i_upp = i_low + 1
    if i_upp >= n:
        return sorted_values[i_low]
    val_low = sorted_values[i_low]
    val_upp = sorted_values[i_upp]
    fraction = k - i_low
    return val_low + (val_upp - val_low) * fraction


def _max(values: list[float]) -> float:
    max_value = float("-inf")
    for x in values:
        max_value = max(max_value, x)
    if max_value == float("-inf"):
        return float("nan")
    return max_value


def _describe(data: dict[str, list[float]]) -> None:
    metrics: dict[str, Callable[[list[float]], int | float]] = {
        "Count": _count,
        "Mean": _mean,
        "Std": _std,
        "Min": _min,
        "25%": lambda x: _percent(x, 25),
        "50%": lambda x: _percent(x, 50),
        "75%": lambda x: _percent(x, 75),
        "Max": _max,
    }
    stats: dict[str, list[float]] = {m: [] for m in metrics}
    for values in data.values():
        for m, func in metrics.items():
            stats[m].append(func(values))

    headers = list(data.keys())
    col_widths = {}
    for h in headers:
        header_width = len(h)
        if header_width > BASE_METRIC_WIDTH:
            col_widths[h] = header_width + 2
        else:
            col_widths[h] = MIN_COLUMN_WIDTH

    print(" " * BASE_METRIC_WIDTH, end="")
    for h in headers:
        print(f"{h:>{col_widths[h]}}", end="")
    print()

    for m in metrics:
        print(f"{m:<{BASE_METRIC_WIDTH}}", end="")
        for h in headers:
            val = stats[m][headers.index(h)]
            print(f"{val:>{col_widths[h]}.6f}", end="")
        print()


def _clean_data(data: dict[str, list[float | None | str]]) -> dict[str, list[float]]:
    clean: dict[str, list[float]] = {}
    for key, values in data.items():
        clean[key] = [x for x in values if isinstance(x, float)]
    return clean


def main(filepath: str):
    try:
        raw = parse_data(filepath, targets=COURSES)
    except Exception as e:
        print(e)
        sys.exit(1)
    data = _clean_data(raw)
    _describe(data)


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGC:
        print("Error: program needs an argument: dataset path.")
        sys.exit(1)
    main(sys.argv[1])
