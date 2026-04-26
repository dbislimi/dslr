from matplotlib.lines import Line2D

from .constants import HOUSE_COLORS, PLOT_DIR, PLOT_DPI


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


def hide_axis_ticks(ax) -> None:
    ax.set_xticks([])
    ax.set_yticks([])


def save_png(fig, filename: str) -> None:
    """Save ``fig`` to ``PLOT_DIR/filename``. Creates the directory if needed."""
    try:
        PLOT_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            PLOT_DIR / filename,
            dpi=PLOT_DPI,
            bbox_inches="tight",
            pad_inches=0.02,
            pil_kwargs={"optimize": True, "compress_level": 9},
        )
    except OSError as e:
        print(f"Error: cannot save plot {filename}: {e}")
