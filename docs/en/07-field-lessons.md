# 07 · Field Lessons: Hard Rules From a Real Replication (2026-10-25)

Distilled from one complete real-world run of this skill （末日生存房车， delivered on
TapTap Maker / Lua). Full version: `skill/references/field-lessons-maker-replication.md`.

## The seven rules

1. **Frame-by-frame event table.** Round 1 is more than 16 keyframes. Every rule goes
   into an event table (event ID / timestamp / input / before→after state / evidence /
   confidence grade: observed, re-verified, inferred, unknown). Numbers come only from
   OCR or pixel measurement — an agent once read the currency 1300 as 300 three times.
2. **Complete UI inventory.** Every UI element in the video is cropped, specced and given
   a recorded disposition (generated asset / programmatic draw with reason). The
   inventory must be empty before Round 3.
3. **Dual-layer QA gate.** Before any build, a headless harness loads the REAL scripts
   (engine APIs stubbed) and drives every screen plus the full main flow by state:
   numeric assertions AND UI hit-tests. A green remote build proves compilation only.
4. **DPR variants in tests.** Run the harness at DPR=1 and DPR=3. Engine input
   coordinates are physical pixels; forgetting `input / dpr` shipped a build whose
   buttons were all dead on real phones while desktop tests passed.
5. **Measure, don't trust canvases.** Character/vehicle/wheel proportions are measured
   on rendered composites; nominal sprite/rig canvas sizes lie (transparent padding).
6. **Never copy the original publisher's identity.** Company names, registration
   numbers and copyright lines from the original's title screen stay out of the replica.
7. **Report with evidence.** Progress proactively; conclusions only from seen frames,
   logs or reproducible functional checks.

## Non-HTML targets

For engines other than the browser (Maker/Lua, Unity, …), keep the 3-round swarm,
packets and ledgers; replace the Round-3 HTML merge with Lead hand-integration against
the module contracts, log every cross-module fix in the SDD ledger, and use the
dual-layer harness as the QA gate (note the substitution for
`validate_architecture.py` in the ledger).
