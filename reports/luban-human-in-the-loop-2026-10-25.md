# Daxuan Journal Palette 0.7.0 · 人机协同打磨报告

审查日期：2026-10-25
对象：`daxuan-journal-palette` 论文图片配色 Skill
本轮目标：确认它能否继续改进论文图片配色，并把作者的审美方向纳入可复现的协同流程。

## 1. 验料结果

挑战1 - 真实问题：**成立**。论文图片的配色不是一次性挑 HEX；作者需要在视觉气质、语义准确、灰度/CVD、缩印和图例可读性之间反复取舍。

挑战2 - 独特角度：唯一性来自“科研语义分层 + 东方/矿物视觉家族 + SCI 诊断 + 作者反馈约束 + 真实预览”的组合。当前 0.6.0 已解决颜色层混用问题，本轮在 0.7.0 补齐作者选择和反馈记录。

挑战3 - 安装理由：安装后能得到可运行的主方案、备选方案、五联预览、SCI 审计、作者问题和决策日志；作者不必每轮从头解释“哪里不好看”。

挑战4 - 公共传播性：钩子是“让机器守住科学语义，让作者决定视觉方向”。可展示产物是 `human_review` JSON、五联预览卡和带约束的下一轮记录。

验料结论：**好料，继续打磨**。

## 2. 访行记录

| 同类工作 | 链接 | 类型 | 可学的手艺 | 不能照搬的点 |
|---|---|---|---|---|
| How to design effective scientific figures | https://www.nature.com/articles/s41562-026-02466-9 | 直接/方法 | 把图形设计当作解释科学结果的过程，而不是末端美化 | 文章是指导意见，不提供本地 Agent 交互协议 |
| Choosing Suitable Color Palettes for Accessible and Accurate Science Figures | https://doi.org/10.1002/cpz1.1126 | 直接/方法 | 明确区分定性、连续、发散色带，并强调降低对颜色的单一依赖 | 不能替代当前项目的作者偏好记录 |
| Trade-offs in Data Color Palette Design Tools | https://arc.ieeevis.org/year/2026/program/content/a28ea580-ff24-43c3-b009-56a3f2993f0f/ | 直接/交互研究 | 直接操控、自动评估和预览会改变用户对可访问性的注意力 | 研究结果不能直接当作本项目的界面设计规范 |
| Scientific visualization publication guidelines | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/references/publication_guidelines.md | 间接/手艺 | 保持语义色板、辅助编码、灰度检查和图例顺序 | 不复制其 runtime 或完整绘图库 |
| Analyzing and predicting colour preference of colour palettes | https://pmc.ncbi.nlm.nih.gov/articles/PMC10011186/ | 间接/用户研究 | 用结构化偏好选择和重复评估减少单次印象偏差 | 不把个人选择统计成普遍审美结论 |

## 3. 生态位判断

纵向结论：Skill 已从静态色板路由发展为“候选生成—约束审计—作者选择—重新渲染”的协作型工作流。

横向结论：科学绘图同行强调语义、可访问性和最终尺寸；交互研究表明工具本身会影响用户是否注意到可访问性约束。当前最有价值的差异化是把作者的主观反馈保存成下一轮机器可执行的约束。

一句话新定位：**Daxuan Journal Palette 是一个让作者选择视觉方向、让机器守住科学语义和可读性证据的论文配色协作 Skill。**

## 4. 过尺结果

### 活体验证

- `python3 -m unittest discover -s tests -p 'test_*.py' -q`：**30/30 通过**。
- `check-skill-repo.sh`：**10 PASS、3 WARN、0 FAIL**。
- `route_palette.py "五组白底 LDSC 环形热图"`：正确识别为 `circular`，返回分类环候选，并带 `human_review.status = awaiting_author`。
- `author_review.py create/record` 已真实运行：作者反馈“不要绿色，太暗，希望更丰富”被记录为 `avoid_hues=green`、`lightness_target=airy`、`chroma_target=colorful`。
- 生产图、数据、统计结果和几何没有被该协同脚本修改。

### 九维评分

| 维度 | 权重 | 得分 | 证据 | 主要损耗 |
|---|---:|---:|---|---|
| Frontmatter 与触发条件 | 7 | 6 | 触发科研配色、抽卡、SCI、作者协同 | 尚未为所有 runtime 提供交互 UI |
| 工作流清晰度 | 12 | 11 | 路由、层间契约、review brief、决策状态机 | 多作者审阅规则仍是后续项 |
| 失败模式编码 | 12 | 10 | SCI 缺失回退、选择校验、暂停生产图 | 反馈语义无法映射时仍需人工追问 |
| 检查点设计 | 6 | 6 | 五联预览、灰度/CVD/缩印和作者批准状态 | 尚未做自动图例裁切检测 |
| 可执行具体性 | 17 | 16 | 两个 CLI、JSON 契约、30 个测试 | 公共安装回放尚未完成 |
| 资源整合度 | 4 | 4 | atlas、SCI bridge、preview、review protocol | 无独立网页表单 |
| 整体架构 | 12 | 11 | 语义层、偏好约束、作者决策和证据分离 | 仍是单 Skill 而非模块化套件 |
| 实测表现 | 23 | 20 | 真实命令、真实 JSON、30/30 测试 | 尚无正式用户组的人机可用性测量 |
| 反例与黑名单 | 7 | 7 | 不改生产图、不改科学语义、不混用发散色带 | 发布包装仍有 3 项 WARN |
| **总分** | **100** | **91** | 协同接口已真实运行，主要边界明确 | 交互界面和公共安装仍可继续打磨 |

## 5. 差距清单

### P0

- 当前是 CLI/Agent 协议，尚未有跨 runtime 的可视化选择页面；必须保持 JSON 协议作为稳定底座。
- 作者批准与“只选择方向”已区分，但最终图形批准仍需记录为独立状态。

### P1

- 增加同一数据、同一几何的 A/B/C 并排图，并记录作者选择耗时和修改轮数。
- 增加图例裁切、标签重叠、字体嵌入和最终尺寸的自动检查。
- 为多作者场景增加“作者意见冲突”记录，不自动合并冲突偏好。

### P2

- 提供轻量 HTML review form；不改变 CLI/JSON 主协议。
- 增加项目级偏好档案，例如“本研究默认禁用绿色，但其他项目不继承”。

## 6. 三个打磨方向

### 方案A：细修——加强现有 Agent 协同协议

继续补齐批准状态、反馈词典和更多测试 prompt。风险最低，适合先稳定跨 runtime 行为。

### 方案B：精雕——真实图 A/B/C review showcase（推荐）

将当前 21 结局环形热图固定为 benchmark：同一几何生成三套配色，作者选择后保存决策日志和五联预览。它最能证明人机协同确实改变了工作流。

### 方案C：开套件——CLI + HTML review form

在 JSON 协议之上增加本地静态表单，让作者点击方向、优先级和改动范围。体验最好，但需要额外维护浏览器、文件写入和跨 runtime 兼容。

推荐：**先采用方案 B，再考虑方案 C**。当前 JSON/CLI 协议已经可用，先用真实论文图验证协同质量，避免为了界面增加不必要复杂度。

## 7. 本轮已落地的改写

本轮只改“作者协同接口”一面：

- 新增 [`scripts/author_review.py`](../scripts/author_review.py)：创建 review brief、记录作者选择和自然语言反馈；
- 更新 [`scripts/route_palette.py`](../scripts/route_palette.py)：环形热图识别为 `circular`，返回三问 `human_review` 和生产图暂停点；
- 更新 `SKILL.md`、README、manifest、interface 和输出契约；
- 新增 [`references/human-review-protocol.md`](../references/human-review-protocol.md)；
- 新增 5 个协同测试，完整测试数从 25 增加到 30。

## 8. 交互示例

```text
机器：候选 A ink-mineral-a-sunlit；候选 B div-plum-blue；候选 C hokusai-indigo。
机器：请选择视觉方向、评价优先级和改动范围。
作者：不要绿色，太暗，希望更丰富；优先可读性；允许改配色和图例。
机器：记录 avoid_hues=green、lightness_target=airy、chroma_target=colorful、edit_scope=palette_legend。
机器：重新生成 A/B/C，保持数据、标签和几何不变，等待作者批准。
```

## 9. 执行计划

### 已完成

- [x] 将环形图路由从单一热图类型改为 layer-aware circular；
- [x] 增加三个有限作者问题和 `awaiting_author` 暂停状态；
- [x] 增加选择、反馈、约束和决策日志的 JSON 协议；
- [x] 运行 30 个测试和真实 CLI 回放。

### 下一轮

- [ ] 用当前 21 结局真实环形图生成 A/B/C 并排 benchmark；
- [ ] 记录作者每轮选择和批准状态；
- [ ] 再评估是否值得增加 HTML review form。

本轮不做：不改变生产图，不修改 GWAS 数据或统计结果，不发布、不 merge、不打 tag。

## 10. 出师证书

```text
┌──────────────────────────────────────────────┐
│              出师证书 · 鲁班工坊              │
│                                              │
│  作品：Daxuan Journal Palette 0.7.0          │
│  过尺：86 → 91 / 100（本轮实测）              │
│  定位：作者选方向，机器守语义与可读性证据     │
│  绝活：自然语言反馈 → 可追溯配色约束与日志     │
│  下一步：21 结局真实图 A/B/C review benchmark  │
│                                              │
│  验收师傅：鲁班                               │
└──────────────────────────────────────────────┘
```

## 11. 回炉清单

- 持续观察科学图形设计和可访问性色板指南，重点跟踪语义映射、直接标注、CVD/灰度和最终尺寸要求。
- 保留每轮候选 ID、作者答案、自由文本、被拒绝色板、预览和批准状态；不把一次项目偏好自动变成全局默认。
- 下一轮从真实 21 结局 A/B/C 预览开始；若作者需要点击式选择，再实现 HTML 表单。

## 12. 当前边界

1. 当前已经支持 Agent 询问作者和记录方向，但还不是完整 GUI；CLI/JSON 是稳定接口。
2. 机器可以筛选和审计颜色，不能替作者决定“哪套更好看”。
3. 作者没有明确允许时，反馈只改变颜色约束；不会自动改数据、统计语义或生产图几何。

## 13. 参考来源

- https://www.nature.com/articles/s41562-026-02466-9
- https://doi.org/10.1002/cpz1.1126
- https://arc.ieeevis.org/year/2026/program/content/a28ea580-ff24-43c3-b009-56a3f2993f0f/
- https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/references/publication_guidelines.md
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10011186/
