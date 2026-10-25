# Workflow, Failure Modes, And Debugging

## Before Writing Code

For any change beyond a trivial typo/import/comment:

1. Restate the goal and expected outcome.
2. Clarify ambiguous requirements before implementing.
3. List failure modes:
   - invalid inputs
   - missing dependencies
   - network or IO failures
   - concurrency issues
   - resource exhaustion
   - permissions
   - stale or partial state
4. Classify them:
   - **Core flow:** happy path and direct error cases.
   - **Edge cases:** unusual but valid scenarios.
   - **Out of scope:** name them, do not implement them silently.
5. Check existing code for the same behavior, helpers, mocks, fixtures, and
   conventions. Extend instead of creating parallel machinery.

## Implementation Order

Use Test Driven Development by default when the behavior has a clear contract.
The first code-changing step is the failing test:

1. Write a failing test for the core happy path.
2. Implement the minimum code to pass.
3. Write failing tests for core error cases.
4. Implement error handling.
5. Refactor only while tests stay green.
6. Add edge-case tests after the core flow is solid.

Do not write production code first just because the change is small. If you
skip TDD, state the exception explicitly:

- trivial typo/import/comment edit
- pure documentation change
- exploratory spike before the boundary is known
- mechanical/generated change with no behavior contract

If the boundary is not yet testable, make the boundary testable first. Do not
use "hard to test" as a permanent excuse.

## Staying Focused

- Modify only what the task requires.
- Do not bundle unrelated cleanups, renames, style sweeps, or opportunistic
  refactors.
- Prefer the smallest reversible change that solves the real problem.
- Ship complete: code, tests, docs/wiring introduced by the change, and cleanup
  needed by the change.
- Do not leave TODOs as a substitute for in-scope completion.

## Debugging Process

When something fails:

1. Reproduce it reliably.
2. Isolate the smallest failing input or action.
3. Read the full error, stack trace, logs, and surrounding state.
4. Form one concrete hypothesis.
5. Test that hypothesis with a narrow change, log, assertion, or test.
6. Fix one thing.
7. Verify the fix.
8. Add a regression test where the boundary permits it.

Avoid:

- changing multiple things at once
- deleting error handling to simplify the symptom
- assuming the cause without evidence
- fixing the symptom instead of the root cause

## Before Submitting

Check:

- relevant tests pass
- formatting/linting passes where applicable
- no commented-out code
- no bare TODOs
- error messages are actionable
- no secrets, credentials, or environment-specific values
- docs are updated when behavior, contracts, schema, public APIs, or operational
  workflow changed

## Completion Summary

After code or docs changes, report two layers:

- **Simple summary:** what changed and why it matters.
- **Technical details:** files/APIs touched, behavior mechanics, and verification
  performed.
