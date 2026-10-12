# Design: Temperature Converter

Status: Implemented · Implements: [requirements.md](requirements.md)

## Overview

One Python module, `src/converter.py`, with pure functions plus a thin command-line wrapper.
It uses only the standard library.

Every conversion goes through **Kelvin** as a common base: source unit → Kelvin → target unit.
Each unit is one row in a table, so adding a unit (e.g. Rankine) means adding one row,
not writing new formulas for every pair of units.

## Interface

```python
def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from from_unit to to_unit ("C", "F" or "K")."""
```

This changes the interface. It was `convert(value, unit) -> (value, other_unit)`; with three units,
"the other unit" no longer works, so the caller names the target (AC-12). The function now
returns just the number, because the caller already knows the target unit.

Command line:

```
python3 src/converter.py <value> <from_unit> <to_unit>

python3 src/converter.py 100 C F   # -> 212.00 F
python3 src/converter.py 0 C K     # -> 273.15 K
```

The old two-argument form (`converter.py 100 C`) is removed. It prints the usage message and
exits with code 1.

## Logic

Each unit is defined by an offset and a factor:

```
kelvin = (value + offset) × factor           # to Kelvin
value  = kelvin ÷ factor − offset            # from Kelvin
```

| Unit | Offset | Factor | Absolute zero (derived) | Covers |
|------|--------|--------|-------------------------|--------|
| C    | 273.15 | 1      | -273.15                 | AC-1 – AC-4, AC-8, AC-10 |
| F    | 459.67 | 5/9    | -459.67                 | AC-1 – AC-4, AC-9, AC-11 |
| K    | 0      | 1      | 0                       | AC-8 – AC-11 |

- Adding a unit means adding one row. For example, Rankine would be `offset 0, factor 5/9`.
  The list of valid units, the error message and the absolute-zero check all come from this table.
- Units are case-insensitive (`k` is treated as `K`).
- Converting a unit to itself is allowed and returns the same value.
- The function returns the unrounded value. Rounding happens only for display (AC-7).

## Floating-point precision

Going through Kelvin introduces tiny floating-point errors, e.g. `100 C → F` gives
`211.99999999999994`. This is expected and handled in two places:

- **Display:** output is rounded to 2 decimal places (AC-7), so the user sees `212.00 F`.
  A result that rounds to zero is shown as `0.00`, never `-0.00`.
- **Tests:** compare numbers with `assertAlmostEqual(..., places=9)`, not `assertEqual`.

## Error handling

| Condition           | Behaviour | Covers |
|---------------------|-----------|--------|
| Unknown unit (source or target) | raise `ValueError("Unit must be one of C, F, K")` (list built from the table) | AC-6 |
| Below absolute zero | raise `ValueError("Below absolute zero")` when the value converted to Kelvin is below 0 | AC-5 |
| Error on the command line | print `Error: <message>` and exit with code 1 | AC-5, AC-6 |
| Wrong number of arguments | print the usage message and exit with code 1 | AC-12 |

Checking absolute zero in Kelvin means one rule covers every unit, including future ones.

## Testing

`tests/test_converter.py` uses `unittest`. Each test method names the AC it verifies.

- The existing tests for AC-1 to AC-7 are updated to the new three-argument interface.
  Their expected values stay the same.
- New tests cover AC-8 to AC-12, plus `0 K` (allowed) and `-0.01 K` (error) for AC-5.
- `README.md` examples are updated to the new command format.
