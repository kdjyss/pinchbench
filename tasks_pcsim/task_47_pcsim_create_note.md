---
id: task_47_pcsim_create_note
name: 创建带标签的笔记
category: pcsim_action
grading_type: automated
timeout_seconds: 90
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L2
skills_involved: [notes]
---

## Prompt

用笔记功能创建一个新笔记，标题是学习计划，内容是每天学习Python两小时，标签设为programming

## Expected Behavior

The agent should use pc-sim tools to complete the task: 创建带标签的笔记

Skills involved: notes
Difficulty: L2
Min steps: 1, Max steps: 5

## Grading Criteria

- [ ] Called tool pc_notes_create

## Automated Checks

```python
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
                    first_line = cmd.split("\n")[0]
                    m = re.search(r'pc-sim\s+(pc_\w+)', first_line)
                    if m:
                        tool_calls.append({"tool": m.group(1), "args": cmd})
                elif item.get("type") == "text":
                    response_text += item.get("text", "") + "\n"

    tool_set = set(tc["tool"] for tc in tool_calls)

    # 1. tool_called: pc_notes_create
    scores["called_pc_notes_create"] = 1.0 if 'pc_notes_create' in tool_set else 0.0

    return scores

```
