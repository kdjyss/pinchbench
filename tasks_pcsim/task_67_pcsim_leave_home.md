---
id: task_67_pcsim_leave_home
name: 出门前设备配置
category: pcsim_workflow
grading_type: automated
timeout_seconds: 180
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L5
skills_involved:
  - display
  - battery
  - sound_settings
  - push_notification
---

## Prompt

我要出门了，帮我：把屏幕超时设为1分钟，开启省电模式，把声音切到静音，清除所有通知

## Expected Behavior

The agent should use pc-sim tools to complete the task: 出门前设备配置

Skills involved: display, battery, sound_settings, push_notification
Difficulty: L5
Min steps: 3, Max steps: 15

## Grading Criteria

- [ ] Called tool pc_display_set_timeout
- [ ] Called tool pc_battery_set_power_mode
- [ ] Called one of: pc_sound_settings_set_profile, pc_volume_mute
- [ ] Called tool pc_push_notification_dismiss_all

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

    # 1. tool_called: pc_display_set_timeout
    scores["called_pc_display_set_timeout"] = 1.0 if 'pc_display_set_timeout' in tool_set else 0.0

    # 2. tool_called: pc_battery_set_power_mode
    scores["called_pc_battery_set_power_mode"] = 1.0 if 'pc_battery_set_power_mode' in tool_set else 0.0

    # 3. tool_called: pc_sound_settings_set_profile|pc_volume_mute
    scores["called_sound_lookup"] = 1.0 if (
        'pc_sound_settings_set_profile' in tool_set or
        'pc_volume_mute' in tool_set
    ) else 0.0

    # 4. tool_called: pc_push_notification_dismiss_all
    scores["called_pc_push_notification_dismiss_all"] = 1.0 if 'pc_push_notification_dismiss_all' in tool_set else 0.0

    return scores

```
