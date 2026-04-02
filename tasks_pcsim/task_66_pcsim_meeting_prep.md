---
id: task_66_pcsim_meeting_prep
name: 会议准备全流程
category: pcsim_workflow
grading_type: automated
timeout_seconds: 180
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L5
skills_involved:
  - calendar
  - contacts
  - email
---

## Prompt

帮我准备明天的会议：查看明天的Project Review会议详情，找到参会者David Zhang的邮箱，然后发一封邮件提醒他明天开会

## Expected Behavior

The agent should use pc-sim tools to complete the task: 会议准备全流程

Skills involved: calendar, contacts, email
Difficulty: L5
Min steps: 3, Max steps: 15

## Grading Criteria

- [ ] Called tool pc_calendar_list_events
- [ ] Called one of: pc_contacts_list, pc_contacts_search, pc_contacts_get
- [ ] Called one of: pc_email_send, pc_email_compose, pc_email_forward

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

    # 2. tool_called: pc_contacts_list|pc_contacts_search|pc_contacts_get
    scores["called_contacts_lookup"] = 1.0 if (
        'pc_contacts_list' in tool_set or
        'pc_contacts_search' in tool_set or
        'pc_contacts_get' in tool_set
    ) else 0.0

    # 3. tool_called: pc_email_send|pc_email_compose|pc_email_forward
    scores["called_email_lookup"] = 1.0 if (
        'pc_email_send' in tool_set or
        'pc_email_compose' in tool_set or
        'pc_email_forward' in tool_set
    ) else 0.0

    return scores

```
