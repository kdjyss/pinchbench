#!/usr/bin/env python3
"""Convert pc_environment_monitor YAML task presets to pinchbench markdown format.

Usage:
    python scripts/convert_pcsim_tasks.py \
        --source /root/codes/pc_environment_monitor/eval/task_presets/ \
        --output tasks_pcsim/ \
        --start-number 23
"""

import argparse
import re
import textwrap
from pathlib import Path

import yaml


# === Constants ===

CATEGORY_MAP = {
    "L1": "pcsim_query",
    "L2": "pcsim_action",
    "L3": "pcsim_multi_step",
    "L4": "pcsim_cross_skill",
    "L5": "pcsim_workflow",
    "L6": "pcsim_error_handling",
}

TIMEOUT_MAP = {
    "L1": 60,
    "L2": 90,
    "L3": 120,
    "L4": 120,
    "L5": 180,
    "L6": 90,
}

PRE_EXEC_CMD = "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"

# event_fired events mapped to corresponding tool names.
# All 7 event_fired criteria in the 52 tasks are redundant with existing
# tool_called criteria in the same task, so they are skipped during conversion.
EVENT_TO_TOOL = {
    "contacts.created": "pc_contacts_create",
    "alarm.created": "pc_alarm_create",
    "memo.created": "pc_memo_create",
    "email.sent": "pc_email_send",
    "recorder.started": "pc_recorder_start",
    "recorder.stopped": "pc_recorder_stop",
}


# === Grade function template (Part 1 — shared across all tasks) ===

GRADE_PREAMBLE = '''\
def grade(transcript: list, workspace_path: str) -> dict:
    import re

    scores = {}

    # Extract tool calls and response text from transcript
    tool_calls = []
    response_text = ""
    for entry in transcript:
        if entry.get("type") != "message":
            continue
        msg = entry.get("message", {})
        if msg.get("role") == "assistant":
            for item in msg.get("content", []):
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "toolCall" and item.get("name") == "exec":
                    cmd = item.get("arguments", {}).get("command", "")
                    first_line = cmd.split("\\n")[0]
                    m = re.search(r\'pc-sim\\s+(pc_\\w+)\', first_line)
                    if m:
                        tool_calls.append({"tool": m.group(1), "args": cmd})
                elif item.get("type") == "text":
                    response_text += item.get("text", "") + "\\n"

    tool_set = set(tc["tool"] for tc in tool_calls)

'''


# === Helpers ===

def load_presets(source_dir: Path) -> list[dict]:
    """Load all YAML preset files, sorted by filename."""
    presets = []
    for f in sorted(source_dir.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        data["_filename"] = f.stem  # e.g. "L1_01_weather_query"
        presets.append(data)
    return presets


def make_task_id(index: int, yaml_name: str, start: int) -> tuple[str, str]:
    """Generate task id and filename.

    Returns (task_id, filename) e.g.:
        ('task_23_pcsim_weather_query', 'task_23_pcsim_weather_query.md')
    """
    # Strip LX_NN_ prefix to get the slug
    slug = re.sub(r"^L\d+_\d+_", "", yaml_name)
    num = start + index
    task_id = f"task_{num:02d}_pcsim_{slug}"
    return task_id, f"{task_id}.md"


def filter_criteria(criteria: list[dict]) -> list[dict]:
    """Filter out event_fired criteria (redundant with tool_called in same task)."""
    return [c for c in criteria if c.get("type") != "event_fired"]


def _score_key_for_tool(tool_spec: str) -> str:
    """Generate a score key from a tool spec (possibly pipe-separated)."""
    tools = [t.strip() for t in tool_spec.split("|")]
    if len(tools) == 1:
        return f"called_{tools[0]}"
    # For multi-tool alternatives, use a descriptive key
    # Extract the skill part from the first tool: pc_contacts_search -> contacts
    parts = tools[0].split("_")
    if len(parts) >= 2:
        skill = parts[1]
    else:
        skill = tools[0]
    return f"called_{skill}_lookup"


def _score_key_for_response(condition: str, index: int) -> str:
    """Generate a score key for response_contains criterion."""
    alts = condition.split("|")
    # Use first alternative, cleaned up
    first = alts[0].strip()[:20].replace(" ", "_")
    # Remove non-ascii for key safety
    safe = re.sub(r"[^a-zA-Z0-9_]", "", first)
    if safe:
        return f"response_contains_{safe}"
    return f"response_contains_{index}"


# === Code generators for each criterion type ===

def gen_tool_called_check(criterion: dict, index: int) -> tuple[str, str]:
    """Generate tool_called check code. Returns (code_lines, score_key)."""
    tool_spec = criterion.get("tool", "")
    expected_params = criterion.get("expected_params", {})
    tools = [t.strip() for t in tool_spec.split("|")]

    if expected_params:
        # tool_called_with: check tool + params in command
        score_key = f"called_{tools[0]}_with_params"
        param_checks = []
        for v in expected_params.values():
            param_checks.append(repr(str(v)))

        code = f"    # {index}. tool_called_with: {tool_spec}\n"
        code += f"    _found_{index} = False\n"
        code += f"    for tc in tool_calls:\n"
        if len(tools) == 1:
            code += f"        if {repr(tools[0])} in tc[\"tool\"]:\n"
        else:
            conditions = " or ".join(f'{repr(t)} in tc["tool"]' for t in tools)
            code += f"        if {conditions}:\n"
        if len(param_checks) == 1:
            code += f"            if {param_checks[0]} in tc[\"args\"]:\n"
        else:
            code += f"            if all(p in tc[\"args\"] for p in [{', '.join(param_checks)}]):\n"
        code += f"                _found_{index} = True\n"
        code += f"                break\n"
        code += f"    scores[\"{score_key}\"] = 1.0 if _found_{index} else 0.0\n"
        return code, score_key

    # Simple tool_called
    score_key = _score_key_for_tool(tool_spec)

    if len(tools) == 1:
        code = f"    # {index}. tool_called: {tool_spec}\n"
        code += f"    scores[\"{score_key}\"] = 1.0 if {repr(tools[0])} in tool_set else 0.0\n"
    else:
        code = f"    # {index}. tool_called: {tool_spec}\n"
        conditions = " or\n        ".join(f"{repr(t)} in tool_set" for t in tools)
        code += f"    scores[\"{score_key}\"] = 1.0 if (\n        {conditions}\n    ) else 0.0\n"

    return code, score_key


def gen_response_contains_check(criterion: dict, index: int) -> tuple[str, str]:
    """Generate response_contains check code. Returns (code_lines, score_key)."""
    condition = criterion.get("condition", "")
    alts = [a.strip() for a in condition.split("|") if a.strip()]
    score_key = _score_key_for_response(condition, index)

    alts_repr = repr(alts)
    code = f"    # {index}. response_contains: {condition[:60]}\n"
    code += f"    _found_{index} = False\n"
    code += f"    for _alt in {alts_repr}:\n"
    code += f"        if _alt.lower() in response_text.lower():\n"
    code += f"            _found_{index} = True\n"
    code += f"            break\n"
    code += f"    scores[\"{score_key}\"] = 1.0 if _found_{index} else 0.0\n"

    return code, score_key


def gen_grade_function(criteria: list[dict]) -> str:
    """Generate the complete grade() function as a string."""
    parts = [GRADE_PREAMBLE]

    for i, criterion in enumerate(criteria, 1):
        ctype = criterion.get("type", "")
        if ctype == "tool_called":
            code, _ = gen_tool_called_check(criterion, i)
            parts.append(code + "\n")
        elif ctype == "response_contains":
            code, _ = gen_response_contains_check(criterion, i)
            parts.append(code + "\n")
        # event_fired and state_check are filtered out before reaching here

    parts.append("    return scores\n")
    return "".join(parts)


# === Markdown generation ===

def gen_frontmatter(task_id: str, preset: dict) -> str:
    difficulty = preset.get("difficulty", "L1")
    category = CATEGORY_MAP.get(difficulty, "pcsim_query")
    timeout = TIMEOUT_MAP.get(difficulty, 120)

    lines = [
        "---",
        f"id: {task_id}",
        f"name: {preset.get('description', task_id)}",
        f"category: {category}",
        "grading_type: automated",
        f"timeout_seconds: {timeout}",
        "workspace_files: []",
        f'pre_exec_command: "{PRE_EXEC_CMD}"',
        f"difficulty: {difficulty}",
    ]
    skills = preset.get("skills_involved", [])
    if skills:
        if len(skills) == 1:
            lines.append(f"skills_involved: [{skills[0]}]")
        else:
            lines.append("skills_involved:")
            for s in skills:
                lines.append(f"  - {s}")
    lines.append("---")
    return "\n".join(lines)


def gen_prompt(preset: dict) -> str:
    instruction = preset.get("user_instruction", "").strip()
    return f"## Prompt\n\n{instruction}"


def gen_expected_behavior(preset: dict) -> str:
    desc = preset.get("description", "")
    skills = preset.get("skills_involved", [])
    difficulty = preset.get("difficulty", "")
    min_steps = preset.get("min_steps", 1)
    max_steps = preset.get("max_steps", 5)

    lines = [
        "## Expected Behavior",
        "",
        f"The agent should use pc-sim tools to complete the task: {desc}",
        "",
        f"Skills involved: {', '.join(skills)}",
        f"Difficulty: {difficulty}",
        f"Min steps: {min_steps}, Max steps: {max_steps}",
    ]
    return "\n".join(lines)


def gen_grading_criteria(criteria: list[dict]) -> str:
    lines = ["## Grading Criteria", ""]
    for c in criteria:
        ctype = c.get("type", "")
        if ctype == "tool_called":
            tool = c.get("tool", "")
            params = c.get("expected_params", {})
            if params:
                params_str = ", ".join(f"{k}={v}" for k, v in params.items())
                lines.append(f"- [ ] Called tool {tool} with {params_str}")
            else:
                tools = tool.split("|")
                if len(tools) == 1:
                    lines.append(f"- [ ] Called tool {tool}")
                else:
                    lines.append(f"- [ ] Called one of: {', '.join(tools)}")
        elif ctype == "response_contains":
            condition = c.get("condition", "")
            alts = condition.split("|")
            lines.append(f"- [ ] Response contains: {' or '.join(alts)}")
    return "\n".join(lines)


def render_task_md(task_id: str, preset: dict, criteria: list[dict]) -> str:
    """Assemble the full .md task file content."""
    sections = [
        gen_frontmatter(task_id, preset),
        "",
        gen_prompt(preset),
        "",
        gen_expected_behavior(preset),
        "",
        gen_grading_criteria(criteria),
        "",
        "## Automated Checks",
        "",
        "```python",
        gen_grade_function(criteria),
        "```",
    ]
    return "\n".join(sections) + "\n"


# === Validation ===

def validate_tasks(output_dir: Path) -> bool:
    """Validate generated task files can be loaded and grade functions work."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from lib_tasks import TaskLoader
    from lib_grading import _extract_grading_code

    loader = TaskLoader(output_dir)
    tasks = loader.load_all_tasks()
    print(f"Loaded {len(tasks)} tasks from {output_dir}")

    errors = 0
    for task in tasks:
        code = _extract_grading_code(task)
        if not code:
            print(f"  ✗ {task.task_id}: no grade function found")
            errors += 1
            continue
        ns = {}
        try:
            exec(code, ns)
            result = ns["grade"]([], "/tmp")
            if not isinstance(result, dict):
                print(f"  ✗ {task.task_id}: grade() returned {type(result)}, expected dict")
                errors += 1
                continue
            print(f"  ✓ {task.task_id}: {len(result)} criteria, all 0.0 (empty transcript)")
        except Exception as e:
            print(f"  ✗ {task.task_id}: grade() failed: {e}")
            errors += 1

    if errors:
        print(f"\n{errors} error(s) found!")
        return False
    print(f"\nAll {len(tasks)} tasks validated successfully.")
    return True


# === Main ===

def main():
    parser = argparse.ArgumentParser(
        description="Convert pc_environment_monitor YAML task presets to pinchbench markdown format"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to YAML task presets directory",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for generated .md files",
    )
    parser.add_argument(
        "--start-number",
        type=int,
        default=23,
        help="Starting task number (default: 23)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without writing files",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate generated files after writing",
    )
    args = parser.parse_args()

    source_dir = Path(args.source)
    output_dir = Path(args.output)

    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return

    presets = load_presets(source_dir)
    print(f"Loaded {len(presets)} YAML presets from {source_dir}")

    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    for i, preset in enumerate(presets):
        task_id, filename = make_task_id(i, preset["_filename"], args.start_number)
        criteria = filter_criteria(preset.get("success_criteria", []))
        content = render_task_md(task_id, preset, criteria)

        if args.dry_run:
            print(f"\n{'='*60}")
            print(f"Would write: {output_dir / filename}")
            print(f"{'='*60}")
            print(content[:500])
            if len(content) > 500:
                print(f"... ({len(content)} chars total)")
        else:
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"  Written: {filename} ({task_id})")

    if not args.dry_run:
        print(f"\nGenerated {len(presets)} task files in {output_dir}/")

    if args.validate and not args.dry_run:
        print(f"\n{'='*60}")
        print("Validating generated files...")
        print(f"{'='*60}")
        validate_tasks(output_dir)


if __name__ == "__main__":
    main()
