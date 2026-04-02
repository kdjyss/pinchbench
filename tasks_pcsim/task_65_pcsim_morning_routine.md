---
id: task_65_pcsim_morning_routine
name: 完整起床提醒设置
category: pcsim_workflow
grading_type: automated
timeout_seconds: 180
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L5
skills_involved:
  - alarm
  - weather
  - calendar
---

## Prompt

帮我设置一个完整的起床提醒：先设个明早7点的闹钟，然后查一下明天北京天气，再看看明天有什么日程安排

## Expected Behavior

The agent should use pc-sim tools to complete the task: 完整起床提醒设置

Skills involved: alarm, weather, calendar
Difficulty: L5
Min steps: 3, Max steps: 15

## Grading Criteria

- [ ] Called tool pc_alarm_create
- [ ] Called one of: pc_weather_get_current, pc_weather_get_forecast
- [ ] Called tool pc_calendar_list_events

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

    # 1. tool_called: pc_alarm_create
    scores["called_pc_alarm_create"] = 1.0 if 'pc_alarm_create' in tool_set else 0.0

    # 2. tool_called: pc_weather_get_current|pc_weather_get_forecast
    scores["called_weather_lookup"] = 1.0 if (
        'pc_weather_get_current' in tool_set or
        'pc_weather_get_forecast' in tool_set
    ) else 0.0

    # 3. tool_called: pc_calendar_list_events
    scores["called_pc_calendar_list_events"] = 1.0 if 'pc_calendar_list_events' in tool_set else 0.0

    return scores

```
