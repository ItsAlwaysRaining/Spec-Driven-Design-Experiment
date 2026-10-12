# Spec Driven Design — Minimal Example

A tiny project showing the spec-driven workflow: **write the spec first, then the code.**

Example feature: a temperature converter (Celsius, Fahrenheit and Kelvin).

## Workflow

```
1. requirements.md  →  WHAT we build and how we know it works (acceptance criteria)
2. design.md        →  HOW we build it (interfaces, data, error handling)
3. tasks.md         →  the ordered checklist of implementation steps
4. tests/           →  tests derived directly from the acceptance criteria
5. src/             →  code written to make the tests pass
```

Every acceptance criterion has an ID (e.g. `AC-1`), and the tests use those IDs,
so you can trace each line of code back to a requirement.

## Layout

```
.
├── CLAUDE.md                          # rules for AI assistants working here
├── README.md
├── specs/
│   └── temperature-converter/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
├── src/
│   └── converter.py
└── tests/
    └── test_converter.py
```

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Try it

```bash
python3 src/converter.py <value> <from_unit> <to_unit>

python3 src/converter.py 100 C F    # -> 212.00 F
python3 src/converter.py 32 F C     # -> 0.00 C
python3 src/converter.py 0 C K      # -> 273.15 K
python3 src/converter.py 0 K F      # -> -459.67 F
```

Units are `C`, `F` and `K` (case-insensitive).

## Adding a new feature

1. Open a GitHub issue for each user story (label `user-story`).
2. Create a branch: `git switch -c feature/<name>`.
3. Create `specs/<feature-name>/` and write `requirements.md` there.
4. Get the requirements reviewed, then write `design.md`.
5. Break the design into `tasks.md`.
6. Write the tests, then the code, and tick off the tasks as you finish them.
7. Push and open a pull request (`gh pr create`) with `Closes #<n>` in the description.
8. The repo owner reviews and merges. `main` is protected, so direct pushes are rejected.
