---
name: daxuan-journal-palette
description: |
  这是一个面向期刊论文图表的 Daxuan Skill，用于选择、设计和审查艺术化但可读的科研配色。它根据图表语义、组数、数据类型、期刊场景和目标介质输出可复用的 HEX、R/ggplot2、Python 配色映射、风格说明，以及色盲、灰度、对比度、印刷和多面板一致性检查。用户提到中国水墨、东方色、矿物色、敦煌、宋韵、Nature/Cell 风格、低饱和高级配色、开放抽卡、公共领域作品、随机视觉卡片、从图片提取配色、富集图、热图、柱状图或科研图配色时触发；不用于品牌、网页 UI、照片调色或替代统计分析。
metadata:
  author: Daxuan
  version: "0.7.0"
  maturity: production
---

# Daxuan Journal Palette

Copyright (c) 大轩  
GitHub: https://github.com/DaXuanGarden

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
- 用户想探索内置库之外的视觉风格时，进入 [card-draw-workflow](references/card-draw-workflow.md)：先抽 3–5 张公共领域或生成式卡片，让用户选图，再提取候选色、做语义映射和实际图形审查。明确要求“色彩丰富、多彩或高饱和”时，先进行缩略图色彩丰富度筛选，避免灰度或棕褐色图片占满候选池。不要未经选择、来源记录和审查就把图片颜色当作最终科研色板。
- 用户同时要求“抽卡”和 SCI/期刊适配时，使用 [joint-card-sci-workflow](references/joint-card-sci-workflow.md) 与 `scripts/joint_palette_draw.py`：图片卡只提供视觉线索，SCI 色板按分类、发散热图或环形热图语义筛选；输出 JSON、PNG 和 HTML 联合预览，并记录 seed、匹配距离和来源。不要把图片色与 SCI 色板跨语义拼接。
- 普通请求先使用 `palette-index.json` 和 `route_palette.py` 快速路由，只返回 1 套主方案和最多 2 套备选；完整配方、来源和审查细节按需读取，不默认展开整个色板库。
- 只有用户明确提出“抽卡、随机作品、公共领域卡片、生成视觉卡片、图片提取”等意图时才进入图像流程；抽卡默认 5 张，明确说“一张/单张”时只抽 1 张，显式数量可扩展到 10 张。
- 默认只追问三个缺失信息：图表类型、组数/类别数、白底或深底；其余视觉家族、密度和风险先依据索引自动推断。
- 不触发：网站/应用 UI、品牌 Logo、照片白平衡、统计检验、GWAS 结果解读和一般论文写作；只讨论字体/尺寸而不涉及配色时也不触发本 Skill。

## Circular figure contract

当图形包含多个环层时，先声明每层的语义，再选择色板：

- `outcome_category_ring`：`qualitative`；固定类别顺序；不得使用连续渐变。
- `signed_effect_ring`：`diverging`；明确负端、零点和正端；零点必须位于色带中心。
- `validation_ring`：`neutral-accent`；验证状态与效应方向分离；不得复用热图色阶。

同一图形内不得拼接不同发散色带的成员。对环形热图，必须把分类环、发散热图环和验证环分别写入 `layer_mapping`，并在最终渲染后一起审查；不要只审查色板色条。

## Preference constraints

把用户审美反馈转成可审计约束，而不是临时形容词：

- `avoid_hues`：用户明确排斥的色相，如 `green` 或 `red-green`；
- `lightness_target`：`airy`、`balanced` 或 `ink-heavy`；
- `chroma_target`：`muted`、`moderate` 或 `colorful`；
- `preserve_cues`：需要保留的视觉线索，如 `yellow/olive print cue`；
- `background`：默认 `#FFFFFF`，白底图优先用中等明度填充。

推荐结果必须返回 `applied_constraints` 和 `rejected_candidates`。如果用户说“不要绿色”或“太暗”，先在同一语义家族内过滤或调整，再重新渲染整图；不得只替换一个图例色块，也不得丢失拒绝理由。

## Human-in-the-loop review

配色迭代采用“机器提出受约束候选，作者选择方向，机器记录并复现”的闭环：

1. 先给 1 个主方案和最多 2 个备选，三套候选使用同一数据、几何、标签和导出参数；
2. 只询问三个方向：视觉方向（保持/更亮/更鲜明/更暖/更冷静）、优先级（均衡/可读性/审美/打印与 CVD）和改动范围（只改配色/配色加图例/整图打磨）；
3. 作者选择后，使用 [`scripts/author_review.py`](scripts/author_review.py) 保存 `status`、选择、自由文本反馈和约束；自然语言中的“不要绿色、太暗、太灰”等必须转成 `preference_constraints`；
4. 作者没有选择前，停在 `awaiting_author`，不得改写生产图；选择后才生成下一轮预览；
5. 任何涉及数据、语义映射或统计标记的改变都要另行确认，配色审阅不能悄悄改变科学含义。

`route_palette.py` 会返回同一套 `human_review` 问题和暂停点；需要长期记录时，用 `author_review.py create` 生成 review brief，再用 `author_review.py record` 追加决策日志。这样作者的审美判断保留在流程里，但最终图仍经过灰度、色觉、缩印和人工复核。

## Style Router

按以下顺序路由，不要把“艺术风格”当作数据类型：

1. **数据语义**：定性、连续、发散、循环，或中性灰 + 单一强调色。
2. **视觉家族**：东方纸墨、宋韵青瓷、敦煌矿物、朱砂宫墙、草木土色、北欧矿物、海岸蓝、现代编辑部、印象派大气、平面构成、色域叙事、版画靛蓝、现代水墨矿物、单色强调等；完整清单见 [style-taxonomy](references/style-taxonomy.md)，外部艺术灵感和公开来源见 [artistic-inspiration](references/artistic-inspiration.md)。
3. **介质约束**：白底/深底、单栏/双栏、RGB/PDF/印刷、透明叠加、最终缩印尺寸。
4. **角色分配**：固定背景和文字，再分配主色、支持色、中性灰和一个强调色；同一语义跨面板使用同一颜色。
5. **可读性修正**：在同一家族内先调明度，再调饱和度，最后才调色相；不要为了“更艺术”牺牲相邻元素、灰度和标签识别。

需要让作者先“看见”而不是只读 HEX 时，打开 [palette-gallery](references/palette-gallery.md) 中的静态 HTML 或 SVG 总览；画廊用于选择和比较，最终判断仍以实际图形为准。

## Optional Local Integrations

可按职责调用 `easyplot`、`nature-figure`、`journal-ggplot-stylebook`、
`scientific-visualization`、`imagegen` 和 `sci-color-palettes`；它们只补充
绘图实现或诊断，不替代本 Skill 的语义映射、作者审阅和证据边界。具体边界见
`references/output-contract.md` 和 `references/sci-color-palettes-bridge.md`。

## Compact Workflow

1. 读取快速索引：识别图表语义、关键词、组数和背景；默认只选 1 个主路由和最多 2 个备选。
2. 判断是否明确进入抽卡；未明确提出图像探索时，停留在内置色板快速路径。
3. 对期刊/临床/数据库/色盲/灰度/打印请求，调用 `sci_palette_bridge.py` 做应用档案排序；Daxuan 仍负责视觉家族和图形落地。
4. 只追问缺失的三个关键参数：图表类型、组数/类别数、白底或深底；其余信息先写入 assumptions。
5. 选视觉家族：从索引给出 palette ID、适用图表和主要风险；需要详细 HEX 时再读取 `palette-atlas`。
6. 生成映射：输出颜色名称、HEX、语义角色、R/ggplot2 和 Python 写法，并保留类别顺序。定性类别使用 `sp.select()`，连续/发散数据使用 `sp.ramp()` 或 `div-*`，不混合两个定性色板。
7. 输出 `human_review`：展示主方案和备选，提出三个有限问题，明确 `awaiting_author` 暂停点；作者未选择前不改生产图。
8. 作者选择后，调用 `author_review.py record` 记录选择与反馈，把文字转成约束，再重新生成候选和预览。
9. 审查实际结果：检查相邻颜色对比、灰度层次、常见色觉差异、黑白打印、浅色背景上的文字、透明叠加和导出后的最终尺寸。可调用 SCI 的 `sp.check()`/`sp.report()` 与 EasyPlot 的 palette audit；诊断结果不是认证结论。
10. 生成真实预览：使用 `scripts/render_palette_preview.py` 输出 normal/grayscale/protanopia/deuteranopia/target-size 五联卡；最终环形图还要复查图例、裁切、字体和层间冲突。
11. 交付：默认给 1 套主方案和最多 2 套备选；把来源、算法、偏好约束、作者决策和审查工具写入 `provenance`，正文只展示简短摘要。

### 联合抽卡路径

当请求同时包含“抽卡/图片灵感”和“SCI/论文发表/热图/分类色块”时：

1. 读取卡片 JSON，按固定 seed 抽取 1–10 张并保留来源和权利字段；
2. 对图片候选色运行 SCI 诊断，但把诊断标记为视觉线索审查；
3. 按图表语义从 SCI 库选择完整色板：分类色块用定性 ramp，正负热图用发散 ramp，环形图拆成分类/热图/验证三层；
4. 用 CIE76 距离计算视觉匹配度，输出每张卡与 SCI 候选的对应关系；
5. 生成联合 PNG/HTML 预览，作者选择后再将完整 SCI ramp 映射到真实图形；
6. 明确说明图片颜色没有被直接拼入统计语义色板，最终图形仍需要目标尺寸审查。

## Output Contract

每次输出至少包含 `style_name`、`palette_type`、`semantic_mapping`、`hex`、
`background`、`audit`、`provenance`、`preference_constraints`、`human_review`
和 `rendered_preview`。环形或多层图必须额外提供 `layer_mapping`；详细字段见
`references/output-contract.md`。

## Reference Map

- 视觉家族、关键词和适用图形：[style-taxonomy](references/style-taxonomy.md)
- 风格、HEX 和语义角色：[palette-atlas](references/palette-atlas.md)
- 色盲、灰度、印刷和导出检查：[accessibility-and-print](references/accessibility-and-print.md)
- 输出字段和审阅清单：[output-contract](references/output-contract.md)
- 可视化色板画廊的源文件、生成器和使用方法：[palette-gallery](references/palette-gallery.md)
- 艺术家视觉原则、公开仓库、博物馆开放数据和来源记录：[artistic-inspiration](references/artistic-inspiration.md)
- 开放抽卡、图像提色、来源记录和内置化规则：[card-draw-workflow](references/card-draw-workflow.md)
- 视觉卡片与 SCI 候选的联合抽卡、匹配和预览：[joint-card-sci-workflow](references/joint-card-sci-workflow.md)
- SCI 期刊/应用场景色板适配和审计：[sci-color-palettes-bridge](references/sci-color-palettes-bridge.md)
- 快速关键词路由和轻量匹配表：[palette-index.json](assets/palette-gallery/palette-index.json)、[route_palette.py](scripts/route_palette.py)
- GitHub public skill 仓库结构和发布顺序：[github-publishing](references/github-publishing.md)

## Gate Ladder

- 设计门：色彩数量、语义类型、类别顺序和背景已说明。
- 风格门：视觉家族、关键词、图表密度和介质理由已说明；未把“Nature/Cell 风格”写成官方色板或审稿保证。
- 可读性门：实际图形通过灰度、色觉差异、文字对比和最终尺寸检查，或明确标记为待审查。
- 一致性门：跨面板、图例、正文和补充图的同一语义使用同一映射。
- 证据门：把设计判断、自动化检查和人工确认分开，不把推荐写成已验证的期刊规范。
