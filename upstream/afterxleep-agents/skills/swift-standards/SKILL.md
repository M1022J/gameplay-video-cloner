---
name: swift-standards
version: 1.0.0
description: >-
  Project-agnostic Swift and Apple-platform coding standards. Use immediately
  before writing, modifying, or reviewing Swift code. Covers type choice, API
  design, dependency boundaries, typed errors, persistence, concurrency,
  Sendable, @MainActor, SwiftUI state, continuous animation performance,
  typography, strings, testing, and incremental refactors. Read references for
  depth.
---

# Swift Standards

Use immediately before writing or reviewing Swift code. Pair with the project's
own standards for package layout, tests, fixtures, validation, and product
constraints.

## Mandatory Swift Artifacts

Before editing Swift, decide:

1. Type choice: `struct`, `enum`, `final class`, `actor`, or `@MainActor`.
2. Concurrency model: isolation, `Sendable`, cancellation, task ownership.
3. Error model: typed error boundary and external-error mapping.
4. Testability: behavior to test and boundary to verify.
5. Specialist check: SwiftUI, concurrency, performance, UI verification, or
   pixel-perfect work may need a more specific skill/reference.

## References

- Design philosophy, type choice, API design, and dependencies:
  `references/design-and-api.md`
- Error handling, state, persistence, and wire models:
  `references/errors-state-persistence.md`
- Concurrency, actors, `Sendable`, and task lifecycle:
  `references/concurrency.md`
- SwiftUI, animation performance, typography, strings, and accessibility:
  `references/swiftui-and-ui.md`
- Testing, coverage, refactoring, and quick rules:
  `references/testing-refactoring-rules.md`

## Default Rule

Prefer explicit ownership, typed state, domain errors, visible dependencies, and
small composable units. Improve legacy code incrementally; do not reformat or
rewrite unrelated surfaces.
