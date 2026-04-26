from pathlib import Path

ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent
PLOT_DIR: Path = ROOT_DIR / "plot"
OUTPUT_DIR: Path = ROOT_DIR / "output"
DATASETS_DIR: Path = ROOT_DIR / "datasets"

HOUSE_COLUMN: str = "Hogwarts House"

HOUSES: list[str] = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

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

CHOSEN_COURSES: set[str] = {
    "Astronomy",
    "Herbology",
    "Divination",
    "Muggle Studies",
    "Ancient Runes",
    "History of Magic",
    "Transfiguration",
    "Potions",
    "Charms",
    "Flying",
}


PLOT_DPI: int = 120
