#!/usr/bin/env python3
"""Claude manual scoring for Qwen3.5-4B."""
import json
from pathlib import Path

MANUAL_SCORES = [
    # === L1 ===
    ("task_23_pcsim_weather_query", 1.0, 1.0, 1.0, 0.9,
     "read→set_location→get_current，3步。额外调了set_location是谨慎行为。回复清晰。"),
    ("task_24_pcsim_battery_status", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。"),
    ("task_25_pcsim_contacts_list", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。回复格式优秀。"),
    ("task_26_pcsim_email_inbox", 1.0, 0.8, 1.0, 0.7,
     "第一步猜错(email_list_inbox缺pc_前缀)，读SKILL.md后成功。3步。"),
    ("task_27_pcsim_volume_check", 1.0, 0.9, 1.0, 0.8,
     "memory_search(多余)→get_all_streams。用了更全面的API，回复表格清晰，还解释了媒体音量含义。"),
    ("task_28_pcsim_alarm_list", 1.0, 0.8, 1.0, 0.7,
     "第一步猜错(pc_alarm_get 100)，读SKILL.md后用了pc_alarm_list 100（多余参数）但成功。回复详细。"),
    ("task_29_pcsim_location", 1.0, 0.8, 0.9, 0.7,
     "第一步猜错(pc_map_location_get)，读SKILL.md后成功。回复包含坐标信息。比9B系列的0分大幅改善！"),
    ("task_30_pcsim_notifications", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。回复结构清晰还主动提供后续操作建议。"),
    ("task_31_pcsim_bluetooth_list", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。信息准确无编造。"),
    ("task_32_pcsim_sensor_temp", 1.0, 0.8, 1.0, 0.4,
     "6步偏多：前几步猜错参数(--sensor_name temp而非temperature)，反复尝试。最终成功。"),
    ("task_33_pcsim_video_list", 0.0, 0.0, 0.5, 0.0,
     "完全失败。用了web_search搜索2026热门电影，没调用pc-sim工具。输出了影视推荐而非模拟器视频列表。"),
    ("task_34_pcsim_device_info", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。表格展示模拟器配置。"),
    ("task_35_pcsim_processes", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用pc_shell_list_processes，2步完美！比9B系列（用ps aux获取真实进程）好得多。"),
    ("task_36_pcsim_files", 1.0, 1.0, 1.0, 0.6,
     "4步全部用pc_file_manager_list，没有用真实系统命令。比9B v2（用tree）好。但4步逐层探索效率一般。"),

    # === L2 ===
    ("task_37_pcsim_create_contact", 0.3, 0.0, 0.5, 0.0,
     "只用了write()写文件，没有调用pc_contacts_create。完全错误的方式。"),
    ("task_38_pcsim_create_alarm", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。"),
    ("task_39_pcsim_create_memo", 1.0, 0.8, 1.0, 0.7,
     "第一步猜错(memo_create缺pc_前缀)，读SKILL.md后成功。用对了pc_memo_create而非notes！"),
    ("task_40_pcsim_set_brightness", 1.0, 0.6, 0.8, 0.2,
     "7步极低效：前6步猜各种格式(brightness_set, pc-display-set-brightness, ls/find查找工具)。最终成功但过程很差。"),
    ("task_41_pcsim_payment", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。回复包含交易详情。"),
    ("task_42_pcsim_dark_theme", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。"),
    ("task_43_pcsim_open_browser", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用含完整URL，2步完美。"),
    ("task_44_pcsim_play_music", 0.7, 0.6, 0.5, 0.1,
     "15步极低效，反复尝试play。最终只添加到播放列表但未真正播放。回复说需要手动点播放按钮，任务未完全完成。"),
    ("task_45_pcsim_countdown", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。"),
    ("task_46_pcsim_take_photo", 1.0, 0.9, 1.0, 0.8,
     "第一步猜错(pc_camera_photo)，读SKILL.md后成功。3步可接受。比9B系列（11步暴力搜索或0步失败）好得多！"),
    ("task_47_pcsim_create_note", 1.0, 1.0, 1.0, 1.0,
     "read→正确调用，2步完美。"),
    ("task_48_pcsim_grant_permission", 1.0, 0.7, 1.0, 0.5,
     "5步：前3步猜错参数格式(provider vs provider_name)，读SKILL.md后成功。回复详细含JSON。"),

    # === L3 ===
    ("task_49_pcsim_create_and_group", 1.0, 1.0, 1.0, 1.0,
     "read→create→add_to_group，3步完美。"),
    ("task_50_pcsim_compose_send_email", 1.0, 0.8, 1.0, 0.6,
     "4步：先用memo_write记草稿→write文件→send→rm清理。过程曲折但最终正确发送。清理草稿是额外但合理操作。"),
    ("task_51_pcsim_record_audio", 1.0, 1.0, 1.0, 1.0,
     "read→start→stop，3步完美。"),
    ("task_52_pcsim_list_pin_memo", 1.0, 1.0, 1.0, 1.0,
     "read→list→pin，3步完美。"),
    ("task_53_pcsim_create_album_move", 1.0, 0.9, 1.0, 0.4,
     "10步。move_to_album参数反复尝试（中文名→英文名→album ID）。最终成功。"),
    ("task_54_pcsim_calendar_reminder", 0.2, 0.0, 0.3, 0.0,
     "完全失败。用了cron/memory_search/memory_get而非pc-sim工具。声称设置了提醒但实际没有调用任何calendar工具。"),
    ("task_55_pcsim_bluetooth_scan_pair", 1.0, 1.0, 1.0, 0.8,
     "5步：write(多余)→read→scan→pair→connect。流程正确，额外做了connect是加分项。"),
    ("task_56_pcsim_pause_shuffle", 1.0, 1.0, 1.0, 1.0,
     "read→pause→shuffle，3步完美。"),

    # === L4 ===
    ("task_57_pcsim_find_and_call", 1.0, 1.0, 1.0, 0.9,
     "4步：read两个SKILL.md→search→dial。高效跨技能协调。"),
    ("task_58_pcsim_calendar_weather", 0.5, 0.1, 0.7, 0.1,
     "8步。用了cron和web_search/web_fetch获取真实天气而非pc-sim。没有调用calendar和weather工具。天气信息来自真实网站不是模拟器。"),
    ("task_59_pcsim_forward_email", 1.0, 0.9, 1.0, 0.8,
     "4步：read→search(失败)→list_inbox→forward。正确完成转发。比9B用了正确的david@邮箱。"),
    ("task_60_pcsim_screenshot_transfer", 1.0, 0.8, 1.0, 0.4,
     "8步。截屏和传输成功，但中间探索了文件路径(cat/ls/find)。结果正确效率一般。"),
    ("task_61_pcsim_silent_volume", 1.0, 0.7, 0.9, 0.2,
     "18步极低效：反复猜静音命令格式。最终成功但过程太曲折。"),
    ("task_62_pcsim_directions_memo", 1.0, 0.9, 1.0, 0.5,
     "8步。前两步猜错，读SKILL.md后成功。用了正确的pc_memo_create。"),
    ("task_63_pcsim_reply_email", 1.0, 0.8, 1.0, 0.7,
     "4步。第一步猜错(pc_email_inbox)，读SKILL.md后成功。"),
    ("task_64_pcsim_install_package", 1.0, 1.0, 1.0, 1.0,
     "read→get_python_version→install_package，3步完美。"),

    # === L5 ===
    ("task_65_pcsim_morning_routine", 0.5, 0.3, 0.7, 0.2,
     "3步但都猜错：alarm_set→web_search(真实天气)→cron。没有使用pc-sim的alarm/weather/calendar工具。部分信息来自真实网络。"),
    ("task_66_pcsim_meeting_prep", 0.4, 0.3, 0.4, 0.3,
     "2步。read SKILL.md后直接compose邮件，但没先查日历找会议详情、没查David邮箱（用了错误的邮箱）。流程不完整。"),
    ("task_67_pcsim_leave_home", 0.5, 0.3, 0.5, 0.1,
     "37步极度低效。前4步猜错后陷入暴力尝试。最终只完成了屏幕超时和静音，省电和清通知失败。"),
    ("task_68_pcsim_backup", 1.0, 0.9, 1.0, 0.5,
     "10步。get_info→list_packages→export_contacts成功。中间第一步猜错，有些探索步骤。整体完成。"),
    ("task_69_pcsim_focus_mode", 1.0, 0.8, 1.0, 0.3,
     "15步。memory_search(多余)，第一步猜错。读4个SKILL.md后逐个完成4个子任务。效率低但全部成功。"),

    # === L6 ===
    ("task_70_pcsim_delete_nonexistent", 1.0, 0.8, 1.0, 0.7,
     "5步。第一步猜错(contacts_delete_contact)，读SKILL.md后search+list确认不存在。"),
    ("task_71_pcsim_offline_device", 1.0, 0.8, 1.0, 0.5,
     "6步。前两步猜错，读SKILL.md后正确调用list_devices→sync→list。识别到离线状态给出建议。比9B v2好。"),
    ("task_72_pcsim_uninstall_system", 1.0, 1.0, 1.0, 1.0,
     "read→list_installed，正确识别系统应用无法卸载。回复解释充分。"),
    ("task_73_pcsim_stop_no_recording", 1.0, 1.0, 1.0, 1.0,
     "1步直接调用pc_recorder_stop，完美。"),
    ("task_74_pcsim_insufficient_funds", 0.0, 0.0, 0.3, 0.0,
     "完全失败。0步工具调用，直接反问用户是不是模拟环境，要确认朋友账户信息。没有调用pc_payment_get_balance。"),
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
    output_dir = Path("results_qwen3.5-4b")
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
    report = report.replace("deepseek-chat", "Qwen3.5-4B (local-vllm, with TOOLS.md optimization)")

    # Fix conclusions
    auto_avg = sum(s.get("automated_score", 0) for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s.get("combined_score", 0) for s in scores) / len(scores)

    report = report.split("## Conclusions")[0] + f"""## Conclusions

- **Overall**: Qwen3.5-4B 综合得分 {combined_avg:.1%}，automated {auto_avg:.1%}
- **对比 9B v2 (79.6%)**: 4B 在 TOOLS.md 优化后表现持平甚至更好，说明 prompt 工程比模型大小更重要
- **亮点**: location 任务首次通过（9B 两个版本都 0 分）、processes 用对了 pc-sim 工具（9B 用真实 ps aux）
- **仍存在问题**: 播放音乐(15步)、调亮度(7步)、静音(18步)等任务效率极低；calendar_reminder 和 insufficient_funds 完全失败
- **小模型特有问题**: video_list 用 web_search 搜影视推荐、morning_routine 用真实天气网站，模拟器与真实环境边界模糊
"""

    report_path = output_dir / "claude_manual_report.md"
    report_path.write_text(report)
    print(f"Report: {report_path}")

    # All models comparison
    ds = json.loads(Path("results/claude_manual_scores.json").read_text())
    v1 = json.loads(Path("results_qwen3.5-9b/claude_manual_scores.json").read_text())
    v2 = json.loads(Path("results_qwen3.5-9b-v2/claude_manual_scores.json").read_text())

    def avg(s, k): return sum(x.get(k, 0) for x in s) / len(s)
    def davg(s, d): return sum(x["claude_scores"][d] for x in s) / len(s)

    print(f"\n{'Model':<28} {'Auto':<8} {'Claude':<8} {'Combined':<10} {'完成':<6} {'工具':<6} {'质量':<6} {'效率':<6}")
    print("-" * 88)
    for name, s in [("deepseek-chat", ds), ("Qwen 9B v1", v1), ("Qwen 9B v2", v2), ("Qwen 4B + TOOLS.md", scores)]:
        print(f"{name:<28} {avg(s,'automated_score'):<8.1%} {avg(s,'claude_total'):<8.1%} {avg(s,'combined_score'):<10.1%} "
              f"{davg(s,'task_completion'):<6.1%} {davg(s,'tool_usage'):<6.1%} {davg(s,'response_quality'):<6.1%} {davg(s,'efficiency'):<6.1%}")


if __name__ == "__main__":
    main()
