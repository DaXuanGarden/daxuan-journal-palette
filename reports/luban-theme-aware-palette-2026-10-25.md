# Daxuan Journal Palette · Luban 主题感知配色打磨报告

审查日期：2026-10-25  
对象：`daxuan-journal-palette` 0.8.0 → 0.9.0  
本轮目标：把论文标题/片段/图形含义接入配色规划，让图片灵感有主题来源，让 A/B/C 先有方向再选色板。  
本轮状态：已完成主题规划器、方向性候选门、图片检索计划和人机审阅契约；未修改生产图、未发布远端版本。

## 1. 验料结果（Skill 前提挑战）

挑战1 - 真实问题：**成立**。此前 Skill 能处理图表语义和色板距离，但不能把“久坐—心血管疾病—遗传相关性”转换成主题锚点、视觉隐喻和有理由的候选方向。

挑战2 - 独特角度：唯一性来自 **中文科研审美 + 主题到视觉线索的转换 + 公共领域图片溯源 + 科研语义色板审查**。色板库本身不是护城河，主题规划和可追溯的审阅闭环才是差异化。

挑战3 - 安装理由：用户可以从论文标题和一段结果描述开始，得到可复现的主题简报、图片检索词、A/B/C 方向、色板 ID、距离和拒绝原因；不必先知道 HEX，也不会把同一色相的轻微变体误认为三个方向。

挑战4 - 公共传播性：一句话钩子是 **“把论文主题编译成有方向、有来源、能复查的科研配色。”** 可展示产物是主题简报 JSON、图片检索命令、A/B/C 方向表和真实图形预览；主题规划器已经有可复现样例，真实图形 showcase 仍是下一步。

验料结论：**好料，继续打磨**。核心问题成立，新增主题层后定位更清晰。

## 2. 访行记录（同类 Skill 横向对标）

| 同类项目 | 链接 | 类型 | 可学的手艺 | 不能照搬的点 |
|---|---|---|---|---|
| K-Dense scientific-visualization | [GitHub](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization) | 直接/手艺 | 先保护数据语义，再做颜色、CVD、灰度和最终尺寸检查 | 范围更宽，不承担中文主题和图片溯源 |
| bio-info-skills color palettes | [GitHub](https://github.com/linjf15/bio-info-skills/blob/main/data-visualization/color-palettes/SKILL.md) | 直接 | 明确区分定性、连续、发散、循环，并提醒颜色不是认证 | 主要是通用生物信息色板说明，缺少主题叙事 |
| palettecore | [GitHub](https://github.com/heidihelena/palettecore) | 直接/手艺 | 从种子色生成候选，并同时输出 CIEDE2000、OKLCH、CVD 和灰度审查 | 不应把单一 seed 生成替代论文语义和作者选择 |
| Scicolor | [在线工具](https://yang3kc.github.io/scicolor/) | 直接 | 按色盲友好和分类场景快速浏览、复制和筛选色板 | 更像色板浏览器，不提供论文主题到图片的链路 |
| Scientific colour maps | [Crameri 官方站](https://www.fabiocrameri.ch/colourmaps/) | 间接/手艺 | 感知均匀、可排序、可打印、可引用和可复现 | 主要覆盖连续/发散数据，不解决分类环的审美方向 |
| AgentFigureGallery | [GitHub](https://github.com/Dsadd4/AgentFigureGallery) | 间接/展示 | 用大量真实期刊图和代码作为可见参考，安装后有明确产物 | 参考图不能直接复制成论文配色或暗示期刊认可 |
| Academic Figure Skill | [GitHub](https://github.com/TingxiYu/academic-figure-skill) | 间接/手艺 | 把研究问题、图形计划、期刊尺寸、导出和 QA 编成流程 | 重点是整图生产，不能替代主题配色规划 |

对标得到的结论是：科研色彩工具普遍把“数据语义”和“可读性审查”写得较清楚；优秀图形 Skill 则提供真实可见产物。当前 Skill 应补的不是更多 HEX，而是主题输入、方向角色和图片来源链。

## 3. 生态位判断

纵向结论：Skill 已从色板索引发展为“路由 + 抽卡 + SCI 桥接 + CIE76 候选门”。0.9.0 增加了“论文主题 → 视觉线索 → 方向性 A/B/C → 色板候选”的前置层。

横向结论：同行的信任来自语义规则、可见预览、可复现命令和审计证据；单独展示色条不足以证明方案适合论文。

交叉洞察：应占据的生态位不是“更大的色板库”，而是 **科研作者的主题感知配色编译器**：把论文叙事、图形语义和作者审美转成可解释、可复查的候选方案。

一句话新定位：**Daxuan Journal Palette 把论文主题和图形语义编译成有方向、有来源、能通过 CVD/灰度/缩印复查的科研配色。**

## 4. 过尺结果（活体检查 + 九维质量评分）

### 活体检查

- 原 v0.8.0 基线：32/32 测试通过。
- 新增主题规划测试：3/3 通过；完整测试在本轮结束后重新运行。
- 真实运行 `theme_palette.py`，对“久坐行为与心血管疾病的遗传相关性”生成 JSON 简报。
- 简报识别出主题 `sedentary_cardiovascular`，输出心脏/血管主题锚点、流动/步行/叶脉视觉隐喻、The Met 检索词和 A/B/C 方向。
- 三个方向选出的色板为 `clinical-cool-warm`、`matisse-flat`、`tea-earth-botanical`，两两最小距离 `ΔE76 = 20.22`，超过默认阈值 18。
- `quick_validate.py`：Skill 包结构通过。
- 尚未完成的证据：图片下载后的真实提色和三套真实环形图渲染；当前报告明确标记为下一步，不把规划结果写成最终配色结论。

### 九维评分

| 维度 | 权重 | 得分 | 证据 | 主要短板 |
|---|---:|---:|---|---|
| Frontmatter 与触发条件 | 7 | 7 | 主题、抽卡、SCI、图形语义和排除边界均有触发规则 | 仍需补更多疾病主题词 |
| 工作流清晰度 | 12 | 11 | `theme_palette.py`、抽卡、提色、审阅和输出契约已串联 | 真实图片选择后仍需手动接下一命令 |
| 失败模式编码 | 12 | 10 | 无主题、无图片、距离不足和提色不合格均有回退说明 | 网络/API 失败尚未纳入主题规划器实测 |
| 检查点设计 | 6 | 6 | 主题锚点、视觉隐喻、家族、ΔE 和 provenance 均字段化 | 尚未做真实图目标尺寸检查 |
| 可执行具体性 | 17 | 16 | 标题/片段/图形含义一条命令生成 JSON | 仍需增加一条“选卡后自动提色”串联命令 |
| 资源整合度 | 4 | 4 | atlas、抽卡、提色、SCI bridge、主题 reference 和测试齐全 | 无 |
| 整体架构 | 12 | 11 | 主题层、方向层、语义层和审计层分开 | 主题规则目前是静态词典 |
| 实测表现 | 23 | 20 | 35 项本地测试、主题真实回放和包校验 | 未完成公共目录安装回放与真实图片下载回放 |
| 反例与黑名单 | 7 | 6 | 禁止把图片当证据、禁止绿色代表显著性、禁止相近 A/B/C | 还需增加版权/网络不可用的活体样例 |
| **总分** | **100** | **91** | 结构、测试和主题真实回放均有证据 | 真实图形和公共安装仍是主要损耗 |

## 5. 差距清单

### P0：不补就无法完整交付主题图片配色

- 主题规划器目前生成检索计划，但还没有把“作者选中的 `card_id`”自动传给 `extract_palette.py`；需要保留来源、权利字段、seed 和提色参数。
- 真实主题图片和生产图之间还缺少同一图形的 A/B/C 预览回放；不能只凭 JSON 判断“好看”。

### P1：补上后明显提升理解和传播

- 为当前久坐—心血管论文制作一张无敏感数据的主题配色 showcase：主题输入、图片卡片、提取色板、三方向真实图、CVD/灰度缩印预览。
- 将主题规则从静态词典扩展为可维护的 `theme-profiles.json`，让作者可以新增疾病主题而无需改脚本。
- 增加“图片候选之间的视觉差异门”，避免抽到五张题材不同但颜色相同的图片。

### P2：锦上添花

- 增加作者反馈到主题 profile 的回流统计，例如“偏好冷静蓝、拒绝绿色、需要更鲜明”。
- 增加 PDF/SVG 字体、透明度、裁切和最终尺寸检查。
- 记录 Crameri、Scicolor、AgentFigureGallery 等上游的版本和变化。

## 6. 三个打磨方向

### 方案A：细修——主题规则库

把当前静态 `THEME_RULES` 移到 `assets/theme-profiles.json`，增加主题、锚点、隐喻、图片查询和 A/B/C 候选池。优点是扩展疾病主题简单；风险是词典维护成本增加。

### 方案B：精雕——主题到真实图的可见 benchmark（推荐）

在当前 0.9.0 基础上串联“主题简报 → 作者选卡 → 提色 → 三套真实图 → CVD/灰度/缩印审查”，形成可截图的论文配色案例。它最直接回应当前 A/B/C 难以区分的问题。

### 方案C：开套件——主题、抽卡、审计拆成三个 Skill

将主题规划、图片抽卡/提色和科研图审计拆成独立模块。长期扩展性最好，但安装和版本同步成本最高，目前还没有足够的团队使用证据支持拆分。

推荐选择：**方案B**。当前架构已经能承载主题层，下一步应把它落到真实图形和图片回放，而不是继续扩大色板库。

## 7. 本轮候选改写与实际落地

本轮只刨：**主题感知入口 + 方向性 A/B/C 候选**。不改当前生产环形热图，不删除旧色板，不发布远端版本。

已新增：

| 文件 | 改动 |
|---|---|
| `scripts/theme_palette.py` | 从论文标题/片段/图形含义生成主题锚点、视觉隐喻、图片检索词、方向性候选和人机审阅字段 |
| `references/theme-to-palette.md` | 固化方向规则、图片来源、提色边界和失败回退 |
| `tests/test_theme_palette.py` | 覆盖久坐—心血管主题、通用回退和标题必填 |
| `SKILL.md` / `README.md` | 增加主题规划入口和人机协同步骤 |
| `manifest.json` / `skill-ir.json` | 增加主题简报、图片检索计划和方向性候选输出 |

可直接替换/复用的入口：

```bash
python3 scripts/theme_palette.py \
  --title "久坐行为与心血管疾病的遗传相关性" \
  --fragment "Genetic correlation across cardiovascular outcomes" \
  --figure-meaning "21 outcome rings with signed genetic correlations" \
  --figure-type circular --groups 5 --background white \
  --output qa/theme-palette-brief.json
```

该命令的主题样例保存在 [`reports/examples/theme-palette-sedentary-cardiovascular.json`](examples/theme-palette-sedentary-cardiovascular.json)。

## 8. README 与 Showcase 升级建议

README 现在已经有主题入口，但真正的传播证据应是一张“论文片段 → 图片卡片 → A/B/C → 真实图形 → CVD/灰度”连续 showcase。图片卡片必须显示来源和权利状态，三套真实图必须锁定数据、几何、标签和导出参数，只改变方向色板。

## 9. 执行计划

### 24 小时内

- [x] 固化主题感知规划器和三方向候选门。
- [x] 对当前久坐—心血管论文完成真实主题回放。
- [x] 增加测试、输出契约和 README 入口。

### 3 天内

- [ ] 作者从 A/B/C 方向中选择一个或允许三套都进入真实预览。
- [ ] 运行 The Met 公共领域抽卡，保留作者选中的 `card_id`。
- [ ] 对选中图片运行提色、SCI/CVD/灰度审查。

### 7 天内

- [ ] 生成三套真实环形热图预览和一张可复现 showcase。
- [ ] 把可复用主题 profile 移到 JSON 配置。
- [ ] 进行临时目录安装回放。

本轮不做：不替作者选择图片、不把图片颜色直接套到生产图、不发布或合并远端版本。

## 10. 出师证书

```text
┌──────────────────────────────────────────────┐
│              出师证书 · 鲁班工坊              │
│                                              │
│  作品：Daxuan Journal Palette 0.9.0          │
│  过尺：86 → 91 / 100（本轮实测）              │
│  定位：论文主题感知的科研配色编译器           │
│  绝活：主题锚点 + 图片来源 + 差异化 A/B/C      │
│  下一步：把三方向落到真实图形 benchmark       │
│                                              │
│  验收师傅：鲁班                               │
└──────────────────────────────────────────────┘
```

## 11. 回炉清单

- 持续观察 K-Dense scientific-visualization 的颜色和导出规则、Crameri Scientific Colour Maps 的版本、Scicolor 的分类色板更新，以及 AgentFigureGallery 的真实图形参考池。
- 每轮主题配色保存：标题/片段、图形含义、匹配词、视觉隐喻、图片来源、作者选卡、提色参数、拒绝色板和最终渲染图。
- 下一轮从 P0 的“选卡—提色—真实图回放”开始；不再通过增加同一色相的微调变体来制造候选数量。

## 12. 当前边界

1. 主题匹配是词典和规则推断，不是论文内容理解或生物学结论。
2. 图片是审美输入，不是科学证据；公共领域标记仍需保留来源和权利字段。
3. `ΔE76` 是候选差异筛选信号，不是可读性或期刊接受认证。
4. 最终配色必须在真实图形、目标尺寸、灰度和色觉模拟下复查。

## 13. 参考来源

- https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization
- https://github.com/linjf15/bio-info-skills/blob/main/data-visualization/color-palettes/SKILL.md
- https://github.com/heidihelena/palettecore
- https://yang3kc.github.io/scicolor/
- https://www.fabiocrameri.ch/colourmaps/
- https://github.com/Dsadd4/AgentFigureGallery
- https://github.com/TingxiYu/academic-figure-skill
