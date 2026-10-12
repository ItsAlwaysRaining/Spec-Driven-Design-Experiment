"""Temperature converter. Spec: specs/temperature-converter/"""
import sys

# Each unit converts to Kelvin as: kelvin = (value + offset) * factor
# To add a unit, add a row here. Everything else is derived from this table.
UNITS = {
    "C": (273.15, 1.0),
    "F": (459.67, 5 / 9),
    "K": (0.0, 1.0),
}


def _lookup(unit: str):
    try:
        return UNITS[unit.upper()]
    except KeyError:  # AC-6
        raise ValueError("Unit must be one of " + ", ".join(UNITS)) from None


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from from_unit to to_unit ("C", "F" or "K")."""
    from_offset, from_factor = _lookup(from_unit)
    to_offset, to_factor = _lookup(to_unit)

    kelvin = (value + from_offset) * from_factor
    if kelvin < 0:  # AC-5
        raise ValueError("Below absolute zero")
    return kelvin / to_factor - to_offset  # AC-1 to AC-4, AC-8 to AC-11


def format_result(value: float, unit: str) -> str:
    """Format for display: 2 decimals and the unit, e.g. "212.00 F" (AC-7, AC-15)."""
    text = f"{value:.2f}"
    if text == "-0.00":  # never show negative zero
        text = "0.00"
    return f"{text} {unit.upper()}"


def main(argv) -> int:
    if len(argv) != 3:  # AC-12
        print("Usage: converter.py <value> <from_unit> <to_unit>  (units: "
              + ", ".join(UNITS) + ")")
        return 1
    try:
        result = convert(float(argv[0]), argv[1], argv[2])
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    print(format_result(result, argv[2]))  # AC-7
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
