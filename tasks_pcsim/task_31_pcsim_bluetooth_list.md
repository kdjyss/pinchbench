---
id: task_31_pcsim_bluetooth_list
name: 查看已配对蓝牙设备
category: pcsim_query
grading_type: automated
timeout_seconds: 60
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L1
skills_involved: [bluetooth]
---

## Prompt

看看有什么蓝牙设备连着

## Expected Behavior

The agent should use pc-sim tools to complete the task: 查看已配对蓝牙设备

Skills involved: bluetooth
Difficulty: L1
Min steps: 1, Max steps: 5

## Grading Criteria

- [ ] Called tool pc_bluetooth_list_paired
- [ ] Response contains: Headphones or Mouse

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

    # 1. tool_called: pc_bluetooth_list_paired
    scores["called_pc_bluetooth_list_paired"] = 1.0 if 'pc_bluetooth_list_paired' in tool_set else 0.0

    # 2. response_contains: Headphones|Mouse
    _found_2 = False
    for _alt in ['Headphones', 'Mouse']:
        if _alt.lower() in response_text.lower():
            _found_2 = True
            break
    scores["response_contains_Headphones"] = 1.0 if _found_2 else 0.0

    return scores

```
