# Swift Design And API

## Philosophy

Write Swift for the next maintainer. Favor directness over cleverness, explicit
control flow over abstraction for its own sake, and small composable units over
large multipurpose types.

State, ownership, failure, and side effects should be obvious from the call
site. The default style is explicit and boring: typed values, visible
dependencies, errors that name failed operations, and deliberately isolated
concurrency.

## Type Choice

- `struct`: values, configuration, request/response payloads, snapshots,
  persisted state, parsed results.
- `enum`: finite state, modes, options, domain errors, typed identifiers.
- `final class`: long-lived services, lifecycle coordinators, mutable identity,
  or external resource ownership.
- `actor`: shared mutable async state.
- `@MainActor`: UI-facing state and APIs that must run on the main actor.

Use one primary type per file. Keep small local extensions when they aid
readability. If a file contains unrelated helpers that could be deleted
independently, it is too broad.

## Naming

- Types are nouns.
- Protocols describe capability.
- Functions describe behavior.
- Names should let a reader infer ownership and side effects without opening
  the implementation.

Prefer literal names over clever abbreviations.

## API Design

Make misuse hard.

- Prefer parameter labels that read like a sentence.
- Use domain types over primitive combinations.
- Use a typed input/configuration object for related inputs.
- Avoid boolean behavior parameters; use enums, options, or separate methods.
- Keep side-effect boundaries explicit.
- Split validation, IO, rendering, persistence, and pure transformation.
- Model outcomes directly with typed result objects.
- Use `Void` only when success has no useful outcome beyond completion.

Entrypoints stay thin: parse inputs, validate, resolve dependencies, delegate
to domain logic, render output.

## Dependency Boundaries

Use protocols at edges, not everywhere. Good protocol boundaries include:

- storage
- process execution
- network clients
- backend adapters
- external tool wrappers
- third-party APIs
- clocks/timers/randomness when deterministic tests need substitution

Constructor injection is the default for long-lived services. Convenience
defaults are fine for leaf production types, but core workflows should not rely
on hidden singletons or implicit globals.

Abstractions must pay rent. Do not add a protocol, generic, wrapper, factory, or
manager unless it improves testability, decoupling, or clarity.
