#!/usr/bin/env python3
"""Verify transcript output format by simulating a benchmark run with mock data.

Feeds a mock transcript through the grading + save-transcripts pipeline
to confirm the output JSON structure is correct.

Usage:
    python scripts/verify_transcript_output.py
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib_tasks import TaskLoader
from lib_grading import grade_task


def make_mock_transcript():
    """Create a mock transcript simulating an agent calling pc-sim."""
    return [
        {
            "type": "message",
            "message": {
                "role": "user",
                "content": [{"type": "text", "text": "今天北京天气怎么样"}],
            },
        },
        {
            "type": "message",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "type": "toolCall",
                        "name": "exec",
                        "arguments": {"command": "pc-sim pc_weather_get_current --city Beijing"},
                    }
                ],
                "usage": {"input": 500, "output": 50, "totalTokens": 550, "cost": {"total": 0.001}},
            },
        },
        {
            "type": "message",
            "message": {
                "role": "toolResult",
                "content": [
                    {
                        "type": "text",
                        "text": '{"success": true, "data": {"city": "Beijing", "temp_c": 22, "condition": "sunny", "humidity": 45}}',
                    }
                ],
            },
        },
        {
            "type": "message",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "北京今天天气晴朗(sunny)，气温22°C，湿度45%。适合出门活动。",
                    }
                ],
                "usage": {"input": 600, "output": 80, "totalTokens": 680, "cost": {"total": 0.002}},
            },
        },
    ]


def main():
    tasks_dir = Path(__file__).parent.parent / "tasks_pcsim"
    if not tasks_dir.exists():
        print(f"tasks_pcsim/ not found at {tasks_dir}")
        sys.exit(1)

    loader = TaskLoader(tasks_dir)
    tasks = loader.load_all_tasks()
    task = next((t for t in tasks if t.task_id == "task_23_pcsim_weather_query"), None)
    if not task:
        print("task_23_pcsim_weather_query not found")
        sys.exit(1)

    print(f"Task: {task.task_id} ({task.name})")
    print(f"Prompt: {task.prompt}")
    print(f"Grading type: {task.grading_type}")
    print()

    # Simulate execution result
    mock_transcript = make_mock_transcript()
    execution_result = {
        "agent_id": "main",
        "task_id": task.task_id,
        "status": "success",
        "transcript": mock_transcript,
        "usage": {},
        "workspace": "/tmp/test",
        "exit_code": 0,
        "timed_out": False,
        "execution_time": 3.5,
    }

    # Run grading
    with tempfile.TemporaryDirectory() as tmpdir:
        grade = grade_task(task=task, execution_result=execution_result, skill_dir=Path(tmpdir))

    print(f"=== Automated Grading ===")
    print(f"Score: {grade.score}")
    print(f"Breakdown: {json.dumps(grade.breakdown, ensure_ascii=False, indent=2)}")
    print()

    # Build transcript output (same logic as benchmark.py --save-transcripts)
    transcript_data = {
        "task_id": task.task_id,
        "task_name": task.name,
        "task_prompt": task.prompt,
        "expected_behavior": task.expected_behavior,
        "grading_criteria": task.grading_criteria,
        "difficulty": task.frontmatter.get("difficulty", ""),
        "skills_involved": task.frontmatter.get("skills_involved", []),
        "transcript": mock_transcript,
        "automated_score": grade.score,
        "automated_breakdown": grade.breakdown,
    }

    # Write to temp file and read back to verify
    output_path = Path(tmpdir if 'tmpdir' in dir() else tempfile.mkdtemp()) / "test_transcript.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(transcript_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Read back and validate
    loaded = json.loads(output_path.read_text(encoding="utf-8"))

    print(f"=== Output JSON Validation ===")
    required_fields = [
        "task_id", "task_name", "task_prompt", "expected_behavior",
        "grading_criteria", "difficulty", "skills_involved",
        "transcript", "automated_score", "automated_breakdown",
    ]
    all_ok = True
    for field in required_fields:
        present = field in loaded
        value_preview = str(loaded.get(field, "MISSING"))[:80]
        status = "✓" if present else "✗"
        if not present:
            all_ok = False
        print(f"  {status} {field}: {value_preview}")

    # Validate transcript structure
    transcript = loaded["transcript"]
    print(f"\n  Transcript entries: {len(transcript)}")
    roles = [e.get("message", {}).get("role", "?") for e in transcript if e.get("type") == "message"]
    print(f"  Message roles: {' → '.join(roles)}")

    # Check tool calls are extractable
    tool_calls = []
    for entry in transcript:
        if entry.get("type") != "message":
            continue
        msg = entry.get("message", {})
        if msg.get("role") == "assistant":
            for item in msg.get("content", []):
                if isinstance(item, dict) and item.get("type") == "toolCall":
                    tool_calls.append(f"{item.get('name')}({item.get('arguments', {}).get('command', '')[:50]})")
    print(f"  Tool calls: {tool_calls}")

    # Check response text is extractable
    response_texts = []
    for entry in transcript:
        if entry.get("type") != "message":
            continue
        msg = entry.get("message", {})
        if msg.get("role") == "assistant":
            for item in msg.get("content", []):
                if isinstance(item, dict) and item.get("type") == "text":
                    response_texts.append(item["text"][:60])
    print(f"  Agent responses: {response_texts}")

    print(f"\n=== Final Output JSON ===")
    print(json.dumps(loaded, ensure_ascii=False, indent=2))

    if all_ok:
        print(f"\n✓ All fields present, structure correct. Ready for Claude scoring.")
    else:
        print(f"\n✗ Missing fields detected!")
        sys.exit(1)


if __name__ == "__main__":
    main()
