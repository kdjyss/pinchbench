# PC-Sim Benchmark Report (Claude Manual Scoring)

**Model:** smart-router/auto
**Scorer:** Claude Opus 4.6 (manual review of all 52 transcripts)
**Tasks:** 52

## Overall Scores

| Metric | Score |
|--------|-------|
| Automated Score | 88.9% |
| Claude Manual Score | 85.9% |
| **Combined Score** | **87.1%** |

### Scoring Dimensions (Claude Manual)

| Dimension | Weight | Score | Description |
|-----------|--------|-------|-------------|
| Task Completion | 30% | 92.7% | 是否完整完成用户请求 |
| Tool Usage | 25% | 81.3% | 工具选择是否正确、参数是否合理 |
| Response Quality | 25% | 93.7% | 回答是否清晰、准确、结构化 |
| Efficiency | 20% | 71.5% | 步骤数是否合理 |

## Scores by Difficulty

| Level | Name | Tasks | Auto | Claude | Combined | Efficiency |
|-------|------|-------|------|--------|----------|------------|
| L1 | 信息查询 | 14 | 82.1% | 81.8% | 82.0% | 78.6% |
| L2 | 单步操作 | 12 | 95.8% | 95.1% | 95.4% | 85.0% |
| L3 | 同技能多步 | 8 | 100.0% | 92.8% | 95.7% | 76.2% |
| L4 | 跨技能协作 | 8 | 81.2% | 77.4% | 78.9% | 52.5% |
| L5 | 复杂场景 | 5 | 75.0% | 71.5% | 72.9% | 42.0% |
| L6 | 异常处理 | 5 | 100.0% | 91.9% | 95.1% | 72.0% |

## Detailed Results

| # | Task | Lvl | Auto | Claude | Combined | Steps | Notes |
|---|------|-----|------|--------|----------|-------|-------|
| 1 | 查询北京天气 | L1 | 50% | 65% | 59% | - | 没用pc-sim，用web_search+web_fetch查了真实天气。回复信息丰富但完全绕过了模拟器。 |
| 2 | 查询电池状态 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 3 | 查询联系人列表 | L1 | 100% | 100% | 100% | - | 1步直接调用，完美。 |
| 4 | 查看收件箱邮件 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 5 | 查询当前音量 | L1 | 100% | 100% | 100% | - | 1步直接调用pc_volume_get，完美。 |
| 6 | 查看闹钟列表 | L1 | 100% | 100% | 100% | - | 1步直接调用，完美。 |
| 7 | 查询当前位置 | L1 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 8 | 查看手机通知 | L1 | 100% | 87% | 92% | - | 4步。前两步猜错，读SKILL.md后成功。表格展示。 |
| 9 | 查看已配对蓝牙设备 | L1 | 100% | 94% | 96% | - | 3步。第一步猜错(pc_bluetooth_list)，读SKILL.md后成功。 |
| 10 | 查询室内温度传感器 | L1 | 100% | 98% | 99% | - | 3步。先list_sensors再read，稍多但合理。 |
| 11 | 查看可播放视频列表 | L1 | 100% | 94% | 96% | - | 3步。第一步猜错(pc_video_player_library)，读SKILL.md后成功。 |
| 12 | 查询电脑配置信息 | L1 | 0% | 25% | 15% | - | 猜错(pc_device_info, pc_device_list)后用uname/lscpu/lspci获取 |
| 13 | 查看当前运行进程 | L1 | 50% | 40% | 44% | - | 猜错(pc_shell_processlist, pc_shell pkill)后用ps aux。混淆模拟器。 |
| 14 | 查看文件列表 | L1 | 50% | 43% | 46% | - | 猜错(pc_file_manager_list_root)后用ls和tree。混淆模拟器。 |
| 15 | 创建新联系人 | L2 | 100% | 94% | 96% | - | 3步。read后create缺电话→update补上。过程曲折但正确。 |
| 16 | 设置早起闹钟 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 17 | 创建购物备忘录 | L2 | 100% | 100% | 100% | - | read→正确调用pc_memo_create，2步完美。 |
| 18 | 调整屏幕亮度 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 19 | 支付宝付款 | L2 | 100% | 94% | 96% | - | 3步。第一步猜错(pc_payment_alipay_transfer)，读后成功。 |
| 20 | 切换深色模式 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 21 | 浏览器打开网页 | L2 | 50% | 82% | 70% | - | 4步。前两步猜错(pc_browser_url, pc_web_url)，读后成功。 |
| 22 | 播放指定歌曲 | L2 | 100% | 92% | 95% | - | 5步。前两步猜错(play "Summer Breeze", add_queue)，读后list→play成功 |
| 23 | 设置5分钟倒计时 | L2 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 24 | 拍照 | L2 | 100% | 100% | 100% | - | read→正确调用pc_camera_capture_photo，2步完美。 |
| 25 | 创建带标签的笔记 | L2 | 100% | 98% | 99% | - | 3步。read两个SKILL.md后正确调用。 |
| 26 | 授予应用权限 | L2 | 100% | 82% | 90% | - | 4步。猜错→web_search→读→成功。用了web搜索很奇怪。 |
| 27 | 创建联系人并加入分组 | L3 | 100% | 94% | 96% | - | 4步。中间多创建了一个work组(不必要)。 |
| 28 | 撰写并发送邮件 | L3 | 100% | 98% | 99% | - | 3步。compose→send，逻辑合理。 |
| 29 | 开始并停止录音 | L3 | 100% | 98% | 99% | - | 3步。start→stop→stop(重复一次)。 |
| 30 | 查看备忘录并置顶 | L3 | 100% | 87% | 92% | - | 5步。pin参数猜错两次(m002, --pinned 1)，读后成功。 |
| 31 | 创建相册并移入照片 | L3 | 100% | 80% | 88% | - | 7步。move_to_album猜错参数多次，创建了两个相册(旅行2026+travel2026)。回复说缓存 |
| 32 | 查看日程并修改提醒时间 | L3 | 100% | 85% | 91% | - | 6步。memory_search+web_search(多余)，猜错calendar命令，读后成功。 |
| 33 | 扫描并配对蓝牙设备 | L3 | 100% | 100% | 100% | - | read→scan→pair，3步完美。 |
| 34 | 暂停音乐并开启随机播放 | L3 | 100% | 100% | 100% | - | read→pause→shuffle，3步完美。 |
| 35 | 查联系人电话并拨打 | L4 | 100% | 82% | 90% | - | 6步。猜错3次(contacts_get, call_dial, phone_call_call)，读后成功。 |
| 36 | 查询明天会议和天气 | L4 | 33% | 52% | 44% | - | 7步。calendar_list_events成功，但天气用了web_search+web_fetch查真实天 |
| 37 | 转发邮件给联系人 | L4 | 67% | 74% | 71% | - | 6步。search多次失败，list_inbox找到后forward成功。但转发邮箱用了david.zhang |
| 38 | 截屏并通过蓝牙传输 | L4 | 50% | 50% | 50% | - | 18步极低效。截屏成功但大量猜错命令。蓝牙传输部分声称无法传输图片文件（错误），只发了文本描述。 |
| 39 | 静音并设置媒体音量为0 | L4 | 100% | 76% | 86% | - | 14步极低效。反复猜静音命令。最终成功。 |
| 40 | 查询路线并记录到备忘录 | L4 | 100% | 98% | 99% | - | 4步。read→get_directions→read→memo_create，高效。 |
| 41 | 查看未读邮件并回复 | L4 | 100% | 87% | 92% | - | 5步。前两步猜错(mail inbox, pc_email_inbox)，读后成功。回复用英文'see you |
| 42 | 查看Python版本并安装包 | L4 | 100% | 100% | 100% | - | read→get_python_version→install_package，3步完美。 |
| 43 | 完整起床提醒设置 | L5 | 0% | 16% | 9% | - | 8步。用cron设闹钟(错)，web_search查天气(非pc-sim)，sessions_spawn查日历 |
| 44 | 会议准备全流程 | L5 | 100% | 83% | 90% | - | 13步偏多。前几步猜错，最终找到会议→查David邮箱→发邮件。全部成功。 |
| 45 | 出门前设备配置 | L5 | 100% | 96% | 98% | - | 8步。读4个SKILL.md后4步精准完成。高效。 |
| 46 | 设备完整备份准备 | L5 | 100% | 88% | 92% | - | 10步。第一步猜错。get_info→list_packages→export_contacts→write。 |
| 47 | 专注模式全配置 | L5 | 75% | 76% | 75% | - | 23步极低效。前几步猜错大量命令。4个子任务基本完成(dnd→brightness→play→countdow |
| 48 | 删除不存在的联系人 | L6 | 100% | 96% | 97% | - | 2步。memory_search(多余)→list确认不存在。高效。 |
| 49 | 向离线设备传输文件 | L6 | 100% | 86% | 91% | - | 10步。正确识别平板离线，但大量探索(list_albums/list_photos/send多次)。最终发到 |
| 50 | 尝试卸载系统应用 | L6 | 100% | 78% | 87% | - | 10步。前6步猜各种命令(list, --help, list-skills多次)。最终识别系统应用无法卸载。 |
| 51 | 无录音状态下停止录音 | L6 | 100% | 100% | 100% | - | read→正确调用，2步完美。 |
| 52 | 余额不足时的支付处理 | L6 | 100% | 100% | 100% | - | read→get_balance，2步完美。 |

## Key Findings

### 查询北京天气 (L1) — Combined: 59.0%
- Auto: 50.0%, Claude: 65.0%
- Completion=0.8, Tool=0.0, Response=1.0, Efficiency=0.8
- 没用pc-sim，用web_search+web_fetch查了真实天气。回复信息丰富但完全绕过了模拟器。

### 查看手机通知 (L1) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 4步。前两步猜错，读SKILL.md后成功。表格展示。

### 查询电脑配置信息 (L1) — Combined: 15.0%
- Auto: 0.0%, Claude: 25.0%
- Completion=0.3, Tool=0.1, Response=0.3, Efficiency=0.3
- 猜错(pc_device_info, pc_device_list)后用uname/lscpu/lspci获取真实系统信息。混淆模拟器和宿主机。

### 查看当前运行进程 (L1) — Combined: 44.3%
- Auto: 50.0%, Claude: 40.5%
- Completion=0.5, Tool=0.2, Response=0.5, Efficiency=0.4
- 猜错(pc_shell_processlist, pc_shell pkill)后用ps aux。混淆模拟器。

### 查看文件列表 (L1) — Combined: 45.8%
- Auto: 50.0%, Claude: 43.0%
- Completion=0.5, Tool=0.2, Response=0.6, Efficiency=0.4
- 猜错(pc_file_manager_list_root)后用ls和tree。混淆模拟器。

### 浏览器打开网页 (L2) — Combined: 69.5%
- Auto: 50.0%, Claude: 82.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.5
- 4步。前两步猜错(pc_browser_url, pc_web_url)，读后成功。

### 播放指定歌曲 (L2) — Combined: 94.9%
- Auto: 100.0%, Claude: 91.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.7
- 5步。前两步猜错(play "Summer Breeze", add_queue)，读后list→play成功。

### 授予应用权限 (L2) — Combined: 89.5%
- Auto: 100.0%, Claude: 82.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.5
- 4步。猜错→web_search→读→成功。用了web搜索很奇怪。

### 查看备忘录并置顶 (L3) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 5步。pin参数猜错两次(m002, --pinned 1)，读后成功。

### 创建相册并移入照片 (L3) — Combined: 88.3%
- Auto: 100.0%, Claude: 80.5%
- Completion=1.0, Tool=0.8, Response=0.9, Efficiency=0.4
- 7步。move_to_album猜错参数多次，创建了两个相册(旅行2026+travel2026)。回复说缓存问题。

### 查看日程并修改提醒时间 (L3) — Combined: 91.0%
- Auto: 100.0%, Claude: 85.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.5
- 6步。memory_search+web_search(多余)，猜错calendar命令，读后成功。

### 查联系人电话并拨打 (L4) — Combined: 89.5%
- Auto: 100.0%, Claude: 82.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.5
- 6步。猜错3次(contacts_get, call_dial, phone_call_call)，读后成功。

### 查询明天会议和天气 (L4) — Combined: 44.2%
- Auto: 33.3%, Claude: 51.5%
- Completion=0.6, Tool=0.4, Response=0.7, Efficiency=0.3
- 7步。calendar_list_events成功，但天气用了web_search+web_fetch查真实天气而非pc-sim。混合使用了模拟器和真实数据。回复说明天没有会议（错误）。

### 转发邮件给联系人 (L4) — Combined: 71.1%
- Auto: 66.7%, Claude: 74.0%
- Completion=0.8, Tool=0.7, Response=0.9, Efficiency=0.5
- 6步。search多次失败，list_inbox找到后forward成功。但转发邮箱用了david.zhang@而非david@。

### 截屏并通过蓝牙传输 (L4) — Combined: 49.7%
- Auto: 50.0%, Claude: 49.5%
- Completion=0.6, Tool=0.5, Response=0.6, Efficiency=0.2
- 18步极低效。截屏成功但大量猜错命令。蓝牙传输部分声称无法传输图片文件（错误），只发了文本描述。

### 静音并设置媒体音量为0 (L4) — Combined: 85.9%
- Auto: 100.0%, Claude: 76.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.2
- 14步极低效。反复猜静音命令。最终成功。

### 查看未读邮件并回复 (L4) — Combined: 92.2%
- Auto: 100.0%, Claude: 87.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.6
- 5步。前两步猜错(mail inbox, pc_email_inbox)，读后成功。回复用英文'see you tomorrow'而非中文。

### 完整起床提醒设置 (L5) — Combined: 9.3%
- Auto: 0.0%, Claude: 15.5%
- Completion=0.2, Tool=0.1, Response=0.2, Efficiency=0.1
- 8步。用cron设闹钟(错)，web_search查天气(非pc-sim)，sessions_spawn查日历(失败)。3个子任务都没正确完成。

### 会议准备全流程 (L5) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- 13步偏多。前几步猜错，最终找到会议→查David邮箱→发邮件。全部成功。

### 设备完整备份准备 (L5) — Combined: 92.5%
- Auto: 100.0%, Claude: 87.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.5
- 10步。第一步猜错。get_info→list_packages→export_contacts→write。完成。

### 专注模式全配置 (L5) — Combined: 75.3%
- Auto: 75.0%, Claude: 75.5%
- Completion=0.9, Tool=0.7, Response=1.0, Efficiency=0.3
- 23步极低效。前几步猜错大量命令。4个子任务基本完成(dnd→brightness→play→countdown)。

### 向离线设备传输文件 (L6) — Combined: 91.3%
- Auto: 100.0%, Claude: 85.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.4
- 10步。正确识别平板离线，但大量探索(list_albums/list_photos/send多次)。最终发到手机上，是合理的替代方案。

### 尝试卸载系统应用 (L6) — Combined: 87.1%
- Auto: 100.0%, Claude: 78.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.3
- 10步。前6步猜各种命令(list, --help, list-skills多次)。最终识别系统应用无法卸载。

## Conclusions

- **Overall**: smart-router/auto 综合表现接近 Qwen 9B v3，automated 88.9%
- **亮点**: L3 多步任务 100% 满分，L6 异常处理 100% 满分，leave_home 一次通过
- **问题**: weather_query 用了 web_search 而非 pc-sim，device_info/processes/files 用系统命令混淆模拟器
- **效率短板**: silent_volume(14步)、focus_mode(23步)、screenshot_transfer(18步)
- **智能路由特点**: 部分任务自动选择了 web 工具而非 pc-sim，说明路由策略对模拟器场景不够精准
