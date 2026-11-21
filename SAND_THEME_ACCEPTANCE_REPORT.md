# Sand Pair Acceptance Report — 暖沙米色（浅）+ 夜沙炭褐（深）

阶段 3+4 验收报告（2026-11-21）。两套主题配套成对，本报告覆盖全部可机读验收项。真实站点视觉确认由用户在 GGn（Brave）中完成，本报告不虚构任何未执行的浏览器测试。

## 一、交付物

| 文件 | 说明 |
|---|---|
| `ggn-morandi-warm-sand.css` | 浅色主题，由 warm-paper 受控复制生成 |
| `ggn-morandi-night-sand.css` | 深色主题，由 dark-green 受控复制生成 |
| `build_sand_themes.py` | 受控生成器（可复现，带 diff 白名单断言） |
| `sand_contrast.py` + `sand_contrast_report.txt` | 双主题 WCAG 对比度套件 |
| `audit_sand.py` + `audit_sand_report.txt` | 双主题静态审计套件 |
| `SAND_THEME_TOKENS.md` | 双主题语义 Token 规范 |

## 二、对比度套件（sand_contrast.py）

**268 项检查全部 PASS（warm-sand 134 + night-sand 134，0 失败）**。

- warm-sand：正文 12.54:1（锚点 #F5F2EB）；fg-accent 全 10 表面 ≥4.5（surface-9 上最紧 4.60）；语义色/比例梯/链接/按钮全配对达标；告警底 #EBE1D6（14% fg-orange over surface-4）正文 10.86、链接 5.15。
- night-sand：正文 12.20:1（surface-2）；fg-accent 于 s0–s5 全部 ≥4.5（最紧 4.79）；语义色 5.3–8.1；按钮深字 7.94；告警底 #6E5843（**45% fg-orange over surface-0，dark 公式**）正文 5.20、链接（--fg-accent-soft）3.94 ≥ 父主题实测 3.89。
- 深色矩阵四项已批准适配（fg-accent 文字范围 s0–s5、结构填充 ≥2.7 记录、告警链接 ≥3.9、边框阈值 1.9/3.0 优于父主题实测 1.65/2.0），详见 SAND_THEME_TOKENS.md 第三节。

## 三、静态审计（audit_sand.py）

**54 项检查全部 PASS（0 失败）**，覆盖：

1. Token 一致性：两文件各 58 个 :root Token 与规范逐项一致；
2. 与父主题结构 parity（!important 367、:has 239、@media 38、rgba(var( 3 等计数一致）；
3. 受控 diff：warm-sand 58 行、night-sand 60 行改动，全部落在白名单（头注释 1 + 调色注释 1–2 + Token 59 + wordmark 基色 1），**0 行越权改动**；
4. 父主题残留清除：warm-paper 10 个旧 Token 值与 dark 表面 10 值零残留；dark-green 15 个旧 Token 值与浅色表面/陶土值零残留；
5. 既有适配继承：warm-sand（无 brightness(5) 白闪、对话框图标不反转、拖动克隆暖阴影、封面浅色 wash、搜索框正文色、buff hover surface-5、告警链接 fg-accent）；night-sand（封面深色 wash brightness(0.5)、拖动克隆黑阴影、buff hover surface-4、告警链接 fg-accent-soft、**blue-night swatch 块按深色主题惯例继承**）；
6. §10 toolkit 区与各自父主题逐字节相等；5 个其他主题变体块（abyss/oled/graphite/ember/nocturne）完整保留；
7. 动效与焦点：prefers-reduced-motion、jelly-effect keyframes 清单与父主题一致、:focus-visible 规则在位；
8. 正文硬编码色：warm-sand 18 项、night-sand 19 项，全部在已批准清单内（奖章/符号/UI 默认），wordmark 基色分别换为 #302b25 / #14110d；
9. 外部资源：@imports 与 12 个字体相对路径不变、wordmark 字体内嵌不变；
10. 生产父文件 SHA256 与阶段 0 基线一致（dark-green / warm-paper 全程只读未被触碰）。

## 四、已批准保留项（登记，非阻塞）

- 浅色奖章 16 项中 12 项在浅底 <3:1 —— 沿 warm-paper 验收结论（用户放行）原样继承；
- night-sand 结构填充 s6–s9 上的 fg-accent 最低 2.74:1 —— 仅作非文字装饰用途，父主题同位置 3.16–4.27，属陶土饱和度换取向；
- 深色告警链接 3.94:1 —— 父主题实测 3.89 同水平；
- 阴影 tint（浅 rgba(60,54,40,α) / 深 rgba(0,0,0,α)）、`--ggn-bg` 图标瓦片、字体栈：继承父主题。

## 五、过程修正记录

- 首轮 night-sand `--fg-orange #DCA87E` / `--fg-accent-soft #E0B896` 在深色告警公式（45%/surface-0）下链接对比 3.50 < 父主题 3.89，调整为 `#D2A278` / `#E5C09E` 后 3.94 ≥ 父主题，其余用途全部改善；
- 审计脚本曾按浅色公式误检深色告警与 blue-night swatch，已按父主题真实形态修正检查项（54/54 通过）。

## 六、结论

两套 sand 主题通过全部可机读验收（268 对比 + 54 审计，0 失败），生产主题未受影响，可进入阶段 5 发布。真实站点各页面视觉确认由用户以 GitHub Pages 地址完成。
