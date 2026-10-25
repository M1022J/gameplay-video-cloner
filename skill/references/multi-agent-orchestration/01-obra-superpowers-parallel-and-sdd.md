# Parallel Subagent Dispatch & Subagent-Driven Development (`obra/superpowers`)

- **Isolated Context Briefs**: Give each subagent only its scoped task brief (`Files to read`, `Files to write`, `Required Contract Exports`) so session context stays clean.
- **Two-Stage Review Gate**: Run Spec Compliance + Code Quality verification after every subagent completes its module, and log rulings in `sdd_ledger.md`.
