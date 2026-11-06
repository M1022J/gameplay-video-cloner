# snapcn

snapcn is a shadcn registry of hand-tuned Remotion components for product videos — launch films, demos, motion graphics. When the user is building or editing a Remotion video:

- **Compose, don't animate.** Find the snapcn component for each beat before writing any `interpolate()`/`spring()` of your own. Use the `snapcn` skill (`skills/snapcn`) or, with a Pro key, the `snapcn_search_components` → `snapcn_component` → `snapcn_plan_video` tools.
- **Install:** `npx shadcn@latest add @snapcn/<name>` — the file lands in `components/snap-cn/` and the user owns it. Only install names that exist (https://snapcn.dev/llms.txt).
- **Dark frames:** components default to the light palette; pass `mode="dark"` on a dark frame or the scene renders black.
- **Check the frame:** render a still (`npx remotion still`, or `snapcn_preview`) before calling a scene done.

Remotion is a prerequisite — snapcn does not create the project (`npx create-video@latest` does).
