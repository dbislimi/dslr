#!/usr/bin/env python3
import sys
from math import ceil

import matplotlib.pyplot as plt

from utils import (
    COURSES,
    HOUSE_COLORS,
    HOUSE_COLUMN,
    HOUSES,
    add_top_legend,
    available_courses,
    convert_to_float,
    parse_data,
    save_png,
    title_size_for_fig,
)

EXPECTED_ARGC = 2


def plot_histo(
    data: dict[str, dict[str, list[float]]],
    axes,
    courses: list[str],
    diag: bool = False,
):
    if not diag:
        axes = axes.ravel()

    for index, course in enumerate(courses):
        grades_per_houses = data[course]
        ax = axes[index] if not diag else axes[index][index]

        names = list(grades_per_houses.keys())
        grades = list(grades_per_houses.values())
        colors = [HOUSE_COLORS.get(name) for name in names]

        ax.hist(
            grades,
            bins=30,
            color=colors,
            alpha=0.55,
            histtype="stepfilled",
        )
        ax.set_title(course, fontsize=10)
        ax.set_xlabel("Grade", fontsize=8)
        ax.set_ylabel("Count", fontsize=8)
        ax.tick_params(axis="both", labelsize=7)


def histogram(data: dict[str, dict[str, list[float]]], courses: list[str]):
    nb_course = len(courses)
    cols = 4
    rows = ceil(nb_course / cols)

    fig, axes = plt.subplots(
        nrows=rows,
        ncols=cols,
        figsize=(5 * cols, 3.6 * rows),
        squeeze=False,
    )

    plot_histo(data, axes, courses)

    axes_flat = axes.ravel()
    for index in range(nb_course, rows * cols):
        axes_flat[index].axis("off")

    add_top_legend(fig)
    title_size = title_size_for_fig(fig)
    fig.suptitle(
        "Histogram by Course and House",
        fontsize=title_size,
        fontweight="bold",
        y=0.982,
    )

    plt.tight_layout(rect=(0, 0, 1, 0.89))
    save_png(fig, "histogram.png")
    plt.close(fig)


def clean_data_for_histogram(
    data: dict[str, list[float | None]],
    houses: list[str | None],
    courses: list[str],
) -> dict[str, dict[str, list[float]]]:
    grades_per_courses: dict[str, dict[str, list[float]]] = {
        course: {} for course in courses
    }
    for header in courses:
        course = data.get(header)
        if course is None:
            continue
        grades_per_houses: dict[str, list[float]] = {house: [] for house in HOUSES}
        for house, grade in zip(houses, course):
            if isinstance(house, str) and isinstance(grade, float):
                grades_per_houses.setdefault(house, []).append(grade)
        grades_per_courses[header] = grades_per_houses
    return grades_per_courses


def main(filepath: str):
    targets: set[str] = COURSES | {HOUSE_COLUMN}
    try:
        raw = parse_data(filepath, targets)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    if (houses := raw.get(HOUSE_COLUMN)) is None:
        print(f"Error: missing '{HOUSE_COLUMN}' column in dataset.")
        sys.exit(1)

    courses = available_courses(raw, COURSES)
    if not courses:
        print("Error: no known numeric course columns found in dataset.")
        sys.exit(1)
    clean = convert_to_float(raw, courses, delete_none=False)
    data = clean_data_for_histogram(clean, houses, courses)
    histogram(data, courses)


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGC:
        print("Error: program needs an argument PATH.")
        sys.exit(1)
    main(sys.argv[1])
