---
id: task_61_pcsim_silent_volume
name: 静音并设置媒体音量为0
category: pcsim_cross_skill
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L4
skills_involved:
  - sound_settings
  - volume
---

## Prompt

把手机声音设为静音模式，然后把媒体音量调到0

## Expected Behavior

The agent should use pc-sim tools to complete the task: 静音并设置媒体音量为0

Skills involved: sound_settings, volume
Difficulty: L4
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_sound_settings_set_profile
- [ ] Called tool pc_volume_set

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

    # 1. tool_called: pc_sound_settings_set_profile
    scores["called_pc_sound_settings_set_profile"] = 1.0 if 'pc_sound_settings_set_profile' in tool_set else 0.0

    # 2. tool_called: pc_volume_set
    scores["called_pc_volume_set"] = 1.0 if 'pc_volume_set' in tool_set else 0.0

    return scores

```
