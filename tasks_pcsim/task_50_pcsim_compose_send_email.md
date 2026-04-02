---
id: task_50_pcsim_compose_send_email
name: 撰写并发送邮件
category: pcsim_multi_step
grading_type: automated
timeout_seconds: 120
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L3
skills_involved: [email]
---

## Prompt

写一封邮件给alice@example.com，主题是项目进度，内容是本周完成了80%的开发工作，然后发送

## Expected Behavior

The agent should use pc-sim tools to complete the task: 撰写并发送邮件

Skills involved: email
Difficulty: L3
Min steps: 2, Max steps: 10

## Grading Criteria

- [ ] Called tool pc_email_send

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

    # 1. tool_called: pc_email_send
    scores["called_pc_email_send"] = 1.0 if 'pc_email_send' in tool_set else 0.0

    return scores

```
