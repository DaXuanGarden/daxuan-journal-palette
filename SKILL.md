---
name: daxuan-journal-palette
description: |
  这是一个面向期刊论文图表的 Daxuan Skill，用于选择、设计和审查艺术化但可读的科研配色。它根据图表语义、组数、数据类型、期刊场景和目标介质输出可复用的 HEX、R/ggplot2、Python 配色映射、风格说明，以及色盲、灰度、对比度、印刷和多面板一致性检查。用户提到中国水墨、东方色、矿物色、敦煌、宋韵、Nature/Cell 风格、低饱和高级配色、富集图、热图、柱状图或科研图配色时触发；不用于品牌、网页 UI、照片调色或替代统计分析。
metadata:
  author: Daxuan
  version: "0.3.0"
  maturity: production
---

# Daxuan Journal Palette

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/

## Router Rules

- 处理期刊论文中的科研图表配色：先读图表语义，再选色板和介质策略。
- 名义分类使用定性色板；数值强度使用连续色带；正负方向使用发散色带；不要把定性颜色伪装成连续梯度。
- 先问清楚类别顺序、类别数、背景、输出尺寸、期刊/媒介、是否需要色盲和灰度检查；信息缺失时明确假设。
- 先在 `style-taxonomy` 中确定视觉家族，再在 `palette-atlas` 中选具体配方；不要只因为色名好看就跳过语义和缩印判断。
- 五组以内优先使用有层次的颜色；类别更多时减少饱和度差异，配合直接标签、形状或分面。不要依靠红绿单独表达差异。
- 多面板中固定同一语义到同一颜色；不要按面板重新排序颜色。深色文字配浅色填充，深色条形可配浅描边。
- 色板先分配“背景/文字/中性/主色/辅助色/强调色/描边”角色，再把角色映射到组别；艺术风格只改变视觉语汇，不改变数据语义。
- 白底密集图默认选择中等明度、低到中等饱和度的色板；浅粉、米黄、雾蓝只用于较大面积或有描边的填充。
- 用户选择风格 A 时，白底密集图优先使用 `ink-mineral-a-sunlit`：`#6D98AF`、`#7DACA3`、`#CBA064`、`#CE8793`、`#A28BAF`。它保留 A 的色相关系，但把明度提高到更适合白底缩印的中间范围；原始较深版本仍保留为 `ink-mineral-a`。
- 不承诺“期刊必然接受”或“绝对色盲安全”；实际可读性必须结合图形几何、最终尺寸和输出介质检查。
- 不触发：网站/应用 UI、品牌 Logo、照片白平衡、统计检验、GWAS 结果解读和一般论文写作；只讨论字体/尺寸而不涉及配色时也不触发本 Skill。

## Style Router

按以下顺序路由，不要把“艺术风格”当作数据类型：

1. **数据语义**：定性、连续、发散、循环，或中性灰 + 单一强调色。
2. **视觉家族**：东方纸墨、宋韵青瓷、敦煌矿物、朱砂宫墙、草木土色、北欧矿物、海岸蓝、现代编辑部、单色强调等；完整清单见 [style-taxonomy](references/style-taxonomy.md)。
3. **介质约束**：白底/深底、单栏/双栏、RGB/PDF/印刷、透明叠加、最终缩印尺寸。
4. **角色分配**：固定背景和文字，再分配主色、支持色、中性灰和一个强调色；同一语义跨面板使用同一颜色。
5. **可读性修正**：在同一家族内先调明度，再调饱和度，最后才调色相；不要为了“更艺术”牺牲相邻元素、灰度和标签识别。

需要让作者先“看见”而不是只读 HEX 时，打开 [palette-gallery](references/palette-gallery.md) 中的静态 HTML 或 SVG 总览；画廊用于选择和比较，最终判断仍以实际图形为准。

## Optional Local Integrations

需要更宽的色板或图形审查时，可按职责融合本机 Skill，不把它们的名称误写成期刊规范：

| 本机 Skill | 可借鉴内容 | 在本 Skill 中的边界 |
|---|---|---|
| `easyplot` | `china.*`/`dongfang.*` 视觉家族、viridis/CET 连续色带、palette audit、最终尺寸和印刷检查 | 采用配方和诊断思路，不把自动分数写成认证 |
| `nature-figure` | claim-first 图形契约、中性背景 + 信号色、跨面板语义固定 | 作为通用出版设计原则，不声称 Nature 官方色板 |
| `journal-ggplot-stylebook` | 命名向量、`theme_classic()`/`theme_prism()`、R/ggplot2 导出习惯 | 只补充绘图实现，不替代颜色语义或统计审查 |
| `scientific-visualization` 类工作流 | 介质、尺寸、导出和证据边界 | 保留本 Skill 的中国/东方艺术谱系和轻量输出契约 |

## Compact Workflow

1. 记录对象：图表类型、语义变量、类别数、顺序、背景、画布/缩印尺寸、期刊或媒介、输出格式。
2. 选视觉家族：写明家族、关键词（如“纸本、低饱和、冷暖平衡”）和不适用场景；从 [style-taxonomy](references/style-taxonomy.md) 选家族，从 [palette-atlas](references/palette-atlas.md) 选配方。
3. 选色族：定性、连续、发散、循环，或“中性灰 + 一个强调色”；连续/发散色带要明确方向和中点。
4. 生成映射：输出颜色名称、HEX、语义角色、R/ggplot2 和 Python 写法，并保留类别顺序。
5. 审查实际结果：检查相邻颜色对比、灰度层次、常见色觉差异、黑白打印、浅色背景上的文字、透明叠加和导出后的最终尺寸。可调用 EasyPlot 的 palette audit；诊断结果不是认证结论。
6. 交付：给出一套主方案，最多补充两套备选；说明适用场景、风格理由、风险、假设和需要人工确认的点。

## Output Contract

每次输出包含：

- `style_name`：风格名和适用对象。
- `style_family`：视觉家族、关键词、适合的图形密度和不适用场景。
- `style_rationale`：该家族如何服务图表层级、语义和目标介质；不要写成历史或期刊官方来源。
- `palette_type`：qualitative / sequential / diverging / cyclic / neutral-accent。
- `semantic_mapping`：每个组/通路/状态对应的语义角色。
- `hex`：按显示顺序列出的精确 HEX。
- `text_color`、`background`、`outline`：文字、背景和描边建议。
- `R`、`Python`：可直接复制的命名向量或字典；没有代码需求时仍给最小示例。
- `audit`：对比度、灰度、色觉差异、印刷和最终尺寸检查的结果或待检查项。
- `assumptions`：缺失信息、来源边界和未验证的假设。
- `provenance`：色板 ID、是否为本地设计配方、是否调整过明度/饱和度，以及审查工具和版本（如有）。
- `visual_preview`：画廊/ SVG 预览路径；若未生成，标记为 unavailable。

## Reference Map

- 视觉家族、关键词和适用图形：[style-taxonomy](references/style-taxonomy.md)
- 风格、HEX 和语义角色：[palette-atlas](references/palette-atlas.md)
- 色盲、灰度、印刷和导出检查：[accessibility-and-print](references/accessibility-and-print.md)
- 输出字段和审阅清单：[output-contract](references/output-contract.md)
- 可视化色板画廊的源文件、生成器和使用方法：[palette-gallery](references/palette-gallery.md)
- GitHub public skill 仓库结构和发布顺序：[github-publishing](references/github-publishing.md)

## Gate Ladder

- 设计门：色彩数量、语义类型、类别顺序和背景已说明。
- 风格门：视觉家族、关键词、图表密度和介质理由已说明；未把“Nature/Cell 风格”写成官方色板或审稿保证。
- 可读性门：实际图形通过灰度、色觉差异、文字对比和最终尺寸检查，或明确标记为待审查。
- 一致性门：跨面板、图例、正文和补充图的同一语义使用同一映射。
- 证据门：把设计判断、自动化检查和人工确认分开，不把推荐写成已验证的期刊规范。
