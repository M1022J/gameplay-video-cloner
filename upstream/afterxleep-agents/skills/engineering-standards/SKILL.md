---
name: engineering-standards
version: 1.0.0
description: >-
  Project-agnostic engineering standards. Use before planning code changes,
  before writing code, while reviewing code, and when deciding failure modes,
  TDD order, code organization, comments, error handling, tests, mocks,
  fixtures, refactors, dependencies, delegation, completion summaries, or git
  hygiene. Read the matching references for depth.
---

# Engineering Standards

Use before planning a code change and again before writing code. Keep this file
as the router; load the reference that matches the work.

## Core Principles

1. Clarity over cleverness.
2. Explicit over implicit.
3. Composition over inheritance.
4. Fail fast and fail loud.
5. Delete code when possible.
6. Verify instead of assuming.

## Required Planning Artifacts

Before non-trivial code changes, surface:

1. Goal and scope.
2. Failure modes, classified core / edge / out-of-scope.
3. Existing-code survey.
4. TDD plan: the first failing test, then the implementation and failure-case
   tests that follow.
5. Documentation/update plan, if behavior or contracts change.

## Test Driven Development Is The Default

For behavior with a clear contract, write the failing test before implementation
code. Do not skip straight to production code because the change looks small.

Allowed exceptions:

- trivial typo/import/comment edits
- pure documentation changes
- exploratory spikes where the boundary is genuinely unknown
- generated or mechanical changes with no behavior contract

When taking an exception, state it explicitly and add or update regression tests
as soon as the behavior boundary is known.

## References

- Workflow, failure modes, debugging, and completion:
  `references/workflow.md`
- Code organization, API style, comments, and errors:
  `references/code-quality.md`
- Testing, mocks, fixtures, and TDD:
  `references/testing.md`
- Refactoring and dependency decisions:
  `references/refactoring-dependencies.md`
- Git, PRs, and delegation:
  `references/collaboration.md`

## Default Rule

If a project has its own standards, apply those first. Use this skill for the
general engineering bar that remains true across projects.
