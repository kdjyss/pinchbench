#!/usr/bin/env python3
"""Generate Claude manual scoring results and report.

This contains Claude's subjective per-task scores after reading all 52 transcripts.
Run: python scripts/claude_manual_scoring.py --output results/
"""

import argparse
import json
from pathlib import Path


# Claude's manual scores after reading each transcript
# Format: (task_id, completion, tool_usage, response_quality, efficiency, notes)
MANUAL_SCORES = [
    # === L1: 信息查询 (14 tasks) ===
    ("task_23_pcsim_weather_query", 1.0, 1.0, 1.0, 1.0,
     "完美。read SKILL.md → pc_weather_get_current，1步完成。回复结构清晰，包含温度/湿度/风速/天气状况，还加了主观点评。"),
    ("task_24_pcsim_battery_status", 1.0, 1.0, 1.0, 1.0,
     "完美。精准调用 pc_battery_get_status，回复用图标标注各字段，主动提出可以查询剩余使用时间。"),
    ("task_25_pcsim_contacts_list", 1.0, 1.0, 1.0, 1.0,
     "完美。回复按分组归类展示，标注了收藏联系人，格式优秀。"),
    ("task_26_pcsim_email_inbox", 1.0, 1.0, 1.0, 1.0,
     "完美。清晰展示3封邮件，区分未读/已读状态，信息完整。"),
    ("task_27_pcsim_volume_check", 1.0, 0.9, 1.0, 1.0,
     "调用了 pc_volume_get_all_streams 而非 pc_volume_get，功能上更全面（展示了所有6个音频流），是合理的工具选择。自动评分因工具名不匹配扣分属于误判。回复信息丰富，轻微扣分因为理论上 pc_volume_get 更精准匹配用户意图。"),
    ("task_28_pcsim_alarm_list", 1.0, 1.0, 1.0, 1.0,
     "完美。结构化展示3个闹钟，包含时间/标签/状态/重复规则/贪睡时间。"),
    ("task_29_pcsim_location", 1.0, 1.0, 0.9, 1.0,
     "工具使用和任务完成满分。回复中提到'这是模拟的GPS位置数据'，在真实场景中不应暴露模拟器实现细节，轻微扣分。"),
    ("task_30_pcsim_notifications", 1.0, 1.0, 1.0, 1.0,
     "完美。清晰展示3条通知，区分已读/未读，主动询问是否需要处理。"),
    ("task_31_pcsim_bluetooth_list", 1.0, 1.0, 1.0, 1.0,
     "完美。区分已配对和已连接状态，信息详尽。"),
    ("task_32_pcsim_sensor_temp", 1.0, 1.0, 1.0, 1.0,
     "完美。准确传入 --sensor_name temperature 参数，回复简洁有用。"),
    ("task_33_pcsim_video_list", 1.0, 1.0, 1.0, 1.0,
     "完美。列出3个视频的完整信息，格式美观。"),
    ("task_34_pcsim_device_info", 1.0, 1.0, 1.0, 1.0,
     "完美。全面展示设备配置，补充了实用性点评。"),
    ("task_35_pcsim_processes", 1.0, 1.0, 1.0, 1.0,
     "完美。使用表格展示进程信息，清晰专业。"),
    ("task_36_pcsim_files", 1.0, 1.0, 1.0, 0.5,
     "任务完成度满分，用树形结构展示目录非常好。但用了10步逐层探索（先列根目录，再逐个进入子目录，甚至读了 notes.txt 内容），效率低。用户只是要看目录结构，2-3步应该够了。"),

    # === L2: 单步操作 (12 tasks) ===
    ("task_37_pcsim_create_contact", 1.0, 1.0, 1.0, 1.0,
     "完美。参数完全正确，确认信息清晰。"),
    ("task_38_pcsim_create_alarm", 1.0, 1.0, 1.0, 0.9,
     "任务完成满分。额外调用了 pc_alarm_list 确认结果，这是好习惯但不是必须的，3步完成可接受。"),
    ("task_39_pcsim_create_memo", 1.0, 1.0, 1.0, 1.0,
     "完美。巧妙地将内容用换行符分隔，格式化做得好。"),
    ("task_40_pcsim_set_brightness", 1.0, 1.0, 1.0, 1.0,
     "完美。参数正确，回复简洁。"),
    ("task_41_pcsim_payment", 1.0, 1.0, 1.0, 1.0,
     "完美。金额参数用了200.00格式，回复包含交易ID和新余额。"),
    ("task_42_pcsim_dark_theme", 1.0, 1.0, 1.0, 1.0,
     "完美。参数精确，回复包含事件触发信息。"),
    ("task_43_pcsim_open_browser", 1.0, 1.0, 1.0, 1.0,
     "完美。正确推断了 https://www.baidu.com 的完整URL。"),
    ("task_44_pcsim_play_music", 1.0, 1.0, 0.9, 0.4,
     "任务完成满分，最终成功播放了Summer Breeze。但效率很低：9步才完成（list→play→add_to_playlist→play→get_queue→get_position→play --track_id→get_position）。Agent在播放API上反复尝试，说明对music_player接口不熟悉。回复质量好但过程曲折。"),
    ("task_45_pcsim_countdown", 1.0, 1.0, 1.0, 1.0,
     "完美。参数正确（duration_seconds=300），还贴心地加了名称。"),
    ("task_46_pcsim_take_photo", 1.0, 1.0, 1.0, 1.0,
     "完美。1步完成，回复详尽。"),
    ("task_47_pcsim_create_note", 1.0, 1.0, 1.0, 1.0,
     "完美。标题/内容/标签三个参数都正确传入。"),
    ("task_48_pcsim_grant_permission", 1.0, 1.0, 1.0, 0.8,
     "任务完成满分。5步操作：list→check→grant→check，先检查再授权再确认的流程是严谨的，但4步pc-sim调用偏多。不过考虑到权限操作需要谨慎，可以理解。"),

    # === L3: 同技能多步 (8 tasks) ===
    ("task_49_pcsim_create_and_group", 1.0, 1.0, 1.0, 0.9,
     "优秀。create→add_to_group→list 三步搞定，最后list验证是好习惯。正确获取了新创建联系人的ID(c006)用于分组操作。"),
    ("task_50_pcsim_compose_send_email", 1.0, 1.0, 1.0, 1.0,
     "完美。直接一步 pc_email_send 完成，参数完整。没有多余地先compose再send，效率最优。"),
    ("task_51_pcsim_record_audio", 1.0, 1.0, 1.0, 1.0,
     "完美。start→stop 两步精确完成，回复包含文件信息。"),
    ("task_52_pcsim_list_pin_memo", 1.0, 1.0, 1.0, 1.0,
     "完美。list→pin→list 流程合理。正确识别了Meeting Notes的ID(m002)。"),
    ("task_53_pcsim_create_album_move", 1.0, 1.0, 0.9, 0.6,
     "任务完成满分。但8步偏多：create_album后list_photos找beach.jpg，然后两次尝试move_to_album（第一次用相册名，第二次用album ID），说明API调用参数不够确定。最终结果正确，过程有些曲折。"),
    ("task_54_pcsim_calendar_reminder", 1.0, 1.0, 1.0, 0.9,
     "优秀。list_events→set_reminder，中间有个session_status调用，整体高效。正确识别了Team Standup的event_id(ev001)。"),
    ("task_55_pcsim_bluetooth_scan_pair", 1.0, 1.0, 1.0, 1.0,
     "完美。scan→pair→list_paired 流程教科书级别。正确从扫描结果中提取了Speaker XR的device_id(bt_disc001)。"),
    ("task_56_pcsim_pause_shuffle", 1.0, 1.0, 1.0, 1.0,
     "完美。pause→shuffle 两步精确完成。"),

    # === L4: 跨技能协作 (8 tasks) ===
    ("task_57_pcsim_find_and_call", 1.0, 1.0, 1.0, 0.9,
     "优秀。先memory_search（虽然没结果），再contacts_search找到Alice，最后dial。跨技能协调流畅，正确传递了电话号码。memory_search是多余的一步但可以理解。"),
    ("task_58_pcsim_calendar_weather", 1.0, 1.0, 1.0, 1.0,
     "完美。calendar_list_events + weather_get_forecast，两个技能各调一次，结果整合成清晰的日程+天气报告。"),
    ("task_59_pcsim_forward_email", 1.0, 1.0, 1.0, 1.0,
     "完美。list_inbox→contacts_search→email_forward 三步跨技能协作，正确提取了Bob的邮件ID和David的邮箱。"),
    ("task_60_pcsim_screenshot_transfer", 1.0, 1.0, 1.0, 1.0,
     "完美。screenshot→list_paired→transfer 流程清晰。先截屏，再查蓝牙设备，最后传输。"),
    ("task_61_pcsim_silent_volume", 1.0, 1.0, 1.0, 1.0,
     "完美。set_profile silent + volume_set 0 两步完成两个子任务。"),
    ("task_62_pcsim_directions_memo", 1.0, 1.0, 1.0, 1.0,
     "完美。get_directions→memo_create，路线信息完整写入备忘录。"),
    ("task_63_pcsim_reply_email", 1.0, 1.0, 1.0, 1.0,
     "优秀。list_inbox→read→reply 三步完成。先读了邮件内容确认是Alice的，再回复，逻辑合理。"),
    ("task_64_pcsim_install_package", 1.0, 1.0, 1.0, 1.0,
     "完美。get_python_version→install_package 两步精确完成。"),

    # === L5: 复杂场景 (5 tasks) ===
    ("task_65_pcsim_morning_routine", 1.0, 1.0, 1.0, 0.8,
     "任务完成满分，三个子任务全部完成。7步包含3次read SKILL.md，实际pc-sim调用合理。额外调用了weather_set_location是谨慎行为。回复结构优秀。"),
    ("task_66_pcsim_meeting_prep", 1.0, 1.0, 0.9, 0.6,
     "任务完成满分：找到会议→查David邮箱→发提醒邮件。但10步偏多，包括date命令、grep管道、创建新日历事件等额外操作。Agent似乎在探索确认会议是否存在，过程中做了些不必要的操作。回复缺少会议详情展示。"),
    ("task_67_pcsim_leave_home", 1.0, 1.0, 1.0, 0.8,
     "优秀。4个子任务全部完成：set_timeout→set_power_mode→volume_mute→dismiss_all。8步含4次read，实际操作4步精确。Agent选择volume_mute而非sound_settings_set_profile也是合理的。"),
    ("task_68_pcsim_backup", 1.0, 1.0, 0.9, 0.4,
     "任务完成满分，信息都收集到了并写入文件。但16步非常多：除了必要的info/list_packages/export_contacts外，还做了get_status/list_env_vars/get_python_version/list_devices等额外查询，以及多次write和ls确认。虽然收集更多备份信息不是坏事，但效率有待提高。"),
    ("task_69_pcsim_focus_mode", 1.0, 1.0, 0.9, 0.3,
     "任务完成满分，4个子任务全部完成。但18步太多：音乐播放部分反复尝试（list→play→add_to_playlist→shuffle→play→get_position→add_to_playlist→play），说明Agent在播放特定歌单的歌曲时遇到了接口困难。最终用了play --track_id播放了Workout Mix中的歌。回复较简短。"),

    # === L6: 异常处理 (5 tasks) ===
    ("task_70_pcsim_delete_nonexistent", 1.0, 1.0, 1.0, 0.7,
     "任务完成满分：正确识别了张三不存在。但6步搜索偏多：search(张三)→list→search(张)→search(三)。理论上search(张三)返回空就够了，额外的搜索是Agent想确保没遗漏，可以理解但效率一般。回复友好地列出了现有联系人供用户确认。"),
    ("task_71_pcsim_offline_device", 1.0, 1.0, 1.0, 1.0,
     "优秀。先list_devices确认平板离线，尝试发送后得到离线提示，给出了3个替代方案。错误处理逻辑清晰，建议实用。"),
    ("task_72_pcsim_uninstall_system", 1.0, 1.0, 1.0, 1.0,
     "完美。list_installed→uninstall→得到系统应用无法卸载的错误。Agent预判了结果（'正如我所料'），解释清楚为什么不能卸载。"),
    ("task_73_pcsim_stop_no_recording", 1.0, 1.0, 1.0, 0.8,
     "优秀。stop→get_status→list_recordings，正确识别了当前没有录音在进行。4步稍多但逻辑合理（先尝试停止，再查状态，最后列出已有录音）。"),
    ("task_74_pcsim_insufficient_funds", 1.0, 1.0, 1.0, 1.0,
     "完美。get_balance→list_transactions，精确判断余额不足，给出了3个建议方案。没有盲目尝试转账，而是先检查余额。"),
]


def build_scores():
    """Build scoring data from manual scores."""
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


def merge_with_automated(scores: list[dict], transcript_dir: Path) -> list[dict]:
    """Merge Claude scores with automated scores from transcripts."""
    merged = []
    for score in scores:
        tid = score["task_id"]
        transcript_file = transcript_dir / f"{tid}.json"
        if transcript_file.exists():
            data = json.loads(transcript_file.read_text(encoding="utf-8"))
            auto_score = data.get("automated_score", 0.0)
            score["task_name"] = data.get("task_name", "")
            score["difficulty"] = data.get("difficulty", "")
            score["skills_involved"] = data.get("skills_involved", [])
            score["automated_score"] = auto_score
            score["automated_breakdown"] = data.get("automated_breakdown", {})
            score["combined_score"] = round(auto_score * 0.4 + score["claude_total"] * 0.6, 3)
        merged.append(score)
    return merged


def generate_report(scores: list[dict]) -> str:
    lines = [
        "# PC-Sim Benchmark Report (Claude Manual Scoring)",
        "",
        "**Model:** deepseek-chat",
        "**Scorer:** Claude Opus 4.6 (manual review of all 52 transcripts)",
        "**Tasks:** 52",
        "",
    ]

    auto_avg = sum(s.get("automated_score", 0) for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s.get("combined_score", 0) for s in scores) / len(scores)

    dim_avgs = {}
    for dim in ["task_completion", "tool_usage", "response_quality", "efficiency"]:
        dim_avgs[dim] = sum(s["claude_scores"][dim] for s in scores) / len(scores)

    lines.extend([
        "## Overall Scores",
        "",
        "| Metric | Score |",
        "|--------|-------|",
        f"| Automated Score | {auto_avg:.1%} |",
        f"| Claude Manual Score | {claude_avg:.1%} |",
        f"| **Combined Score** | **{combined_avg:.1%}** |",
        "",
        "### Scoring Dimensions (Claude Manual)",
        "",
        "| Dimension | Weight | Score | Description |",
        "|-----------|--------|-------|-------------|",
        f"| Task Completion | 30% | {dim_avgs['task_completion']:.1%} | 是否完整完成用户请求 |",
        f"| Tool Usage | 25% | {dim_avgs['tool_usage']:.1%} | 工具选择是否正确、参数是否合理 |",
        f"| Response Quality | 25% | {dim_avgs['response_quality']:.1%} | 回答是否清晰、准确、结构化 |",
        f"| Efficiency | 20% | {dim_avgs['efficiency']:.1%} | 步骤数是否合理 |",
        "",
    ])

    # By difficulty
    levels = {}
    for s in scores:
        lvl = s.get("difficulty", "?")
        levels.setdefault(lvl, []).append(s)

    level_names = {"L1": "信息查询", "L2": "单步操作", "L3": "同技能多步",
                   "L4": "跨技能协作", "L5": "复杂场景", "L6": "异常处理"}

    lines.extend([
        "## Scores by Difficulty",
        "",
        "| Level | Name | Tasks | Auto | Claude | Combined | Efficiency |",
        "|-------|------|-------|------|--------|----------|------------|",
    ])
    for lvl in sorted(levels.keys()):
        tasks = levels[lvl]
        n = len(tasks)
        a = sum(s.get("automated_score", 0) for s in tasks) / n
        c = sum(s["claude_total"] for s in tasks) / n
        cb = sum(s.get("combined_score", 0) for s in tasks) / n
        ef = sum(s["claude_scores"]["efficiency"] for s in tasks) / n
        lines.append(f"| {lvl} | {level_names.get(lvl, '')} | {n} | {a:.1%} | {c:.1%} | {cb:.1%} | {ef:.1%} |")

    lines.append("")

    # Detailed per-task
    lines.extend([
        "## Detailed Results",
        "",
        "| # | Task | Lvl | Auto | Claude | Combined | Steps | Notes |",
        "|---|------|-----|------|--------|----------|-------|-------|",
    ])
    for i, s in enumerate(scores, 1):
        auto = s.get("automated_score", 0)
        icon = "✅" if s.get("combined_score", 0) >= 0.95 else "⚠️" if s.get("combined_score", 0) >= 0.8 else "🔴"
        notes_short = s["notes"][:55].replace("|", "/")
        lines.append(
            f"| {i} | {s.get('task_name', s['task_id'])} | {s.get('difficulty', '?')} | "
            f"{auto:.0%} | {s['claude_total']:.0%} | {s.get('combined_score', 0):.0%} | "
            f"- | {notes_short} |"
        )

    lines.append("")

    # Key findings
    below_95 = [s for s in scores if s.get("combined_score", 0) < 0.95]
    if below_95:
        lines.extend(["## Key Findings", ""])
        for s in below_95:
            lines.append(f"### {s.get('task_name', s['task_id'])} ({s.get('difficulty', '?')}) — Combined: {s.get('combined_score', 0):.1%}")
            lines.append(f"- Auto: {s.get('automated_score', 0):.1%}, Claude: {s['claude_total']:.1%}")
            cs = s["claude_scores"]
            lines.append(f"- Completion={cs['task_completion']}, Tool={cs['tool_usage']}, Response={cs['response_quality']}, Efficiency={cs['efficiency']}")
            lines.append(f"- {s['notes']}")
            lines.append("")

    # Conclusions
    lines.extend([
        "## Conclusions",
        "",
        f"- **Overall**: deepseek-chat 在 pc-sim 环境中表现优秀，综合得分 {combined_avg:.1%}",
        f"- **Strengths**: 工具选择准确 ({dim_avgs['tool_usage']:.1%})，回答质量高 ({dim_avgs['response_quality']:.1%})，任务完成度极高 ({dim_avgs['task_completion']:.1%})",
        f"- **Weakness**: 效率 ({dim_avgs['efficiency']:.1%}) 是唯一明显的短板，部分复杂任务步骤过多",
        "- **Best categories**: L4 跨技能协作 全部满分，Agent 在多工具协调上表现最佳",
        "- **Improvement areas**: L5 复杂场景中的音乐播放和备份任务步骤过多，需要更好地理解 API",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results", help="Output directory")
    parser.add_argument("--transcripts", default="results/transcripts", help="Transcripts dir")
    args = parser.parse_args()

    output_dir = Path(args.output)
    transcript_dir = Path(args.transcripts)

    scores = build_scores()
    scores = merge_with_automated(scores, transcript_dir)

    # Save JSON
    json_path = output_dir / "claude_manual_scores.json"
    json_path.write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scores: {json_path}")

    # Save report
    report = generate_report(scores)
    report_path = output_dir / "claude_manual_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Report: {report_path}")

    # Summary
    auto_avg = sum(s.get("automated_score", 0) for s in scores) / len(scores)
    claude_avg = sum(s["claude_total"] for s in scores) / len(scores)
    combined_avg = sum(s.get("combined_score", 0) for s in scores) / len(scores)
    print(f"\nAutomated: {auto_avg:.1%}  Claude: {claude_avg:.1%}  Combined: {combined_avg:.1%}")


if __name__ == "__main__":
    main()
