#!/usr/bin/env python3
import sys

import matplotlib.pyplot as plt

from data_analysis.histogram import clean_data_for_histogram, plot_histo
from data_analysis.scatter_plot import plot_scatter
from utils import (
    COURSES,
    HOUSE_COLUMN,
    add_top_legend,
    available_courses,
    convert_to_float,
    hide_axis_ticks,
    parse_data,
    save_png,
    title_size_for_fig,
)

EXPECTED_ARGC = 2


def pairplot(raw: dict[str, list[str | None]], houses: list[str | None]):
    courses = available_courses(raw, COURSES)
    nb_course = len(courses)

    if nb_course == 0:
        raise ValueError("No known course columns were found for pair plot.")

    fig, axes = plt.subplots(
        nrows=nb_course,
        ncols=nb_course,
        figsize=(5.4 * nb_course, 5.4 * nb_course),
        squeeze=False,
    )
    data = convert_to_float(raw, courses, delete_none=False)
    plot_scatter(data, houses, axes, courses, draw_diagonal_labels=False)
    histo_data = clean_data_for_histogram(data, houses, courses)
    plot_histo(histo_data, axes, courses, diag=True)

    add_top_legend(fig, anchor_y=0.972)
    title_size = title_size_for_fig(fig)
    fig.suptitle(
        "Pair Plot by Course and House",
        fontsize=title_size,
        fontweight="bold",
        y=0.993,
    )

    for row_axes in axes:
        for ax in row_axes:
            hide_axis_ticks(ax)

    save_png(fig, "pair_plot.png")
    plt.close(fig)


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
    try:
        pairplot(raw, houses)
    except ValueError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGC:
        print("Error: program needs an argument PATH.")
        sys.exit(1)
    main(sys.argv[1])
