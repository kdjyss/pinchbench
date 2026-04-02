# PC-Sim Benchmark Report (Claude Manual Scoring)

**Model:** Qwen3.5-9B (local-vllm)
**Scorer:** Claude Opus 4.6 (manual review of all 52 transcripts)
**Tasks:** 52

## Overall Scores

| Metric | Score |
|--------|-------|
| Automated Score | 77.2% |
| Claude Manual Score | 75.0% |
| **Combined Score** | **75.9%** |

### Scoring Dimensions (Claude Manual)

| Dimension | Weight | Score | Description |
|-----------|--------|-------|-------------|
| Task Completion | 30% | 82.9% | 是否完整完成用户请求 |
| Tool Usage | 25% | 71.3% | 工具选择是否正确、参数是否合理 |
| Response Quality | 25% | 80.4% | 回答是否清晰、准确、结构化 |
| Efficiency | 20% | 61.2% | 步骤数是否合理 |

## Scores by Difficulty

| Level | Name | Tasks | Auto | Claude | Combined | Efficiency |
|-------|------|-------|------|--------|----------|------------|
| L1 | 信息查询 | 14 | 67.9% | 62.8% | 64.8% | 55.7% |
| L2 | 单步操作 | 12 | 79.2% | 83.5% | 81.8% | 70.0% |
| L3 | 同技能多步 | 8 | 93.8% | 86.1% | 89.2% | 65.0% |
| L4 | 跨技能协作 | 8 | 62.5% | 70.1% | 67.1% | 63.7% |
| L5 | 复杂场景 | 5 | 73.3% | 65.5% | 68.6% | 38.0% |
| L6 | 异常处理 | 5 | 100.0% | 88.6% | 93.2% | 68.0% |

## Detailed Results

| # | Task | Lvl | Auto | Claude | Combined | Steps | Notes |
|---|------|-----|------|--------|----------|-------|-------|
| 1 | 查询北京天气 | L1 | 100% | 98% | 98% | - | 正确调用 pc_weather_get_current，回复简洁清晰。风速数据(22km/h vs seed的 |
| 2 | 查询电池状态 | L1 | 0% | 0% | 0% | - | 完全失败。编造命令 pc-battery --status，没读 SKILL.md，无输出。 |
| 3 | 查询联系人列表 | L1 | 100% | 100% | 100% | - | 直接调用正确工具，表格展示清晰。 |
| 4 | 查看收件箱邮件 | L1 | 100% | 84% | 91% | - | 最终成功但前两步猜错命令(pc-sim email inbox, pc_sim_email_inbox)，第3 |
| 5 | 查询当前音量 | L1 | 100% | 87% | 92% | - | 前两步猜错(volume_get_all, pc_volume_get)，读SKILL.md后成功。最终用了p |
| 6 | 查看闹钟列表 | L1 | 100% | 100% | 100% | - | 先读SKILL.md再执行，完美。表格展示。 |
| 7 | 查询当前位置 | L1 | 0% | 0% | 0% | - | 完全跑偏。被IDENTITY.md干扰，进入自我介绍模式，没执行任何工具。 |
| 8 | 查看手机通知 | L1 | 100% | 84% | 91% | - | 前两步猜错(pc_notification_list, pc_notification list)，读SKIL |
| 9 | 查看已配对蓝牙设备 | L1 | 100% | 82% | 89% | - | 前两步猜错(pc_bluetooth_list_paired_devices, pc_bluetooth_li |
| 10 | 查询室内温度传感器 | L1 | 0% | 0% | 0% | - | 输出XML乱码，模型格式理解失败，没调用任何工具。 |
| 11 | 查看可播放视频列表 | L1 | 100% | 100% | 100% | - | 先读SKILL.md再执行，完美。 |
| 12 | 查询电脑配置信息 | L1 | 0% | 25% | 15% | - | 猜错命令(pc-sim device_info)，转而用系统命令uname/lscpu获取了真实宿主机信息而非 |
| 13 | 查看当前运行进程 | L1 | 50% | 45% | 47% | - | 先猜错(pc_process_list)，转用ps aux获取真实进程。回复内容是真实进程而非模拟器数据，部分 |
| 14 | 查看文件列表 | L1 | 100% | 74% | 84% | - | 读了SKILL.md后正确调用pc_file_manager_list，但还额外用了ls和tree查看真实文件 |
| 15 | 创建新联系人 | L2 | 100% | 71% | 83% | - | 6步太多：先write、再猜错(contacts_create)、读SKILL.md、创建时缺电话号码、两次u |
| 16 | 设置早起闹钟 | L2 | 100% | 100% | 100% | - | 先读SKILL.md再执行，参数正确，完美。 |
| 17 | 创建购物备忘录 | L2 | 0% | 64% | 38% | - | 用了pc_notes_create而非pc_memo_create，混淆了notes和memo两个skill。 |
| 18 | 调整屏幕亮度 | L2 | 100% | 95% | 97% | - | 先读SKILL.md再执行，参数正确。回复过于简短。 |
| 19 | 支付宝付款 | L2 | 100% | 100% | 100% | - | 先读SKILL.md再执行，参数精确，回复包含交易详情。 |
| 20 | 切换深色模式 | L2 | 100% | 84% | 90% | - | 先猜错(display_set_dark)，读SKILL.md后成功。回复过于简短。 |
| 21 | 浏览器打开网页 | L2 | 50% | 84% | 70% | - | 第一步参数格式错(pc_browser_open_url baidu.com 缺--url)，第二步修正。回复 |
| 22 | 播放指定歌曲 | L2 | 100% | 76% | 86% | - | 10步完成，反复尝试不同播放方式。最终成功但效率很低。回复用了英文。 |
| 23 | 设置5分钟倒计时 | L2 | 100% | 98% | 99% | - | 先memory_search（多余），读SKILL.md后正确执行。参数正确。 |
| 24 | 拍照 | L2 | 0% | 37% | 22% | - | 11步暴力搜索：pc_gallery_screenshot→screenshot→screencapture→ |
| 25 | 创建带标签的笔记 | L2 | 100% | 100% | 100% | - | 先读SKILL.md再执行，参数正确，完美。 |
| 26 | 授予应用权限 | L2 | 100% | 93% | 96% | - | 先memory_search（多余），读SKILL.md后正确执行。回复简短但准确。 |
| 27 | 创建联系人并加入分组 | L3 | 100% | 100% | 100% | - | 先读SKILL.md，create→add_to_group，流程正确高效。 |
| 28 | 撰写并发送邮件 | L3 | 100% | 96% | 98% | - | 先compose再send，比deepseek多一步但逻辑合理。 |
| 29 | 开始并停止录音 | L3 | 100% | 88% | 92% | - | start→stop 正确，但后面多了4步(read/edit/write)做日志记录，不必要。 |
| 30 | 查看备忘录并置顶 | L3 | 100% | 100% | 100% | - | 先读SKILL.md，list→pin，完美。 |
| 31 | 创建相册并移入照片 | L3 | 100% | 86% | 91% | - | 11步：多次尝试move_to_album用不同参数（相册名→album ID→英文名），过程曲折但最终成功。 |
| 32 | 查看日程并修改提醒时间 | L3 | 50% | 48% | 49% | - | 6步但只完成了list_events，没有执行set_reminder。先memory_search和sess |
| 33 | 扫描并配对蓝牙设备 | L3 | 100% | 74% | 84% | - | 16步暴力尝试：先猜各种蓝牙命令(bluetoothctl/btctl/bt-manager)，最终读SKIL |
| 34 | 暂停音乐并开启随机播放 | L3 | 100% | 98% | 98% | - | 先读SKILL.md，pause→shuffle，高效。回复准确地指出了当前没在播放。 |
| 35 | 查联系人电话并拨打 | L4 | 100% | 94% | 96% | - | contacts_search→尝试pc_phone_call→读SKILL.md→dial。中间一步猜错但快 |
| 36 | 查询明天会议和天气 | L4 | 0% | 8% | 4% | - | 完全失败。4次memory_search和cron调用，没有调用任何pc-sim工具。反问用户用什么日历应用， |
| 37 | 转发邮件给联系人 | L4 | 0% | 28% | 16% | - | 只读了SKILL.md和执行了email_search（不存在的命令），没有完成转发。回复只说'搜索没有找到结 |
| 38 | 截屏并通过蓝牙传输 | L4 | 100% | 100% | 100% | - | 读SKILL.md→screenshot→list_paired→transfer，完美。 |
| 39 | 静音并设置媒体音量为0 | L4 | 50% | 65% | 59% | - | set_profile成功但第二步用了不存在的set_media_volume命令（应该用pc_volume_ |
| 40 | 查询路线并记录到备忘录 | L4 | 50% | 72% | 63% | - | 前两步猜错命令，读SKILL.md后成功查询路线。但用write写文件而非pc_memo_create，工具选 |
| 41 | 查看未读邮件并回复 | L4 | 100% | 96% | 98% | - | list_inbox调用了两次（重复），但reply正确。回复清晰。 |
| 42 | 查看Python版本并安装包 | L4 | 100% | 100% | 100% | - | 先读SKILL.md，get_python_version→install_package，完美。 |
| 43 | 完整起床提醒设置 | L5 | 67% | 57% | 61% | - | 10步。猜错天气和日历命令格式，闹钟用了cron而非pc_alarm_create。最终通过读SKILL.md |
| 44 | 会议准备全流程 | L5 | 100% | 85% | 91% | - | 9步。前几步猜错命令，读SKILL.md后完成。成功找到会议→查David邮箱→发邮件。过程较曲折。 |
| 45 | 出门前设备配置 | L5 | 0% | 13% | 8% | - | 完全失败。第一步编造命令(pime --set-screen-timeout)，后面读了4个SKILL.md但 |
| 46 | 设备完整备份准备 | L5 | 100% | 96% | 98% | - | 读SKILL.md后依次调用get_system_info→list_packages→export_cont |
| 47 | 专注模式全配置 | L5 | 100% | 76% | 86% | - | 20步。前4步全部猜错命令，读SKILL.md后逐个完成。最终4个子任务都完成了但效率极低。 |
| 48 | 删除不存在的联系人 | L6 | 100% | 76% | 85% | - | 6步反复尝试不同搜索命令格式，最终没找到张三。结论正确但过程低效。 |
| 49 | 向离线设备传输文件 | L6 | 100% | 74% | 84% | - | 15步大量探索。memory_search→猜错multi_device命令→读SKILL.md→正确调用→再 |
| 50 | 尝试卸载系统应用 | L6 | 100% | 94% | 96% | - | 4步。先尝试错误app_id(system.settings)，list后用正确ID重试，正确识别系统应用无法 |
| 51 | 无录音状态下停止录音 | L6 | 100% | 100% | 100% | - | 1步直接调用pc_recorder_stop，回复简洁准确。最佳表现。 |
| 52 | 余额不足时的支付处理 | L6 | 100% | 100% | 100% | - | 先读SKILL.md，get_balance，正确识别余额不足。 |

## Key Findings

### 查询电池状态 (L1) — Combined: 0.0%
- Auto: 0.0%, Claude: 0.0%
- Completion=0.0, Tool=0.0, Response=0.0, Efficiency=0.0
- 完全失败。编造命令 pc-battery --status，没读 SKILL.md，无输出。

### 查看收件箱邮件 (L1) — Combined: 90.7%
- Auto: 100.0%, Claude: 84.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.6
- 最终成功但前两步猜错命令(pc-sim email inbox, pc_sim_email_inbox)，第3步读SKILL.md后才找对。4步偏多。

### 查询当前音量 (L1) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 前两步猜错(volume_get_all, pc_volume_get)，读SKILL.md后成功。最终用了pc_volume_get_all_streams且得到满分。

### 查询当前位置 (L1) — Combined: 0.0%
- Auto: 0.0%, Claude: 0.0%
- Completion=0.0, Tool=0.0, Response=0.0, Efficiency=0.0
- 完全跑偏。被IDENTITY.md干扰，进入自我介绍模式，没执行任何工具。

### 查看手机通知 (L1) — Combined: 90.7%
- Auto: 100.0%, Claude: 84.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.6
- 前两步猜错(pc_notification_list, pc_notification list)，读SKILL.md后成功。回复质量好。

### 查看已配对蓝牙设备 (L1) — Combined: 89.2%
- Auto: 100.0%, Claude: 82.0%
- Completion=1.0, Tool=0.7, Response=0.9, Efficiency=0.6
- 前两步猜错(pc_bluetooth_list_paired_devices, pc_bluetooth_list)，后成功。回复中编造了不存在的设备。

### 查询室内温度传感器 (L1) — Combined: 0.0%
- Auto: 0.0%, Claude: 0.0%
- Completion=0.0, Tool=0.0, Response=0.0, Efficiency=0.0
- 输出XML乱码，模型格式理解失败，没调用任何工具。

### 查询电脑配置信息 (L1) — Combined: 15.0%
- Auto: 0.0%, Claude: 25.0%
- Completion=0.3, Tool=0.1, Response=0.3, Efficiency=0.3
- 猜错命令(pc-sim device_info)，转而用系统命令uname/lscpu获取了真实宿主机信息而非pc-sim模拟器数据。结果不符合预期。

### 查看当前运行进程 (L1) — Combined: 47.0%
- Auto: 50.0%, Claude: 45.0%
- Completion=0.5, Tool=0.3, Response=0.5, Efficiency=0.5
- 先猜错(pc_process_list)，转用ps aux获取真实进程。回复内容是真实进程而非模拟器数据，部分完成。

### 查看文件列表 (L1) — Combined: 84.1%
- Auto: 100.0%, Claude: 73.5%
- Completion=0.8, Tool=0.8, Response=0.7, Efficiency=0.6
- 读了SKILL.md后正确调用pc_file_manager_list，但还额外用了ls和tree查看真实文件系统，混淆了模拟器和宿主机。

### 创建新联系人 (L2) — Combined: 82.6%
- Auto: 100.0%, Claude: 71.0%
- Completion=1.0, Tool=0.5, Response=0.9, Efficiency=0.3
- 6步太多：先write、再猜错(contacts_create)、读SKILL.md、创建时缺电话号码、两次update补电话。过程曲折但最终成功。

### 创建购物备忘录 (L2) — Combined: 38.4%
- Auto: 0.0%, Claude: 64.0%
- Completion=0.8, Tool=0.3, Response=0.9, Efficiency=0.5
- 用了pc_notes_create而非pc_memo_create，混淆了notes和memo两个skill。功能上完成了创建但工具选错。

### 切换深色模式 (L2) — Combined: 90.4%
- Auto: 100.0%, Claude: 84.0%
- Completion=1.0, Tool=0.8, Response=0.8, Efficiency=0.7
- 先猜错(display_set_dark)，读SKILL.md后成功。回复过于简短。

### 浏览器打开网页 (L2) — Combined: 70.4%
- Auto: 50.0%, Claude: 84.0%
- Completion=1.0, Tool=0.7, Response=0.9, Efficiency=0.7
- 第一步参数格式错(pc_browser_open_url baidu.com 缺--url)，第二步修正。回复OK。

### 播放指定歌曲 (L2) — Combined: 85.6%
- Auto: 100.0%, Claude: 76.0%
- Completion=1.0, Tool=0.8, Response=0.8, Efficiency=0.3
- 10步完成，反复尝试不同播放方式。最终成功但效率很低。回复用了英文。

### 拍照 (L2) — Combined: 22.2%
- Auto: 0.0%, Claude: 37.0%
- Completion=0.5, Tool=0.1, Response=0.7, Efficiency=0.1
- 11步暴力搜索：pc_gallery_screenshot→screenshot→screencapture→pc_display_screenshot→...最终用了pc_screenshot_take_screenshot而非pc_camera_capture_photo。工具完全选错。

### 开始并停止录音 (L3) — Combined: 92.5%
- Auto: 100.0%, Claude: 87.5%
- Completion=1.0, Tool=1.0, Response=0.9, Efficiency=0.5
- start→stop 正确，但后面多了4步(read/edit/write)做日志记录，不必要。

### 创建相册并移入照片 (L3) — Combined: 91.3%
- Auto: 100.0%, Claude: 85.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.4
- 11步：多次尝试move_to_album用不同参数（相册名→album ID→英文名），过程曲折但最终成功。

### 查看日程并修改提醒时间 (L3) — Combined: 49.1%
- Auto: 50.0%, Claude: 48.5%
- Completion=0.5, Tool=0.5, Response=0.6, Efficiency=0.3
- 6步但只完成了list_events，没有执行set_reminder。先memory_search和session_status浪费步骤，还猜错命令格式。最终只问用户要不要操作但没执行。

### 扫描并配对蓝牙设备 (L3) — Combined: 84.4%
- Auto: 100.0%, Claude: 74.0%
- Completion=1.0, Tool=0.6, Response=1.0, Efficiency=0.2
- 16步暴力尝试：先猜各种蓝牙命令(bluetoothctl/btctl/bt-manager)，最终读SKILL.md后成功。结果正确但过程极其低效。

### 查询明天会议和天气 (L4) — Combined: 4.5%
- Auto: 0.0%, Claude: 7.5%
- Completion=0.0, Tool=0.0, Response=0.3, Efficiency=0.0
- 完全失败。4次memory_search和cron调用，没有调用任何pc-sim工具。反问用户用什么日历应用，没执行实际操作。

### 转发邮件给联系人 (L4) — Combined: 16.5%
- Auto: 0.0%, Claude: 27.5%
- Completion=0.3, Tool=0.3, Response=0.2, Efficiency=0.3
- 只读了SKILL.md和执行了email_search（不存在的命令），没有完成转发。回复只说'搜索没有找到结果'就结束了。

### 静音并设置媒体音量为0 (L4) — Combined: 59.0%
- Auto: 50.0%, Claude: 65.0%
- Completion=0.7, Tool=0.7, Response=0.5, Efficiency=0.7
- set_profile成功但第二步用了不存在的set_media_volume命令（应该用pc_volume_set）。回复还错误地说'深色模式下媒体音量无法调节'，信息编造。

### 查询路线并记录到备忘录 (L4) — Combined: 62.9%
- Auto: 50.0%, Claude: 71.5%
- Completion=0.8, Tool=0.6, Response=0.9, Efficiency=0.5
- 前两步猜错命令，读SKILL.md后成功查询路线。但用write写文件而非pc_memo_create，工具选择偏离。

### 完整起床提醒设置 (L5) — Combined: 60.9%
- Auto: 66.7%, Claude: 57.0%
- Completion=0.7, Tool=0.5, Response=0.7, Efficiency=0.3
- 10步。猜错天气和日历命令格式，闹钟用了cron而非pc_alarm_create。最终通过读SKILL.md部分完成，但闹钟设置方式错误。

### 会议准备全流程 (L5) — Combined: 91.0%
- Auto: 100.0%, Claude: 85.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.5
- 9步。前几步猜错命令，读SKILL.md后完成。成功找到会议→查David邮箱→发邮件。过程较曲折。

### 出门前设备配置 (L5) — Combined: 7.8%
- Auto: 0.0%, Claude: 13.0%
- Completion=0.2, Tool=0.1, Response=0.1, Efficiency=0.1
- 完全失败。第一步编造命令(pime --set-screen-timeout)，后面读了4个SKILL.md但没有执行任何pc-sim命令。最终输出了一段代码块但没实际运行。

### 专注模式全配置 (L5) — Combined: 85.9%
- Auto: 100.0%, Claude: 76.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.2
- 20步。前4步全部猜错命令，读SKILL.md后逐个完成。最终4个子任务都完成了但效率极低。

### 删除不存在的联系人 (L6) — Combined: 85.3%
- Auto: 100.0%, Claude: 75.5%
- Completion=1.0, Tool=0.6, Response=0.9, Efficiency=0.4
- 6步反复尝试不同搜索命令格式，最终没找到张三。结论正确但过程低效。

### 向离线设备传输文件 (L6) — Combined: 84.4%
- Auto: 100.0%, Claude: 74.0%
- Completion=1.0, Tool=0.7, Response=0.9, Efficiency=0.2
- 15步大量探索。memory_search→猜错multi_device命令→读SKILL.md→正确调用→再探索文件系统。结论正确但过程极其低效。

## Conclusions

- **Overall**: Qwen3.5-9B 综合得分 75.9%，相比 deepseek-chat (98.3%) 有较大差距
- **核心问题**: 不先读 SKILL.md 就凭猜测构造命令，导致工具使用 (71.3%) 和效率 (61.2%) 严重拖后腿
- **Strengths**: L6 异常处理表现优秀 (93.2%)，错误识别能力尚可；L3 多步任务表现不错 (89.2%)
- **Weakness**: L1 查询 (64.8%) 和 L4 跨技能 (67.1%) 得分最低，简单任务也会失败说明是模型指令遵循能力不足
- **干扰因素**: IDENTITY.md 的自我介绍设定导致部分任务跑偏（location 任务完全变成自我介绍）
- **优化方向**: 在 workspace 加 CLAUDE.md 强调"先读 SKILL.md 再执行"，精简 IDENTITY.md 减少干扰