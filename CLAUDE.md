# Project rules

This project follows spec-driven design.

- Write no code without a spec. Each feature lives in `specs/<feature-name>/` with
  `requirements.md`, `design.md` and `tasks.md`.
- Work in order: requirements → design → tasks → tests → code.
- Every acceptance criterion has an ID (`AC-n`), and each test names the ID it covers.
- If the code needs to differ from the spec, update the spec first.
- Tick tasks in `tasks.md` as you finish them.
- Each user story has a GitHub issue (label `user-story`), linked from `requirements.md`.
  New stories get a new issue (`gh issue create --label user-story`).

## Git workflow

- `main` is protected: every change goes through a pull request.
- Start each piece of work on a new branch off an up-to-date `main`:
  `feature/<name>` for features, `fix/<name>` for bug fixes, `chore/<name>` for tooling and docs.
- Push the branch and open a PR with `gh pr create`, filling in `.github/pull_request_template.md`.
  Put `Closes #<n>` in the PR description for each user story the PR completes.
- Never merge a PR. The repo owner reviews and merges every PR (`gh pr merge` is denied
  in `.claude/settings.json`). After a merge: `git switch main && git pull`.
- Run the tests with `python3 -m unittest discover -s tests -v` (Python 3.9, stdlib only).
