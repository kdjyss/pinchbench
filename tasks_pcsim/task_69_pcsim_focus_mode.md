---
id: task_69_pcsim_focus_mode
name: 专注模式全配置
category: pcsim_workflow
grading_type: automated
timeout_seconds: 180
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L5
skills_involved:
  - push_notification
  - display
  - music_player
  - timer
---

## Prompt

今天效率太低了，帮我做些调整：开启免打扰模式，把屏幕亮度调到最高，播放我的Workout Mix歌单里的歌，然后创建一个倒计时45分钟的番茄钟

## Expected Behavior

The agent should use pc-sim tools to complete the task: 专注模式全配置

Skills involved: push_notification, display, music_player, timer
Difficulty: L5
Min steps: 3, Max steps: 15

## Grading Criteria

- [ ] Called one of: pc_push_notification_set_dnd, pc_sound_settings_set_dnd
- [ ] Called tool pc_display_set_brightness
- [ ] Called tool pc_music_player_play
- [ ] Called tool pc_timer_create_countdown

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

    # 1. tool_called: pc_push_notification_set_dnd|pc_sound_settings_set_dnd
    scores["called_push_lookup"] = 1.0 if (
        'pc_push_notification_set_dnd' in tool_set or
        'pc_sound_settings_set_dnd' in tool_set
    ) else 0.0

    # 2. tool_called: pc_display_set_brightness
    scores["called_pc_display_set_brightness"] = 1.0 if 'pc_display_set_brightness' in tool_set else 0.0

    # 3. tool_called: pc_music_player_play
    scores["called_pc_music_player_play"] = 1.0 if 'pc_music_player_play' in tool_set else 0.0

    # 4. tool_called: pc_timer_create_countdown
    scores["called_pc_timer_create_countdown"] = 1.0 if 'pc_timer_create_countdown' in tool_set else 0.0

    return scores

```
