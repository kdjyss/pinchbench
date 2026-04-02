# PC-Sim Benchmark Report (Claude Manual Scoring)

**Model:** Qwen3.5-9B v3 (with TOOLS.md optimization)
**Scorer:** Claude Opus 4.6 (manual review of all 52 transcripts)
**Tasks:** 52

## Overall Scores

| Metric | Score |
|--------|-------|
| Automated Score | 90.5% |
| Claude Manual Score | 87.6% |
| **Combined Score** | **88.8%** |

### Scoring Dimensions (Claude Manual)

| Dimension | Weight | Score | Description |
|-----------|--------|-------|-------------|
| Task Completion | 30% | 93.1% | 是否完整完成用户请求 |
| Tool Usage | 25% | 85.0% | 工具选择是否正确、参数是否合理 |
| Response Quality | 25% | 93.8% | 回答是否清晰、准确、结构化 |
| Efficiency | 20% | 75.0% | 步骤数是否合理 |

## Scores by Difficulty

| Level | Name | Tasks | Auto | Claude | Combined | Efficiency |
|-------|------|-------|------|--------|----------|------------|
| L1 | 信息查询 | 14 | 96.4% | 93.8% | 94.8% | 89.3% |
| L2 | 单步操作 | 12 | 95.8% | 95.9% | 95.9% | 86.7% |
| L3 | 同技能多步 | 8 | 87.5% | 82.2% | 84.4% | 67.5% |
| L4 | 跨技能协作 | 8 | 66.7% | 70.9% | 69.2% | 58.8% |
| L5 | 复杂场景 | 5 | 95.0% | 81.2% | 86.7% | 42.0% |
| L6 | 异常处理 | 5 | 100.0% | 92.6% | 95.6% | 78.0% |

## Detailed Results

| # | Task | Lvl | Auto | Claude | Combined | Steps | Notes |
|---|------|-----|------|--------|----------|-------|-------|
| 1 | 查询北京天气 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 2 | 查询电池状态 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 3 | 查询联系人列表 | L1 | 100% | 100% | 100% | - | 1步直接调用，表格展示，完美。 |
| 4 | 查看收件箱邮件 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 5 | 查询当前音量 | L1 | 100% | 100% | 100% | - | 1步直接调用pc_volume_get，完美。主动询问是否查看其他音频流。 |
| 6 | 查看闹钟列表 | L1 | 100% | 100% | 100% | - | 1步直接调用，表格展示，完美。 |
| 7 | 查询当前位置 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。v1/v2都是0分，v3修复了！ |
| 8 | 查看手机通知 | L1 | 100% | 94% | 96% | - | 第一步猜错(pc_notification_list)，第二步成功。回复详细。 |
| 9 | 查看已配对蓝牙设备 | L1 | 100% | 94% | 96% | - | memory_search(多余)→read→正确调用。3步稍多但结果准确。 |
| 10 | 查询室内温度传感器 | L1 | 100% | 100% | 100% | - | read→正确调用含正确参数，2步完美。 |
| 11 | 查看可播放视频列表 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。v1失败，v2用6步猜，v3直接成功。 |
| 12 | 查询电脑配置信息 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。展示模拟器配置而非真实系统。 |
| 13 | 查看当前运行进程 | L1 | 50% | 34% | 40% | - | 直接用ps aux查真实进程，没调用pc_shell_list_processes。混淆了模拟器和宿主机。 |
| 14 | 查看文件列表 | L1 | 100% | 92% | 95% | - | 5步全部用pc_file_manager_list，没用系统命令。比之前版本好。但5步逐层探索效率一般。 |
| 15 | 创建新联系人 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。参数正确。 |
| 16 | 设置早起闹钟 | L2 | 100% | 96% | 98% | - | memory_search(多余)→read→正确调用。3步，额外参数--date tomorrow可接受。 |
| 17 | 创建购物备忘录 | L2 | 100% | 100% | 100% | - | read→正确调用pc_memo_create，2步完美。 |
| 18 | 调整屏幕亮度 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 19 | 支付宝付款 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 20 | 切换深色模式 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 21 | 浏览器打开网页 | L2 | 50% | 89% | 73% | - | 第一步猜错(pc_browser_op)，读SKILL.md后成功。3步。 |
| 22 | 播放指定歌曲 | L2 | 100% | 100% | 100% | - | read→list→play --track_id，3步精准。v1需10步，v2需10步，v3只要3步。 |
| 23 | 设置5分钟倒计时 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 24 | 拍照 | L2 | 100% | 94% | 96% | - | 第一步猜错(pc_camera_take_photo)，读SKILL.md后成功。3步。v1=11步，v2=0 |
| 25 | 创建带标签的笔记 | L2 | 100% | 74% | 84% | - | 9步太多：前7步猜各种命令(notes_exists, createnote, --help, install |
| 26 | 授予应用权限 | L2 | 100% | 98% | 99% | - | read两个SKILL.md→正确调用。3步高效。 |
| 27 | 创建联系人并加入分组 | L3 | 100% | 100% | 100% | - | read→create→add_to_group，3步完美。 |
| 28 | 撰写并发送邮件 | L3 | 100% | 100% | 100% | - | read→直接pc_email_send，2步完美。 |
| 29 | 开始并停止录音 | L3 | 100% | 96% | 98% | - | read→start→stop→write(多余日志)。4步，write不必要。 |
| 30 | 查看备忘录并置顶 | L3 | 100% | 87% | 92% | - | 5步。pin时猜错参数(m002→--memoId→读SKILL.md→--memo_id)。最终成功。 |
| 31 | 创建相册并移入照片 | L3 | 100% | 83% | 90% | - | 8步。create_album和move_to_album各猜错一次参数。最终成功。 |
| 32 | 查看日程并修改提醒时间 | L3 | 0% | 8% | 4% | - | 完全失败。memory_search→sessions_spawn→session_status，没调用任何p |
| 33 | 扫描并配对蓝牙设备 | L3 | 100% | 100% | 100% | - | read→scan→pair，3步完美。 |
| 34 | 暂停音乐并开启随机播放 | L3 | 100% | 84% | 91% | - | 5步。前两步猜错(pc_music_pause, pc_music_shuffle_active)，读SKIL |
| 35 | 查联系人电话并拨打 | L4 | 100% | 92% | 95% | - | 5步。先get了c002(Bob)再get c001(Alice)，多查了一次。最终正确拨号。 |
| 36 | 查询明天会议和天气 | L4 | 100% | 98% | 99% | - | 4步：read两个SKILL.md→list_events→get_forecast。高效跨技能协调。v1/v |
| 37 | 转发邮件给联系人 | L4 | 33% | 52% | 45% | - | 4步。list_inbox成功找到Bob邮件，但search失败后没有继续forward。只列出了邮件没完成转 |
| 38 | 截屏并通过蓝牙传输 | L4 | 0% | 21% | 13% | - | 6步全部失败。猜错截屏命令后转用bash/scrot/python截图，完全脱离pc-sim。v2满分，v3严 |
| 39 | 静音并设置媒体音量为0 | L4 | 100% | 74% | 85% | - | 26步极度低效。反复猜静音和音量命令格式。最终成功但过程极其曲折。 |
| 40 | 查询路线并记录到备忘录 | L4 | 100% | 98% | 99% | - | 4步：read→get_directions→read→memo_create。高效。 |
| 41 | 查看未读邮件并回复 | L4 | 100% | 100% | 100% | - | read→list_inbox→reply，3步完美。 |
| 42 | 查看Python版本并安装包 | L4 | 0% | 32% | 19% | - | 用python --version和pip install，没用pc-sim工具。获取真实系统信息。 |
| 43 | 完整起床提醒设置 | L5 | 100% | 80% | 88% | - | 11步。前3步猜错，读3个SKILL.md后完成3个子任务。效率一般但全部成功。 |
| 44 | 会议准备全流程 | L5 | 100% | 83% | 90% | - | 10步。前几步猜错，但最终找到会议→查David邮箱→发邮件。全部成功。 |
| 45 | 出门前设备配置 | L5 | 100% | 83% | 90% | - | 11步。前4步猜错，读4个SKILL.md后4个子任务全部完成。效率一般但全成功。 |
| 46 | 设备完整备份准备 | L5 | 75% | 74% | 74% | - | 10步。第一步猜错(pc_system_info)。完成了list_packages/export_conta |
| 47 | 专注模式全配置 | L5 | 100% | 86% | 91% | - | 13步。读4个SKILL.md后逐个完成。dnd→brightness→music(用Night Drive替 |
| 48 | 删除不存在的联系人 | L6 | 100% | 91% | 95% | - | 3步。第一步猜错(contacts_delete)，search+list确认不存在。高效。 |
| 49 | 向离线设备传输文件 | L6 | 100% | 100% | 100% | - | read→list_devices，2步完美。正确识别离线状态并提供建议。 |
| 50 | 尝试卸载系统应用 | L6 | 100% | 85% | 91% | - | 6步。前3步猜错(app_manager list, finial_app_list, list-tools) |
| 51 | 无录音状态下停止录音 | L6 | 100% | 87% | 92% | - | 4步。read后猜错(pc-recorder-stop缺pc-sim前缀)，第3步成功。额外get_statu |
| 52 | 余额不足时的支付处理 | L6 | 100% | 100% | 100% | - | read→get_balance，2步完美。正确识别余额不足。 |

## Key Findings

### 查看当前运行进程 (L1) — Combined: 40.1%
- Auto: 50.0%, Claude: 33.5%
- Completion=0.5, Tool=0.0, Response=0.5, Efficiency=0.3
- 直接用ps aux查真实进程，没调用pc_shell_list_processes。混淆了模拟器和宿主机。

### 浏览器打开网页 (L2) — Combined: 73.4%
- Auto: 50.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(pc_browser_op)，读SKILL.md后成功。3步。

### 创建带标签的笔记 (L2) — Combined: 84.4%
- Auto: 100.0%, Claude: 74.0%
- Completion=1.0, Tool=0.6, Response=1.0, Efficiency=0.2
- 9步太多：前7步猜各种命令(notes_exists, createnote, --help, install_app, list-skills|grep)。最终成功但效率极差。

### 查看备忘录并置顶 (L3) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 5步。pin时猜错参数(m002→--memoId→读SKILL.md→--memo_id)。最终成功。

### 创建相册并移入照片 (L3) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- 8步。create_album和move_to_album各猜错一次参数。最终成功。

### 查看日程并修改提醒时间 (L3) — Combined: 4.5%
- Auto: 0.0%, Claude: 7.5%
- Completion=0.0, Tool=0.0, Response=0.3, Efficiency=0.0
- 完全失败。memory_search→sessions_spawn→session_status，没调用任何pc-sim工具。声称没有日历功能。

### 暂停音乐并开启随机播放 (L3) — Combined: 90.7%
- Auto: 100.0%, Claude: 84.5%
- Completion=1.0, Tool=0.8, Response=0.9, Efficiency=0.6
- 5步。前两步猜错(pc_music_pause, pc_music_shuffle_active)，读SKILL.md后成功。

### 查联系人电话并拨打 (L4) — Combined: 94.9%
- Auto: 100.0%, Claude: 91.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.7
- 5步。先get了c002(Bob)再get c001(Alice)，多查了一次。最终正确拨号。

### 转发邮件给联系人 (L4) — Combined: 44.8%
- Auto: 33.3%, Claude: 52.5%
- Completion=0.5, Tool=0.6, Response=0.5, Efficiency=0.5
- 4步。list_inbox成功找到Bob邮件，但search失败后没有继续forward。只列出了邮件没完成转发。

### 截屏并通过蓝牙传输 (L4) — Combined: 12.6%
- Auto: 0.0%, Claude: 21.0%
- Completion=0.3, Tool=0.1, Response=0.3, Efficiency=0.1
- 6步全部失败。猜错截屏命令后转用bash/scrot/python截图，完全脱离pc-sim。v2满分，v3严重退步。

### 静音并设置媒体音量为0 (L4) — Combined: 84.7%
- Auto: 100.0%, Claude: 74.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.1
- 26步极度低效。反复猜静音和音量命令格式。最终成功但过程极其曲折。

### 查看Python版本并安装包 (L4) — Combined: 18.9%
- Auto: 0.0%, Claude: 31.5%
- Completion=0.3, Tool=0.0, Response=0.5, Efficiency=0.5
- 用python --version和pip install，没用pc-sim工具。获取真实系统信息。

### 完整起床提醒设置 (L5) — Combined: 88.3%
- Auto: 100.0%, Claude: 80.5%
- Completion=1.0, Tool=0.8, Response=0.9, Efficiency=0.4
- 11步。前3步猜错，读3个SKILL.md后完成3个子任务。效率一般但全部成功。

### 会议准备全流程 (L5) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- 10步。前几步猜错，但最终找到会议→查David邮箱→发邮件。全部成功。

### 出门前设备配置 (L5) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- 11步。前4步猜错，读4个SKILL.md后4个子任务全部完成。效率一般但全成功。

### 设备完整备份准备 (L5) — Combined: 74.4%
- Auto: 75.0%, Claude: 74.0%
- Completion=0.8, Tool=0.7, Response=0.9, Efficiency=0.5
- 10步。第一步猜错(pc_system_info)。完成了list_packages/export_contacts/get_status/list_devices。但没用pc_device_manager_get_info或pc_runtime_env_get_system_info。

### 专注模式全配置 (L5) — Combined: 91.3%
- Auto: 100.0%, Claude: 85.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.4
- 13步。读4个SKILL.md后逐个完成。dnd→brightness→music(用Night Drive替代Workout Mix)→countdown。全部成功。

### 删除不存在的联系人 (L6) — Combined: 94.6%
- Auto: 100.0%, Claude: 91.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.8
- 3步。第一步猜错(contacts_delete)，search+list确认不存在。高效。

### 尝试卸载系统应用 (L6) — Combined: 91.0%
- Auto: 100.0%, Claude: 85.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.5
- 6步。前3步猜错(app_manager list, finial_app_list, list-tools)。list_installed→uninstall成功识别系统应用。

### 无录音状态下停止录音 (L6) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 4步。read后猜错(pc-recorder-stop缺pc-sim前缀)，第3步成功。额外get_status确认。

## Conclusions

- **Overall**: Qwen3.5-9B v3 是 Qwen 系列最佳表现，TOOLS.md 优化效果显著
- **对比 v1→v3 进化**: Auto 77.2%→90.5%(+13.3%), 多个关键任务从 0 分修复为满分
- **修复的关键任务**: location(v1/v2都0分)、video_list、calendar_weather、leave_home
- **L1 查询**: 96.4% auto，几乎追平 deepseek-chat(96.4%)
- **L5 工作流**: 95.0% auto，大幅超越 v1(73.3%)和 v2(70.0%)
- **持续问题**: processes 仍用 ps aux、install_package 仍用 pip、calendar_reminder 完全失败
- **效率仍是短板**: 部分任务步骤过多(silent_volume 26步, focus_mode 13步)
- **与 deepseek-chat 的差距从 22% 缩小到 ~8%**
