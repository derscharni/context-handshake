---
date: 2026-04-07
session-type: technical
goal: A working CI pipeline that runs unit tests and type checks on every PR
constraints:
  - GitHub Actions, not Jenkins or CircleCI
  - Must complete in under 3 minutes
  - No secrets stored in the workflow file
  - Python 3.12, pytest, mypy
active-context: We currently run tests manually before merging. Two bugs shipped last week because someone forgot.
open-questions:
  - Should we block merges on failure or just warn?
  - Do we need a separate job for type checking or can it run in parallel?
---
