# Design: Temperature Converter

Status: Approved · Implements: [requirements.md](requirements.md)

## Overview

One Python module, `src/converter.py`, with pure functions plus a thin command-line wrapper.
It uses only the standard library.

## Interface

```python
def convert(value: float, unit: str) -> Tuple[float, str]:
    """Convert value from unit ("C" or "F") to the other unit.
    Returns (converted_value, target_unit)."""
```

Command line:

```
python3 src/converter.py <value> <unit>
```

## Logic

| From | Formula            | Absolute zero | Covers |
|------|--------------------|---------------|--------|
| C    | `F = C × 9/5 + 32` | -273.15       | AC-1, AC-2 |
| F    | `C = (F − 32) × 5/9` | -459.67     | AC-3, AC-4 |

- The unit is case-insensitive (`c` is treated as `C`).
- The function returns the unrounded value. Rounding happens only for display (AC-7).

## Error handling

| Condition           | Behaviour | Covers |
|---------------------|-----------|--------|
| Unknown unit        | raise `ValueError("Unit must be 'C' or 'F'")` | AC-6 |
| Below absolute zero | raise `ValueError("Below absolute zero")`     | AC-5 |
| Error on the command line | print `Error: <message>` and exit with code 1 | AC-5, AC-6 |

## Testing

`tests/test_converter.py` uses `unittest`. Each test method names the AC it verifies.
