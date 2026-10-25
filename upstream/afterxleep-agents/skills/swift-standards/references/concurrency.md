# Swift Concurrency

## Principles

Concurrency is explicit. Shared mutable state must not rely on undocumented
thread-affinity assumptions.

- Isolate shared mutable state with `actor` or `@MainActor`.
- Use locks only for narrow boundaries with clear synchronization invariants.
- A type that starts async work owns cancellation and cleanup.
- Long-lived tasks, stream consumers, timers, and observers need lifecycle
  control.
- Prefer async APIs end to end over callback/DispatchQueue/lock/task-detached
  glue.

## Actor Isolation

Choose isolation deliberately:

- UI-facing state and APIs: `@MainActor`.
- Shared mutable async state: `actor`.
- Immutable values crossing tasks: `Sendable` value types.
- Services with mutable identity: isolate internally or expose actor-isolated
  methods.

Do not use `@MainActor` to paper over unclear ownership. If non-UI work is slow
or blocking, keep it off the main actor and hop back only to publish UI state.

## Sendable

Treat `Sendable` as a correctness contract.

- Prefer value types with sendable stored properties.
- Do not conform reference types casually.
- `@unchecked Sendable` requires a short comment explaining the synchronization
  guarantee.
- Avoid capturing non-sendable mutable state in concurrently-executing closures.
- Audit escaping closures and stored callbacks for actor isolation.

## Cancellation

Cancellation should propagate through long-running workflows:

- process execution
- streaming
- polling
- network requests
- timers
- UI tasks tied to view lifetime

Check cancellation at natural boundaries. Clean up resources when a task is
cancelled. Do not leave orphaned tasks that can mutate state after the owner is
gone.

## Bridging Older APIs

When bridging callbacks:

- prefer `withCheckedContinuation` / `withCheckedThrowingContinuation`
- resume exactly once
- map callback errors into typed domain errors at the boundary
- document any lifetime or cancellation limitation
- avoid `Task.detached` unless isolation and lifetime are explicit

When consuming async sequences, own the task and cancel it in `deinit`,
`onDisappear`, or the owning lifecycle hook.
