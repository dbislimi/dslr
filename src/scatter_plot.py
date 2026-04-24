#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt

from utils import (
    COURSES,
    EXPECTED_ARGC,
    HOUSE_COLORS,
    HOUSE_COLUMN,
    PLOT_PATH,
    PlotMargins,
    add_top_legend,
    apply_plot_margins,
    available_courses,
    hide_axis_ticks,
    parse_data,
    title_size_for_fig,
)


def _diagonal_label(course: str) -> str:
    words = course.split()
    if len(words) <= 1:
        return course
    split_index = len(words) // 2
    return f"{' '.join(words[:split_index])}\n{' '.join(words[split_index:])}"


def _group_points_by_house(
    grades_x: list[str | float | None],
    grades_y: list[str | float | None],
    houses: list[str | float | None],
) -> dict[str, tuple[list[float], list[float]]]:
    grouped: dict[str, tuple[list[float], list[float]]] = {
        house: ([], []) for house in HOUSE_COLORS
    }
    for grade_x, grade_y, house in zip(grades_x, grades_y, houses):
        if (
            not isinstance(grade_x, float)
            or not isinstance(grade_y, float)
            or not isinstance(house, str)
            or house not in grouped
        ):
            continue
        x_vals, y_vals = grouped[house]
        x_vals.append(grade_x)
        y_vals.append(grade_y)
    return grouped


def plot_scatter(
    data: dict[str, list[str | float | None]],
    houses: list[str | float | None],
    axes,
    courses: list[str],
    draw_diagonal_labels: bool = True,
):
    for row, courses_y in enumerate(courses):
        grades_y = data[courses_y]
        for col, courses_x in enumerate(courses):
            grades_x = data[courses_x]
            ax = axes[row][col]

            if row == col:
                if draw_diagonal_labels:
                    ax.text(
                        0.5,
                        0.5,
                        _diagonal_label(courses_x),
                        transform=ax.transAxes,
                        ha="center",
                        va="center",
                        fontsize=14,
                        fontweight="black",
                        linespacing=1.2,
                        clip_on=True,
                    )
                    hide_axis_ticks(ax)
                continue

            grouped = _group_points_by_house(grades_x, grades_y, houses)

            for house, color in HOUSE_COLORS.items():
                x_vals, y_vals = grouped[house]
                ax.scatter(
                    x_vals,
                    y_vals,
                    s=14,
                    alpha=0.65,
                    c=color,
                    edgecolors="none",
                )

            hide_axis_ticks(ax)


def scatter(
    data: dict[str, list[str | float | None]], houses: list[str | float | None]
):
    courses = available_courses(data, COURSES)
    nb_course = len(courses)

    if nb_course == 0:
        raise ValueError("No known course columns were found for scatter plot.")

    fig, axes = plt.subplots(
        nrows=nb_course,
        ncols=nb_course,
        figsize=(5.4 * nb_course, 5.4 * nb_course),
        squeeze=False,
    )

    plot_scatter(data, houses, axes, courses, draw_diagonal_labels=True)

    add_top_legend(fig, anchor_y=0.972)

    title_size = title_size_for_fig(fig)
    fig.suptitle(
        "Scatter Matrix by House",
        fontsize=title_size,
        fontweight="bold",
        y=0.993,
    )
    apply_plot_margins(
        fig,
        PlotMargins(left=0.003, right=0.999, bottom=0.003, top=0.9),
    )

    PLOT_PATH.mkdir(parents=True, exist_ok=True)
    plt.savefig(PLOT_PATH / "scatter_plot.png", dpi=200)
    plt.close(fig)


def main(filepath: str):
    try:
        raw = parse_data(filepath)
    except Exception as e:
        print(e)
        sys.exit(1)

    if (houses := raw.get(HOUSE_COLUMN)) is None:
        print(f"Error: missing '{HOUSE_COLUMN}' column in dataset.")
        sys.exit(1)

    try:
        scatter(raw, houses)
    except ValueError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != EXPECTED_ARGC:
        print("Error: program needs an argument PATH.")
        sys.exit(1)
    main(sys.argv[1])
