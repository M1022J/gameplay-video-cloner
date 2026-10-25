# Code Quality

## Organization

- One primary type per file.
- Filename matches the primary type.
- Group by feature/domain, not by broad technical buckets like `Models`,
  `Helpers`, `Managers`, or `Utils`.
- Shared utilities belong in a neutral shared layer with no domain dependencies.
- Features should be deletable without breaking unrelated code.
- No circular dependencies.

Preferred dependency direction:

```text
Features -> Services -> Core
```

Cross-product wire contracts belong in a contract-only module both sides depend
on. Contract modules contain serializable shapes and stable identifiers only:
no IO, process spawning, UI imports, business logic, or side-effect helpers.

## Naming

- Types/classes: `UpperCamelCase`.
- Functions/variables: `lowerCamelCase`.
- Constants: follow the language convention.
- Protocols/interfaces: `UpperCamelCase`, named as a noun or capability.

Names should describe what the thing represents or does, not how it is
implemented.

## Functions And APIs

- Functions do one thing.
- Keep parameters to roughly 3-4; use a configuration/input object for related
  data.
- Avoid boolean behavior parameters; use enums, options, or separate methods
  when behavior differs.
- Make misuse hard with explicit labels and domain types.
- Keep entrypoints thin: parse, validate, resolve dependencies, delegate, render.
- Split pure transformations from IO, persistence, process execution, network,
  and UI concerns.
- Return typed outcomes when useful; use void only when success carries no data.

## Comments

Default to no comments. A desired comment often means a name is unclear, a
function is too large, or an abstraction is missing.

Use comments only for why:

- hidden constraints
- workarounds
- subtle invariants
- surprising behavior
- public API contracts or pitfalls

Rules:

- one line preferred, two is the ceiling
- no preambles
- no restating what the code says
- no change history, ticket bookkeeping, or PR references
- TODO format: `// TODO: [reason / blocker] description`

Self-check: if deleting the comment would not confuse the next maintainer, do
not write it.

## Error Handling

Errors are API design.

- Define domain-specific error types at module boundaries.
- Include useful context: operation, path, ID, input value, command, current
  state, or environment when relevant.
- Translate external errors at boundaries so callers do not depend on
  implementation details.
- Let callers distinguish cases programmatically.
- Distinguish transient from permanent failures when behavior differs.
- Fail at the source; do not pass invalid state downstream hoping someone else
  handles it.
- Use optional/nullable values only for true absence, not hidden failure.

An actionable error should answer:

- what failed?
- with which relevant inputs?
- what boundary failed?
- can the caller retry, recover, or correct input?
