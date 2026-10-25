# 01 · Overview

## What this is

Gameplay Video Cloner is an AI-agent skill for **replicating a game directly from its
gameplay video**: feed it a gameplay video, screen recording, GIF, or video URL, and it
produces a playable 1:1 replica (HTML5 Canvas / Phaser / Three.js, etc.).

It is not one-shot prompt generation. It is an engineered pipeline built around a
**Lead Agent + Parallel Subagents Swarm**: first measure the facts from the video
(aspect ratio, palette, HUD layout, scene cuts), then hand physics, skeletal animation,
and HUD/audio to isolated specialist subagents working in parallel, and only deliver
after a two-stage review and an architecture gate.

## Why this repository exists

In the original skill package (zip), the reference docs were summaries only — 24 files of
a few hundred bytes each — while the real substance lived in the 14 open-source
repositories it cites. This repository **downloads all 14 sources and integrates the
cited content** together with the skill itself and the single-file handbook
(`HANDBOOK.md`) into one ready-to-use project. See `SOURCES.md` for provenance.

## Layout

| Part | Location |
|---|---|
| Skill entry point | `SKILL.md` (repo root) |
| 12 executable scripts | `skill/scripts/` |
| 18 reference playbooks | `skill/references/` |
| Single-file handbook (full embedded scripts + all playbooks) | `HANDBOOK.md` |
| The 14 upstream sources, full text | `upstream/` (14 directories) |
| This documentation (Chinese + English) | `docs/zh/`, `docs/en/` |

## Good for

- Cloning/prototyping small-game gameplay (merge puzzles, survivors-likes, platformers, runners, tower defense)
- Reverse-engineering tuning from a recording: speeds, gravity, cooldowns, waves, score curves
- 2D skeletal rigging (Spine/Rive approach) or procedural 3D skeletal animation for existing characters
- A reusable pattern for multi-agent game development: task decomposition, contracts, acceptance gates

## Not in scope

- It does not recover the original game's art assets or code — it replicates gameplay
  and presentation rules; art is drawn/generated procedurally.
- Rules the video never shows are marked **unknown**, never invented. That evidence
  discipline is core to this workflow.
