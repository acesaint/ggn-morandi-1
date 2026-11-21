# Sand Pair Theme Tokens — 暖沙米色（浅）+ 夜沙炭褐（深）

阶段 1 规范。两套主题配套成对：同为暖沙色族、共享语义结构；浅色锚点 `#F5F2EB`（用户指定），深色锚点 `#25231F`。对比度精算见 `sand_contrast_report.txt`（**268 项全部 PASS**）。

- 浅色 `ggn-morandi-warm-sand.css` ← 由 `ggn-morandi-warm-paper.css` 受控复制（Token 替换）
- 深色 `ggn-morandi-night-sand.css` ← 由 `ggn-morandi-dark-green.css` 受控复制（Token 替换）

## 一、暖沙米色（浅）语义 Token

| Token | 值 | 角色 |
|---|---|---|
| --surface-0 | `#EDE9DF` | 页面深层底色（header 基底） |
| --surface-1 | `#E8E3D8` | 沙岩阴影层 |
| --surface-2 | `#F0EDE5` | 柔和面板 / html 背景 |
| --surface-3 | `#F5F2EB` | **主阅读底（锚点）** |
| --surface-4 | `#FBF9F4` | 纸白卡片 |
| --surface-5 | `#E9E4D9` | 按压层（buff hover 等） |
| --surface-6 | `#F7F4ED` | 浅抬升 |
| --surface-7 | `#FAF8F2` | 高抬升（拖动克隆底） |
| --surface-8 | `#FDFCF8` | 最亮层（时间线底） |
| --surface-9 | `#DDD6C8` | 暖石压层（斑马纹/hover 填充） |
| --line-1 / 2 / 3 / 4 | `#E1DCCF` / `#ADA591` / `#837B68` / `#7E7767` | 发丝线 → 最强边框 |
| --ink-0 … --ink-8 | `#302B25` `#39332C` `#484138` `#574F44` `#61594D` `#6A6255` `#706A5B` `#7C7566` `#817A6A` | 暖墨正文 → 最淡提示 |
| --fg-accent / -soft | `#7D5335` / `#8D674B` | 陶土棕强调 / 柔和陶土（环、图标、边） |
| --control | `#626A58` | 鼠尾草控件填充 |
| --on-fill | `#FFFFFF` | 填充上文字 |
| --fg-good / bad / warn | `#4F6847` / `#984C3D` / `#765A22` | 成功 / 错误 / 警告 |
| --fg-bad-soft | `#A05544` | Delete 静止态 |
| --fg-bonus / cost | `#52683D` / `#765A22` | 加分 / 消耗 |
| --fg-error / error-link / report | `#A04A3C` / `#9E4739` / `#A34A35` | 错误文字/链接/举报 |
| --fg-orange | `#87501D` | 告警条基色（alert mix 14%） |
| --state-leeching/seeding/uploaded/snatched | `#4E6B42` `#6F6522` `#75577D` `#9A5644` | 做种状态四色 |
| --cat-stream/conference/birthday | `#376B60` `#765A22` `#7D5A80` | 分类色 |
| --ratio-0…9 | `#A34A35` → `#4F6847` 插值 | 分享率红→绿 |
| --shadow-1/2/3 | `rgba(60,54,40,α)`（继承父主题） | 暖褐阴影 |
| --surface-deep-rgb / --surface-2-rgb | `237, 233, 223` / `240, 237, 229` | 与 s0/s2 对应 |

**关键对比度**：正文 ink-0/surface-3 **12.54:1**；强调 fg-accent/surface-3 **5.94:1**、全 10 表面 ≥4.5；按钮白字/控件 **5.64:1**；alert 混底 `#EBE1D6` 上正文 10.86:1、强调链接 5.15:1。

### 与提案的唯一偏移

提案陶土强调为 `#805638`（surface-3 上 5.68:1）；全 10 表面矩阵中 surface-9（`#DDD6C8`）上仅 4.43:1，故微调为 **`#7D5335`**（surface-9 上 4.60:1，RGB 偏移 ≤3/1/3，肉眼不可辨，色相族不变）。

## 二、夜沙炭褐（深）语义 Token

| Token | 值 | 角色 |
|---|---|---|
| --surface-0 | `#1D1B18` | 深炭背景（header 基底） |
| --surface-1 | `#22201C` | 过渡层 |
| --surface-2 | `#25231F` | **主阅读底 / html 背景** |
| --surface-3 | `#302D27` | 暖炭面板（blur-bg） |
| --surface-4 | `#39352E` | 卡片 |
| --surface-5 | `#423E37` | 按压层 |
| --surface-6 | `#4F4A42` | 抬升 |
| --surface-7 | `#59534A` | 高抬升（拖动克隆底） |
| --surface-8 | `#635C53` | 时间线底 |
| --surface-9 | `#68615B` | 结构填充（斑马纹/hover） |
| --line-1 / 2 / 3 / 4 | `#322F28` / `#555045` / `#756D60` / `#948C7F` | 发丝线 → 最强边框 |
| --ink-0 … --ink-8 | `#EAE2D5` `#D8D0C2` `#CFC7B8` `#C4B8A5` `#BCB0A0` `#B0A696` `#A69C8C` `#928B7B` `#857E6E` | 羊皮纸正文 → 最淡提示 |
| --fg-accent / -soft | `#D8A37E` / `#E5C09E` | 低饱和陶土 / 柔陶土 |
| --control | `#AAB49A` | 灰鼠尾草控件 |
| --on-fill | `#1D1B18` | 填充上文字（深炭） |
| --fg-good / bad / warn | `#A6BD91` / `#E39A86` / `#D5B36F` | 成功 / 错误 / 警告 |
| --fg-bad-soft | `#DB8E7A` | Delete 静止态 |
| --fg-bonus / cost | `#B7C49C` / `#D2BC8E` | 加分 / 消耗 |
| --fg-error / error-link / report | `#E5A79A` / `#EDBCAE` / `#DCA28E` | 错误文字/链接/举报 |
| --fg-orange | `#D2A278` | 告警条基色（dark 公式 45% over surface-0） |
| --state-leeching/seeding/uploaded/snatched | `#A6BD91` `#D5B36F` `#C9B4C4` `#DCA28E` | 做种状态四色 |
| --cat-stream/conference/birthday | `#A3BDB2` `#D2BC8E` `#CBB3C4` | 分类色 |
| --ratio-0…9 | `#DCA28E` → `#A6BD91` 插值 | 分享率红→绿 |
| --shadow-1/2/3 | `rgba(0,0,0,α)`（继承父主题） | 纯黑阴影 |
| --surface-deep-rgb / --surface-2-rgb | `29, 27, 24` / `37, 35, 31` | 与 s0/s2 对应 |

**关键对比度**：正文 ink-0/surface-2 **12.20:1**、ink-0/surface-3 10.68:1；强调 fg-accent/surface-2 **7.07:1**、s0–s5 全部 ≥4.5；按钮深字/控件 **7.94:1**；告警底 `#6E5843`（**dark 公式：45% fg-orange over surface-0**，继承父主题，非浅色的 14%/surface-4）上正文 5.20:1、告警链接（继承父主题用 --fg-accent-soft）3.94:1。

> Token 微调记录：首轮 `--fg-orange #DCA87E` / `--fg-accent-soft #E0B896` 在 dark 告警公式下链接仅 3.50:1（父主题实测 3.89），调整为 `#D2A278` / `#E5C09E` 后告警链接 3.94:1 ≥ 父主题水平，其余用途（独立文字 6.86–7.51:1、环/图标 ≥7.18:1）全部改善。

## 三、深色矩阵的已批准适配（与浅色 135 项结构的差异）

1. **fg-accent 文字范围**：≥4.5:1 于 surface-0…5（全部承载文字的表面）；surface-6…9 属结构填充（斑马/hover），强调色仅以非文字形式出现，最低值 2.74:1 记录在案。父主题 dark-green 同位置实测 s6≈4.27、s9≈3.16 —— 本主题陶土饱和度更高，在结构填充上更低，属色相强度换取向，登记为可接受。
2. **告警链接 ≥3.9:1**（dark 告警公式 45%/surface-0；父主题同位置实测 ≈3.89，夜沙 3.94；链接 Token 继承父主题为 --fg-accent-soft）。
3. **line-2 输入框边 ≥1.9:1**（夜沙 1.96，优于父主题 ≈1.65）；**line-3 ≥3.0:1**（夜沙 3.07，优于父主题 ≈2.0）。
4. 其余配对（正文、次级墨、链接、按钮、语义色、比例梯、读帖图标、悬停 delta）与浅色矩阵同阈值。

## 四、正文硬编码色清单（阶段 2 后由 audit_sand.py 核验）

- **warm-sand**：继承 warm-paper 的 18 项（奖章/符号/UI 默认 `#123456` `#b58058` `#edc245` `#bfbfbf` `#c0c0c0` `#cd7f32` `#d4af37` `#8ccada` `#cacaca` `#ff4727` `#f8d832` `#c4a316` `#ffc107` `#efba5b` `#8a6a4f` `#c9584a` `#f44336`），wordmark 边缘基色 `#33352b → #302b25`（同步新 ink-0）。
- **night-sand**：继承 dark-green 的 19 项（上列 + `#ccc`），wordmark 边缘基色 `#05070d → #14110d`（蓝黑换暖近黑）。
- 浅色奖章 16 项中 12 项对比 <3:1 的历史结论（用户放行保持原样）原样继承，登记于验收报告。
- 阴影 tint：浅色 `rgba(60,54,40,α)`、深色 `rgba(0,0,0,α)` 均继承父主题，不做改动。

## 五、风险与边界

- 两套新 CSS 均不改 DOM/布局/功能，只换 Token 与两处 wordmark 基色行。
- 图标滤镜（浅色去 `brightness(5)` 白闪、深色保留暗底反转方案）、对话框、封面 wash、搜索框文字等既有适配全部继承父主题，因两套 sand 与各自父主题表面亮度差 ≤2%，滤镜安全裕度充足。
- §10 toolkit 其他主题切换块原样继承。
- 生产主题 dark-green / warm-paper 全程只读。
