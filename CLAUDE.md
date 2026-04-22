# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a course repository (not an application). It organizes 18 weeks of Python CPE (UVA Online Judge) practice material, plus student submission tracking. There is no build system, no package manifest, no test runner at the repo root — each solution is a standalone Python script run with `python3 <file>.py`.

The repo serves two audiences simultaneously:
1. **Instructor/TA side** (this checkout, `main` branch): authoritative course content — weekly problem statements, in-class examples, grading guides, submission trackers.
2. **Student side** (forks from the GitHub template): students add their own solutions under `weeks/week-XX/solutions/<student-id>/` and open PRs against upstream `main`.

## Layout that matters

- `weeks/week-XX/QUESTION-<UVA#>.md` — problem statements (Traditional Chinese). **Do not modify these casually**; they are referenced by CI and the submission policy treats them as read-only for students.
- `weeks/week-XX/README.md` — weekly overview / task instructions.
- `weeks/week-XX/solutions/<student-id>/` — the **only** path students are permitted to change (enforced by `.github/workflows/submission-policy-check.yml`).
- `weeks/week-04/in-class/` — instructor's in-class example scripts (`R01-*.py` … naming = Bloom taxonomy level + topic, tied to Python Cookbook chapters).
- `docs/SUBMISSION_GUIDE.md`, `docs/TA_GRADING_GUIDE.md` — authoritative rules for submissions and grading. Consult before changing anything about the PR workflow.
- `docs/analysis/` — generated analysis of the 49 questions (JSON/CSV/reports). Treat as derived data.
- `IN_CLASS_EXERCISE.md`, `HOMEWORK.md` — per-student PR submission trackers, updated weekly.
- `CHECK_LIST.md` — quality-check status for the 49 question documents.

## Submission policy (enforced by CI)

`.github/workflows/submission-policy-check.yml` runs on every PR and requires:
- PR title matches `Week XX - <student-id> - <name>` (two-digit week, numeric ID).
- **Every** changed file path matches `^weeks/week-[0-9]{2}/solutions/[0-9]+/`. Any file outside that scope fails the check.

When authoring or reviewing a student-scope change, keep edits strictly inside one student's solutions folder. Instructor-side edits (question docs, trackers, in-class examples) happen on `main` directly, not via the student PR flow.

## Conventions worth knowing

- **Language**: repo documentation and code comments are in **Traditional Chinese** (繁體中文). Follow suit when editing existing docs.
- **Per-problem solution pattern** (from `weeks/week-XX/README.md`): students submit 4 files per problem — an AI-generated "easy" version with Chinese comments, a hand-typed formal version, a unit test, and a test-run log.
- **Upstream workflow**: students add this repo as `upstream` and sync via `git fetch upstream && git merge upstream/main`. When making changes on `main` here, assume downstream forks will pull them.

## Running / testing code

There is no repo-level test runner. Individual scripts and tests are run directly, e.g.:

```bash
python3 weeks/week-04/in-class/R01-strings-split-match.py
python3 -m unittest weeks/week-03/solutions/<id>/test_100.py
```

Student solutions are expected to pass their own `unittest` suites; there is no aggregate CI that executes them.
