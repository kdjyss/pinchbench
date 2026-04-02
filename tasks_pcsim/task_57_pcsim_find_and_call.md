---
id: task_57_pcsim_find_and_call
name: 查联系人电话并拨打
category: pcsim_cross_skill
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L4
skills_involved:
  - contacts
  - phone_call
---

## Prompt

查一下联系人Alice的电话号码，然后打给她

## Expected Behavior

The agent should use pc-sim tools to complete the task: 查联系人电话并拨打

Skills involved: contacts, phone_call
Difficulty: L4
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called one of: pc_contacts_search, pc_contacts_list, pc_contacts_get
- [ ] Called tool pc_phone_call_dial
- [ ] Response contains: +1-555-0101

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

    # 1. tool_called: pc_contacts_search|pc_contacts_list|pc_contacts_get
    scores["called_contacts_lookup"] = 1.0 if (
        'pc_contacts_search' in tool_set or
        'pc_contacts_list' in tool_set or
        'pc_contacts_get' in tool_set
    ) else 0.0

    # 2. tool_called: pc_phone_call_dial
    scores["called_pc_phone_call_dial"] = 1.0 if 'pc_phone_call_dial' in tool_set else 0.0

    # 3. response_contains: +1-555-0101
    _found_3 = False
    for _alt in ['+1-555-0101']:
        if _alt.lower() in response_text.lower():
            _found_3 = True
            break
    scores["response_contains_15550101"] = 1.0 if _found_3 else 0.0

    return scores

```
