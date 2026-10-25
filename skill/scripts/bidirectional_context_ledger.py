#!/usr/bin/env python3
"""
bidirectional_context_ledger.py
Bidirectional Temporal Context Graph & Longitudinal Economy Curve Fitter ("上下结合判断" 核心引擎)
Sources:
- HKUDS/VideoRAG & HKUDS/VideoAgent (Dual-channel Temporal Knowledge Graph & Cross-Timestamp Entity Linking)
- ttengwang/awesome_long_form_video_understanding (MovieChat Short-Term Sliding Window + Long-Term Consolidation Memory, VideoTree, MM-Narrator)

How this enables "上下结合判断" (Combining Upstream & Downstream Context Across 10,000+ Frames):
1. Forward Pass (上文推下文 - Rolling State Accumulation):
   - As each chunk (chunk_001 .. chunk_N) is analyzed, `append-chunk` logs observed Game States, Entities/Items,
     Causal Transitions (e.g. "Picked up Fire Tome at 02:14"), Numeric Samples (e.g. Level/Wave/Cost/HP at timestamp t),
     and Pending Hypotheses ("Unknown purple bar under avatar at 03:10 - what triggers it?").
2. Backward Pass (下文反推上文 - Retrospective Hypothesis Resolution & Causal Backfill):
   - When a later chunk (e.g. chunk_018 at 24:50) reveals the effect or trigger (e.g. "Purple bar reaches 100% and triggers Demon Form"),
     `resolve-hypothesis` or `reconcile` automatically backfills the earlier chunk's state node and creates a verified
     Bidirectional Causal Edge: `[t_cause: 03:10 (Soul Orb Pickup)] ---> [t_effect: 24:50 (Demon Transformation)]`.
3. Multi-Timestamp Longitudinal Curve Fitting:
   - Automatically collects numerical observations logged across the entire 30–60 minute video (e.g. upgrade costs at Lv.1, Lv.5, Lv.12, Lv.30)
     and fits Linear (`y = a*x + b`) vs. Exponential (`y = a * r^x`) formulas with R^2 goodness-of-fit so the cloned game uses the exact late-game math!
"""
import os
import sys
import json
import math
import argparse
import numpy as np


def init_ledger(ledger_path: str, game_title: str = "Long Video Game Replica"):
    os.makedirs(os.path.dirname(os.path.abspath(ledger_path)), exist_ok=True)
    data = {
        "game_title": game_title,
        "chunks_analyzed": [],
        "finite_state_machine_nodes": {},
        "state_transitions": [],
        "causal_links_bidirectional": [],
        "unresolved_hypotheses": [],
        "resolved_hypotheses": [],
        "numeric_time_series": {},
        "fitted_progression_formulas": {},
    }
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[bidirectional_context_ledger] Initialized rolling ledger at {ledger_path}")
    return data


def fit_curve_from_samples(samples: list):
    """Fits both Linear (y = m*x + c) and Exponential (y = a * r^x) models to longitudinal (x, y) data points."""
    if len(samples) < 2:
        return {"model": "constant", "formula_js": f"{samples[0]['y'] if samples else 1}", "r2": 1.0}

    xs = np.array([float(s["x"]) for s in samples], dtype=np.float64)
    ys = np.array([float(s["y"]) for s in samples], dtype=np.float64)

    # Linear fit: y = m*x + c
    m, c = np.polyfit(xs, ys, 1)
    y_pred_lin = m * xs + c
    ss_tot = float(np.sum((ys - np.mean(ys)) ** 2)) or 1.0
    r2_lin = 1.0 - float(np.sum((ys - y_pred_lin) ** 2)) / ss_tot

    # Exponential fit (if all ys > 0): ln(y) = ln(a) + x * ln(r)
    if np.all(ys > 0) and (np.max(xs) > np.min(xs)):
        slope, intercept = np.polyfit(xs, np.log(ys), 1)
        a = math.exp(intercept)
        r = math.exp(slope)
        y_pred_exp = a * (r ** xs)
        r2_exp = 1.0 - float(np.sum((ys - y_pred_exp) ** 2)) / ss_tot
        if r2_exp > r2_lin + 0.02:
            return {
                "model": "exponential",
                "base_a": round(a, 4),
                "growth_rate_r": round(r, 4),
                "formula_js": f"Math.round({a:.2f} * Math.pow({r:.4f}, x))",
                "r2": round(r2_exp, 4),
                "sample_count": len(samples),
            }

    return {
        "model": "linear",
        "slope_m": round(float(m), 4),
        "intercept_c": round(float(c), 4),
        "formula_js": f"Math.round({m:.2f} * x + {c:.2f})",
        "r2": round(r2_lin, 4),
        "sample_count": len(samples),
    }


def append_chunk_observation(ledger_path: str, obs_json_path: str):
    """
    Merges observations from a newly inspected chunk into the rolling ledger, linking upstream context
    and resolving any prior hypotheses matched by new downstream evidence.
    """
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)
    with open(obs_json_path, "r", encoding="utf-8") as f:
        obs = json.load(f)

    chunk_id = obs.get("chunk_id", f"chunk_{len(ledger['chunks_analyzed'])+1:03d}")
    if chunk_id not in ledger["chunks_analyzed"]:
        ledger["chunks_analyzed"].append(chunk_id)

    # 1. Merge discovered FSM states
    for st in obs.get("states_observed", []):
        name = st["state_name"]
        if name not in ledger["finite_state_machine_nodes"]:
            ledger["finite_state_machine_nodes"][name] = {
                "first_seen_chunk": chunk_id,
                "first_seen_sec": st.get("timestamp_sec", 0.0),
                "occurrences": 1,
                "description": st.get("description", ""),
            }
        else:
            ledger["finite_state_machine_nodes"][name]["occurrences"] += 1

    # 2. Record state transitions
    for tr in obs.get("transitions", []):
        ledger["state_transitions"].append({
            "chunk_id": chunk_id,
            "timestamp_sec": tr.get("timestamp_sec", 0.0),
            "from_state": tr["from_state"],
            "to_state": tr["to_state"],
            "trigger": tr.get("trigger", ""),
        })

    # 3. Record new upstream->downstream causal links
    for cl in obs.get("causal_links", []):
        ledger["causal_links_bidirectional"].append({
            "cause_chunk": cl.get("cause_chunk", chunk_id),
            "cause_timestamp_sec": cl.get("cause_timestamp_sec", 0.0),
            "cause_event": cl["cause_event"],
            "effect_chunk": chunk_id,
            "effect_timestamp_sec": cl.get("effect_timestamp_sec", 0.0),
            "effect_event": cl["effect_event"],
            "verified_mechanism": cl.get("verified_mechanism", ""),
        })

    # 4. Add new unresolved hypotheses from this chunk
    for hyp in obs.get("new_hypotheses", []):
        ledger["unresolved_hypotheses"].append({
            "hypothesis_id": hyp.get("id", f"H{len(ledger['unresolved_hypotheses'])+1:03d}"),
            "origin_chunk": chunk_id,
            "origin_timestamp_sec": hyp.get("timestamp_sec", 0.0),
            "question": hyp["question"],
            "visual_clue": hyp.get("visual_clue", ""),
        })

    # 5. Backward Pass ("下文反推上文"): Resolve earlier upstream hypotheses using downstream evidence in this chunk
    for res in obs.get("resolved_hypotheses", []):
        hid = res.get("hypothesis_id")
        remaining = []
        for h in ledger["unresolved_hypotheses"]:
            if h["hypothesis_id"] == hid or h["question"] == res.get("question"):
                h["resolved_in_chunk"] = chunk_id
                h["resolved_at_sec"] = res.get("timestamp_sec", 0.0)
                h["downstream_proof"] = res["downstream_proof"]
                h["inferred_game_rule"] = res["inferred_game_rule"]
                ledger["resolved_hypotheses"].append(h)
                # Also promote to a verified bidirectional causal link
                ledger["causal_links_bidirectional"].append({
                    "cause_chunk": h["origin_chunk"],
                    "cause_timestamp_sec": h["origin_timestamp_sec"],
                    "cause_event": h["visual_clue"],
                    "effect_chunk": chunk_id,
                    "effect_timestamp_sec": res.get("timestamp_sec", 0.0),
                    "effect_event": res["downstream_proof"],
                    "verified_mechanism": res["inferred_game_rule"],
                })
            else:
                remaining.append(h)
        ledger["unresolved_hypotheses"] = remaining

    # 6. Append longitudinal numerical samples (e.g. upgrade_cost, enemy_hp, xp_required across levels/waves)
    for series_name, points in obs.get("numeric_samples", {}).items():
        if series_name not in ledger["numeric_time_series"]:
            ledger["numeric_time_series"][series_name] = []
        for pt in points:
            ledger["numeric_time_series"][series_name].append({
                "chunk_id": chunk_id,
                "timestamp_sec": pt.get("timestamp_sec", 0.0),
                "x": pt["x"],
                "y": pt["y"],
            })
        ledger["fitted_progression_formulas"][series_name] = fit_curve_from_samples(ledger["numeric_time_series"][series_name])

    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

    print(
        f"[bidirectional_context_ledger] Updated {chunk_id}: "
        f"{len(ledger['finite_state_machine_nodes'])} FSM states, "
        f"{len(ledger['causal_links_bidirectional'])} bidirectional causal links, "
        f"{len(ledger['resolved_hypotheses'])} resolved upstream/downstream hypotheses."
    )
    return ledger


def export_context_brief(ledger_path: str, out_md_path: str):
    """Exports a compact Context Brief to feed into the next chunk's analysis prompt or final GDD synthesis."""
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    lines = [
        f"# Bidirectional Rolling Context Brief — {ledger['game_title']}",
        f"- **Chunks Analyzed So Far**: `{len(ledger['chunks_analyzed'])}` (`{', '.join(ledger['chunks_analyzed'][-5:])}`)",
        "",
        "## 1. Discovered Finite State Machine (FSM) Nodes",
    ]
    for name, info in ledger["finite_state_machine_nodes"].items():
        lines.append(f"- **`{name}`** (first seen `{info['first_seen_chunk']}` @ `{info['first_seen_sec']}s`, count={info['occurrences']}): {info['description']}")

    lines.append("\n## 2. Verified Bidirectional Causal Rules (上文因 <-> 下文果)")
    for cl in ledger["causal_links_bidirectional"]:
        lines.append(
            f"- `[{cl['cause_chunk']} @ {cl['cause_timestamp_sec']}s]` **{cl['cause_event']}** "
            f"<==> `[{cl['effect_chunk']} @ {cl['effect_timestamp_sec']}s]` **{cl['effect_event']}** "
            f"-> **Rule**: `{cl['verified_mechanism']}`"
        )

    lines.append("\n## 3. Longitudinal Fitted Economy & Progression Curves")
    for sname, fit in ledger["fitted_progression_formulas"].items():
        lines.append(f"- **`{sname}`** (`{fit['model']}`, $R^2={fit['r2']}$, n={fit.get('sample_count', 1)}): `{fit['formula_js']}`")

    lines.append("\n## 4. Pending Upstream Hypotheses (Watch for Downstream Answers in Next Chunks!)")
    for h in ledger["unresolved_hypotheses"]:
        lines.append(f"- **`{h['hypothesis_id']}`** (`{h['origin_chunk']} @ {h['origin_timestamp_sec']}s`): {h['question']} (Clue: {h['visual_clue']})")

    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[bidirectional_context_ledger] Exported rolling context brief to {out_md_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bidirectional temporal context ledger for multi-chunk long gameplay videos.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("ledger_path")
    p_init.add_argument("--title", default="Long Gameplay Replica")

    p_app = sub.add_parser("append-chunk")
    p_app.add_argument("ledger_path")
    p_app.add_argument("obs_json_path")

    p_exp = sub.add_parser("export-brief")
    p_exp.add_argument("ledger_path")
    p_exp.add_argument("out_md_path")

    args = parser.parse_args()
    if args.cmd == "init":
        init_ledger(args.ledger_path, args.title)
    elif args.cmd == "append-chunk":
        append_chunk_observation(args.ledger_path, args.obs_json_path)
    elif args.cmd == "export-brief":
        export_context_brief(args.ledger_path, args.out_md_path)
