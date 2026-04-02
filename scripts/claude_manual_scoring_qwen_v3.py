#!/usr/bin/env python3
"""Claude manual scoring for Qwen3.5-9B v3 (with TOOLS.md optimization)."""
import json
from pathlib import Path

MANUAL_SCORES = [
    # === L1 ===
    ("task_23_pcsim_weather_query", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_24_pcsim_battery_status", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_25_pcsim_contacts_list", 1.0, 1.0, 1.0, 1.0, "1步直接调用，表格展示，完美。"),
    ("task_26_pcsim_email_inbox", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_27_pcsim_volume_check", 1.0, 1.0, 1.0, 1.0, "1步直接调用pc_volume_get，完美。主动询问是否查看其他音频流。"),
    ("task_28_pcsim_alarm_list", 1.0, 1.0, 1.0, 1.0, "1步直接调用，表格展示，完美。"),
    ("task_29_pcsim_location", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。v1/v2都是0分，v3修复了！"),
    ("task_30_pcsim_notifications", 1.0, 0.9, 1.0, 0.8, "第一步猜错(pc_notification_list)，第二步成功。回复详细。"),
    ("task_31_pcsim_bluetooth_list", 1.0, 0.9, 1.0, 0.8, "memory_search(多余)→read→正确调用。3步稍多但结果准确。"),
    ("task_32_pcsim_sensor_temp", 1.0, 1.0, 1.0, 1.0, "read→正确调用含正确参数，2步完美。"),
    ("task_33_pcsim_video_list", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。v1失败，v2用6步猜，v3直接成功。"),
    ("task_34_pcsim_device_info", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。展示模拟器配置而非真实系统。"),
    ("task_35_pcsim_processes", 0.5, 0.0, 0.5, 0.3, "直接用ps aux查真实进程，没调用pc_shell_list_processes。混淆了模拟器和宿主机。"),
    ("task_36_pcsim_files", 1.0, 1.0, 1.0, 0.6, "5步全部用pc_file_manager_list，没用系统命令。比之前版本好。但5步逐层探索效率一般。"),

    # === L2 ===
    ("task_37_pcsim_create_contact", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。参数正确。"),
    ("task_38_pcsim_create_alarm", 1.0, 1.0, 1.0, 0.8, "memory_search(多余)→read→正确调用。3步，额外参数--date tomorrow可接受。"),
    ("task_39_pcsim_create_memo", 1.0, 1.0, 1.0, 1.0, "read→正确调用pc_memo_create，2步完美。"),
    ("task_40_pcsim_set_brightness", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_41_pcsim_payment", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_42_pcsim_dark_theme", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_43_pcsim_open_browser", 1.0, 0.8, 1.0, 0.7, "第一步猜错(pc_browser_op)，读SKILL.md后成功。3步。"),
    ("task_44_pcsim_play_music", 1.0, 1.0, 1.0, 1.0, "read→list→play --track_id，3步精准。v1需10步，v2需10步，v3只要3步。"),
    ("task_45_pcsim_countdown", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_46_pcsim_take_photo", 1.0, 0.9, 1.0, 0.8, "第一步猜错(pc_camera_take_photo)，读SKILL.md后成功。3步。v1=11步，v2=0步，v3=3步。"),
    ("task_47_pcsim_create_note", 1.0, 0.6, 1.0, 0.2, "9步太多：前7步猜各种命令(notes_exists, createnote, --help, install_app, list-skills|grep)。最终成功但效率极差。"),
    ("task_48_pcsim_grant_permission", 1.0, 1.0, 1.0, 0.9, "read两个SKILL.md→正确调用。3步高效。"),

    # === L3 ===
    ("task_49_pcsim_create_and_group", 1.0, 1.0, 1.0, 1.0, "read→create→add_to_group，3步完美。"),
    ("task_50_pcsim_compose_send_email", 1.0, 1.0, 1.0, 1.0, "read→直接pc_email_send，2步完美。"),
    ("task_51_pcsim_record_audio", 1.0, 1.0, 1.0, 0.8, "read→start→stop→write(多余日志)。4步，write不必要。"),
    ("task_52_pcsim_list_pin_memo", 1.0, 0.8, 1.0, 0.6, "5步。pin时猜错参数(m002→--memoId→读SKILL.md→--memo_id)。最终成功。"),
    ("task_53_pcsim_create_album_move", 1.0, 0.8, 1.0, 0.4, "8步。create_album和move_to_album各猜错一次参数。最终成功。"),
    ("task_54_pcsim_calendar_reminder", 0.0, 0.0, 0.3, 0.0, "完全失败。memory_search→sessions_spawn→session_status，没调用任何pc-sim工具。声称没有日历功能。"),
    ("task_55_pcsim_bluetooth_scan_pair", 1.0, 1.0, 1.0, 1.0, "read→scan→pair，3步完美。"),
    ("task_56_pcsim_pause_shuffle", 1.0, 0.8, 0.9, 0.6, "5步。前两步猜错(pc_music_pause, pc_music_shuffle_active)，读SKILL.md后成功。"),

    # === L4 ===
    ("task_57_pcsim_find_and_call", 1.0, 0.9, 1.0, 0.7, "5步。先get了c002(Bob)再get c001(Alice)，多查了一次。最终正确拨号。"),
    ("task_58_pcsim_calendar_weather", 1.0, 1.0, 1.0, 0.9, "4步：read两个SKILL.md→list_events→get_forecast。高效跨技能协调。v1/v2都是0分！"),
    ("task_59_pcsim_forward_email", 0.5, 0.6, 0.5, 0.5, "4步。list_inbox成功找到Bob邮件，但search失败后没有继续forward。只列出了邮件没完成转发。"),
    ("task_60_pcsim_screenshot_transfer", 0.3, 0.1, 0.3, 0.1, "6步全部失败。猜错截屏命令后转用bash/scrot/python截图，完全脱离pc-sim。v2满分，v3严重退步。"),
    ("task_61_pcsim_silent_volume", 1.0, 0.7, 1.0, 0.1, "26步极度低效。反复猜静音和音量命令格式。最终成功但过程极其曲折。"),
    ("task_62_pcsim_directions_memo", 1.0, 1.0, 1.0, 0.9, "4步：read→get_directions→read→memo_create。高效。"),
    ("task_63_pcsim_reply_email", 1.0, 1.0, 1.0, 1.0, "read→list_inbox→reply，3步完美。"),
    ("task_64_pcsim_install_package", 0.3, 0.0, 0.5, 0.5, "用python --version和pip install，没用pc-sim工具。获取真实系统信息。"),

    # === L5 ===
    ("task_65_pcsim_morning_routine", 1.0, 0.8, 0.9, 0.4, "11步。前3步猜错，读3个SKILL.md后完成3个子任务。效率一般但全部成功。"),
    ("task_66_pcsim_meeting_prep", 1.0, 0.8, 1.0, 0.4, "10步。前几步猜错，但最终找到会议→查David邮箱→发邮件。全部成功。"),
    ("task_67_pcsim_leave_home", 1.0, 0.8, 1.0, 0.4, "11步。前4步猜错，读4个SKILL.md后4个子任务全部完成。效率一般但全成功。"),
    ("task_68_pcsim_backup", 0.8, 0.7, 0.9, 0.5, "10步。第一步猜错(pc_system_info)。完成了list_packages/export_contacts/get_status/list_devices。但没用pc_device_manager_get_info或pc_runtime_env_get_system_info。"),
    ("task_69_pcsim_focus_mode", 1.0, 0.9, 1.0, 0.4, "13步。读4个SKILL.md后逐个完成。dnd→brightness→music(用Night Drive替代Workout Mix)→countdown。全部成功。"),

    # === L6 ===
    ("task_70_pcsim_delete_nonexistent", 1.0, 0.8, 1.0, 0.8, "3步。第一步猜错(contacts_delete)，search+list确认不存在。高效。"),
    ("task_71_pcsim_offline_device", 1.0, 1.0, 1.0, 1.0, "read→list_devices，2步完美。正确识别离线状态并提供建议。"),
    ("task_72_pcsim_uninstall_system", 1.0, 0.8, 1.0, 0.5, "6步。前3步猜错(app_manager list, finial_app_list, list-tools)。list_installed→uninstall成功识别系统应用。"),
    ("task_73_pcsim_stop_no_recording", 1.0, 0.8, 1.0, 0.6, "4步。read后猜错(pc-recorder-stop缺pc-sim前缀)，第3步成功。额外get_status确认。"),
    ("task_74_pcsim_insufficient_funds", 1.0, 1.0, 1.0, 1.0, "read→get_balance，2步完美。正确识别余额不足。"),
]


def build_scores():
    results = []
    for task_id, completion, tool, response, efficiency, notes in MANUAL_SCORES:
        claude_total = completion * 0.30 + tool * 0.25 + response * 0.25 + efficiency * 0.20
        results.append({
            "task_id": task_id,
            "claude_scores": {
                "task_completion": completion,
                "tool_usage": tool,
                "response_quality": response,
                "efficiency": efficiency,
            },
            "claude_total": round(claude_total, 3),
            "notes": notes,
        })
    return results


def merge_with_automated(scores, transcript_dir):
    for score in scores:
        f = transcript_dir / f"{score['task_id']}.json"
        if f.exists():
            data = json.loads(f.read_text(encoding="utf-8"))
            score["task_name"] = data.get("task_name", "")
            score["difficulty"] = data.get("difficulty", "")
            score["skills_involved"] = data.get("skills_involved", [])
            score["automated_score"] = data.get("automated_score", 0.0)
            score["automated_breakdown"] = data.get("automated_breakdown", {})
            score["combined_score"] = round(
                score["automated_score"] * 0.4 + score["claude_total"] * 0.6, 3)
    return scores


def main():
    output_dir = Path("results_qwen3.5-9b-v3")
    transcript_dir = output_dir / "transcripts"

    scores = build_scores()
    scores = merge_with_automated(scores, transcript_dir)

    json_path = output_dir / "claude_manual_scores.json"
    json_path.write_text(json.dumps(scores, ensure_ascii=False, indent=2))
    print(f"Scores: {json_path}")

    # Generate report
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from claude_manual_scoring import generate_report
    report = generate_report(scores)
    report = report.replace("deepseek-chat", "Qwen3.5-9B v3 (with TOOLS.md optimization)")
    report = report.split("## Conclusions")[0] + """## Conclusions

- **Overall**: Qwen3.5-9B v3 是 Qwen 系列最佳表现，TOOLS.md 优化效果显著
- **对比 v1→v3 进化**: Auto 77.2%→90.5%(+13.3%), 多个关键任务从 0 分修复为满分
- **修复的关键任务**: location(v1/v2都0分)、video_list、calendar_weather、leave_home
- **L1 查询**: 96.4% auto，几乎追平 deepseek-chat(96.4%)
- **L5 工作流**: 95.0% auto，大幅超越 v1(73.3%)和 v2(70.0%)
- **持续问题**: processes 仍用 ps aux、install_package 仍用 pip、calendar_reminder 完全失败
- **效率仍是短板**: 部分任务步骤过多(silent_volume 26步, focus_mode 13步)
- **与 deepseek-chat 的差距从 22% 缩小到 ~8%**
"""
    report_path = output_dir / "claude_manual_report.md"
    report_path.write_text(report)
    print(f"Report: {report_path}")

    # All models comparison
    all_results = []
    for name, path in [
        ("deepseek-chat", "results/claude_manual_scores.json"),
        ("Qwen 9B v1", "results_qwen3.5-9b/claude_manual_scores.json"),
        ("Qwen 9B v2", "results_qwen3.5-9b-v2/claude_manual_scores.json"),
        ("Qwen 4B", "results_qwen3.5-4b/claude_manual_scores.json"),
        ("Qwen 9B v3", "results_qwen3.5-9b-v3/claude_manual_scores.json"),
    ]:
        p = Path(path)
        if p.exists():
            all_results.append((name, json.loads(p.read_text())))

    def avg(s, k): return sum(x.get(k, 0) for x in s) / len(s)
    def davg(s, d): return sum(x["claude_scores"][d] for x in s) / len(s)

    print(f"\n{'Model':<28} {'Auto':<8} {'Claude':<8} {'Combined':<10} {'完成':<6} {'工具':<6} {'质量':<6} {'效率':<6}")
    print("-" * 88)
    for name, s in all_results:
        print(f"{name:<28} {avg(s,'automated_score'):<8.1%} {avg(s,'claude_total'):<8.1%} {avg(s,'combined_score'):<10.1%} "
              f"{davg(s,'task_completion'):<6.1%} {davg(s,'tool_usage'):<6.1%} {davg(s,'response_quality'):<6.1%} {davg(s,'efficiency'):<6.1%}")


if __name__ == "__main__":
    main()
