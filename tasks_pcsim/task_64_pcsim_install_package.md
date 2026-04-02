---
id: task_64_pcsim_install_package
name: 查看Python版本并安装包
category: pcsim_cross_skill
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L4
skills_involved: [runtime_env]
---

## Prompt

查看Python版本，然后安装一个叫matplotlib的包

## Expected Behavior

The agent should use pc-sim tools to complete the task: 查看Python版本并安装包

Skills involved: runtime_env
Difficulty: L4
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called one of: pc_runtime_env_get_python_version, pc_runtime_env_get_system_info
- [ ] Called tool pc_runtime_env_install_package

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

    # 1. tool_called: pc_runtime_env_get_python_version|pc_runtime_env_get_system_info
    scores["called_runtime_lookup"] = 1.0 if (
        'pc_runtime_env_get_python_version' in tool_set or
        'pc_runtime_env_get_system_info' in tool_set
    ) else 0.0

    # 2. tool_called: pc_runtime_env_install_package
    scores["called_pc_runtime_env_install_package"] = 1.0 if 'pc_runtime_env_install_package' in tool_set else 0.0

    return scores

```
