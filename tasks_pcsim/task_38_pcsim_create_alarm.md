---
id: task_38_pcsim_create_alarm
name: 设置早起闹钟
category: pcsim_action
grading_type: automated
timeout_seconds: 90
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L2
skills_involved: [alarm]
---

## Prompt

设一个明早6点半的闹钟

## Expected Behavior

The agent should use pc-sim tools to complete the task: 设置早起闹钟

Skills involved: alarm
Difficulty: L2
Min steps: 1, Max steps: 5

## Grading Criteria

- [ ] Called tool pc_alarm_create with time=06:30

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

    # 1. tool_called_with: pc_alarm_create
    _found_1 = False
    for tc in tool_calls:
        if 'pc_alarm_create' in tc["tool"]:
            if '06:30' in tc["args"]:
                _found_1 = True
                break
    scores["called_pc_alarm_create_with_params"] = 1.0 if _found_1 else 0.0

    return scores

```
