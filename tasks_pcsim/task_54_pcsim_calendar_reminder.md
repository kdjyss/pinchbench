---
id: task_54_pcsim_calendar_reminder
name: 查看日程并修改提醒时间
category: pcsim_multi_step
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L3
skills_involved: [calendar]
---

## Prompt

查看今天的日程，然后把Team Standup的提醒改成提前30分钟

## Expected Behavior

The agent should use pc-sim tools to complete the task: 查看日程并修改提醒时间

Skills involved: calendar
Difficulty: L3
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_calendar_list_events
- [ ] Called tool pc_calendar_set_reminder

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

    # 2. tool_called: pc_calendar_set_reminder
    scores["called_pc_calendar_set_reminder"] = 1.0 if 'pc_calendar_set_reminder' in tool_set else 0.0

    return scores

```
