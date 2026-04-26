from typing import Any, Literal, overload


@overload
def convert_to_float(
    data: dict[str, list[str | None]], courses: list[str], delete_none: Literal[True]
) -> dict[str, list[float]]: ...


@overload
def convert_to_float(
    data: dict[str, list[str | None]], courses: list[str], delete_none: Literal[False]
) -> dict[str, list[float | None]]: ...


def convert_to_float(
    data: dict[str, list[str | None]], courses: list[str], delete_none: bool
) -> dict[str, list[float]] | dict[str, list[float | None]]:
    clean: dict[str, list[Any]] = {}

    for course in courses:
        grades = data.get(course)
        if grades is None:
            continue
        clean_list: list[Any] = []
        for grade in grades:
            if grade is None:
                if not delete_none:
                    clean_list.append(grade)
            else:
                try:
                    clean_list.append(float(grade))
                except (ValueError, TypeError):
                    pass
        if len(clean_list) != 0:
            clean[course] = clean_list
    return clean


def available_courses(
    data: dict[str, list[str | None]], courses: set[str]
) -> list[str]:
    """Return courses present in ``data`` (sorted for determinism)."""
    return sorted(course for course in courses if course in data)
