#!/usr/bin/env python3
"""Claude manual scoring for Qwen3.5-9B v2 (after openclaw updates)."""
import json
from pathlib import Path

MANUAL_SCORES = [
    # === L1 ===
    ("task_23_pcsim_weather_query", 1.0, 1.0, 1.0, 1.0,
     "完美。read SKILL.md → 正确调用，回复简洁准确。"),
    ("task_24_pcsim_battery_status", 1.0, 0.8, 1.0, 0.7,
     "v1的0分修复了。第一步猜错(pc-sim battery status)，读SKILL.md后成功。3步完成可接受。"),
    ("task_25_pcsim_contacts_list", 1.0, 0.7, 1.0, 0.4,
     "5步偏多：前3步猜错(pc_contacts list, contacts list, list-skills|grep)，读SKILL.md后成功。回复表格格式好。"),
    ("task_26_pcsim_email_inbox", 1.0, 0.8, 1.0, 0.7,
     "第一步猜错(pc_email_inbox)，读SKILL.md后成功。3步可接受。"),
    ("task_27_pcsim_volume_check", 1.0, 1.0, 0.9, 1.0,
     "1步直接调用 pc_volume_get，完美！v1需要4步。回复简洁但偏短。"),
    ("task_28_pcsim_alarm_list", 1.0, 1.0, 1.0, 1.0,
     "1步直接调用，表格展示，完美。"),
    ("task_29_pcsim_location", 0.0, 0.0, 0.2, 0.0,
     "仍然失败。只做了memory_search，没有调用任何pc-sim工具。反问用户位置信息而非查模拟器。"),
    ("task_30_pcsim_notifications", 1.0, 0.7, 1.0, 0.4,
     "5步：前3步猜错(push_notification list, list-skills|grep, push_notification list --user)。回复质量好。"),
    ("task_31_pcsim_bluetooth_list", 1.0, 0.8, 1.0, 0.7,
     "第一步猜错(pc_bluetooth_connected_devices)，读SKILL.md后成功。回复准确无编造。比v1改善。"),
    ("task_32_pcsim_sensor_temp", 1.0, 1.0, 1.0, 1.0,
     "v1的0分修复了。read SKILL.md → 正确调用，完美。"),
    ("task_33_pcsim_video_list", 1.0, 0.6, 1.0, 0.3,
     "6步太多：前5步全在猜(pc_video_player list, pc_video_info, -l|grep, --help, list-tools|grep)。最终成功但效率极低。"),
    ("task_34_pcsim_device_info", 1.0, 1.0, 1.0, 1.0,
     "v1的0分修复了。read SKILL.md → 正确调用，回复准确展示模拟器配置。"),
    ("task_35_pcsim_processes", 0.5, 0.3, 0.5, 0.5,
     "与v1相同问题：猜错(pc_process_list)后用ps aux获取真实进程。"),
    ("task_36_pcsim_files", 0.5, 0.3, 0.6, 0.3,
     "v1退步。直接用tree命令查看真实文件系统，没有调用pc_file_manager_list。混淆了模拟器和宿主机。"),

    # === L2 ===
    ("task_37_pcsim_create_contact", 1.0, 0.9, 1.0, 0.8,
     "比v1大幅改善(v1=6步)。memory_search(多余)→read→正确创建，3步。参数正确。"),
    ("task_38_pcsim_create_alarm", 1.0, 0.6, 1.0, 0.3,
     "7步太多：前5步猜各种格式(alarm_set, help, web_search, list-skills, alarm_set again)，读SKILL.md后成功。比v1(2步)严重退步。"),
    ("task_39_pcsim_create_memo", 1.0, 1.0, 1.0, 1.0,
     "v1的0分修复了！read SKILL.md → pc_memo_create，这次用对了工具。完美。"),
    ("task_40_pcsim_set_brightness", 1.0, 1.0, 0.8, 1.0,
     "read → 正确调用。回复过于简短但准确。"),
    ("task_41_pcsim_payment", 1.0, 0.7, 1.0, 0.5,
     "5步：memory_search(多余)→猜错(pay 200 --platform)→猜错(get_info)→read→成功。回复清晰。"),
    ("task_42_pcsim_dark_theme", 1.0, 1.0, 0.8, 1.0,
     "read → 正确调用，完美。回复简短。"),
    ("task_43_pcsim_open_browser", 1.0, 0.8, 1.0, 0.7,
     "v1修复：第一步猜错(browser_open_url)，读SKILL.md后成功。回复详细。"),
    ("task_44_pcsim_play_music", 1.0, 1.0, 1.0, 1.0,
     "大幅改善！read→list→play --track_id，3步精准完成。v1需要10步。"),
    ("task_45_pcsim_countdown", 1.0, 0.8, 1.0, 0.7,
     "第一步猜错(pc_timer_timershell)，读SKILL.md后成功。3步可接受。"),
    ("task_46_pcsim_take_photo", 0.0, 0.0, 0.0, 0.0,
     "完全失败。0步调用，无输出。比v1(11步暴力搜索)更差，这次连尝试都没有。"),
    ("task_47_pcsim_create_note", 1.0, 1.0, 1.0, 0.9,
     "read→create→tag，3步流程合理。额外调用tag补充标签是合理操作。"),
    ("task_48_pcsim_grant_permission", 0.0, 0.1, 0.0, 0.0,
     "v1满分现在变0分。猜错命令(system_permission_grant)，读SKILL.md后又猜(list-skills|grep)，最终输出HEARTBEAT_OK乱码。完全失败。"),

    # === L3 ===
    ("task_49_pcsim_create_and_group", 1.0, 1.0, 1.0, 1.0,
     "read→create→add_to_group，3步完美。"),
    ("task_50_pcsim_compose_send_email", 1.0, 1.0, 1.0, 1.0,
     "read→直接pc_email_send，2步完美。比v1(4步compose+send)更高效。"),
    ("task_51_pcsim_record_audio", 1.0, 1.0, 1.0, 1.0,
     "read→start→stop，3步完美。比v1(7步)大幅改善。"),
    ("task_52_pcsim_list_pin_memo", 1.0, 0.8, 1.0, 0.5,
     "6步：list后pin时猜错参数(--id vs --memo_id)两次，读SKILL.md后成功。"),
    ("task_53_pcsim_create_album_move", 1.0, 0.9, 1.0, 0.4,
     "9步。move_to_album参数反复尝试（中文名→英文名→album ID）。最终成功。"),
    ("task_54_pcsim_calendar_reminder", 1.0, 1.0, 1.0, 1.0,
     "v1的0.5修复为满分！read→list_events→set_reminder，3步完美。"),
    ("task_55_pcsim_bluetooth_scan_pair", 0.0, 0.0, 0.0, 0.0,
     "v1满分现在变0分。0步调用，无输出。完全失败。"),
    ("task_56_pcsim_pause_shuffle", 1.0, 0.8, 0.9, 0.5,
     "5步：前两步猜错(pc_music_pause, pc_music_shuffle)，读SKILL.md后成功。"),

    # === L4 ===
    ("task_57_pcsim_find_and_call", 1.0, 0.8, 1.0, 0.7,
     "5步。第一步猜错(contacts_get)，中间一步猜错(dial --contact_id)。最终正确拨号。"),
    ("task_58_pcsim_calendar_weather", 1.0, 0.8, 0.9, 0.5,
     "v1的0分修复了！7步偏多(session_status+2步猜错)，但成功获取日历和天气。回复有日期偏差但信息基本正确。"),
    ("task_59_pcsim_forward_email", 0.8, 0.7, 0.8, 0.7,
     "v1的0分改善。4步：search失败→list_inbox→forward。转发成功但用了错误邮箱(david.zhang@而非david@)。"),
    ("task_60_pcsim_screenshot_transfer", 1.0, 0.9, 1.0, 0.2,
     "18步极其低效：截屏和蓝牙传输成功，但中间大量探索(cat截图文件、find搜索、ls目录)。结果正确但过程臃肿。"),
    ("task_61_pcsim_silent_volume", 1.0, 1.0, 1.0, 0.9,
     "v1修复！4步：read两个SKILL.md→set_profile→volume_set，正确使用了两个skill。"),
    ("task_62_pcsim_directions_memo", 1.0, 1.0, 1.0, 0.9,
     "v1修复！4步：read→get_directions→read→memo_create。这次用了正确的pc_memo_create而非write文件。"),
    ("task_63_pcsim_reply_email", 1.0, 1.0, 1.0, 1.0,
     "read→list_inbox→reply，3步完美。"),
    ("task_64_pcsim_install_package", 0.3, 0.0, 0.5, 0.5,
     "v1满分现在变0分。直接用python3 --version和pip3 install，完全没用pc-sim工具。获取了真实系统Python版本而非模拟器。"),

    # === L5 ===
    ("task_65_pcsim_morning_routine", 1.0, 0.8, 1.0, 0.4,
     "v1修复为满分！10步偏多(前3步猜错)，但3个子任务全部完成。回复结构优秀。"),
    ("task_66_pcsim_meeting_prep", 1.0, 0.8, 1.0, 0.5,
     "8步。前两步猜错，读SKILL.md后完成。成功找会议→查邮箱→发邮件。"),
    ("task_67_pcsim_leave_home", 1.0, 0.8, 1.0, 0.3,
     "v1的0分修复了！12步偏多(前4步猜错)，但4个子任务全部完成。回复清晰。"),
    ("task_68_pcsim_backup", 0.5, 0.3, 0.5, 0.2,
     "v1退步。18步，用了真实系统命令(uname/rpm/dpkg)而非pc-sim工具。混淆了模拟器和宿主机。只有contacts_export用了pc-sim。"),
    ("task_69_pcsim_focus_mode", 0.0, 0.0, 0.2, 0.0,
     "v1满分现在变0分。11步全部失败：编造各种奇怪命令格式(parse_pcsim_launch, pc_display { json }, pc_audio play等)。Agent完全无法调用任何工具。"),

    # === L6 ===
    ("task_70_pcsim_delete_nonexistent", 1.0, 0.8, 1.0, 0.8,
     "4步。第一步猜错(contacts_delete_contact)，读SKILL.md后search+list确认不存在。比v1(6步)改善。"),
    ("task_71_pcsim_offline_device", 0.3, 0.2, 0.4, 0.3,
     "v1满分现在退步。1步猜错(multi_device list)后就放弃，没读SKILL.md。回复建议用AirDrop/iCloud，完全脱离pc-sim场景。"),
    ("task_72_pcsim_uninstall_system", 1.0, 1.0, 1.0, 1.0,
     "read→list_installed，正确识别系统应用无法卸载。回复解释充分。"),
    ("task_73_pcsim_stop_no_recording", 1.0, 0.7, 1.0, 0.6,
     "4步：前两步猜错(recorder_stop不带pc-sim前缀)，读SKILL.md后成功。"),
    ("task_74_pcsim_insufficient_funds", 1.0, 1.0, 1.0, 1.0,
     "read→get_balance，正确识别余额不足。完美。"),
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


def generate_report(scores):
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from claude_manual_scoring import generate_report as gen
    report = gen(scores)
    report = report.replace("deepseek-chat", "Qwen3.5-9B v2 (local-vllm, after openclaw updates)")

    # Fix conclusions
    auto_avg = sum(s.get("automated_score", 0) for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s.get("combined_score", 0) for s in scores) / len(scores)

    old_conclusions = report.split("## Conclusions\n")[-1]
    new_conclusions = f"""## Conclusions

- **Overall**: Qwen3.5-9B v2 综合得分 {combined_avg:.1%}，相比 v1 (75.9%) 有所提升
- **v1→v2 改善**: 12 个任务改善（含 6 个从 0 分修复），主要受益于 BOOTSTRAP.md 删除和 IDENTITY.md 精简
- **v1→v2 退步**: 7 个任务退步（含 4 个从满分跌到 0 分），体现小模型的不稳定性
- **持续问题**: 不先读 SKILL.md 就猜命令仍是核心瓶颈，几乎所有非满分任务都有这个特征
- **模拟器混淆**: 部分任务仍会用系统命令(ps/tree/pip)替代 pc-sim 工具
- **与 deepseek-chat (98.3%) 的差距**: 主要在工具使用准确性和效率上，任务理解能力差距不大
"""
    report = report.split("## Conclusions")[0] + new_conclusions
    return report


def main():
    output_dir = Path("results_qwen3.5-9b-v2")
    transcript_dir = output_dir / "transcripts"

    scores = build_scores()
    scores = merge_with_automated(scores, transcript_dir)

    json_path = output_dir / "claude_manual_scores.json"
    json_path.write_text(json.dumps(scores, ensure_ascii=False, indent=2))
    print(f"Scores: {json_path}")

    report = generate_report(scores)
    report_path = output_dir / "claude_manual_report.md"
    report_path.write_text(report)
    print(f"Report: {report_path}")

    # 三版对比摘要
    ds = json.loads(Path("results/claude_manual_scores.json").read_text())
    v1 = json.loads(Path("results_qwen3.5-9b/claude_manual_scores.json").read_text())

    def avg(s, k): return sum(x.get(k, 0) for x in s) / len(s)
    def davg(s, d): return sum(x["claude_scores"][d] for x in s) / len(s)

    print(f"\n{'Model':<25} {'Auto':<8} {'Claude':<8} {'Combined':<10} {'完成':<6} {'工具':<6} {'质量':<6} {'效率':<6}")
    print("-" * 85)
    for name, s in [("deepseek-chat", ds), ("Qwen v1", v1), ("Qwen v2", scores)]:
        print(f"{name:<25} {avg(s,'automated_score'):<8.1%} {avg(s,'claude_total'):<8.1%} {avg(s,'combined_score'):<10.1%} "
              f"{davg(s,'task_completion'):<6.1%} {davg(s,'tool_usage'):<6.1%} {davg(s,'response_quality'):<6.1%} {davg(s,'efficiency'):<6.1%}")


if __name__ == "__main__":
    main()
