#!/usr/bin/env python3
"""Lead-Agent to Parallel-Subagents Mission Orchestrator (obra/superpowers & sickn33/subagent-orchestrator)."""
import argparse, json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default="./subagent_workspace")
    parser.add_argument("--game-title", default="Replicated Game")
    args = parser.parse_args()
    proj = Path(args.project_dir)
    proj.mkdir(parents=True, exist_ok=True)
    (proj / "mission_brief.json").write_text(json.dumps({"goal": args.game_title, "rounds": 3, "subagents": 5}, indent=2), encoding="utf-8")
    (proj / "sdd_ledger.md").write_text(f"# SDD Ledger - {args.game_title}\n", encoding="utf-8")

if __name__ == "__main__":
    main()
