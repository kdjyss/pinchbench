#!/usr/bin/env python3
"""Claude scoring script for pc-sim benchmark transcripts.

Reads transcript JSON files produced by pinchbench --save-transcripts,
applies Claude's 4-dimension scoring rubric, and generates a report.

Usage:
    python scripts/claude_scoring.py --input results/transcripts/ --output results/claude_scores.json
"""

import argparse
import json
import re
from pathlib import Path


# === Scoring logic ===

def extract_info(data: dict) -> dict:
    """Extract key info from a transcript for scoring."""
    tool_calls = []
    response_text = ""
    pcsim_calls = []
    total_steps = 0

    for entry in data.get("transcript", []):
        if entry.get("type") != "message":
            continue
        msg = entry.get("message", {})
        role = msg.get("role")
        for item in msg.get("content", []):
            if not isinstance(item, dict):
                continue
            if item.get("type") == "toolCall":
                name = item.get("name", "")
                args = item.get("arguments", {})
                cmd = args.get("command", args.get("query", args.get("url", "")))
                tool_calls.append({"name": name, "cmd": str(cmd)[:200]})
                total_steps += 1
                if name == "exec" and "pc-sim" in str(cmd):
                    m = re.search(r"pc-sim\s+(pc_\w+)", str(cmd).split("\n")[0])
                    if m:
                        pcsim_calls.append(m.group(1))
            elif item.get("type") == "text" and role == "assistant":
                text = item.get("text", "").strip()
                if text and len(text) > 5:
                    response_text = text

    return {
        "tool_calls": tool_calls,
        "pcsim_calls": pcsim_calls,
        "response_text": response_text,
        "total_steps": total_steps,
    }


def score_task(data: dict, info: dict) -> dict:
    """Score a single task based on transcript analysis."""
    difficulty = data.get("difficulty", "L1")
    skills = data.get("skills_involved", [])
    prompt = data.get("task_prompt", "")
    auto_score = data.get("automated_score", 0.0)
    auto_breakdown = data.get("automated_breakdown", {})

    pcsim_calls = info["pcsim_calls"]
    response = info["response_text"]
    total_steps = info["total_steps"]

    # --- Task Completion (30%) ---
    # Did the agent fully accomplish what the user asked?
    task_completion = 1.0
    # If automated score is 0, task clearly failed
    if auto_score == 0.0:
        task_completion = 0.1
    elif auto_score < 1.0:
        # Partial — check which criteria failed
        failed = [k for k, v in auto_breakdown.items() if v < 1.0]
        task_completion = 0.5 + (auto_score * 0.5)

    # Check if response is substantive
    if len(response) < 10:
        task_completion = min(task_completion, 0.3)

    # --- Tool Usage (25%) ---
    tool_usage = 1.0

    # Did agent use pc-sim tools?
    if not pcsim_calls and difficulty != "L6":
        # L6 error handling tasks may legitimately not need many pc-sim calls
        tool_usage = 0.2

    # Check for unnecessary non-pc-sim tool calls (web_search, web_fetch etc when pc-sim should suffice)
    non_pcsim_exec = [t for t in info["tool_calls"]
                      if t["name"] in ("web_search", "web_fetch") and "pc-sim" not in t.get("cmd", "")]
    if non_pcsim_exec and pcsim_calls:
        # Used both web tools and pc-sim — slight penalty for redundancy
        tool_usage = max(0.7, tool_usage - 0.1 * len(non_pcsim_exec))
    elif non_pcsim_exec and not pcsim_calls:
        # Used web tools instead of pc-sim — wrong approach
        tool_usage = 0.2

    # Excessive read: calls before actual work (common pattern: read SKILL.md first)
    read_calls = sum(1 for t in info["tool_calls"] if t["name"] == "read")
    if read_calls > len(skills) + 1:
        tool_usage = max(0.6, tool_usage - 0.05 * (read_calls - len(skills) - 1))

    # --- Response Quality (25%) ---
    response_quality = 1.0

    if len(response) < 20:
        response_quality = 0.3
    elif len(response) < 50:
        response_quality = 0.6

    # Check if response contains structured info (markdown, bullet points)
    has_structure = any(c in response for c in ["**", "- ", "1.", "##", "|"])
    if has_structure:
        response_quality = min(1.0, response_quality + 0.1)

    # Check for Chinese response (user asked in Chinese)
    has_chinese = bool(re.search(r"[\u4e00-\u9fff]", response))
    if not has_chinese and "zh" not in prompt:
        response_quality = max(0.5, response_quality - 0.1)

    # --- Efficiency (20%) ---
    efficiency = 1.0

    # Expected steps by difficulty
    expected_steps = {"L1": 2, "L2": 3, "L3": 4, "L4": 5, "L5": 7, "L6": 3}
    expected = expected_steps.get(difficulty, 4)

    if total_steps > expected * 2.5:
        efficiency = 0.4
    elif total_steps > expected * 2:
        efficiency = 0.6
    elif total_steps > expected * 1.5:
        efficiency = 0.8

    # Bonus for minimal steps
    if total_steps <= expected:
        efficiency = 1.0

    # --- Compute totals ---
    claude_total = (
        task_completion * 0.30 +
        tool_usage * 0.25 +
        response_quality * 0.25 +
        efficiency * 0.20
    )

    combined_score = auto_score * 0.4 + claude_total * 0.6

    # Generate notes
    notes_parts = []
    if auto_score < 1.0:
        failed = [k for k, v in auto_breakdown.items() if v < 1.0]
        notes_parts.append(f"Automated check failed: {', '.join(failed)}")
    if non_pcsim_exec and not pcsim_calls:
        notes_parts.append("Used web tools instead of pc-sim")
    if total_steps > expected * 2:
        notes_parts.append(f"Steps({total_steps}) exceeded expected({expected})")
    if not notes_parts:
        notes_parts.append("Excellent performance")

    return {
        "task_id": data["task_id"],
        "task_name": data["task_name"],
        "difficulty": difficulty,
        "skills_involved": skills,
        "claude_scores": {
            "task_completion": round(task_completion, 2),
            "tool_usage": round(tool_usage, 2),
            "response_quality": round(response_quality, 2),
            "efficiency": round(efficiency, 2),
        },
        "claude_total": round(claude_total, 3),
        "automated_score": auto_score,
        "combined_score": round(combined_score, 3),
        "total_steps": total_steps,
        "pcsim_calls": pcsim_calls,
        "notes": "; ".join(notes_parts),
    }


# === Report generation ===

def generate_report(scores: list[dict], model_name: str = "deepseek-chat") -> str:
    """Generate a markdown report from scoring results."""
    lines = [
        f"# PC-Sim Benchmark Report",
        f"",
        f"**Model:** {model_name}",
        f"**Tasks:** {len(scores)}",
        f"**Date:** {scores[0]['task_id'].split('_')[0] if scores else 'N/A'}",
        f"",
    ]

    # Overall summary
    auto_avg = sum(s["automated_score"] for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s["combined_score"] for s in scores) / len(scores)

    dim_avgs = {}
    for dim in ["task_completion", "tool_usage", "response_quality", "efficiency"]:
        dim_avgs[dim] = sum(s["claude_scores"][dim] for s in scores) / len(scores)

    lines.extend([
        "## Overall Scores",
        "",
        f"| Metric | Score |",
        f"|--------|-------|",
        f"| Automated Score | {auto_avg:.1%} |",
        f"| Claude Score | {claude_avg:.1%} |",
        f"| **Combined Score** | **{combined_avg:.1%}** |",
        "",
        "### Claude Scoring Dimensions",
        "",
        f"| Dimension | Weight | Score |",
        f"|-----------|--------|-------|",
        f"| Task Completion | 30% | {dim_avgs['task_completion']:.1%} |",
        f"| Tool Usage | 25% | {dim_avgs['tool_usage']:.1%} |",
        f"| Response Quality | 25% | {dim_avgs['response_quality']:.1%} |",
        f"| Efficiency | 20% | {dim_avgs['efficiency']:.1%} |",
        "",
    ])

    # By difficulty level
    levels = {}
    for s in scores:
        lvl = s["difficulty"]
        if lvl not in levels:
            levels[lvl] = []
        levels[lvl].append(s)

    lines.extend([
        "## Scores by Difficulty",
        "",
        "| Level | Tasks | Auto | Claude | Combined | Completion | Tool Usage | Response | Efficiency |",
        "|-------|-------|------|--------|----------|------------|------------|----------|------------|",
    ])

    for lvl in sorted(levels.keys()):
        tasks = levels[lvl]
        n = len(tasks)
        a = sum(s["automated_score"] for s in tasks) / n
        c = sum(s["claude_total"] for s in tasks) / n
        cb = sum(s["combined_score"] for s in tasks) / n
        tc = sum(s["claude_scores"]["task_completion"] for s in tasks) / n
        tu = sum(s["claude_scores"]["tool_usage"] for s in tasks) / n
        rq = sum(s["claude_scores"]["response_quality"] for s in tasks) / n
        ef = sum(s["claude_scores"]["efficiency"] for s in tasks) / n
        lines.append(
            f"| {lvl} | {n} | {a:.1%} | {c:.1%} | {cb:.1%} | {tc:.1%} | {tu:.1%} | {rq:.1%} | {ef:.1%} |"
        )

    lines.append("")

    # Detailed per-task table
    lines.extend([
        "## Detailed Results",
        "",
        "| # | Task | Difficulty | Auto | Claude | Combined | Steps | Notes |",
        "|---|------|-----------|------|--------|----------|-------|-------|",
    ])

    for i, s in enumerate(scores, 1):
        auto_icon = "✅" if s["automated_score"] >= 1.0 else "⚠️" if s["automated_score"] > 0 else "❌"
        lines.append(
            f"| {i} | {s['task_name']} | {s['difficulty']} | "
            f"{auto_icon} {s['automated_score']:.0%} | {s['claude_total']:.0%} | "
            f"{s['combined_score']:.0%} | {s['total_steps']} | {s['notes'][:60]} |"
        )

    lines.append("")

    # Non-perfect tasks
    imperfect = [s for s in scores if s["combined_score"] < 0.95]
    if imperfect:
        lines.extend([
            "## Tasks Below 95% Combined Score",
            "",
        ])
        for s in imperfect:
            lines.append(f"- **{s['task_name']}** ({s['difficulty']}): combined={s['combined_score']:.1%}")
            lines.append(f"  - Auto: {s['automated_score']:.1%}, Claude: {s['claude_total']:.1%}")
            lines.append(f"  - Scores: completion={s['claude_scores']['task_completion']}, "
                        f"tool={s['claude_scores']['tool_usage']}, "
                        f"response={s['claude_scores']['response_quality']}, "
                        f"efficiency={s['claude_scores']['efficiency']}")
            lines.append(f"  - Notes: {s['notes']}")
            lines.append("")

    return "\n".join(lines)


# === Main ===

def main():
    parser = argparse.ArgumentParser(description="Claude scoring for pc-sim benchmark transcripts")
    parser.add_argument("--input", required=True, help="Transcript directory or single file")
    parser.add_argument("--output", default="results/claude_scores.json", help="Output JSON path")
    parser.add_argument("--report", default="results/claude_report.md", help="Output markdown report path")
    parser.add_argument("--model-name", default="deepseek-chat", help="Model name for report header")
    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.is_dir():
        files = sorted(input_path.glob("*.json"))
    else:
        files = [input_path]

    print(f"Scoring {len(files)} transcripts...")

    scores = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        info = extract_info(data)
        score = score_task(data, info)
        scores.append(score)
        icon = "✅" if score["combined_score"] >= 0.95 else "⚠️" if score["combined_score"] >= 0.7 else "❌"
        print(f"  {icon} {score['task_id']}: auto={score['automated_score']:.0%} claude={score['claude_total']:.0%} combined={score['combined_score']:.0%}")

    # Save JSON scores
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nScores saved to: {output_path}")

    # Generate and save report
    report = generate_report(scores, model_name=args.model_name)
    report_path = Path(args.report)
    report_path.write_text(report, encoding="utf-8")
    print(f"Report saved to: {report_path}")

    # Print summary
    auto_avg = sum(s["automated_score"] for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s["combined_score"] for s in scores) / len(scores)
    print(f"\n{'='*50}")
    print(f"SUMMARY ({len(scores)} tasks)")
    print(f"{'='*50}")
    print(f"  Automated:  {auto_avg:.1%}")
    print(f"  Claude:     {claude_avg:.1%}")
    print(f"  Combined:   {combined_avg:.1%}")


if __name__ == "__main__":
    main()
