from __future__ import annotations

from typing import Any


REQUIRED_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]


def parse_bool(value: str) -> bool:
    """Convert config bool text to Python bool."""
    lowered = value.strip().lower()

    if lowered == "true":
        return True
    if lowered == "false":
        return False

    raise ValueError("PERFECT must be True or False.")


def parse_coords(value: str) -> tuple[int, int]:
    """Convert 'x,y' string to coordinates tuple."""
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError("Coordinates must be in format x,y")

    x = int(parts[0].strip())
    y = int(parts[1].strip())

    return (x, y)


def parse_config(filename: str) -> dict[str, Any]:
    """Read and validate config file."""
    raw: dict[str, str] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid config line: {line}")

            key, value = line.split("=", 1)
            raw[key.strip().upper()] = value.strip()

    for key in REQUIRED_KEYS:
        if key not in raw:
            raise ValueError(f"Missing required key: {key}")

    return {
        "WIDTH": int(raw["WIDTH"]),
        "HEIGHT": int(raw["HEIGHT"]),
        "ENTRY": parse_coords(raw["ENTRY"]),
        "EXIT": parse_coords(raw["EXIT"]),
        "OUTPUT_FILE": raw["OUTPUT_FILE"],
        "PERFECT": parse_bool(raw["PERFECT"]),
        "SEED": int(raw["SEED"]) if "SEED" in raw else None,
    }
