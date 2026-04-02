---
id: task_59_pcsim_forward_email
name: 转发邮件给联系人
category: pcsim_cross_skill
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L4
skills_involved:
  - email
  - contacts
---

## Prompt

把Bob Wang的邮件转发给David Zhang

## Expected Behavior

The agent should use pc-sim tools to complete the task: 转发邮件给联系人

Skills involved: email, contacts
Difficulty: L4
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_email_list_inbox
- [ ] Called one of: pc_contacts_list, pc_contacts_search, pc_contacts_get
- [ ] Called tool pc_email_forward

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

    # 1. tool_called: pc_email_list_inbox
    scores["called_pc_email_list_inbox"] = 1.0 if 'pc_email_list_inbox' in tool_set else 0.0

    # 2. tool_called: pc_contacts_list|pc_contacts_search|pc_contacts_get
    scores["called_contacts_lookup"] = 1.0 if (
        'pc_contacts_list' in tool_set or
        'pc_contacts_search' in tool_set or
        'pc_contacts_get' in tool_set
    ) else 0.0

    # 3. tool_called: pc_email_forward
    scores["called_pc_email_forward"] = 1.0 if 'pc_email_forward' in tool_set else 0.0

    return scores

```
