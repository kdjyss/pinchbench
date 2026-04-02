# PC-Sim Benchmark Report (Claude Manual Scoring)

**Model:** Qwen3.5-9B v2 (local-vllm, after openclaw updates)
**Scorer:** Claude Opus 4.6 (manual review of all 52 transcripts)
**Tasks:** 52

## Overall Scores

| Metric | Score |
|--------|-------|
| Automated Score | 83.0% |
| Claude Manual Score | 77.4% |
| **Combined Score** | **79.6%** |

### Scoring Dimensions (Claude Manual)

| Dimension | Weight | Score | Description |
|-----------|--------|-------|-------------|
| Task Completion | 30% | 84.4% | 是否完整完成用户请求 |
| Tool Usage | 25% | 73.1% | 工具选择是否正确、参数是否合理 |
| Response Quality | 25% | 84.6% | 回答是否清晰、准确、结构化 |
| Efficiency | 20% | 63.1% | 步骤数是否合理 |

## Scores by Difficulty

| Level | Name | Tasks | Auto | Claude | Combined | Efficiency |
|-------|------|-------|------|--------|----------|------------|
| L1 | 信息查询 | 14 | 85.7% | 78.2% | 81.2% | 64.3% |
| L2 | 单步操作 | 12 | 83.3% | 76.7% | 79.4% | 65.8% |
| L3 | 同技能多步 | 8 | 87.5% | 81.6% | 84.0% | 67.5% |
| L4 | 跨技能协作 | 8 | 83.3% | 82.0% | 82.5% | 67.5% |
| L5 | 复杂场景 | 5 | 70.0% | 58.6% | 63.2% | 28.0% |
| L6 | 异常处理 | 5 | 80.0% | 81.1% | 80.7% | 74.0% |

## Detailed Results

| # | Task | Lvl | Auto | Claude | Combined | Steps | Notes |
|---|------|-----|------|--------|----------|-------|-------|
| 1 | 查询北京天气 | L1 | 100% | 100% | 100% | - | 完美。read SKILL.md → 正确调用，回复简洁准确。 |
| 2 | 查询电池状态 | L1 | 100% | 89% | 93% | - | v1的0分修复了。第一步猜错(pc-sim battery status)，读SKILL.md后成功。3步完成 |
| 3 | 查询联系人列表 | L1 | 100% | 80% | 88% | - | 5步偏多：前3步猜错(pc_contacts list, contacts list, list-skills |
| 4 | 查看收件箱邮件 | L1 | 100% | 89% | 93% | - | 第一步猜错(pc_email_inbox)，读SKILL.md后成功。3步可接受。 |
| 5 | 查询当前音量 | L1 | 100% | 98% | 98% | - | 1步直接调用 pc_volume_get，完美！v1需要4步。回复简洁但偏短。 |
| 6 | 查看闹钟列表 | L1 | 100% | 100% | 100% | - | 1步直接调用，表格展示，完美。 |
| 7 | 查询当前位置 | L1 | 0% | 5% | 3% | - | 仍然失败。只做了memory_search，没有调用任何pc-sim工具。反问用户位置信息而非查模拟器。 |
| 8 | 查看手机通知 | L1 | 100% | 80% | 88% | - | 5步：前3步猜错(push_notification list, list-skills/grep, push |
| 9 | 查看已配对蓝牙设备 | L1 | 100% | 89% | 93% | - | 第一步猜错(pc_bluetooth_connected_devices)，读SKILL.md后成功。回复准确 |
| 10 | 查询室内温度传感器 | L1 | 100% | 100% | 100% | - | v1的0分修复了。read SKILL.md → 正确调用，完美。 |
| 11 | 查看可播放视频列表 | L1 | 100% | 76% | 86% | - | 6步太多：前5步全在猜(pc_video_player list, pc_video_info, -l/gre |
| 12 | 查询电脑配置信息 | L1 | 100% | 100% | 100% | - | v1的0分修复了。read SKILL.md → 正确调用，回复准确展示模拟器配置。 |
| 13 | 查看当前运行进程 | L1 | 50% | 45% | 47% | - | 与v1相同问题：猜错(pc_process_list)后用ps aux获取真实进程。 |
| 14 | 查看文件列表 | L1 | 50% | 44% | 46% | - | v1退步。直接用tree命令查看真实文件系统，没有调用pc_file_manager_list。混淆了模拟器和 |
| 15 | 创建新联系人 | L2 | 100% | 94% | 96% | - | 比v1大幅改善(v1=6步)。memory_search(多余)→read→正确创建，3步。参数正确。 |
| 16 | 设置早起闹钟 | L2 | 100% | 76% | 86% | - | 7步太多：前5步猜各种格式(alarm_set, help, web_search, list-skills, |
| 17 | 创建购物备忘录 | L2 | 100% | 100% | 100% | - | v1的0分修复了！read SKILL.md → pc_memo_create，这次用对了工具。完美。 |
| 18 | 调整屏幕亮度 | L2 | 100% | 95% | 97% | - | read → 正确调用。回复过于简短但准确。 |
| 19 | 支付宝付款 | L2 | 100% | 82% | 90% | - | 5步：memory_search(多余)→猜错(pay 200 --platform)→猜错(get_info |
| 20 | 切换深色模式 | L2 | 100% | 95% | 97% | - | read → 正确调用，完美。回复简短。 |
| 21 | 浏览器打开网页 | L2 | 100% | 89% | 93% | - | v1修复：第一步猜错(browser_open_url)，读SKILL.md后成功。回复详细。 |
| 22 | 播放指定歌曲 | L2 | 100% | 100% | 100% | - | 大幅改善！read→list→play --track_id，3步精准完成。v1需要10步。 |
| 23 | 设置5分钟倒计时 | L2 | 100% | 89% | 93% | - | 第一步猜错(pc_timer_timershell)，读SKILL.md后成功。3步可接受。 |
| 24 | 拍照 | L2 | 0% | 0% | 0% | - | 完全失败。0步调用，无输出。比v1(11步暴力搜索)更差，这次连尝试都没有。 |
| 25 | 创建带标签的笔记 | L2 | 100% | 98% | 99% | - | read→create→tag，3步流程合理。额外调用tag补充标签是合理操作。 |
| 26 | 授予应用权限 | L2 | 0% | 2% | 2% | - | v1满分现在变0分。猜错命令(system_permission_grant)，读SKILL.md后又猜(li |
| 27 | 创建联系人并加入分组 | L3 | 100% | 100% | 100% | - | read→create→add_to_group，3步完美。 |
| 28 | 撰写并发送邮件 | L3 | 100% | 100% | 100% | - | read→直接pc_email_send，2步完美。比v1(4步compose+send)更高效。 |
| 29 | 开始并停止录音 | L3 | 100% | 100% | 100% | - | read→start→stop，3步完美。比v1(7步)大幅改善。 |
| 30 | 查看备忘录并置顶 | L3 | 100% | 85% | 91% | - | 6步：list后pin时猜错参数(--id vs --memo_id)两次，读SKILL.md后成功。 |
| 31 | 创建相册并移入照片 | L3 | 100% | 86% | 91% | - | 9步。move_to_album参数反复尝试（中文名→英文名→album ID）。最终成功。 |
| 32 | 查看日程并修改提醒时间 | L3 | 100% | 100% | 100% | - | v1的0.5修复为满分！read→list_events→set_reminder，3步完美。 |
| 33 | 扫描并配对蓝牙设备 | L3 | 0% | 0% | 0% | - | v1满分现在变0分。0步调用，无输出。完全失败。 |
| 34 | 暂停音乐并开启随机播放 | L3 | 100% | 82% | 90% | - | 5步：前两步猜错(pc_music_pause, pc_music_shuffle)，读SKILL.md后成功 |
| 35 | 查联系人电话并拨打 | L4 | 100% | 89% | 93% | - | 5步。第一步猜错(contacts_get)，中间一步猜错(dial --contact_id)。最终正确拨号 |
| 36 | 查询明天会议和天气 | L4 | 100% | 82% | 90% | - | v1的0分修复了！7步偏多(session_status+2步猜错)，但成功获取日历和天气。回复有日期偏差但信 |
| 37 | 转发邮件给联系人 | L4 | 67% | 76% | 72% | - | v1的0分改善。4步：search失败→list_inbox→forward。转发成功但用了错误邮箱(davi |
| 38 | 截屏并通过蓝牙传输 | L4 | 100% | 82% | 89% | - | 18步极其低效：截屏和蓝牙传输成功，但中间大量探索(cat截图文件、find搜索、ls目录)。结果正确但过程臃 |
| 39 | 静音并设置媒体音量为0 | L4 | 100% | 98% | 99% | - | v1修复！4步：read两个SKILL.md→set_profile→volume_set，正确使用了两个sk |
| 40 | 查询路线并记录到备忘录 | L4 | 100% | 98% | 99% | - | v1修复！4步：read→get_directions→read→memo_create。这次用了正确的pc_ |
| 41 | 查看未读邮件并回复 | L4 | 100% | 100% | 100% | - | read→list_inbox→reply，3步完美。 |
| 42 | 查看Python版本并安装包 | L4 | 0% | 32% | 19% | - | v1满分现在变0分。直接用python3 --version和pip3 install，完全没用pc-sim工 |
| 43 | 完整起床提醒设置 | L5 | 100% | 83% | 90% | - | v1修复为满分！10步偏多(前3步猜错)，但3个子任务全部完成。回复结构优秀。 |
| 44 | 会议准备全流程 | L5 | 100% | 85% | 91% | - | 8步。前两步猜错，读SKILL.md后完成。成功找会议→查邮箱→发邮件。 |
| 45 | 出门前设备配置 | L5 | 100% | 81% | 89% | - | v1的0分修复了！12步偏多(前4步猜错)，但4个子任务全部完成。回复清晰。 |
| 46 | 设备完整备份准备 | L5 | 50% | 39% | 43% | - | v1退步。18步，用了真实系统命令(uname/rpm/dpkg)而非pc-sim工具。混淆了模拟器和宿主机。 |
| 47 | 专注模式全配置 | L5 | 0% | 5% | 3% | - | v1满分现在变0分。11步全部失败：编造各种奇怪命令格式(parse_pcsim_launch, pc_dis |
| 48 | 删除不存在的联系人 | L6 | 100% | 91% | 95% | - | 4步。第一步猜错(contacts_delete_contact)，读SKILL.md后search+list |
| 49 | 向离线设备传输文件 | L6 | 0% | 30% | 18% | - | v1满分现在退步。1步猜错(multi_device list)后就放弃，没读SKILL.md。回复建议用Ai |
| 50 | 尝试卸载系统应用 | L6 | 100% | 100% | 100% | - | read→list_installed，正确识别系统应用无法卸载。回复解释充分。 |
| 51 | 无录音状态下停止录音 | L6 | 100% | 84% | 91% | - | 4步：前两步猜错(recorder_stop不带pc-sim前缀)，读SKILL.md后成功。 |
| 52 | 余额不足时的支付处理 | L6 | 100% | 100% | 100% | - | read→get_balance，正确识别余额不足。完美。 |

## Key Findings

### 查询电池状态 (L1) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- v1的0分修复了。第一步猜错(pc-sim battery status)，读SKILL.md后成功。3步完成可接受。

### 查询联系人列表 (L1) — Combined: 88.3%
- Auto: 100.0%, Claude: 80.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.4
- 5步偏多：前3步猜错(pc_contacts list, contacts list, list-skills|grep)，读SKILL.md后成功。回复表格格式好。

### 查看收件箱邮件 (L1) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(pc_email_inbox)，读SKILL.md后成功。3步可接受。

### 查询当前位置 (L1) — Combined: 3.0%
- Auto: 0.0%, Claude: 5.0%
- Completion=0.0, Tool=0.0, Response=0.2, Efficiency=0.0
- 仍然失败。只做了memory_search，没有调用任何pc-sim工具。反问用户位置信息而非查模拟器。

### 查看手机通知 (L1) — Combined: 88.3%
- Auto: 100.0%, Claude: 80.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.4
- 5步：前3步猜错(push_notification list, list-skills|grep, push_notification list --user)。回复质量好。

### 查看已配对蓝牙设备 (L1) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(pc_bluetooth_connected_devices)，读SKILL.md后成功。回复准确无编造。比v1改善。

### 查看可播放视频列表 (L1) — Combined: 85.6%
- Auto: 100.0%, Claude: 76.0%
- Completion=1.0, Tool=0.6, Response=1.0, Efficiency=0.3
- 6步太多：前5步全在猜(pc_video_player list, pc_video_info, -l|grep, --help, list-tools|grep)。最终成功但效率极低。

### 查看当前运行进程 (L1) — Combined: 47.0%
- Auto: 50.0%, Claude: 45.0%
- Completion=0.5, Tool=0.3, Response=0.5, Efficiency=0.5
- 与v1相同问题：猜错(pc_process_list)后用ps aux获取真实进程。

### 查看文件列表 (L1) — Combined: 46.1%
- Auto: 50.0%, Claude: 43.5%
- Completion=0.5, Tool=0.3, Response=0.6, Efficiency=0.3
- v1退步。直接用tree命令查看真实文件系统，没有调用pc_file_manager_list。混淆了模拟器和宿主机。

### 设置早起闹钟 (L2) — Combined: 85.6%
- Auto: 100.0%, Claude: 76.0%
- Completion=1.0, Tool=0.6, Response=1.0, Efficiency=0.3
- 7步太多：前5步猜各种格式(alarm_set, help, web_search, list-skills, alarm_set again)，读SKILL.md后成功。比v1(2步)严重退步。

### 支付宝付款 (L2) — Combined: 89.5%
- Auto: 100.0%, Claude: 82.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.5
- 5步：memory_search(多余)→猜错(pay 200 --platform)→猜错(get_info)→read→成功。回复清晰。

### 浏览器打开网页 (L2) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- v1修复：第一步猜错(browser_open_url)，读SKILL.md后成功。回复详细。

### 设置5分钟倒计时 (L2) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 第一步猜错(pc_timer_timershell)，读SKILL.md后成功。3步可接受。

### 拍照 (L2) — Combined: 0.0%
- Auto: 0.0%, Claude: 0.0%
- Completion=0.0, Tool=0.0, Response=0.0, Efficiency=0.0
- 完全失败。0步调用，无输出。比v1(11步暴力搜索)更差，这次连尝试都没有。

### 授予应用权限 (L2) — Combined: 1.5%
- Auto: 0.0%, Claude: 2.5%
- Completion=0.0, Tool=0.1, Response=0.0, Efficiency=0.0
- v1满分现在变0分。猜错命令(system_permission_grant)，读SKILL.md后又猜(list-skills|grep)，最终输出HEARTBEAT_OK乱码。完全失败。

### 查看备忘录并置顶 (L3) — Combined: 91.0%
- Auto: 100.0%, Claude: 85.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.5
- 6步：list后pin时猜错参数(--id vs --memo_id)两次，读SKILL.md后成功。

### 创建相册并移入照片 (L3) — Combined: 91.3%
- Auto: 100.0%, Claude: 85.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.4
- 9步。move_to_album参数反复尝试（中文名→英文名→album ID）。最终成功。

### 扫描并配对蓝牙设备 (L3) — Combined: 0.0%
- Auto: 0.0%, Claude: 0.0%
- Completion=0.0, Tool=0.0, Response=0.0, Efficiency=0.0
- v1满分现在变0分。0步调用，无输出。完全失败。

### 暂停音乐并开启随机播放 (L3) — Combined: 89.5%
- Auto: 100.0%, Claude: 82.5%
- Completion=1.0, Tool=0.8, Response=0.9, Efficiency=0.5
- 5步：前两步猜错(pc_music_pause, pc_music_shuffle)，读SKILL.md后成功。

### 查联系人电话并拨打 (L4) — Combined: 93.4%
- Auto: 100.0%, Claude: 89.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.7
- 5步。第一步猜错(contacts_get)，中间一步猜错(dial --contact_id)。最终正确拨号。

### 查询明天会议和天气 (L4) — Combined: 89.5%
- Auto: 100.0%, Claude: 82.5%
- Completion=1.0, Tool=0.8, Response=0.9, Efficiency=0.5
- v1的0分修复了！7步偏多(session_status+2步猜错)，但成功获取日历和天气。回复有日期偏差但信息基本正确。

### 转发邮件给联系人 (L4) — Combined: 72.0%
- Auto: 66.7%, Claude: 75.5%
- Completion=0.8, Tool=0.7, Response=0.8, Efficiency=0.7
- v1的0分改善。4步：search失败→list_inbox→forward。转发成功但用了错误邮箱(david.zhang@而非david@)。

### 截屏并通过蓝牙传输 (L4) — Combined: 88.9%
- Auto: 100.0%, Claude: 81.5%
- Completion=1.0, Tool=0.9, Response=1.0, Efficiency=0.2
- 18步极其低效：截屏和蓝牙传输成功，但中间大量探索(cat截图文件、find搜索、ls目录)。结果正确但过程臃肿。

### 查看Python版本并安装包 (L4) — Combined: 18.9%
- Auto: 0.0%, Claude: 31.5%
- Completion=0.3, Tool=0.0, Response=0.5, Efficiency=0.5
- v1满分现在变0分。直接用python3 --version和pip3 install，完全没用pc-sim工具。获取了真实系统Python版本而非模拟器。

### 完整起床提醒设置 (L5) — Combined: 89.8%
- Auto: 100.0%, Claude: 83.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.4
- v1修复为满分！10步偏多(前3步猜错)，但3个子任务全部完成。回复结构优秀。

### 会议准备全流程 (L5) — Combined: 91.0%
- Auto: 100.0%, Claude: 85.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.5
- 8步。前两步猜错，读SKILL.md后完成。成功找会议→查邮箱→发邮件。

### 出门前设备配置 (L5) — Combined: 88.6%
- Auto: 100.0%, Claude: 81.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.3
- v1的0分修复了！12步偏多(前4步猜错)，但4个子任务全部完成。回复清晰。

### 设备完整备份准备 (L5) — Combined: 43.4%
- Auto: 50.0%, Claude: 39.0%
- Completion=0.5, Tool=0.3, Response=0.5, Efficiency=0.2
- v1退步。18步，用了真实系统命令(uname/rpm/dpkg)而非pc-sim工具。混淆了模拟器和宿主机。只有contacts_export用了pc-sim。

### 专注模式全配置 (L5) — Combined: 3.0%
- Auto: 0.0%, Claude: 5.0%
- Completion=0.0, Tool=0.0, Response=0.2, Efficiency=0.0
- v1满分现在变0分。11步全部失败：编造各种奇怪命令格式(parse_pcsim_launch, pc_display { json }, pc_audio play等)。Agent完全无法调用任何工具。

### 删除不存在的联系人 (L6) — Combined: 94.6%
- Auto: 100.0%, Claude: 91.0%
- Completion=1.0, Tool=0.8, Response=1.0, Efficiency=0.8
- 4步。第一步猜错(contacts_delete_contact)，读SKILL.md后search+list确认不存在。比v1(6步)改善。

### 向离线设备传输文件 (L6) — Combined: 18.0%
- Auto: 0.0%, Claude: 30.0%
- Completion=0.3, Tool=0.2, Response=0.4, Efficiency=0.3
- v1满分现在退步。1步猜错(multi_device list)后就放弃，没读SKILL.md。回复建议用AirDrop/iCloud，完全脱离pc-sim场景。

### 无录音状态下停止录音 (L6) — Combined: 90.7%
- Auto: 100.0%, Claude: 84.5%
- Completion=1.0, Tool=0.7, Response=1.0, Efficiency=0.6
- 4步：前两步猜错(recorder_stop不带pc-sim前缀)，读SKILL.md后成功。

## Conclusions

- **Overall**: Qwen3.5-9B v2 综合得分 79.6%，相比 v1 (75.9%) 有所提升
- **v1→v2 改善**: 12 个任务改善（含 6 个从 0 分修复），主要受益于 BOOTSTRAP.md 删除和 IDENTITY.md 精简
- **v1→v2 退步**: 7 个任务退步（含 4 个从满分跌到 0 分），体现小模型的不稳定性
- **持续问题**: 不先读 SKILL.md 就猜命令仍是核心瓶颈，几乎所有非满分任务都有这个特征
- **模拟器混淆**: 部分任务仍会用系统命令(ps/tree/pip)替代 pc-sim 工具
- **与 deepseek-chat (98.3%) 的差距**: 主要在工具使用准确性和效率上，任务理解能力差距不大
