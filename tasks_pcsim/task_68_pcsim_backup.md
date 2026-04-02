---
id: task_68_pcsim_backup
name: 设备完整备份准备
category: pcsim_workflow
grading_type: automated
timeout_seconds: 180
workspace_files: []
pre_exec_command: "rm -rf ~/.pc-simulator/data/state && mkdir -p ~/.pc-simulator/data/state"
difficulty: L5
skills_involved:
  - runtime_env
  - contacts
  - file_manager
---

## Prompt

帮我做个完整的设备备份准备：查看系统信息，列出所有已安装的包，导出联系人列表，然后把这些信息都写到一个文件里

## Expected Behavior

The agent should use pc-sim tools to complete the task: 设备完整备份准备

Skills involved: runtime_env, contacts, file_manager
Difficulty: L5
Min steps: 3, Max steps: 15

## Grading Criteria

- [ ] Called one of: pc_device_manager_get_info, pc_runtime_env_get_system_info
- [ ] Called tool pc_runtime_env_list_packages
- [ ] Called one of: pc_contacts_list, pc_contacts_export_contacts
- [ ] Response contains: 备份 or backup or 已保存 or 写入 or saved

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

    # 1. tool_called: pc_device_manager_get_info|pc_runtime_env_get_system_info
    scores["called_device_lookup"] = 1.0 if (
        'pc_device_manager_get_info' in tool_set or
        'pc_runtime_env_get_system_info' in tool_set
    ) else 0.0

    # 2. tool_called: pc_runtime_env_list_packages
    scores["called_pc_runtime_env_list_packages"] = 1.0 if 'pc_runtime_env_list_packages' in tool_set else 0.0

    # 3. tool_called: pc_contacts_list|pc_contacts_export_contacts
    scores["called_contacts_lookup"] = 1.0 if (
        'pc_contacts_list' in tool_set or
        'pc_contacts_export_contacts' in tool_set
    ) else 0.0

    # 4. response_contains: 备份|backup|已保存|写入|saved
    _found_4 = False
    for _alt in ['备份', 'backup', '已保存', '写入', 'saved']:
        if _alt.lower() in response_text.lower():
            _found_4 = True
            break
    scores["response_contains_4"] = 1.0 if _found_4 else 0.0

    return scores

```
