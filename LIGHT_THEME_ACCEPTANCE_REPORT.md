# GGN Morandi Warm Paper — 阶段 4 验收报告

> **性质**：只读审计报告。本阶段未修改任何主题 CSS；仅新增本报告与可复现审计脚本 `audit_light.py`。
> **审计对象**：浅色分支 `morandi-light-warm-paper` @ `3105f95`（候选发布版，288,886 B / 13,065 行）。
> **对照基线**：深绿生产版 `main` @ `82f9d69`（`ggn-morandi-dark-green.css`，290,893 B）。
> **复现命令**：`python3 audit_light.py`（34 项静态检查）+ `python3 morandi_light_contrast.py`（135 项 WCAG 检查）。

## 1. 验证结论总览

| 类别 | 结果 |
|---|---|
| 静态审计套件 | **34/34 PASS**（`audit_light.py`，含令牌对照 55 项、§10 与深绿版逐字节一致 8,523B、旧深色值零残留、批准偏差全部在位） |
| WCAG 对比度 | **135/135 PASS**（正文 ≥4.5:1、控件/图形 ≥3:1，覆盖全部消费配对） |
| 结构奇偶 | !important 367、:has 239、@media 38、rgba(var() 3——与已验收深绿版完全同数 |
| 动效降级 | `prefers-reduced-motion` 块在位；jelly 动画已豁免；flickerAnimation 不存在（深绿阶段3已删）；keyframes 清单与深绿版一致（仅 jelly-effect） |
| 焦点反馈 | 26 条 :focus 规则 + 2 条 :focus-visible（对话框链接 2px accent 描边）；输入焦点圈 fg-accent-soft 实测 ≥3.3:1——与已验收深绿版同构 |
| 资源实测 | 分支 CDN：CSS 200/`text/css`；Open Sans/Bebas 字体 200/`font/woff2`；game-bg.svg 200；logo PNG 200；图标 SVG 200。**CDN 内容 SHA-256 与本地一致**（`bbde3891…`） |
| 深绿无回归 | `main` HEAD 仍 `82f9d69`；深绿文件本地 SHA=Pages 线上 SHA（`8ba14f26…`）；深绿 Pages/jsDelivr 均 200/`text/css` |
| 真实浏览器 | Chrome 157 headless 实拍 harness 桌面 1440/窄屏 800 两档：暖纸主色、按钮、链接、告警混合底、语义色、ratio 色带全部像素级命中；零暗块、零横向溢出 |
| 真实 GGn 站点 | **用户已完成**：批次 1（头部）+ 阶段 3 全站（browse/详情/论坛/资料/首页/商店/收件箱/日历/top10/上传/弹窗 tooltip）逐项通过 |

## 2. 变更清单（浅色版相对深绿版的全部差异）

7 个差异块（阶段 2）+ 2 行（批次 1）+ 8 行（批次 2–6），合计 +75/−149，全部经用户批准或按批准流程登记：

| 类别 | 内容 |
|---|---|
| 令牌块 | `:root` 55 项浅色值（规范 §2–§6） |
| §10 重构 | 删除 blue-night 默认浅色块 75 行；五主题变体（abyss/oled/graphite/ember/nocturne）逐字节保留 |
| 批准偏差 4 行 | 告警混色 14%+surface-4、告警链接 fg-accent、hr→line-2、wordmark 暗边 #33352b |
| 批次 1 修复 2 行 | 搜索框输入文字 ink-8→ink-4（2.74→4.66:1）；buff hover s4→s5 |
| 批次 2–6 修复 8 行 | 白闪 hover ×4→brightness(0.7)；对话框关闭图标去反色+hover 压暗；拖拽克隆阴影暖化；封面横幅洗白（brightness 1.1 / saturate 0.85） |

## 3. 问题分级

### 严重（阻塞发布）
**无。**

### 一般（已知、已量化、待发布裁决）
| # | 项 | 实测 | 处置状态 |
|---|---|---|---|
| G1 | 奖章材质色 12/16 浅底 <3:1（金 #d4af37 1.78、银 1.54、钻 1.53、亮黄 1.43、琥珀 1.38 等） | 图形级对比不足，但材质身份清晰、有文字标签同现 | 用户阶段 3 全站检查已看过并放行；如需加深可一次提交按同色相处理 |
| G2 | ink-8 告警条角标 12px | 2.74:1（原浅色主题同位 2.84） | R2 登记，提示级角色 |
| G3 | ink-6 在最深井底 | 4.15:1（原主题同位 4.10） | R1 登记，标签级角色 |
| G4 | 输入框边 line-2 | 1.97:1（原主题 1.16） | R3 登记，井色落差辅助辨识 |

### 可接受（功能保留/双主题同理）
| # | 项 | 理由 |
|---|---|---|
| A1 | 灯箱 curtain / tags_modal / ui-widget-overlay 黑幕 0.6–0.72 | 功能性压暗，浅色主题同样需要 |
| A2 | game-bg.svg 亮彩纹理 9–11% 透明 | 原浅色模式同样直接复用；用户两轮截图均放行 |
| A3 | logo PNG 白高光融入纸面 | 形状由深描边+紫色品牌色承载；用户实站看过并放行 |
| A4 | 封面横幅洗白（brightness 1.1） | 用户全站检查含游戏主题页，已放行 |
| A5 | 拖拽克隆暖阴影 0.3 | 与暖阴影族一致的抬升反馈 |
| A6 | toolkit 在浅色文件上无 warm-paper 暗块 | 浅色专案非目标；五主题切换能力不受影响 |

### 未验证项（如实声明）
- **我未做**：真实 GGn 登录态浏览器截图（所有线上视觉验收均由用户完成并逐批放行）。
- **我未做**：真实站点窄屏（<800px）独立截图——harness 窄屏 800px 由我实拍通过；更窄档沿袭深绿版已验证的同一断点结构。
- **未单独验证**：IE/旧 Edge 等不支持 `color-mix`/`:has` 的引擎——与深绿版能力边界完全相同（深绿版已在现代 Brave/Chrome 全站验证）。

## 4. 发布就绪状态

- 候选文件：`ggn-morandi-warm-paper.css` @ 分支 `morandi-light-warm-paper` `3105f95`。
- 候选线上地址（实测 200/`text/css`、SHA-256 与本地一致）：
  `https://cdn.jsdelivr.net/gh/acesaint/ggn-morandi-1@morandi-light-warm-paper/ggn-morandi-warm-paper.css`
- 发布边界：`main` 与深绿线上地址未动；GitHub Pages 仍只发布 `main`。

## 5. 阶段 5（待用户明确放行后执行）

1. 将 `ggn-morandi-warm-paper.css` 合入 `main`（与深绿主题同仓并行）；
2. 更新 README：浅色主题安装地址（Pages 版 `https://acesaint.github.io/ggn-morandi-1/ggn-morandi-warm-paper.css` 为主）；
3. 实测最终地址 HTTP/MIME/SHA，purge jsDelivr，确认深绿地址继续可用；
4. 等用户在 GGn External CSS 填入最终 Pages 地址硬刷新，做最终确认。

**在你明确说「阶段 4 验收通过并放行发布」之前，不合并、不发布、不动 main。**
