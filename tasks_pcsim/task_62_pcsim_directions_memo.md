---
id: task_62_pcsim_directions_memo
name: 查询路线并记录到备忘录
category: pcsim_cross_skill
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L4
skills_involved:
  - map_location
  - memo
---

## Prompt

帮我查一下从北京到上海怎么走，然后把路线信息写到备忘录里

## Expected Behavior

The agent should use pc-sim tools to complete the task: 查询路线并记录到备忘录

Skills involved: map_location, memo
Difficulty: L4
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_map_location_get_directions
- [ ] Called tool pc_memo_create

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

    # 1. tool_called: pc_map_location_get_directions
    scores["called_pc_map_location_get_directions"] = 1.0 if 'pc_map_location_get_directions' in tool_set else 0.0

    # 2. tool_called: pc_memo_create
    scores["called_pc_memo_create"] = 1.0 if 'pc_memo_create' in tool_set else 0.0

    return scores

```
