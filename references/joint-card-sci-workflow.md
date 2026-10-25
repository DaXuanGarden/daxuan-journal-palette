# 联合抽卡：视觉卡片 × SCI 色板

当作者既想保留“抽卡”的探索感，又需要一套能够解释和复查的科研配色时，使用 `scripts/joint_palette_draw.py`。它把两个层次放在同一个结果里：

1. **视觉卡片层**：从 3–10 张公共领域或生成式卡片中按 seed 抽取，保留图片来源、版权、提取算法和候选 HEX。图片只表达气质和色彩方向。
2. **SCI 语义层**：按图表类型调用 `sci_palette_bridge.py`，从 `sci-color-palettes` 的应用档案和诊断中筛选完整色板。SCI 色板才是最终科研图的语义候选。

两层通过 `mean_delta_e` 和 `visual_match` 建立“视觉线索—语义候选”的对应关系，但不会把图片色和 SCI 色板交叉拼接。这样可以回答“哪张卡的气质接近哪一套可审查的科研色板”，同时保留分类色、发散热图色和验证状态色各自的语义边界。

## 图表适配

| 请求 | SCI 层 | 适用场景 | 规则 |
|---|---|---|---|
| `categorical` | `database` 定性色板 | 分类色块、分组柱状图、外层结局类别环 | 使用 `sp.select()` 保留原色板成员和顺序 |
| `heatmap` | `diverging` 发散色带 | 有正负方向和零点的相关性/效应热图 | 使用 7 色 ramp；第 4 色固定为零点 |
| `circular` | 分类环 + 发散热图环 + 中性验证环 | 当前 LDSC/Genova/HDL 环形热图 | 三个语义层分别审查，验证层用灰色 + 一个强调色 |
| `all` | 输出以上三类 | 需要一次比较所有候选时 | 预览同时展示三种适配结果 |

## 运行

```bash
python3 scripts/joint_palette_draw.py \
  --cards-json /path/to/colorful_cards_v2_with_palettes.json \
  --figure all --groups 5 --draw-count 10 \
  --seed 20261025 \
  --output-dir /path/to/qa/joint_palette_draw
```

输出：

- `joint_palette_draw.json`：抽卡顺序、每张卡的来源和提取色、SCI 候选、匹配距离、应用诊断和 provenance；
- `joint_palette_preview.png`：左侧 10 张视觉卡片，右侧分类/热图/环形热图候选；每张卡下方显示对应的 SCI 匹配；
- `index.html`：可放大查看图片和复制候选色值的轻量预览。

## 选择规则

- 同一个 seed 得到同一个抽卡顺序，便于比较和复现；
- `visual_match` 只作为审美接近度，不能替代 SCI 应用门或最终图形检查；
- 分类色板、发散色带和验证状态不能互相借色；
- 图片卡的颜色进入最终色板前仍需在目标图形、灰度、色觉差异、白底对比度和最终尺寸下复核；
- 预览中的 `quality` 是库级诊断或分数，不是“期刊接受”或“色盲认证”。

## 最小输出契约

```yaml
mode: joint-card-sci
request: {figure: circular, groups: 5, background: white}
cards:
  - card_id: card-03
    visual_cue: cyan / glacier
    extracted_hex: ["#315C6B", "#7DAFA8", "#D8B16A"]
matches:
  categorical:
    - {card_id: card-03, sci_palette_id: burgundy-clin-hi, mean_delta_e: 18.2}
  heatmap:
    - {card_id: card-03, sci_palette_id: div-plum-sage-deep, mean_delta_e: 16.7}
policy:
  - "visual cards guide mood; SCI ramps carry semantic meaning"
```
