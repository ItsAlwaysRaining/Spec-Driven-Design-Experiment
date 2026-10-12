# Design: Temperature Converter

Status: Implemented · Implements: [requirements.md](requirements.md)

## Overview

Two Python modules, both using only the standard library:

- `src/converter.py`: pure conversion functions plus a thin command-line wrapper (US-1 to US-4).
- `src/gui.py`: a small local web page for US-5, built on top of `converter.py`.
  See [Browser page (US-5)](#browser-page-us-5).

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

## Browser page (US-5)

### How it runs

```
python3 src/gui.py
```

1. Starts Python's built-in web server (`http.server`) on `127.0.0.1` only, so no other device
   can reach it.
2. Lets the operating system pick a free port, so it never clashes with something already running.
3. Opens the page in the default browser (`webbrowser`), and prints the address in the terminal
   in case the browser doesn't open.
4. Keeps running until the user presses **Ctrl+C** in the terminal.

All of these are in the standard library, so nothing needs installing (AC-18).

### The page

Plain HTML, with no CSS, JavaScript or images, so it has the browser's default look
(minimal-formatting constraint):

```
Temperature Converter

Value [ 100        ]  Unit [ C ▾ ]  [ Convert ]

212.00 F
373.15 K
```

- A normal HTML **form** submitted with GET: `/?value=100&unit=C`. Pressing **Enter** in the
  field submits it too, with no JavaScript needed.
- The unit list is built from `UNITS` in `converter.py`, so a new unit appears automatically
  (AC-13, AC-17).
- After converting, the form keeps the entered value and selected unit, so the user can change
  one thing and convert again (AC-16).
- On first load (no `value` in the address) the page shows the empty form and no results.
- Any path other than `/` returns `404 Not Found` (browsers ask for `/favicon.ico` on their own).

### Code structure

The logic is kept out of the web server, so it can be tested without a browser:

| Function | Where | Does | Covers |
|----------|-------|------|--------|
| `format_result(value, unit) -> str` | `converter.py` | `"212.00 F"`: 2 decimals, never `-0.00`. Moved out of the CLI's `main()` so the CLI and the page share it. CLI output does not change. | AC-7, AC-15 |
| `conversion_lines(value_text, from_unit) -> List[str]` | `gui.py` | Parses the text, converts to every unit in `UNITS` except the source, in table order, and formats each one. Raises `ValueError` with a message for the user. | AC-14 – AC-17 |
| `render_page(value_text, unit) -> str` | `gui.py` | Builds the full HTML: the form, then either the result lines or the error. | AC-13, AC-16 |
| `make_server(port=0) -> HTTPServer` | `gui.py` | Creates the server on `127.0.0.1` without starting it or opening a browser. Used by `main()` and by the tests. | AC-18 |
| `main()` | `gui.py` | `make_server()`, opens the browser, serves until Ctrl+C. | AC-18 |

### Errors (AC-16)

The page shows `Error: <message>` where the results would be. The server keeps running.

| Input | Message |
|-------|---------|
| Empty, not a number, `nan` or `inf` | `Enter a number` |
| Below absolute zero | `Below absolute zero` (from `convert()`) |
| Unknown unit (only possible by editing the address) | `Unit must be one of C, F, K` (from `convert()`) |

### Security

The entered value is shown back on the page, so it is escaped with `html.escape` before being
written into the HTML. Otherwise typing something like `<script>` into the field would run as
code in the page. The server only listens on `127.0.0.1`.

### Known gap, not fixed here

Python's `float()` accepts `nan` and `inf`, so the command line prints `nan F` today. The page
rejects these. Fixing the CLI is a change to US-3 and belongs in its own issue.

### Testing

New file `tests/test_gui.py`, using `unittest` as before. Each test names its AC.

- `conversion_lines`: AC-14 (`100 C` → `212.00 F`, `373.15 K`, source unit not included),
  AC-15 (`-17.78 C` gives `0.00 F`), AC-16 (empty, `abc`, `nan`, below absolute zero).
- AC-17: temporarily add a unit to `UNITS` in the test (`unittest.mock.patch.dict`, e.g. Rankine
  `offset 0, factor 5/9`) and check it appears in both the unit list and the results.
- `render_page`: the form has the value field and every unit (AC-13); an error replaces the
  results (AC-16); `<script>` in the value comes back escaped.
- AC-18: start `make_server()` on a free port in a background thread, fetch
  `/?value=100&unit=C` with `urllib`, check the results are in the page, then shut it down.
  The tests never open a browser.
- Existing CLI tests stay unchanged and protect the `format_result` move.
- Manual check before the PR: run `python3 src/gui.py` and try it in the browser.
