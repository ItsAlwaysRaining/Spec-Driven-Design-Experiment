"""Temperature converter. Spec: specs/temperature-converter/"""
import sys
from typing import Tuple

ABSOLUTE_ZERO = {"C": -273.15, "F": -459.67}


def convert(value: float, unit: str) -> Tuple[float, str]:
    """Convert value from unit ("C" or "F") to the other unit.
    Returns (converted_value, target_unit)."""
    unit = unit.upper()
    if unit not in ABSOLUTE_ZERO:  # AC-6
        raise ValueError("Unit must be 'C' or 'F'")
    if value < ABSOLUTE_ZERO[unit]:  # AC-5
        raise ValueError("Below absolute zero")

    if unit == "C":  # AC-1, AC-2
        return value * 9 / 5 + 32, "F"
    return (value - 32) * 5 / 9, "C"  # AC-3, AC-4


def main(argv) -> int:
    if len(argv) != 2:
        print("Usage: converter.py <value> <C|F>")
        return 1
    try:
        result, target = convert(float(argv[0]), argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    print(f"{result:.2f} {target}")  # AC-7
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
