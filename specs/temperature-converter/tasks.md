# Tasks: Temperature Converter

Implements: [design.md](design.md)

## US-1 to US-3: Celsius ⇄ Fahrenheit (done)

- [x] **T1** Write the tests for AC-1 to AC-7 in `tests/test_converter.py` (they should fail at first)
- [x] **T2** Implement `convert()` for C → F (AC-1, AC-2)
- [x] **T3** Implement `convert()` for F → C (AC-3, AC-4)
- [x] **T4** Add validation for the unit and absolute zero (AC-5, AC-6)
- [x] **T5** Add the command-line wrapper with 2-decimal output (AC-7)
- [x] **T6** Run all the tests and confirm they pass

## US-4: Kelvin ([#5](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/5))

Tests first:

- [x] **T7** Update the existing tests to `convert(value, from_unit, to_unit)` and the three-argument
  command line, comparing with `assertAlmostEqual(..., places=9)` (AC-1 to AC-7)
- [x] **T8** Add tests for AC-8 to AC-12, `0 K` allowed and `-0.01 K` rejected (AC-5), an unknown
  target unit (AC-6), the two-argument form printing usage (AC-12), and no `-0.00` in the output.
  Run them and confirm they fail.

Then code:

- [x] **T9** Replace the C/F formulas with the unit table (offset, factor) and convert through
  Kelvin (AC-1 to AC-4, AC-8 to AC-11)
- [x] **T10** Build validation from the table: unknown source or target unit (AC-6), and absolute
  zero checked in Kelvin (AC-5)
- [x] **T11** Update the command line: three arguments, usage message on the wrong number of arguments,
  2-decimal output that never shows `-0.00` (AC-7, AC-12)
- [x] **T12** Update the `README.md` examples to the new command format

Finish:

- [x] **T13** Run all the tests and confirm they pass
- [x] **T14** Open a PR with `Closes #5` for review

## US-5: Browser page ([#6](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/6))

Tests first:

- [ ] **T15** Add a test for `format_result()` to `tests/test_converter.py`: `212.00 F`, and `0.00`
  instead of `-0.00` (AC-7, AC-15)
- [ ] **T16** Create `tests/test_gui.py` with tests for `conversion_lines` (AC-14 to AC-16), a unit
  added to `UNITS` appearing automatically (AC-17), `render_page` (AC-13, AC-16, escaping `<script>`)
  and a real server on a free port (AC-18). Run them and confirm they fail.

Then code:

- [ ] **T17** Move the 2-decimal formatting from the CLI's `main()` into `format_result()` in
  `converter.py`, and use it in the CLI. CLI output must not change (AC-7, AC-15)
- [ ] **T18** Create `src/gui.py` with `conversion_lines()`: parse the text, reject empty, non-numbers,
  `nan` and `inf`, and convert to every other unit in table order (AC-14 to AC-17)
- [ ] **T19** Add `render_page()`: plain HTML form with the unit list from `UNITS`, keeping the entered
  value and unit, then the results or `Error: <message>`, with the value escaped (AC-13, AC-16, AC-17)
- [ ] **T20** Add `make_server()` and `main()`: listen on `127.0.0.1`, free port, open the browser,
  print the address, stop on Ctrl+C (AC-18)
- [ ] **T21** Update `README.md`: how to start the page, and add `gui.py` and `test_gui.py` to the layout

Finish:

- [ ] **T22** Run all the tests and confirm they pass
- [ ] **T23** Manual check: run `python3 src/gui.py` and try a conversion, an error and the Enter key
  in the browser
- [ ] **T24** Open a PR with `Closes #6` for review
