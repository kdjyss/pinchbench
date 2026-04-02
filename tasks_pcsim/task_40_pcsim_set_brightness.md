---
id: task_40_pcsim_set_brightness
name: 调整屏幕亮度
category: pcsim_action
grading_type: automated
timeout_seconds: 90
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L2
skills_involved: [display]
---

## Prompt

把屏幕亮度调到50

## Expected Behavior

The agent should use pc-sim tools to complete the task: 调整屏幕亮度

Skills involved: display
Difficulty: L2
Min steps: 1, Max steps: 5

## Grading Criteria

- [ ] Called tool pc_display_set_brightness with level=50

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

    # 1. tool_called_with: pc_display_set_brightness
    _found_1 = False
    for tc in tool_calls:
        if 'pc_display_set_brightness' in tc["tool"]:
            if '50' in tc["args"]:
                _found_1 = True
                break
    scores["called_pc_display_set_brightness_with_params"] = 1.0 if _found_1 else 0.0

    return scores

```
