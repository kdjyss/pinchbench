---
id: task_43_pcsim_open_browser
name: 浏览器打开网页
category: pcsim_action
grading_type: automated
timeout_seconds: 90
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L2
skills_involved: [browser]
---

## Prompt

在浏览器打开百度

## Expected Behavior

The agent should use pc-sim tools to complete the task: 浏览器打开网页

Skills involved: browser
Difficulty: L2
Min steps: 1, Max steps: 5

## Grading Criteria

- [ ] Called tool pc_browser_open_url
- [ ] Response contains: baidu

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

    # 1. tool_called: pc_browser_open_url
    scores["called_pc_browser_open_url"] = 1.0 if 'pc_browser_open_url' in tool_set else 0.0

    # 2. response_contains: baidu
    _found_2 = False
    for _alt in ['baidu']:
        if _alt.lower() in response_text.lower():
            _found_2 = True
            break
    scores["response_contains_baidu"] = 1.0 if _found_2 else 0.0

    return scores

```
