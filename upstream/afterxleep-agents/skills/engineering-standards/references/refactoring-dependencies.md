# Refactoring And Dependencies

## Refactoring Rules

A refactor preserves observable behavior. If behavior changes, it is not a
refactor; land it separately.

Refactor when:

- it makes the requested change easier
- tests already pin the behavior
- touched code is hard to understand and the improvement is scoped
- the refactor removes meaningful duplication or clarifies ownership

Do not refactor:

- while debugging
- without coverage for the behavior being moved
- unrelated to the current task
- as a bundled "while I'm here" change

## Refactoring Workflow

Before refactoring:

1. Inventory the touched public behavior.
2. Audit coverage for each behavior.
3. Add characterization tests for uncovered behavior.
4. Run the pins green before changing structure.
5. Make one structural change.
6. Run the pins again.
7. Repeat.

If a pin turns red, behavior drifted. Back out or narrow the step.

If pinning is impossible at the current boundary, that is design feedback: the
first refactor should make the boundary testable.

## Dependency Decisions

Before adding a dependency, ask:

1. Can the project solve this clearly in a small amount of code?
2. Is the dependency actively maintained?
3. What is the transitive dependency cost?
4. What is the license?
5. What happens if it disappears or changes ownership?
6. Can it be isolated behind an interface the project owns?

Rules:

- wrap third-party APIs behind project-owned interfaces
- isolate imports to wrapper modules where practical
- pin versions explicitly
- update deliberately, not automatically
- avoid adding dependencies for simple transforms, formatting, parsing, or
  helpers the standard library already handles well

## Abstraction Bar

Add an abstraction only when it:

- improves testability
- decouples a volatile or external boundary
- removes real duplication
- simplifies a complex workflow
- matches an established project pattern

Do not add protocols, managers, factories, or generic layers just to look
architectural. Abstractions must pay rent.
