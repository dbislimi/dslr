#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from utils import (
    CHOSEN_COURSES,
    HOUSES,
    OUTPUT_DIR,
    available_courses,
    convert_to_float,
    parse_data,
)

EXPECTED_ARGC = 3


def dict_to_matrix(data_dict: dict[str, list[float]], headers: list[str]) -> NDArray:
    cols = [np.asarray(data_dict[header], dtype=float) for header in headers]
    m = len(cols[0])
    if any(len(c) != m for c in cols):
        raise ValueError("dict_to_matrix: All columns must be the same length.")
    x = np.column_stack(cols)
    return x


def _clean_data(
    data: dict[str, list[float | None]],
    means: dict[str, float],
    stds: dict[str, float],
) -> dict[str, list[float]]:
    clean_dict: dict[str, list[float]] = {}
    for key, values in data.items():
        mean = means[key]
        std = stds[key]
        if std == 0:
            std = 1.0
        clean_list = []
        for value in values:
            if isinstance(value, float):
                clean_list.append((value - mean) / std)
            else:
                clean_list.append(0.0)
        clean_dict[key] = clean_list
    return clean_dict


def _get_weights(path: str) -> dict:
    p = Path(path)
    if not p.is_file():
        p = OUTPUT_DIR / path
    if not p.is_file():
        raise FileNotFoundError(f"Weights file not found: {path}")
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except OSError as e:
        raise FileNotFoundError(f"Cannot read weights file {p}: {e}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {p}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("Invalid json: expected an object at top level.")
    required_keys = {"means", "stds", "weights"}
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"Missing keys in json: {', '.join(sorted(missing))}")
    if not isinstance(data["means"], dict) or not isinstance(data["stds"], dict):
        raise ValueError("Invalid 'means'/'stds': expected objects.")
    missing_courses = CHOSEN_COURSES - data["means"].keys()
    if missing_courses:
        raise ValueError(
            f"Missing course(s) in weights: {', '.join(sorted(missing_courses))}"
        )
    return data


def _predict(data: NDArray, weights: NDArray):
    result = np.dot(data, weights)  # (x, n) . (n, 4) = (x, 4)
    preds = np.argmax(result, axis=1)
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with (OUTPUT_DIR / "houses.csv").open(mode="w", encoding="utf-8") as f:
            f.write("Index,Hogwarts House\n")
            for i, p in enumerate(preds):
                f.write(f"{i},{HOUSES[p]}\n")
    except OSError as e:
        print(f"Error: cannot write predictions: {e}")
        sys.exit(1)


def main(dataset_path: str, weights_path: str) -> None:
    try:
        weights = _get_weights(weights_path)
        raw = parse_data(dataset_path, targets=CHOSEN_COURSES)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    courses = available_courses(raw, CHOSEN_COURSES)
    missing = CHOSEN_COURSES - set(courses)
    if missing:
        print(f"Missing courses in dataset: {', '.join(sorted(missing))}")
        sys.exit(1)
    to_float = convert_to_float(raw, courses, delete_none=False)
    data = _clean_data(to_float, weights["means"], weights["stds"])
    try:
        x = dict_to_matrix(data, courses)
        x = np.c_[np.ones(x.shape[0]), x]
        w = dict_to_matrix(weights["weights"], HOUSES)
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    _predict(x, w)


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGC:
        print("Error: program needs two arguments: dataset path, weights path.")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
