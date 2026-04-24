import csv
from collections.abc import Mapping
from pathlib import Path
from typing import NamedTuple

from matplotlib.lines import Line2D

PLOT_PATH = Path(__file__).resolve().parent.parent / "plot"
HOUSE_COLUMN = "Hogwarts House"
HOUSE_COLORS: dict[str, str] = {
    "Gryffindor": "#c1121f",
    "Hufflepuff": "#ffb703",
    "Ravenclaw": "#1d3557",
    "Slytherin": "#2a9d8f",
}
COURSES: set[str] = {
    "Arithmancy",
    "Astronomy",
    "Herbology",
    "Defense Against the Dark Arts",
    "Divination",
    "Muggle Studies",
    "Ancient Runes",
    "History of Magic",
    "Transfiguration",
    "Potions",
    "Care of Magical Creatures",
    "Charms",
    "Flying",
}
HOUSES: set[str] = {"Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"}

EXPECTED_ARGC = 2


class PlotMargins(NamedTuple):
    left: float = 0.01
    right: float = 0.995
    bottom: float = 0.01
    top: float = 0.9
    wspace: float = 0.08
    hspace: float = 0.08


def available_courses(data: Mapping[str, object], courses: set[str]) -> list[str]:
    return [course for course in sorted(courses) if course in data]


def legend_handles() -> list[Line2D]:
    handles: list[Line2D] = []
    for house, color in HOUSE_COLORS.items():
        handles.append(
            Line2D(
                [0],
                [0],
                marker="o",
                linestyle="",
                markerfacecolor=color,
                markeredgecolor="none",
                markersize=7,
                label=house,
            )
        )
    return handles


def add_top_legend(fig, anchor_y: float = 0.958) -> None:
    fig.legend(
        handles=legend_handles(),
        loc="upper center",
        ncol=len(HOUSE_COLORS),
        frameon=True,
        fancybox=True,
        framealpha=0.95,
        prop={"size": 16},
        bbox_to_anchor=(0.5, anchor_y),
    )


def title_size_for_fig(fig, minimum: int = 28, maximum: int = 48) -> int:
    return max(minimum, min(maximum, int(fig.get_figwidth() * 0.95)))


def apply_plot_margins(fig, margins: PlotMargins | None = None) -> None:
    margins = margins or PlotMargins()
    fig.subplots_adjust(
        left=margins.left,
        right=margins.right,
        bottom=margins.bottom,
        top=margins.top,
        wspace=margins.wspace,
        hspace=margins.hspace,
    )


def hide_axis_ticks(ax) -> None:
    ax.set_xticks([])
    ax.set_yticks([])


def _append(
    data: dict[str, list[str | float | None]], key: str, value: str | float | None
):
    if value == "":
        value = None

    try:
        parsed_value = float(value) if value is not None else None
    except (ValueError, TypeError):
        parsed_value = value

    data.setdefault(key, []).append(parsed_value)


def parse_data(
    filepath: str, targets: set[str] | None = None
) -> dict[str, list[str | float | None]]:
    """Parse a CSV file into a dictionary of columns."""

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Error: {filepath} is not a valid path.")

    columns: dict[str, list[str | float | None]] = {}

    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, restval="")

        if targets:
            for row in reader:
                for header in targets:
                    if header in row:
                        _append(columns, header, row[header])
                    else:
                        print("Warning: header not found.")
        else:
            for row in reader:
                for key, value in row.items():
                    _append(columns, key, value)
    return dict(columns)
