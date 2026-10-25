# Swift Testing, Refactoring, And Quick Rules

## Testing

TDD is the default for logic with a clear contract:

- parsing
- validation
- state transitions
- persistence rules
- error mapping
- configuration resolution
- deterministic orchestration

Order:

1. failing happy-path test
2. smallest passing implementation
3. core failure-case tests
4. error handling
5. refactor with tests green
6. edge cases

For process-heavy integration, external tool wrappers, transport glue, or UI
flows, a short spike can be acceptable. Formalize the discovered contract with
regression tests once the shape is known.

Every bug fix adds a regression test unless the current boundary makes that
genuinely impossible. Treat that as design feedback.

## Coverage

Coverage is a safety metric, not a vanity number.

Prioritize coverage for:

- persistence and migrations
- parsing and serialization
- state transitions
- error mapping
- config resolution
- concurrency coordination
- domain rules

Review branch coverage, not just line coverage. The valuable uncovered paths are
fallbacks, retries, cancellation, invalid inputs, and error mapping.

Hard-to-cover code is often a structure problem: hidden side effects, large
functions, unclear boundaries, or poor separation between pure and operational
work.

## Refactoring Swift

Apply standards incrementally. Do not reformat or rewrite a codebase just
because the guide is stricter than existing code.

When touching old code, improve the nearby boundary:

- extract one pure function
- replace one loose dictionary with a typed model
- move one persistence rule into storage
- introduce one domain error replacing a generic failure
- isolate one shared mutable state path

Do not change behavior and structure in the same step.

## Quick Rules

- `let` by default; `var` only when mutation is required.
- `throws` for recoverable operational failure.
- `Result` only when failure must be ordinary data.
- `guard` for required preconditions and early exits.
- Enums over booleans for behavior modes.
- Typed constants over repeated literals.
- Config structs over long argument lists.
- Domain types over tuples when the result has meaning beyond local scope.
- Explicit access control; make `public` deliberate.
- `final class` unless subclassing is necessary.
- Small protocol surfaces over broad weakly-owned abstractions.
- Typed models over `[String: Any]` except at parsing/transport edges.
- Explicit actor isolation over informal thread assumptions.
- Core Animation representables over SwiftUI state-driven loops for continuous
  effects.
- Straightforward control flow over dense chaining when chaining reduces
  clarity.
- Comments explain why, not what.
