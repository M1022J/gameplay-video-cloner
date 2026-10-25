# SwiftUI And UI

## SwiftUI State

- UI-facing observable state belongs on the main actor.
- Keep `body` cheap and declarative.
- Move business logic out of views.
- Prefer small view structs with explicit inputs.
- Use stable identity in lists and collections.
- Do not perform IO, parsing, process execution, or expensive computation from
  `body`.

State ownership should be obvious:

- local ephemeral UI state stays local
- model/domain state belongs in a view model or service boundary
- async work started by a view should be cancelled when the view disappears or
  the task identity changes

## Continuous Animation Performance

Continuous animations must not drive SwiftUI view invalidation.

Use Core Animation-backed representables for permanent/repeating effects:

- loading spinners
- indeterminate progress sweeps
- pulsing dots/status rings
- shimmer
- repeating decorative motion

Avoid for indefinite effects:

- `TimelineView(.animation)`
- `withAnimation(...repeatForever...)`
- state-driven `rotationEffect`
- timers or async loops that update SwiftUI state every frame

SwiftUI animation is appropriate for finite state transitions: opening/closing
panels, selection changes, hover feedback, short fades, and one-shot
affordances.

Layer-backed components should preserve layout explicitly: stable SwiftUI
frames, drawing contained in the representable, layer updates without implicit
layout animation on geometry changes, and semantic inputs only.

## Typography

Prefer named text styles:

- `.body`
- `.headline`
- `.subheadline`
- `.caption`
- `.title`, `.title2`, `.title3`
- `.largeTitle`

Use weights on named styles when needed:

```swift
Text("Title").font(.headline.weight(.bold))
```

Reach for fixed `.system(size:)` only when the element is not really text or
when a design has a deliberate non-scaling reason, such as calibrated icon
badges or graphic dimensions.

## Strings And Localization

Centralize repeated, user-facing, or contract-significant strings. The exact
mechanism is project-specific, but the goal is stable review and search:

- user-facing copy should be localizable
- prompt templates should not be scattered across call sites
- URLs and deep links should be auditable
- log prefixes and error fragments should be consistent
- wire vocabulary should be typed

Avoid concatenating localizable sentence fragments. Prefer complete strings with
format specifiers or interpolation points that preserve grammar.

## Accessibility

New user-facing UI should account for:

- meaningful labels
- traits/actions for custom controls
- Dynamic Type
- contrast
- reduced motion
- keyboard navigation where applicable

If a visual affordance is available by swipe, hover, or icon-only control, expose
an equivalent accessible action or label.
