---
id: task_58_pcsim_calendar_weather
name: 查询明天会议和天气
category: pcsim_cross_skill
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L4
skills_involved:
  - calendar
  - weather
---

## Prompt

明天有什么会议？顺便看看明天的天气

## Expected Behavior

The agent should use pc-sim tools to complete the task: 查询明天会议和天气

Skills involved: calendar, weather
Difficulty: L4
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_calendar_list_events
- [ ] Called one of: pc_weather_get_current, pc_weather_get_forecast
- [ ] Response contains: Project Review or 项目评审 or 项目审查 or project review

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

    # 1. tool_called: pc_calendar_list_events
    scores["called_pc_calendar_list_events"] = 1.0 if 'pc_calendar_list_events' in tool_set else 0.0

    # 2. tool_called: pc_weather_get_current|pc_weather_get_forecast
    scores["called_weather_lookup"] = 1.0 if (
        'pc_weather_get_current' in tool_set or
        'pc_weather_get_forecast' in tool_set
    ) else 0.0

    # 3. response_contains: Project Review|项目评审|项目审查|project review
    _found_3 = False
    for _alt in ['Project Review', '项目评审', '项目审查', 'project review']:
        if _alt.lower() in response_text.lower():
            _found_3 = True
            break
    scores["response_contains_Project_Review"] = 1.0 if _found_3 else 0.0

    return scores

```
