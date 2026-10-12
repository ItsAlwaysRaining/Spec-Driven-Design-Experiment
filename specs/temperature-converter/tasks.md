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

- [ ] **T7** Update the existing tests to `convert(value, from_unit, to_unit)` and the three-argument
  command line, comparing with `assertAlmostEqual(..., places=9)` (AC-1 to AC-7)
- [ ] **T8** Add tests for AC-8 to AC-12, `0 K` allowed and `-0.01 K` rejected (AC-5), an unknown
  target unit (AC-6), the two-argument form printing usage (AC-12), and no `-0.00` in the output.
  Run them and confirm they fail.

Then code:

- [ ] **T9** Replace the C/F formulas with the unit table (offset, factor) and convert through
  Kelvin (AC-1 to AC-4, AC-8 to AC-11)
- [ ] **T10** Build validation from the table: unknown source or target unit (AC-6), and absolute
  zero checked in Kelvin (AC-5)
- [ ] **T11** Update the command line: three arguments, usage message on the wrong number of arguments,
  2-decimal output that never shows `-0.00` (AC-7, AC-12)
- [ ] **T12** Update the `README.md` examples to the new command format

Finish:

- [ ] **T13** Run all the tests and confirm they pass
- [ ] **T14** Open a PR with `Closes #5` for review
