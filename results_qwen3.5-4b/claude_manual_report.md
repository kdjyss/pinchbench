# PC-Sim Benchmark Report (Claude Manual Scoring)

**Model:** Qwen3.5-4B (local-vllm, with TOOLS.md optimization)
**Scorer:** Claude Opus 4.6 (manual review of all 52 transcripts)
**Tasks:** 52

## Overall Scores

| Metric | Score |
|--------|-------|
| Automated Score | 84.6% |
| Claude Manual Score | 81.9% |
| **Combined Score** | **83.0%** |

### Scoring Dimensions (Claude Manual)

| Dimension | Weight | Score | Description |
|-----------|--------|-------|-------------|
| Task Completion | 30% | 88.7% | 是否完整完成用户请求 |
| Tool Usage | 25% | 78.5% | 工具选择是否正确、参数是否合理 |
| Response Quality | 25% | 90.4% | 回答是否清晰、准确、结构化 |
| Efficiency | 20% | 65.6% | 步骤数是否合理 |

## Scores by Difficulty

| Level | Name | Tasks | Auto | Claude | Combined | Efficiency |
|-------|------|-------|------|--------|----------|------------|
| L1 | 信息查询 | 14 | 89.3% | 88.8% | 89.0% | 77.1% |
| L2 | 单步操作 | 12 | 91.7% | 83.8% | 87.0% | 69.2% |
| L3 | 同技能多步 | 8 | 87.5% | 85.2% | 86.2% | 72.5% |
| L4 | 跨技能协作 | 8 | 83.3% | 82.8% | 83.0% | 57.5% |
| L5 | 复杂场景 | 5 | 56.7% | 57.0% | 56.9% | 28.0% |
| L6 | 异常处理 | 5 | 80.0% | 76.3% | 77.8% | 64.0% |

## Detailed Results

| # | Task | Lvl | Auto | Claude | Combined | Steps | Notes |
|---|------|-----|------|--------|----------|-------|-------|
| 1 | 查询北京天气 | L1 | 100% | 98% | 99% | - | read→set_location→get_current，3步。额外调了set_location是谨慎行为。 |
| 2 | 查询电池状态 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 3 | 查询联系人列表 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。回复格式优秀。 |
| 4 | 查看收件箱邮件 | L1 | 100% | 89% | 93% | - | 第一步猜错(email_list_inbox缺pc_前缀)，读SKILL.md后成功。3步。 |
| 5 | 查询当前音量 | L1 | 50% | 94% | 76% | - | memory_search(多余)→get_all_streams。用了更全面的API，回复表格清晰，还解释了 |
| 6 | 查看闹钟列表 | L1 | 100% | 89% | 93% | - | 第一步猜错(pc_alarm_get 100)，读SKILL.md后用了pc_alarm_list 100（多 |
| 7 | 查询当前位置 | L1 | 100% | 86% | 92% | - | 第一步猜错(pc_map_location_get)，读SKILL.md后成功。回复包含坐标信息。比9B系列的 |
| 8 | 查看手机通知 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。回复结构清晰还主动提供后续操作建议。 |
| 9 | 查看已配对蓝牙设备 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。信息准确无编造。 |
| 10 | 查询室内温度传感器 | L1 | 100% | 83% | 90% | - | 6步偏多：前几步猜错参数(--sensor_name temp而非temperature)，反复尝试。最终成功 |
| 11 | 查看可播放视频列表 | L1 | 0% | 12% | 8% | - | 完全失败。用了web_search搜索2026热门电影，没调用pc-sim工具。输出了影视推荐而非模拟器视频列 |
| 12 | 查询电脑配置信息 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。表格展示模拟器配置。 |
| 13 | 查看当前运行进程 | L1 | 100% | 100% | 100% | - | read→正确调用pc_shell_list_processes，2步完美！比9B系列（用ps aux获取真实 |
| 14 | 查看文件列表 | L1 | 100% | 92% | 95% | - | 4步全部用pc_file_manager_list，没有用真实系统命令。比9B v2（用tree）好。但4步逐 |
| 15 | 创建新联系人 | L2 | 0% | 22% | 13% | - | 只用了write()写文件，没有调用pc_contacts_create。完全错误的方式。 |
| 16 | 设置早起闹钟 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 17 | 创建购物备忘录 | L2 | 100% | 89% | 93% | - | 第一步猜错(memo_create缺pc_前缀)，读SKILL.md后成功。用对了pc_memo_create |
| 18 | 调整屏幕亮度 | L2 | 100% | 69% | 81% | - | 7步极低效：前6步猜各种格式(brightness_set, pc-display-set-brightnes |
| 19 | 支付宝付款 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。回复包含交易详情。 |
| 20 | 切换深色模式 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 21 | 浏览器打开网页 | L2 | 100% | 100% | 100% | - | read→正确调用含完整URL，2步完美。 |
| 22 | 播放指定歌曲 | L2 | 100% | 50% | 70% | - | 15步极低效，反复尝试play。最终只添加到播放列表但未真正播放。回复说需要手动点播放按钮，任务未完全完成。 |
| 23 | 设置5分钟倒计时 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 24 | 拍照 | L2 | 100% | 94% | 96% | - | 第一步猜错(pc_camera_photo)，读SKILL.md后成功。3步可接受。比9B系列（11步暴力搜索 |
| 25 | 创建带标签的笔记 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 26 | 授予应用权限 | L2 | 100% | 82% | 90% | - | 5步：前3步猜错参数格式(provider vs provider_name)，读SKILL.md后成功。回复 |
| 27 | 创建联系人并加入分组 | L3 | 100% | 100% | 100% | - | read→create→add_to_group，3步完美。 |
| 28 | 撰写并发送邮件 | L3 | 100% | 87% | 92% | - | 4步：先用memo_write记草稿→write文件→send→rm清理。过程曲折但最终正确发送。清理草稿是额 |
| 29 | 开始并停止录音 | L3 | 100% | 100% | 100% | - | read→start→stop，3步完美。 |
| 30 | 查看备忘录并置顶 | L3 | 100% | 100% | 100% | - | read→list→pin，3步完美。 |
| 31 | 创建相册并移入照片 | L3 | 100% | 86% | 91% | - | 10步。move_to_album参数反复尝试（中文名→英文名→album ID）。最终成功。 |
| 32 | 查看日程并修改提醒时间 | L3 | 0% | 14% | 8% | - | 完全失败。用了cron/memory_search/memory_get而非pc-sim工具。声称设置了提醒但 |
| 33 | 扫描并配对蓝牙设备 | L3 | 100% | 96% | 98% | - | 5步：write(多余)→read→scan→pair→connect。流程正确，额外做了connect是加分 |
| 34 | 暂停音乐并开启随机播放 | L3 | 100% | 100% | 100% | - | read→pause→shuffle，3步完美。 |
| 35 | 查联系人电话并拨打 | L4 | 100% | 98% | 99% | - | 4步：read两个SKILL.md→search→dial。高效跨技能协调。 |
| 36 | 查询明天会议和天气 | L4 | 0% | 37% | 22% | - | 8步。用了cron和web_search/web_fetch获取真实天气而非pc-sim。没有调用calend |
| 37 | 转发邮件给联系人 | L4 | 67% | 94% | 83% | - | 4步：read→search(失败)→list_inbox→forward。正确完成转发。比9B用了正确的da |
| 38 | 截屏并通过蓝牙传输 | L4 | 100% | 83% | 90% | - | 8步。截屏和传输成功，但中间探索了文件路径(cat/ls/find)。结果正确效率一般。 |
| 39 | 静音并设置媒体音量为0 | L4 | 100% | 74% | 84% | - | 18步极低效：反复猜静音命令格式。最终成功但过程太曲折。 |
| 40 | 查询路线并记录到备忘录 | L4 | 100% | 88% | 92% | - | 8步。前两步猜错，读SKILL.md后成功。用了正确的pc_memo_create。 |
| 41 | 查看未读邮件并回复 | L4 | 100% | 89% | 93% | - | 4步。第一步猜错(pc_email_inbox)，读SKILL.md后成功。 |
| 42 | 查看Python版本并安装包 | L4 | 100% | 100% | 100% | - | read→get_python_version→install_package，3步完美。 |
| 43 | 完整起床提醒设置 | L5 | 0% | 44% | 26% | - | 3步但都猜错：alarm_set→web_search(真实天气)→cron。没有使用pc-sim的alarm |
| 44 | 会议准备全流程 | L5 | 33% | 36% | 35% | - | 2步。read SKILL.md后直接compose邮件，但没先查日历找会议详情、没查David邮箱（用了错误 |
| 45 | 出门前设备配置 | L5 | 50% | 37% | 42% | - | 37步极度低效。前4步猜错后陷入暴力尝试。最终只完成了屏幕超时和静音，省电和清通知失败。 |
| 46 | 设备完整备份准备 | L5 | 100% | 88% | 92% | - | 10步。get_info→list_packages→export_contacts成功。中间第一步猜错，有些 |
| 47 | 专注模式全配置 | L5 | 100% | 81% | 89% | - | 15步。memory_search(多余)，第一步猜错。读4个SKILL.md后逐个完成4个子任务。效率低但全 |
| 48 | 删除不存在的联系人 | L6 | 100% | 89% | 93% | - | 5步。第一步猜错(contacts_delete_contact)，读SKILL.md后search+list |
| 49 | 向离线设备传输文件 | L6 | 100% | 85% | 91% | - | 6步。前两步猜错，读SKILL.md后正确调用list_devices→sync→list。识别到离线状态给出 |
| 50 | 尝试卸载系统应用 | L6 | 100% | 100% | 100% | - | read→list_installed，正确识别系统应用无法卸载。回复解释充分。 |
| 51 | 无录音状态下停止录音 | L6 | 100% | 100% | 100% | - | 1步直接调用pc_recorder_stop，完美。 |
| 52 | 余额不足时的支付处理 | L6 | 0% | 8% | 4% | - | 完全失败。0步工具调用，直接反问用户是不是模拟环境，要确认朋友账户信息。没有调用pc_payment_get_ |

## Key Findings

### 查看收件箱邮件 (L1) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(email_list_inbox缺pc_前缀)，读SKILL.md后成功。3步。

### 查询当前音量 (L1) — Combined: 76.1%
- Auto: 50.0%, Claude: 93.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.8
- memory_search(多余)→get_all_streams。用了更全面的API，回复表格清晰，还解释了媒体音量含义。

### 查看闹钟列表 (L1) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(pc_alarm_get 100)，读SKILL.md后用了pc_alarm_list 100（多余参数）但成功。回复详细。

### 查询当前位置 (L1) — Combined: 91.9%
- Auto: 100.0%, Claude: 86.5%
- Completion=1.0, Tool=0.8, Response=0.9, Efficiency=0.7
- 第一步猜错(pc_map_location_get)，读SKILL.md后成功。回复包含坐标信息。比9B系列的0分大幅改善！

### 查询室内温度传感器 (L1) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- 6步偏多：前几步猜错参数(--sensor_name temp而非temperature)，反复尝试。最终成功。

### 查看可播放视频列表 (L1) — Combined: 7.5%
- Auto: 0.0%, Claude: 12.5%
- Completion=0.0, Tool=0.0, Response=0.5, Efficiency=0.0
- 完全失败。用了web_search搜索2026热门电影，没调用pc-sim工具。输出了影视推荐而非模拟器视频列表。

### 创建新联系人 (L2) — Combined: 12.9%
- Auto: 0.0%, Claude: 21.5%
- Completion=0.3, Tool=0.0, Response=0.5, Efficiency=0.0
- 只用了write()写文件，没有调用pc_contacts_create。完全错误的方式。

### 创建购物备忘录 (L2) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(memo_create缺pc_前缀)，读SKILL.md后成功。用对了pc_memo_create而非notes！

### 调整屏幕亮度 (L2) — Combined: 81.4%
- Auto: 100.0%, Claude: 69.0%
- Completion=1.0, Tool=0.6, Response=0.8, Efficiency=0.2
- 7步极低效：前6步猜各种格式(brightness_set, pc-display-set-brightness, ls/find查找工具)。最终成功但过程很差。

### 播放指定歌曲 (L2) — Combined: 70.3%
- Auto: 100.0%, Claude: 50.5%
- Completion=0.7, Tool=0.6, Response=0.5, Efficiency=0.1
- 15步极低效，反复尝试play。最终只添加到播放列表但未真正播放。回复说需要手动点播放按钮，任务未完全完成。

### 授予应用权限 (L2) — Combined: 89.5%
- Auto: 100.0%, Claude: 82.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.5
- 5步：前3步猜错参数格式(provider vs provider_name)，读SKILL.md后成功。回复详细含JSON。

### 撰写并发送邮件 (L3) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 4步：先用memo_write记草稿→write文件→send→rm清理。过程曲折但最终正确发送。清理草稿是额外但合理操作。

### 创建相册并移入照片 (L3) — Combined: 91.3%
- Auto: 100.0%, Claude: 85.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.4
- 10步。move_to_album参数反复尝试（中文名→英文名→album ID）。最终成功。

### 查看日程并修改提醒时间 (L3) — Combined: 8.1%
- Auto: 0.0%, Claude: 13.5%
- Completion=0.2, Tool=0.0, Response=0.3, Efficiency=0.0
- 完全失败。用了cron/memory_search/memory_get而非pc-sim工具。声称设置了提醒但实际没有调用任何calendar工具。

### 查询明天会议和天气 (L4) — Combined: 22.2%
- Auto: 0.0%, Claude: 37.0%
- Completion=0.5, Tool=0.1, Response=0.7, Efficiency=0.1
- 8步。用了cron和web_search/web_fetch获取真实天气而非pc-sim。没有调用calendar和weather工具。天气信息来自真实网站不是模拟器。

### 转发邮件给联系人 (L4) — Combined: 82.8%
- Auto: 66.7%, Claude: 93.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.8
- 4步：read→search(失败)→list_inbox→forward。正确完成转发。比9B用了正确的david@邮箱。

### 截屏并通过蓝牙传输 (L4) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- 8步。截屏和传输成功，但中间探索了文件路径(cat/ls/find)。结果正确效率一般。

### 静音并设置媒体音量为0 (L4) — Combined: 84.4%
- Auto: 100.0%, Claude: 74.0%
- Completion=1.0, Tool=0.7, Response=0.9, Efficiency=0.2
- 18步极低效：反复猜静音命令格式。最终成功但过程太曲折。

### 查询路线并记录到备忘录 (L4) — Combined: 92.5%
- Auto: 100.0%, Claude: 87.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.5
- 8步。前两步猜错，读SKILL.md后成功。用了正确的pc_memo_create。

### 查看未读邮件并回复 (L4) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 4步。第一步猜错(pc_email_inbox)，读SKILL.md后成功。

### 完整起床提醒设置 (L5) — Combined: 26.4%
- Auto: 0.0%, Claude: 44.0%
- Completion=0.5, Tool=0.3, Response=0.7, Efficiency=0.2
- 3步但都猜错：alarm_set→web_search(真实天气)→cron。没有使用pc-sim的alarm/weather/calendar工具。部分信息来自真实网络。

### 会议准备全流程 (L5) — Combined: 34.6%
- Auto: 33.3%, Claude: 35.5%
- Completion=0.4, Tool=0.3, Response=0.4, Efficiency=0.3
- 2步。read SKILL.md后直接compose邮件，但没先查日历找会议详情、没查David邮箱（用了错误的邮箱）。流程不完整。

### 出门前设备配置 (L5) — Combined: 42.2%
- Auto: 50.0%, Claude: 37.0%
- Completion=0.5, Tool=0.3, Response=0.5, Efficiency=0.1
- 37步极度低效。前4步猜错后陷入暴力尝试。最终只完成了屏幕超时和静音，省电和清通知失败。

### 设备完整备份准备 (L5) — Combined: 92.5%
- Auto: 100.0%, Claude: 87.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.5
- 10步。get_info→list_packages→export_contacts成功。中间第一步猜错，有些探索步骤。整体完成。

### 专注模式全配置 (L5) — Combined: 88.6%
- Auto: 100.0%, Claude: 81.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.3
- 15步。memory_search(多余)，第一步猜错。读4个SKILL.md后逐个完成4个子任务。效率低但全部成功。

### 删除不存在的联系人 (L6) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 5步。第一步猜错(contacts_delete_contact)，读SKILL.md后search+list确认不存在。

### 向离线设备传输文件 (L6) — Combined: 91.0%
- Auto: 100.0%, Claude: 85.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.5
- 6步。前两步猜错，读SKILL.md后正确调用list_devices→sync→list。识别到离线状态给出建议。比9B v2好。

### 余额不足时的支付处理 (L6) — Combined: 4.5%
- Auto: 0.0%, Claude: 7.5%
- Completion=0.0, Tool=0.0, Response=0.3, Efficiency=0.0
- 完全失败。0步工具调用，直接反问用户是不是模拟环境，要确认朋友账户信息。没有调用pc_payment_get_balance。

## Conclusions

- **Overall**: Qwen3.5-4B 综合得分 83.0%，automated 84.6%
- **对比 9B v2 (79.6%)**: 4B 在 TOOLS.md 优化后表现持平甚至更好，说明 prompt 工程比模型大小更重要
- **亮点**: location 任务首次通过（9B 两个版本都 0 分）、processes 用对了 pc-sim 工具（9B 用真实 ps aux）
- **仍存在问题**: 播放音乐(15步)、调亮度(7步)、静音(18步)等任务效率极低；calendar_reminder 和 insufficient_funds 完全失败
- **小模型特有问题**: video_list 用 web_search 搜影视推荐、morning_routine 用真实天气网站，模拟器与真实环境边界模糊
