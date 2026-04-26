import csv
from pathlib import Path


def _append(data: dict[str, list[str | None]], key: str, value: str | None) -> None:
    if value == "":
        value = None
    data.setdefault(key, []).append(value)


def parse_data(
    filepath: str, targets: set[str] | None = None
) -> dict[str, list[str | None]]:
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Error: {filepath} is not a valid path.")

    columns: dict[str, list[str | None]] = {}

    try:
        f = path.open(mode="r", newline="", encoding="utf-8")
    except OSError as e:
        raise FileNotFoundError(f"Error: cannot open {filepath}: {e}") from e

    with f:
        try:
            reader = csv.DictReader(f, restval="")
        except csv.Error as e:
            raise ValueError(f"Error: malformed CSV {filepath}: {e}") from e

        if targets is None:
            for row in reader:
                for key, value in row.items():
                    _append(columns, key, value)
            return columns

        header_fields = set(reader.fieldnames or [])
        missing_headers = [t for t in targets if t not in header_fields]
        for header in missing_headers:
            print(f"Warning: header '{header}' not found in CSV.")

        for row in reader:
            for header in targets:
                _append(columns, header, row.get(header))
    return columns
