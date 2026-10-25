# Errors, State, Persistence, And Wire Models

## Error Handling

Error handling is API design.

- Each domain boundary exposes typed errors that name the failed operation.
- Include enough context to diagnose: path, identifier, command, invalid value,
  current state, environment, or response status.
- Translate `Foundation`, decoding, filesystem, process, and network errors at
  module boundaries unless the boundary is intentionally low-level.
- Prefer `throws` for operational failures.
- Use `Result` only when failure must be carried as ordinary data.
- Do not use `Optional` to hide failure when "missing" and "failed" differ.
- Use `try?` sparingly, only when failure is intentionally non-fatal and
  discarded.
- Validate files, command availability, input shape, and preconditions before
  expensive work.

Typed errors should let callers distinguish cases programmatically.

## State

State should be explicit, typed, and owned by the narrowest reasonable boundary.

- Avoid loose dictionaries for meaningful domain state.
- Prefer value snapshots for read-only views of mutable systems.
- Keep mutation APIs intentional.
- Make illegal states unrepresentable where practical.
- Keep transient UI state separate from durable product/domain state.

## Persistence

Persisted state is a first-class design concern.

- Stored models are typed.
- Stored formats are version-aware and migration-safe.
- Defaults are conservative and owned by the persistence layer.
- Normalization belongs close to storage: canonical paths, legacy migration,
  schema fallback, default decoding.
- Writes are atomic when correctness matters.
- Locking, migration, and recovery should be centralized and tested directly.

Persist durable state, not values that are trivially recomputed.

## Serialization And Wire Models

Stable wire or persistence shapes need compatibility discipline:

- Add fields additively where possible.
- Prefer optional additions with `decodeIfPresent` when older producers/consumers
  exist.
- Renames and type changes are breaking.
- Keep round-trip tests for stable formats.
- Separate serializable shape from behavior helpers when multiple products or
  modules consume the same contract.
- Avoid raw string comparisons for shared vocabulary; use typed raw-value enums.

Behavior helpers belong at the owning product/module boundary, not inside a
contract-only shape when that shape is shared broadly.
