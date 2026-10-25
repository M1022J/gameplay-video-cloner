# 06 · Upstream Sources & Integration Notes

## Integration principles
1. **Include what is cited**: everything the skill actually references is included in
   full. Giant general-purpose monorepos (thousands of unrelated skills) contribute only
   the one cited skill, with the origin repo and pinned commit recorded in `SOURCES.md`
   so anything else can be fetched upstream at that commit.
2. **No rewriting**: integration only strips `.git`; no upstream file is modified, and
   every directory keeps its original LICENSE.
3. **Traceability**: `SOURCES.md` records all 14 sources — URL, commit SHA, included
   scope, and exceptions.

## The 14 sources at a glance
- Multi-agent orchestration (5): obra/superpowers, kieranklaassen (Gist),
  sickn33/antigravity-awesome-skills, qodex-ai/ai-agent-skills,
  VoltAgent/awesome-claude-code-subagents
- 2D/3D skeletal animation (4): GenielabsOpenSource/spine-animation-ai,
  BowTiedSwan/rive-skills, composio-community/opencode-skills, arjun988/blender-skills
- Video / art / engine studios (5): ybuild-ai/ai-game-art-pipeline-skill, video-db/skills,
  PlayableIntelligence/game-creator, gamedev-skills/awesome-gamedev-agent-skills,
  Donchitos/Claude-Code-Game-Studios

## Two handbook errata (verified)
- `kieranklaassen/orchestrating-swarms` is not a GitHub repository; it is the author's
  Gist ("Claude Code Swarm Orchestration Skill"), included from the Gist at
  `upstream/orchestrating-swarms/`.
- `qodex-ai/multi-agent-orchestration` does not exist as a repo; the correct repo is
  `qodex-ai/ai-agent-skills`, and its same-named skill directory is the cited content.

## Known exceptions
- PlayableIntelligence/game-creator's `assets/` (140MB) and `examples/` (70MB) are not
  included (not cited by this skill); its `skills/playdotfun` and `skills/unity-mcp`
  were symlinks into uninitialized submodules and were skipped as well.
- 16 binary media files (demo GIFs/MP4, illustrative images) are not part of the GitHub
  upload (the snapshot channel accepts UTF-8 text only); see `docs/BINARY_FILES.md`.
  They are present in the local integrated copy.

## Licensing
Each upstream keeps its own license (spine-animation-ai: PolyForm Noncommercial 1.0.0;
most others MIT / Apache-2.0 — the LICENSE file in each directory governs). This
integration does not change any upstream terms.
