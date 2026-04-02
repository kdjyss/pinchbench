---
id: task_53_pcsim_create_album_move
name: 创建相册并移入照片
category: pcsim_multi_step
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L3
skills_involved: [gallery]
---

## Prompt

创建一个新相册叫旅行2026，然后把beach.jpg移到这个相册

## Expected Behavior

The agent should use pc-sim tools to complete the task: 创建相册并移入照片

Skills involved: gallery
Difficulty: L3
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_gallery_create_album
- [ ] Called tool pc_gallery_move_to_album

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

    # 1. tool_called: pc_gallery_create_album
    scores["called_pc_gallery_create_album"] = 1.0 if 'pc_gallery_create_album' in tool_set else 0.0

    # 2. tool_called: pc_gallery_move_to_album
    scores["called_pc_gallery_move_to_album"] = 1.0 if 'pc_gallery_move_to_album' in tool_set else 0.0

    return scores

```
