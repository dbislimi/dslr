"""Shared utilities.

Submodules:
- ``constants``: project-wide names, paths, and palettes
- ``csv_io``    : CSV parsing
- ``data``      : numeric coercion / column filtering helpers
- ``plot``      : matplotlib helpers (legend, save, etc.)

"""

from .constants import (
    CHOSEN_COURSES,
    COURSES,
    DATASETS_DIR,
    HOUSE_COLORS,
    HOUSE_COLUMN,
    HOUSES,
    OUTPUT_DIR,
    PLOT_DIR,
    PLOT_DPI,
    ROOT_DIR,
)
from .csv_io import parse_data
from .data import available_courses, convert_to_float
from .plot import (
    add_top_legend,
    hide_axis_ticks,
    legend_handles,
    save_png,
    title_size_for_fig,
)

__all__ = [
    "CHOSEN_COURSES",
    "COURSES",
    "DATASETS_DIR",
    "HOUSE_COLORS",
    "HOUSE_COLUMN",
    "HOUSES",
    "OUTPUT_DIR",
    "PLOT_DIR",
    "PLOT_DPI",
    "ROOT_DIR",
    "add_top_legend",
    "available_courses",
    "convert_to_float",
    "hide_axis_ticks",
    "legend_handles",
    "parse_data",
    "save_png",
    "title_size_for_fig",
]
