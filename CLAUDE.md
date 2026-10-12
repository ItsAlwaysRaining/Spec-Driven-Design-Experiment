# Project rules

This project follows spec-driven design.

- Write no code without a spec. Each feature lives in `specs/<feature-name>/` with
  `requirements.md`, `design.md` and `tasks.md`.
- Work in order: requirements → design → tasks → tests → code.
- Every acceptance criterion has an ID (`AC-n`), and each test names the ID it covers.
- If the code needs to differ from the spec, update the spec first.
- Tick tasks in `tasks.md` as you finish them.
- Each user story has a GitHub issue (label `user-story`), linked from `requirements.md`.
  New stories get a new issue (`gh issue create --label user-story`), and the commit that
  completes a story says `Closes #<n>`.
- Run the tests with `python3 -m unittest discover -s tests -v` (Python 3.9, stdlib only).
