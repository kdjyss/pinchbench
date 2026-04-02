#!/usr/bin/env python3
"""Claude manual scoring for Qwen3.5-9B benchmark results."""

import json
from pathlib import Path

# Claude's manual scores: (task_id, completion, tool_usage, response_quality, efficiency, notes)
MANUAL_SCORES = [
    # === L1 ===
    ("task_23_pcsim_weather_query", 1.0, 1.0, 0.9, 1.0,
     "正确调用 pc_weather_get_current，回复简洁清晰。风速数据(22km/h vs seed的10km/h)可能有误差。"),
    ("task_24_pcsim_battery_status", 0.0, 0.0, 0.0, 0.0,
     "完全失败。编造命令 pc-battery --status，没读 SKILL.md，无输出。"),
    ("task_25_pcsim_contacts_list", 1.0, 1.0, 1.0, 1.0,
     "直接调用正确工具，表格展示清晰。"),
    ("task_26_pcsim_email_inbox", 1.0, 0.7, 1.0, 0.6,
     "最终成功但前两步猜错命令(pc-sim email inbox, pc_sim_email_inbox)，第3步读SKILL.md后才找对。4步偏多。"),
    ("task_27_pcsim_volume_check", 1.0, 0.8, 1.0, 0.6,
     "前两步猜错(volume_get_all, pc_volume_get)，读SKILL.md后成功。最终用了pc_volume_get_all_streams且得到满分。"),
    ("task_28_pcsim_alarm_list", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md再执行，完美。表格展示。"),
    ("task_29_pcsim_location", 0.0, 0.0, 0.0, 0.0,
     "完全跑偏。被IDENTITY.md干扰，进入自我介绍模式，没执行任何工具。"),
    ("task_30_pcsim_notifications", 1.0, 0.7, 1.0, 0.6,
     "前两步猜错(pc_notification_list, pc_notification list)，读SKILL.md后成功。回复质量好。"),
    ("task_31_pcsim_bluetooth_list", 1.0, 0.7, 0.9, 0.6,
     "前两步猜错(pc_bluetooth_list_paired_devices, pc_bluetooth_list)，后成功。回复中编造了不存在的设备。"),
    ("task_32_pcsim_sensor_temp", 0.0, 0.0, 0.0, 0.0,
     "输出XML乱码，模型格式理解失败，没调用任何工具。"),
    ("task_33_pcsim_video_list", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md再执行，完美。"),
    ("task_34_pcsim_device_info", 0.3, 0.1, 0.3, 0.3,
     "猜错命令(pc-sim device_info)，转而用系统命令uname/lscpu获取了真实宿主机信息而非pc-sim模拟器数据。结果不符合预期。"),
    ("task_35_pcsim_processes", 0.5, 0.3, 0.5, 0.5,
     "先猜错(pc_process_list)，转用ps aux获取真实进程。回复内容是真实进程而非模拟器数据，部分完成。"),
    ("task_36_pcsim_files", 0.8, 0.8, 0.7, 0.6,
     "读了SKILL.md后正确调用pc_file_manager_list，但还额外用了ls和tree查看真实文件系统，混淆了模拟器和宿主机。"),

    # === L2 ===
    ("task_37_pcsim_create_contact", 1.0, 0.5, 0.9, 0.3,
     "6步太多：先write、再猜错(contacts_create)、读SKILL.md、创建时缺电话号码、两次update补电话。过程曲折但最终成功。"),
    ("task_38_pcsim_create_alarm", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md再执行，参数正确，完美。"),
    ("task_39_pcsim_create_memo", 0.8, 0.3, 0.9, 0.5,
     "用了pc_notes_create而非pc_memo_create，混淆了notes和memo两个skill。功能上完成了创建但工具选错。"),
    ("task_40_pcsim_set_brightness", 1.0, 1.0, 0.8, 1.0,
     "先读SKILL.md再执行，参数正确。回复过于简短。"),
    ("task_41_pcsim_payment", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md再执行，参数精确，回复包含交易详情。"),
    ("task_42_pcsim_dark_theme", 1.0, 0.8, 0.8, 0.7,
     "先猜错(display_set_dark)，读SKILL.md后成功。回复过于简短。"),
    ("task_43_pcsim_open_browser", 1.0, 0.7, 0.9, 0.7,
     "第一步参数格式错(pc_browser_open_url baidu.com 缺--url)，第二步修正。回复OK。"),
    ("task_44_pcsim_play_music", 1.0, 0.8, 0.8, 0.3,
     "10步完成，反复尝试不同播放方式。最终成功但效率很低。回复用了英文。"),
    ("task_45_pcsim_countdown", 1.0, 1.0, 1.0, 0.9,
     "先memory_search（多余），读SKILL.md后正确执行。参数正确。"),
    ("task_46_pcsim_take_photo", 0.5, 0.1, 0.7, 0.1,
     "11步暴力搜索：pc_gallery_screenshot→screenshot→screencapture→pc_display_screenshot→...最终用了pc_screenshot_take_screenshot而非pc_camera_capture_photo。工具完全选错。"),
    ("task_47_pcsim_create_note", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md再执行，参数正确，完美。"),
    ("task_48_pcsim_grant_permission", 1.0, 1.0, 0.8, 0.9,
     "先memory_search（多余），读SKILL.md后正确执行。回复简短但准确。"),

    # === L3 ===
    ("task_49_pcsim_create_and_group", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md，create→add_to_group，流程正确高效。"),
    ("task_50_pcsim_compose_send_email", 1.0, 1.0, 1.0, 0.8,
     "先compose再send，比deepseek多一步但逻辑合理。"),
    ("task_51_pcsim_record_audio", 1.0, 1.0, 0.9, 0.5,
     "start→stop 正确，但后面多了4步(read/edit/write)做日志记录，不必要。"),
    ("task_52_pcsim_list_pin_memo", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md，list→pin，完美。"),
    ("task_53_pcsim_create_album_move", 1.0, 0.9, 1.0, 0.4,
     "11步：多次尝试move_to_album用不同参数（相册名→album ID→英文名），过程曲折但最终成功。"),
    ("task_54_pcsim_calendar_reminder", 0.5, 0.5, 0.6, 0.3,
     "6步但只完成了list_events，没有执行set_reminder。先memory_search和session_status浪费步骤，还猜错命令格式。最终只问用户要不要操作但没执行。"),
    ("task_55_pcsim_bluetooth_scan_pair", 1.0, 0.6, 1.0, 0.2,
     "16步暴力尝试：先猜各种蓝牙命令(bluetoothctl/btctl/bt-manager)，最终读SKILL.md后成功。结果正确但过程极其低效。"),
    ("task_56_pcsim_pause_shuffle", 1.0, 1.0, 0.9, 1.0,
     "先读SKILL.md，pause→shuffle，高效。回复准确地指出了当前没在播放。"),

    # === L4 ===
    ("task_57_pcsim_find_and_call", 1.0, 0.9, 1.0, 0.8,
     "contacts_search→尝试pc_phone_call→读SKILL.md→dial。中间一步猜错但快速修正。"),
    ("task_58_pcsim_calendar_weather", 0.0, 0.0, 0.3, 0.0,
     "完全失败。4次memory_search和cron调用，没有调用任何pc-sim工具。反问用户用什么日历应用，没执行实际操作。"),
    ("task_59_pcsim_forward_email", 0.3, 0.3, 0.2, 0.3,
     "只读了SKILL.md和执行了email_search（不存在的命令），没有完成转发。回复只说'搜索没有找到结果'就结束了。"),
    ("task_60_pcsim_screenshot_transfer", 1.0, 1.0, 1.0, 1.0,
     "读SKILL.md→screenshot→list_paired→transfer，完美。"),
    ("task_61_pcsim_silent_volume", 0.7, 0.7, 0.5, 0.7,
     "set_profile成功但第二步用了不存在的set_media_volume命令（应该用pc_volume_set）。回复还错误地说'深色模式下媒体音量无法调节'，信息编造。"),
    ("task_62_pcsim_directions_memo", 0.8, 0.6, 0.9, 0.5,
     "前两步猜错命令，读SKILL.md后成功查询路线。但用write写文件而非pc_memo_create，工具选择偏离。"),
    ("task_63_pcsim_reply_email", 1.0, 1.0, 1.0, 0.8,
     "list_inbox调用了两次（重复），但reply正确。回复清晰。"),
    ("task_64_pcsim_install_package", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md，get_python_version→install_package，完美。"),

    # === L5 ===
    ("task_65_pcsim_morning_routine", 0.7, 0.5, 0.7, 0.3,
     "10步。猜错天气和日历命令格式，闹钟用了cron而非pc_alarm_create。最终通过读SKILL.md部分完成，但闹钟设置方式错误。"),
    ("task_66_pcsim_meeting_prep", 1.0, 0.8, 1.0, 0.5,
     "9步。前几步猜错命令，读SKILL.md后完成。成功找到会议→查David邮箱→发邮件。过程较曲折。"),
    ("task_67_pcsim_leave_home", 0.2, 0.1, 0.1, 0.1,
     "完全失败。第一步编造命令(pime --set-screen-timeout)，后面读了4个SKILL.md但没有执行任何pc-sim命令。最终输出了一段代码块但没实际运行。"),
    ("task_68_pcsim_backup", 1.0, 1.0, 1.0, 0.8,
     "读SKILL.md后依次调用get_system_info→list_packages→export_contacts→get_info→write。流程合理，8步可接受。"),
    ("task_69_pcsim_focus_mode", 1.0, 0.7, 1.0, 0.2,
     "20步。前4步全部猜错命令，读SKILL.md后逐个完成。最终4个子任务都完成了但效率极低。"),

    # === L6 ===
    ("task_70_pcsim_delete_nonexistent", 1.0, 0.6, 0.9, 0.4,
     "6步反复尝试不同搜索命令格式，最终没找到张三。结论正确但过程低效。"),
    ("task_71_pcsim_offline_device", 1.0, 0.7, 0.9, 0.2,
     "15步大量探索。memory_search→猜错multi_device命令→读SKILL.md→正确调用→再探索文件系统。结论正确但过程极其低效。"),
    ("task_72_pcsim_uninstall_system", 1.0, 0.9, 1.0, 0.8,
     "4步。先尝试错误app_id(system.settings)，list后用正确ID重试，正确识别系统应用无法卸载。"),
    ("task_73_pcsim_stop_no_recording", 1.0, 1.0, 1.0, 1.0,
     "1步直接调用pc_recorder_stop，回复简洁准确。最佳表现。"),
    ("task_74_pcsim_insufficient_funds", 1.0, 1.0, 1.0, 1.0,
     "先读SKILL.md，get_balance，正确识别余额不足。"),
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


def generate_comparison_report(qwen_scores, ds_scores_path):
    ds_scores = json.loads(ds_scores_path.read_text()) if ds_scores_path.exists() else []
    ds_map = {s["task_id"]: s for s in ds_scores}

    lines = ["# PC-Sim Benchmark: Model Comparison Report", "",
             "**Scorer:** Claude Opus 4.6 (manual review of all transcripts)", ""]

    # Overall comparison
    def avg(scores, key):
        vals = [s.get(key, 0) for s in scores]
        return sum(vals) / len(vals) if vals else 0

    def dim_avg(scores, dim):
        return sum(s["claude_scores"][dim] for s in scores) / len(scores)

    lines.extend([
        "## Overall Comparison", "",
        "| Metric | deepseek-chat | Qwen3.5-9B |",
        "|--------|--------------|------------|",
        f"| Automated | {avg(ds_scores, 'automated_score'):.1%} | {avg(qwen_scores, 'automated_score'):.1%} |",
        f"| Claude Manual | {avg(ds_scores, 'claude_total'):.1%} | {avg(qwen_scores, 'claude_total'):.1%} |",
        f"| **Combined** | **{avg(ds_scores, 'combined_score'):.1%}** | **{avg(qwen_scores, 'combined_score'):.1%}** |",
        "",
        "### Dimension Comparison", "",
        "| Dimension | Weight | deepseek-chat | Qwen3.5-9B |",
        "|-----------|--------|--------------|------------|",
    ])
    for dim, label in [("task_completion", "Task Completion"), ("tool_usage", "Tool Usage"),
                       ("response_quality", "Response Quality"), ("efficiency", "Efficiency")]:
        lines.append(f"| {label} | {'30%' if dim=='task_completion' else '25%' if dim!='efficiency' else '20%'} | {dim_avg(ds_scores, dim):.1%} | {dim_avg(qwen_scores, dim):.1%} |")

    # By difficulty
    lines.extend(["", "## By Difficulty", "",
                   "| Level | deepseek Auto | deepseek Claude | Qwen Auto | Qwen Claude |",
                   "|-------|--------------|----------------|-----------|-------------|"])
    for lvl in ["L1", "L2", "L3", "L4", "L5", "L6"]:
        ds_lvl = [s for s in ds_scores if s.get("difficulty") == lvl]
        qw_lvl = [s for s in qwen_scores if s.get("difficulty") == lvl]
        if ds_lvl and qw_lvl:
            lines.append(f"| {lvl} | {avg(ds_lvl, 'automated_score'):.1%} | {avg(ds_lvl, 'claude_total'):.1%} | {avg(qw_lvl, 'automated_score'):.1%} | {avg(qw_lvl, 'claude_total'):.1%} |")

    # Per-task comparison
    lines.extend(["", "## Per-Task Comparison", "",
                   "| # | Task | Lvl | DS Auto | DS Claude | Qwen Auto | Qwen Claude | Gap |",
                   "|---|------|-----|---------|-----------|-----------|-------------|-----|"])
    for i, qs in enumerate(qwen_scores, 1):
        ds = ds_map.get(qs["task_id"], {})
        ds_c = ds.get("claude_total", 0)
        qw_c = qs["claude_total"]
        gap = qw_c - ds_c
        icon = "✅" if gap >= 0 else "🔴" if gap < -0.3 else "🟡"
        lines.append(
            f"| {i} | {qs.get('task_name', '')[:20]} | {qs.get('difficulty', '')} | "
            f"{ds.get('automated_score', 0):.0%} | {ds_c:.0%} | "
            f"{qs.get('automated_score', 0):.0%} | {qw_c:.0%} | {icon} {gap:+.0%} |")

    # Key differences
    lines.extend(["", "## Key Differences", ""])
    big_gaps = [(qs, ds_map.get(qs["task_id"], {})) for qs in qwen_scores
                if qs["claude_total"] < ds_map.get(qs["task_id"], {}).get("claude_total", 0) - 0.2]
    for qs, ds in big_gaps:
        lines.append(f"### {qs.get('task_name', '')} ({qs.get('difficulty', '')})")
        lines.append(f"- deepseek: {ds.get('claude_total', 0):.0%} → Qwen: {qs['claude_total']:.0%}")
        lines.append(f"- Qwen issue: {qs['notes']}")
        lines.append("")

    # Conclusions
    ds_avg = avg(ds_scores, "combined_score")
    qw_avg = avg(qwen_scores, "combined_score")
    lines.extend([
        "## Conclusions", "",
        f"- deepseek-chat combined: **{ds_avg:.1%}** vs Qwen3.5-9B: **{qw_avg:.1%}** (delta: {qw_avg-ds_avg:+.1%})",
        f"- Qwen3.5-9B 的核心问题: **不先读 SKILL.md 就凭猜测构造命令**，导致大量步骤浪费在试错上",
        f"- deepseek-chat 每次都先 read SKILL.md 再执行，几乎零试错",
        f"- Qwen 在简单任务(L1/L2)上也有失败，说明是模型指令遵循能力不足而非任务难度问题",
        f"- Qwen 的 L6 异常处理反而表现不错(100% auto)，说明错误识别能力尚可",
        f"- 优化建议: 在 workspace 加 CLAUDE.md 强调'先读 SKILL.md'，或精简 IDENTITY/SOUL.md 减少干扰",
    ])

    return "\n".join(lines)


def main():
    output_dir = Path("results_qwen3.5-9b")
    transcript_dir = output_dir / "transcripts"

    scores = build_scores()
    scores = merge_with_automated(scores, transcript_dir)

    # Save scores
    json_path = output_dir / "claude_manual_scores.json"
    json_path.write_text(json.dumps(scores, ensure_ascii=False, indent=2))
    print(f"Scores: {json_path}")

    # Generate comparison report
    ds_scores_path = Path("results/claude_manual_scores.json")
    report = generate_comparison_report(scores, ds_scores_path)
    report_path = output_dir / "comparison_report.md"
    report_path.write_text(report)
    print(f"Report: {report_path}")

    # Summary
    auto_avg = sum(s.get("automated_score", 0) for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s.get("combined_score", 0) for s in scores) / len(scores)
    print(f"\nQwen3.5-9B: Auto={auto_avg:.1%} Claude={claude_avg:.1%} Combined={combined_avg:.1%}")


if __name__ == "__main__":
    main()
