---
id: task_72_pcsim_uninstall_system
name: 尝试卸载系统应用
category: pcsim_error_handling
grading_type: automated
timeout_seconds: 90
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L6
skills_involved: [runtime_env]
---

## Prompt

卸载系统设置应用

## Expected Behavior

The agent should use pc-sim tools to complete the task: 尝试卸载系统应用

Skills involved: runtime_env
Difficulty: L6
Min steps: 1, Max steps: 5

## Grading Criteria

- [ ] Response contains: 系统应用 or 无法卸载 or cannot

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

    # 1. response_contains: 系统应用|无法卸载|cannot
    _found_1 = False
    for _alt in ['系统应用', '无法卸载', 'cannot']:
        if _alt.lower() in response_text.lower():
            _found_1 = True
            break
    scores["response_contains_1"] = 1.0 if _found_1 else 0.0

    return scores

```
