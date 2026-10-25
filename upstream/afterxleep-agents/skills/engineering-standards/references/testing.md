# Testing, Mocks, And Fixtures

## Principles

- Test Driven Development is the default for behavior changes with a clear
  contract: failing test first, smallest passing implementation, then failure
  cases.
- Tests are isolated: no shared mutable state and no order dependencies.
- Tests should run safely in parallel.
- One behavior per test.
- Test behavior, not implementation details.
- Fast tests get run; slow tests get skipped.
- Prefer the smallest scope that proves the changed behavior.
- Full suites can be expensive; use them deliberately and follow project policy.

## Before Writing A Test

1. Check whether the behavior is already covered.
2. Reuse an existing mock for the owned protocol/interface.
3. Reuse an existing fixture when it fits.
4. Create a new mock or fixture only when the behavior needs it.

Coverage means a test asserts observable output, error, side effect, emitted
event, or persisted state. Merely importing a type or executing a line is not
coverage.

## TDD Order

For new features and behavior changes:

1. Document failure modes before implementation.
2. Write the happy-path test and confirm it fails for the expected reason.
3. Implement the minimum passing code.
4. Add direct failure/error tests and confirm they fail for the expected reason.
5. Implement error handling.
6. Refactor while tests stay green.
7. Add edge cases after the core flow is solid.

For bugs, reproduce first and add a regression test unless the boundary is
genuinely untestable.

TDD exceptions must be explicit and narrow:

- trivial typo/import/comment edits
- pure documentation changes
- exploratory spikes where the contract is unknown
- mechanical/generated changes with no behavior contract

After a spike, convert the learned contract into tests before treating the work
as complete.

## Test Naming

Use descriptive names that encode behavior:

```text
test_{unit}_{condition}_{expectedResult}
```

Examples:

- `test_build_failsWhenSchemeNotFound`
- `test_parse_returnsNilForMalformedJSON`
- `test_cache_fetchesNewDataAfterExpiration`

## Arrange Act Assert

Keep structure simple:

```swift
func test_example() {
    // Arrange

    // Act

    // Assert
}
```

Use one blank line between sections. Avoid extra internal structure unless the
test would otherwise be hard to read.

## What To Test

Test:

- public interface behavior
- error paths
- state transitions
- business/domain logic
- serialization and persistence contracts
- concurrency/lifecycle behavior where correctness depends on it

Do not test:

- private implementation details
- framework/language behavior
- trivial getters/setters
- third-party internals

## Unit Vs Integration

Default to unit tests:

- single component
- mocked owned dependencies
- deterministic fixtures
- fast

Use integration tests for:

- critical end-to-end paths
- real filesystem, process, network, database, simulator/device, or external
  contracts
- complex component interactions
- schema or wire compatibility

## Mocks

Mocks should be owned at the protocol/interface boundary.

Rules:

- one mock per protocol/interface
- stateless or resettable between tests
- track received inputs for verification
- allow stubbing returns/errors
- expose a `reset()` method or equivalent
- do not mock what you do not own; wrap third-party APIs first
- do not create one-off test-specific mocks when a shared mock fits

Typical shape:

```text
MockBuildService
├── stubbedResult
├── receivedConfigurations
├── callCount
└── reset()
```

## Fixtures

Fixtures are static, deterministic, minimal, and local to the owning test
surface.

Rules:

- name descriptively: `validUser`, `expiredToken`, `malformedResponse`
- include only fields relevant to the test
- capture real tool/service output into committed fixtures when tests need it
- do not make checked-in tests depend on sibling projects, the user's home
  directory, or external mutable files
- duplicate small fixtures when that keeps targets independent

A live manual run against an external project can inform a fix, but it must not
become a checked-in test dependency.
