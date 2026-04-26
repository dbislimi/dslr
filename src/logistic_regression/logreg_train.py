#!/usr/bin/env python3
import json
import sys

import numpy as np
from numpy.typing import NDArray

from utils import (
    CHOSEN_COURSES,
    HOUSE_COLUMN,
    HOUSES,
    OUTPUT_DIR,
    available_courses,
    convert_to_float,
    parse_data,
)

EXPECTED_ARGC = 2
FloatArray = NDArray[np.float64]
StrArray = NDArray[np.str_]
Thetas = dict[str, FloatArray]


def _get_means(data: dict[str, list[float | None]]) -> dict[str, float]:
    means = {}
    for key, values in data.items():
        i = 0
        s = 0
        for value in values:
            if isinstance(value, float):
                s += value
                i += 1
        means[key] = s / i
    return means


def _get_stds(data: dict[str, list[float | None]]) -> dict[str, float]:
    stds = {}
    for key, values in data.items():
        valid_values = [value for value in values if isinstance(value, float)]
        n = len(valid_values)
        if n <= 1:
            std = 1.0
        else:
            mean = sum(valid_values) / n
            variance = sum((value - mean) ** 2 for value in valid_values) / (n - 1)
            std = variance**0.5
        if np.isnan(std) or std == 0:
            std = 1.0
        stds[key] = std
    return stds


def _save_weights(
    thetas: Thetas,
    means: dict[str, float],
    stds: dict[str, float],
) -> None:
    data = {
        "means": means,
        "stds": stds,
        "weights": {house: thetas[house].tolist() for house in HOUSES},
    }
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with (OUTPUT_DIR / "weights.json").open(mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        print(f"Error: cannot write weights: {e}")


def _clean_data(
    data: dict[str, list[float | None]],
    houses: list[str | None],
    courses: list[str],
    means: dict[str, float],
    stds: dict[str, float],
) -> tuple[FloatArray, StrArray]:
    clean_dict: dict[str, list[float]] = {}

    for course in courses:
        grades = data[course]
        mean = means[course]
        std = stds[course]
        clean = [((x - mean) / std) if isinstance(x, float) else 0.0 for x in grades]
        clean_dict[course] = clean

    house_labels = np.array(
        [h.strip() if isinstance(h, str) else "" for h in houses], dtype=str
    )
    valid_rows = np.isin(house_labels, HOUSES)
    y_labels = house_labels[valid_rows]

    for course in courses:
        clean_dict[course] = np.array(clean_dict[course])[valid_rows].tolist()
    x_train = np.column_stack([clean_dict[course] for course in courses])
    return x_train, y_labels


def sigmoid(z: FloatArray) -> FloatArray:
    z = np.clip(z, -250, 250)
    return 1 / (1 + np.exp(-z))


def gradient_descent(
    x: FloatArray, y: FloatArray, alpha: float = 0.1, epochs: int = 1000
) -> FloatArray:
    m = x.shape[0]  # nb of students
    n = x.shape[1]  # nb of courses
    theta = np.zeros(n)  # (n, 1)

    for _ in range(epochs):
        z = np.dot(x, theta)  # (m, n) . (n, 1) = (m, 1)
        h = sigmoid(z)  # (m, 1)
        error = h - y  # (m, 1) - (m, 1) = (m, 1)
        gradient = (1 / m) * np.dot(x.T, error)  # (n, m) . (m, 1) = (n, 1)
        theta = theta - (alpha * gradient)  # (n, 1) - (n, 1)
    return theta


def train(x_train: FloatArray, y_labels: StrArray) -> Thetas:
    m = x_train.shape[0]
    x_train_with_bias = np.column_stack((np.ones((m, 1)), x_train))
    thetas: Thetas = {}

    for house in HOUSES:
        print(f"(one vs all) Training for {house}..")
        y = np.where(y_labels == house, 1.0, 0.0)
        theta = gradient_descent(x_train_with_bias, y)
        thetas[house] = theta
    return thetas


def main(filepath: str) -> None:
    targets: set[str] = CHOSEN_COURSES | {HOUSE_COLUMN}

    try:
        raw = parse_data(filepath, targets)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    if (houses := raw.get(HOUSE_COLUMN)) is None:
        print(f"Error: missing '{HOUSE_COLUMN}' column in dataset.")
        sys.exit(1)
    courses = available_courses(raw, CHOSEN_COURSES)
    missing = CHOSEN_COURSES - set(courses)
    if missing:
        print(f"Error: missing course(s) in dataset: {', '.join(sorted(missing))}")
        sys.exit(1)
    to_float = convert_to_float(raw, courses, delete_none=False)
    means = _get_means(to_float)
    stds = _get_stds(to_float)
    x_train, y_labels = _clean_data(to_float, houses, courses, means, stds)
    thetas = train(x_train, y_labels)
    _save_weights(thetas, means, stds)


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGC:
        print("Error: program needs an argument PATH.")
        sys.exit(1)
    main(sys.argv[1])
