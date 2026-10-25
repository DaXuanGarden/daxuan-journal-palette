# Human-in-the-loop palette review protocol

这套协议把“我觉得不好看”变成下一轮可以复现的设计输入。机器负责保持语义、生成候选和做可读性检查；作者负责选择视觉方向和允许的改动范围。

## 一轮交互的边界

每轮只问三个问题：

1. **视觉方向**：保持当前气质、变轻盈、变鲜明、变暖或变冷静；
2. **评价优先级**：均衡、可读性、审美，或打印/CVD；
3. **改动范围**：只改配色、配色加图例，或整图打磨。

候选必须使用相同的数据、统计标记、几何、标签位置和导出参数。作者没有选择前，状态为 `awaiting_author`，不得修改生产图。

## 状态机

```text
candidate_ready
      |
      v
awaiting_author --选择方案--> direction_selected
      |                              |
      +--自由文本反馈---------------> revision_requested
                                     |
                                     v
                              constrained_rerender
                                     |
                                     v
                              author_approval_pending
```

`direction_selected` 表示作者只选了方向；它仍需要经过预览和可读性检查。`revision_requested` 表示反馈已经转成约束，但不能被误写成“作者已批准”。

## 反馈转约束

| 作者说法 | 机器记录 | 后续动作 |
|---|---|---|
| 不要绿色、发绿 | `avoid_hues: [green]` | 在同一语义家族中筛掉绿色候选，重新渲染整图 |
| 太暗、黑压压 | `lightness_target: airy` | 先提高明度，再检查白底文字和缩印 |
| 太灰、没层次 | `chroma_target: moderate` 或 `colorful` | 增加相邻类别区分度，仍保留 CVD 和灰度复查 |
| 保留暖色/冷静感觉 | `preserve_cues: [warm]` 或 `[cool]` | 保留视觉线索，不改变正负方向和统计语义 |
| 图例太远、标签不齐 | `edit_scope: palette_legend` 或 `full_figure` | 只有作者允许该范围时才调整布局 |

无法明确映射的反馈保留在 `feedback` 字段，并回到三个问题中的一个追问；不要擅自猜测作者要改数据或统计含义。

## 交付记录

每轮至少保存：

- 候选 palette ID 和完整颜色顺序；
- 作者的三个答案、选择的候选和自由文本；
- `preference_constraints` 与被拒绝候选；
- 正常视觉、灰度、CVD、目标尺寸预览；
- 是否通过人工审阅、是否仍需作者批准。

脚本 [`scripts/author_review.py`](../scripts/author_review.py) 提供 `create` 和 `record` 两个命令。它不写生产图、不删除文件，也不替作者做最终审美决定。

## 科学边界

配色审阅可以改变视觉表达，但不能悄悄改变数据、效应方向、显著性、类别顺序或验证状态。对于 LDSC/Genova/HDL 环形图，分类环、signed effect 环和 validation 环必须保持独立的语义层；作者只能选择视觉方向，统计含义仍由分析结果决定。
