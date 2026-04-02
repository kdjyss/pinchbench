#!/usr/bin/env python3
"""Claude manual scoring for smart-router/auto."""
import json
from pathlib import Path

MANUAL_SCORES = [
    # === L1 ===
    ("task_23_pcsim_weather_query", 0.8, 0.0, 1.0, 0.8,
     "没用pc-sim，用web_search+web_fetch查了真实天气。回复信息丰富但完全绕过了模拟器。"),
    ("task_24_pcsim_battery_status", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_25_pcsim_contacts_list", 1.0, 1.0, 1.0, 1.0, "1步直接调用，完美。"),
    ("task_26_pcsim_email_inbox", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_27_pcsim_volume_check", 1.0, 1.0, 1.0, 1.0, "1步直接调用pc_volume_get，完美。"),
    ("task_28_pcsim_alarm_list", 1.0, 1.0, 1.0, 1.0, "1步直接调用，完美。"),
    ("task_29_pcsim_location", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_30_pcsim_notifications", 1.0, 0.8, 1.0, 0.6, "4步。前两步猜错，读SKILL.md后成功。表格展示。"),
    ("task_31_pcsim_bluetooth_list", 1.0, 0.9, 1.0, 0.8, "3步。第一步猜错(pc_bluetooth_list)，读SKILL.md后成功。"),
    ("task_32_pcsim_sensor_temp", 1.0, 1.0, 1.0, 0.9, "3步。先list_sensors再read，稍多但合理。"),
    ("task_33_pcsim_video_list", 1.0, 0.9, 1.0, 0.8, "3步。第一步猜错(pc_video_player_library)，读SKILL.md后成功。"),
    ("task_34_pcsim_device_info", 0.3, 0.1, 0.3, 0.3, "猜错(pc_device_info, pc_device_list)后用uname/lscpu/lspci获取真实系统信息。混淆模拟器和宿主机。"),
    ("task_35_pcsim_processes", 0.5, 0.2, 0.5, 0.4, "猜错(pc_shell_processlist, pc_shell pkill)后用ps aux。混淆模拟器。"),
    ("task_36_pcsim_files", 0.5, 0.2, 0.6, 0.4, "猜错(pc_file_manager_list_root)后用ls和tree。混淆模拟器。"),

    # === L2 ===
    ("task_37_pcsim_create_contact", 1.0, 0.9, 1.0, 0.8, "3步。read后create缺电话→update补上。过程曲折但正确。"),
    ("task_38_pcsim_create_alarm", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_39_pcsim_create_memo", 1.0, 1.0, 1.0, 1.0, "read→正确调用pc_memo_create，2步完美。"),
    ("task_40_pcsim_set_brightness", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_41_pcsim_payment", 1.0, 0.9, 1.0, 0.8, "3步。第一步猜错(pc_payment_alipay_transfer)，读后成功。"),
    ("task_42_pcsim_dark_theme", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_43_pcsim_open_browser", 1.0, 0.7, 1.0, 0.5, "4步。前两步猜错(pc_browser_url, pc_web_url)，读后成功。"),
    ("task_44_pcsim_play_music", 1.0, 0.9, 1.0, 0.7, "5步。前两步猜错(play \"Summer Breeze\", add_queue)，读后list→play成功。"),
    ("task_45_pcsim_countdown", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_46_pcsim_take_photo", 1.0, 1.0, 1.0, 1.0, "read→正确调用pc_camera_capture_photo，2步完美。"),
    ("task_47_pcsim_create_note", 1.0, 1.0, 1.0, 0.9, "3步。read两个SKILL.md后正确调用。"),
    ("task_48_pcsim_grant_permission", 1.0, 0.7, 1.0, 0.5, "4步。猜错→web_search→读→成功。用了web搜索很奇怪。"),

    # === L3 ===
    ("task_49_pcsim_create_and_group", 1.0, 0.9, 1.0, 0.8, "4步。中间多创建了一个work组(不必要)。"),
    ("task_50_pcsim_compose_send_email", 1.0, 1.0, 1.0, 0.9, "3步。compose→send，逻辑合理。"),
    ("task_51_pcsim_record_audio", 1.0, 1.0, 1.0, 0.9, "3步。start→stop→stop(重复一次)。"),
    ("task_52_pcsim_list_pin_memo", 1.0, 0.8, 1.0, 0.6, "5步。pin参数猜错两次(m002, --pinned 1)，读后成功。"),
    ("task_53_pcsim_create_album_move", 1.0, 0.8, 0.9, 0.4, "7步。move_to_album猜错参数多次，创建了两个相册(旅行2026+travel2026)。回复说缓存问题。"),
    ("task_54_pcsim_calendar_reminder", 1.0, 0.8, 1.0, 0.5, "6步。memory_search+web_search(多余)，猜错calendar命令，读后成功。"),
    ("task_55_pcsim_bluetooth_scan_pair", 1.0, 1.0, 1.0, 1.0, "read→scan→pair，3步完美。"),
    ("task_56_pcsim_pause_shuffle", 1.0, 1.0, 1.0, 1.0, "read→pause→shuffle，3步完美。"),

    # === L4 ===
    ("task_57_pcsim_find_and_call", 1.0, 0.7, 1.0, 0.5, "6步。猜错3次(contacts_get, call_dial, phone_call_call)，读后成功。"),
    ("task_58_pcsim_calendar_weather", 0.6, 0.4, 0.7, 0.3, "7步。calendar_list_events成功，但天气用了web_search+web_fetch查真实天气而非pc-sim。混合使用了模拟器和真实数据。回复说明天没有会议（错误）。"),
    ("task_59_pcsim_forward_email", 0.8, 0.7, 0.9, 0.5, "6步。search多次失败，list_inbox找到后forward成功。但转发邮箱用了david.zhang@而非david@。"),
    ("task_60_pcsim_screenshot_transfer", 0.6, 0.5, 0.6, 0.2, "18步极低效。截屏成功但大量猜错命令。蓝牙传输部分声称无法传输图片文件（错误），只发了文本描述。"),
    ("task_61_pcsim_silent_volume", 1.0, 0.7, 1.0, 0.2, "14步极低效。反复猜静音命令。最终成功。"),
    ("task_62_pcsim_directions_memo", 1.0, 1.0, 1.0, 0.9, "4步。read→get_directions→read→memo_create，高效。"),
    ("task_63_pcsim_reply_email", 1.0, 0.8, 1.0, 0.6, "5步。前两步猜错(mail inbox, pc_email_inbox)，读后成功。回复用英文'see you tomorrow'而非中文。"),
    ("task_64_pcsim_install_package", 1.0, 1.0, 1.0, 1.0, "read→get_python_version→install_package，3步完美。"),

    # === L5 ===
    ("task_65_pcsim_morning_routine", 0.2, 0.1, 0.2, 0.1, "8步。用cron设闹钟(错)，web_search查天气(非pc-sim)，sessions_spawn查日历(失败)。3个子任务都没正确完成。"),
    ("task_66_pcsim_meeting_prep", 1.0, 0.8, 1.0, 0.4, "13步偏多。前几步猜错，最终找到会议→查David邮箱→发邮件。全部成功。"),
    ("task_67_pcsim_leave_home", 1.0, 1.0, 1.0, 0.8, "8步。读4个SKILL.md后4步精准完成。高效。"),
    ("task_68_pcsim_backup", 1.0, 0.9, 1.0, 0.5, "10步。第一步猜错。get_info→list_packages→export_contacts→write。完成。"),
    ("task_69_pcsim_focus_mode", 0.9, 0.7, 1.0, 0.3, "23步极低效。前几步猜错大量命令。4个子任务基本完成(dnd→brightness→play→countdown)。"),

    # === L6 ===
    ("task_70_pcsim_delete_nonexistent", 1.0, 0.9, 1.0, 0.9, "2步。memory_search(多余)→list确认不存在。高效。"),
    ("task_71_pcsim_offline_device", 1.0, 0.9, 1.0, 0.4, "10步。正确识别平板离线，但大量探索(list_albums/list_photos/send多次)。最终发到手机上，是合理的替代方案。"),
    ("task_72_pcsim_uninstall_system", 1.0, 0.7, 1.0, 0.3, "10步。前6步猜各种命令(list, --help, list-skills多次)。最终识别系统应用无法卸载。"),
    ("task_73_pcsim_stop_no_recording", 1.0, 1.0, 1.0, 1.0, "read→正确调用，2步完美。"),
    ("task_74_pcsim_insufficient_funds", 1.0, 1.0, 1.0, 1.0, "read→get_balance，2步完美。"),
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
    output_dir = Path("results_smartrouter")
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
    report = report.replace("deepseek-chat", "smart-router/auto")
    report = report.split("## Conclusions")[0] + """## Conclusions

- **Overall**: smart-router/auto 综合表现接近 Qwen 9B v3，automated 88.9%
- **亮点**: L3 多步任务 100% 满分，L6 异常处理 100% 满分，leave_home 一次通过
- **问题**: weather_query 用了 web_search 而非 pc-sim，device_info/processes/files 用系统命令混淆模拟器
- **效率短板**: silent_volume(14步)、focus_mode(23步)、screenshot_transfer(18步)
- **智能路由特点**: 部分任务自动选择了 web 工具而非 pc-sim，说明路由策略对模拟器场景不够精准
"""
    report_path = output_dir / "claude_manual_report.md"
    report_path.write_text(report)
    print(f"Report: {report_path}")

    # Full comparison
    all_results = []
    for name, path in [
        ("deepseek-chat", "results/claude_manual_scores.json"),
        ("Qwen 9B v1", "results_qwen3.5-9b/claude_manual_scores.json"),
        ("Qwen 9B v2", "results_qwen3.5-9b-v2/claude_manual_scores.json"),
        ("Qwen 4B", "results_qwen3.5-4b/claude_manual_scores.json"),
        ("Qwen 9B v3", "results_qwen3.5-9b-v3/claude_manual_scores.json"),
        ("smart-router", "results_smartrouter/claude_manual_scores.json"),
    ]:
        p = Path(path)
        if p.exists():
            all_results.append((name, json.loads(p.read_text())))

    def avg(s, k): return sum(x.get(k, 0) for x in s) / len(s)
    def davg(s, d): return sum(x["claude_scores"][d] for x in s) / len(s)

    print(f"\n{'Model':<20} {'Auto':<8} {'Claude':<8} {'Combined':<10} {'完成':<6} {'工具':<6} {'质量':<6} {'效率':<6}")
    print("-" * 82)
    for name, s in all_results:
        print(f"{name:<20} {avg(s,'automated_score'):<8.1%} {avg(s,'claude_total'):<8.1%} {avg(s,'combined_score'):<10.1%} "
              f"{davg(s,'task_completion'):<6.1%} {davg(s,'tool_usage'):<6.1%} {davg(s,'response_quality'):<6.1%} {davg(s,'efficiency'):<6.1%}")


if __name__ == "__main__":
    main()
