#!/usr/bin/env python3
"""Swarm DAG Task Board & Teammate Inbox Coordinator (kieranklaassen/orchestrating-swarms)."""
import argparse, json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board", default="./subagent_workspace/swarm_board.json")
    parser.add_argument("action", choices=["init", "complete", "status"])
    args = parser.parse_args()
    bpath = Path(args.board)
    bpath.parent.mkdir(parents=True, exist_ok=True)
    if args.action == "init":
        bpath.write_text(json.dumps({"team_name": "gameplay-cloner-swarm", "tasks": []}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
