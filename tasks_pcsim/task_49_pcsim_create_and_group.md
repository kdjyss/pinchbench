---
id: task_49_pcsim_create_and_group
name: 创建联系人并加入分组
category: pcsim_multi_step
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L3
skills_involved: [contacts]
---

## Prompt

创建联系人Grace电话13912345678，然后把她加到work分组

## Expected Behavior

The agent should use pc-sim tools to complete the task: 创建联系人并加入分组

Skills involved: contacts
Difficulty: L3
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_contacts_create
- [ ] Called tool pc_contacts_add_to_group

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

    # 1. tool_called: pc_contacts_create
    scores["called_pc_contacts_create"] = 1.0 if 'pc_contacts_create' in tool_set else 0.0

    # 2. tool_called: pc_contacts_add_to_group
    scores["called_pc_contacts_add_to_group"] = 1.0 if 'pc_contacts_add_to_group' in tool_set else 0.0

    return scores

```
