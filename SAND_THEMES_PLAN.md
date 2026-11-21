# Sand Themes Project — Warm Sand (light) + Night Sand (dark)

一个项目、两套配套主题：

- **ggn-morandi-warm-sand.css** — 浅色「暖沙米色」，锚点色 `#F5F2EB`（用户 2026-11-21 确认）。
- **ggn-morandi-night-sand.css** — 深色「夜沙炭褐」，与暖沙同族的低照度版本（用户 2026-11-21 确认方向与色值）。

用户已授权：全流程一次跑完，不逐阶段暂停；最终由用户通过 GitHub Pages 链接做一次视觉确认。

## 阶段 0 — 安全基线（本文件）

### 基线记录（2026-11-21）

| 项 | 值 |
|---|---|
| origin/main HEAD | `fca4a3208613468f25ff429cdf1e84211f9dadbc` |
| 工作分支 | `morandi-sand-pair`（自 main 建立） |
| ggn-morandi-dark-green.css SHA256 | `8ba14f2645564e1ba6a988a410d72661de81da592e533724f27572d90e85b92a` |
| ggn-morandi-warm-paper.css SHA256 | `bbde3891f98056d894826abc5c8a715078b8b1d29980ed88087de5eef70952cc` |
| README.md SHA256（发布前） | `8d165b8b3fa6f4506325b6c89d5b4d1fc7f5b74e638f11ee6723bca9256fe54a` |

### 文件白名单（本项目允许新增/修改）

1. `ggn-morandi-warm-sand.css`（新增，阶段 2 受控生成）
2. `ggn-morandi-night-sand.css`（新增，阶段 2 受控生成）
3. `SAND_THEMES_PLAN.md`、`SAND_THEME_TOKENS.md`、`SAND_THEME_ACCEPTANCE_REPORT.md`（文档）
4. `sand_contrast.py`、`sand_contrast_report.txt`、`build_sand_themes.py`、`audit_sand.py`、`audit_sand_report.txt`（可复现工具与报告）
5. `README.md`（仅阶段 5 增加两个新主题的说明与地址）
6. 本地工作日志（.workbuddy/memory，不入库）

### 禁止触碰

- `ggn-morandi-dark-green.css`、`ggn-morandi-warm-paper.css`（两个已发布生产主题，全程只读；阶段 5 结束时 SHA 必须与基线一致）
- `assets/`、`game-bg.svg`、`toolkit/`、`blue-night_oled.css`、既有审计/规范文档（LIGHT_THEME_*、MORANDI_LIGHT_TOKENS 等）
- §10 toolkit 其他主题切换块（abyss / oled / graphite / ember / nocturne）原样继承，不做改动

### 受控生成策略

- warm-sand 由 **warm-paper.css 受控复制**生成：两套浅色底色亮度带一致，全部浅色适配（图标滤镜、对话框、封面、搜索框文字等）原样继承；仅替换 :root Token 块 + 文件头注释 + wordmark 边缘混色基色（`#33352b → #302b25`）。
- night-sand 由 **dark-green.css 受控复制**生成：全部深色适配原样继承；仅替换 :root Token 块 + 文件头注释 + wordmark 边缘混色基色（`#05070d → #14110d`，将蓝黑换成暖近黑）。
- 生成后 diff 必须证明：除上述白名单行外与父主题零差异。
- 正文硬编码色清单（奖章/符号等 18–19 项）与父主题一致，属已批准保留项，逐项登记。

### 回退方法

- 阶段 5 合入 main 前：`git checkout main` 即完全回退（新文件全部在 morandi-sand-pair 分支）。
- 合入后：`git revert <merge-commit>` 或按本文件基线 SHA 恢复两个生产 CSS。
- 用户侧回退：GGn External CSS 换回 `ggn-morandi-warm-paper.css` 或 `ggn-morandi-dark-green.css` 的 Pages 地址并硬刷新即可，新主题不覆盖任何旧主题。

### 目标发布地址（阶段 5 核验）

- `https://acesaint.github.io/ggn-morandi-1/ggn-morandi-warm-sand.css`
- `https://acesaint.github.io/ggn-morandi-1/ggn-morandi-night-sand.css`

（jsDelivr 镜像同步清理：`https://purge.jsdelivr.net/gh/acesaint/ggn-morandi-1@main/<file>`）

## 阶段

1. **阶段 1** — 只读分析双父主题 Token；产出 `SAND_THEME_TOKENS.md`（两套语义 Token、映射表、硬编码清单、风险）；`sand_contrast.py` 精算全部关键配对至 PASS（正文 ≥4.5:1、控件/大字 ≥3:1）。
2. **阶段 2** — `build_sand_themes.py` 受控生成两个 CSS；diff 验证。
3. **阶段 3+4** — `audit_sand.py` 静态审计（Token 一致性、父主题残留清除、结构 parity、§10 继承、滤镜/阴影继承、硬编码清单）+ 对比度套件 → `SAND_THEME_ACCEPTANCE_REPORT.md`。
4. **阶段 5** — 快进合入 main、更新 README、推送、清 CDN、核验两个 Pages URL 与既有生产文件 SHA 未变。

每阶段提交并推送 GitHub（沿固定流程）。
