# Changelog

本文件记录对用户可见的变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循语义化版本。

## [Unreleased]

### Planned

- 浏览器里的样稿批注：在样稿页面上直接圈位置，生成 P7 改稿指令
- 多语言 deck 的页码与字体提示
- 一个把已有 PPTX 反向拆成逐页稿的入口

## [0.1.0] - 2026-11-10

首个公开版本。

### Added

- 七步主线：判档 → 问需求 → 逐页稿 → 选路线与三页样稿 → 制作 → 验收留版 → 交付说明
- 大活/小事两档：小事填表，大事一次一问，受众问四个维度
- 逐页稿七字段与 P01 起编号，确认后冻结，附基线比对
- 三条制作路线：HTML 演示、整页出图、可编辑 PPTX，均可降级
- 七条按步骤编号的提示词（P1–P7）
- 四类验收清单：内容、画面、操作、备用稿
- 脚本：`doctor.py`（自检）、`new_deck.py`（建项目）、`check_outline.py`（机检与基线比对）、`snapshot.py`（留版）
- 示例：`examples/minimal/` 五页通用题材
- `QUICKSTART.md` 五分钟上手与卡点表
