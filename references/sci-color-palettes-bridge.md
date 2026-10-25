# SCI palette bridge

本 Skill 与本机 `sci-color-palettes` 的关系是“设计层 + 约束层”，不是把两套色板简单拼在一起：

- **Daxuan Journal Palette** 负责视觉家族、图表语义、颜色角色、图例和最终图形审阅。
- **sci-color-palettes** 负责 184 套候选色板的应用场景排序、色盲模拟、CIE76 区分度、明度跨度和 WCAG 对比度诊断。
- 适配器位于 [`scripts/sci_palette_bridge.py`](../scripts/sci_palette_bridge.py)，通过明确的本地路径加载 SCI 包，不把 184 套颜色复制进 Daxuan 的 `palettes.json`。

SCI 库是可选依赖。适配器按 `--sci-root`、`SCI_COLOR_PALETTES_ROOT`、相邻 checkout、默认本地路径的顺序发现它；找不到时 circular/categorical/diverging 三种模式都会返回结构化的 `sci_status: unavailable` 与 `fallback: daxuan-atlas`，不会静默换用另一份路径。用户的 `avoid_hues`、`lightness_target`、`chroma_target` 和 `preserve_cues` 会保留在回退结果中。

## 选择逻辑

`categorical_recommendations()` 将定性图表映射到 SCI 的四个应用档案：

它还接受可选的 `candidate_limit`：这个参数只扩大候选池，`selected_hex` 仍保持请求的组数。联合抽卡使用该参数，让视觉匹配可以在多个已经过应用筛选的 SCI 候选中进行比较。

| Daxuan 请求 | SCI 档案 | 使用场景 |
|---|---|---|
| 临床、森林图、生存曲线、结局状态 | `clinical` | 小尺寸、标签密集、需要深色文字和色觉区分 |
| 队列、数据库、多中心、类别较多 | `database` | 强调类别之间的色相跨度和成对区分度 |
| GWAS、组学、基础科研、灰度打印 | `basic` | 强调明度跨度、灰度层次和色觉差异 |
| 未明确的混合图 | `general` | 用于初筛，仍需看最终图形 |

定性色板使用 `sp.select(sp.palette(id), n)`，保留原色板中的真实成员和顺序。连续色带使用 `sp.ramp()`，不把定性色板插值成连续梯度。

## 当前环形热图的语义分层

当前久坐—心血管遗传相关性环形图有三种不同语义，因此适配器输出三个独立层：

1. **Outcome category ring**：5 个心血管结局类别，使用 `database` 档案进行分类色板筛选；类别顺序在主图和图例中固定。
2. **Signed LDSC heat ring**：遗传相关性有正负方向和零点，使用 `div-*` 发散色带；7 色发散带的第 4 个成员（0-based index 3）固定为中心色，不得打乱。
3. **Validation ring**：HDL/Genova 验证状态是状态标记，使用中性灰 + 单一强调色；不能用热图的正负颜色暗示“验证”或“未验证”。

这里的“一个色板”理解为“每个语义色层一个自洽色板”。不同语义层可以分别有独立色板，但绝不从两个定性色板中抽色拼成新的类别序列，也不把热图色带中的颜色拿去表达验证状态。

## 运行示例

```bash
# 当前 5 类环形热图：输出分类环、发散热图环和验证环的推荐记录
python3 scripts/sci_palette_bridge.py \
  --figure circular --groups 5 \
  > /tmp/circular_heatmap_sci_palette_recommendations.json

# 例：排除绿色、提高白底轻盈感，并保留黄/橄榄视觉线索
python3 scripts/sci_palette_bridge.py \
  --figure circular --groups 5 --avoid-hue green \
  --lightness-target airy --chroma-target moderate \
  --preserve-cue yellow/olive

# 只查看数据库/队列场景的分类色板
python3 scripts/sci_palette_bridge.py \
  --figure categorical --field database --groups 5

# 只查看 signed effect 的发散色带
python3 scripts/sci_palette_bridge.py \
  --figure diverging --n-values 7
```

每个推荐记录均包含 `id`、完整 `hex`、安全子集 `selected_hex`、SCI 应用分数、`fits`、CVD 对比诊断和适用原因。适配器推荐不是期刊认证；最后仍须在目标尺寸、目标背景和实际图形上进行灰度、色觉、文字对比和打印审阅。

如果候选色来自 Daxuan 内置配方或图片提色，而不是 SCI 注册表，可直接调用 `audit_hex([...])`。它沿用 SCI 的 ΔE、CVD、明度跨度和白底对比度计算，但不会把候选色写入任何色板库：

```python
from sci_palette_bridge import audit_hex

audit = audit_hex(["#6D98AF", "#7DACA3", "#CBA064", "#CE8793", "#A28BAF"])
```

## 当前图的建议起点

对目前的 5 类白底环形图，适配器优先给出 `database` 档案，原因是外层类别需要相邻类别之间有稳定的成对区分度和足够的色相跨度。热图层单独使用 SCI 的 `div-*` 家族。实际采用哪一套仍应在环形几何、标签和图例完成后审查，不能只依据库的单个分数决定。

## 非协商规则

- 颜色不是唯一证据：保留直接标签、星号、线型或几何位置等第二视觉线索。
- 浅色成员用于填充或背景带；文字、细线和数据点使用通过对比度检查的深色成员。
- 灰色也是有意义的颜色，可用于中性状态；不要因为“看起来不鲜艳”就删除中性编码。
- 记录 `sci_palette_id`、`sci_field`、`sci_scores`、`sci_gate`、`sci_provenance` 和图层映射，便于复核和复现。
- 最终渲染后重新调用 `sp.check(id)` 或 `sp.report(id)`；库级诊断不能替代人工查看最终导出图。
