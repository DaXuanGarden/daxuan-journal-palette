# Luban 增量打磨报告：联合抽卡 × SCI 语义候选

## 本轮只刨的一个面

把“10 张高清视觉卡片”和 `sci-color-palettes` 候选预览从两个孤立产物，收敛成一个有 seed、来源、匹配距离和图表语义的联合选择流程。

## 交付物

- `scripts/joint_palette_draw.py`：读取卡片 manifest，按 seed 抽卡，运行 SCI 分类/发散/环形图适配，输出 JSON、PNG 和 HTML。
- `references/joint-card-sci-workflow.md`：写明图片层和语义层的边界、图表类型映射和输出契约。
- `tests/test_joint_palette.py`：验证 seed 可复现、分类/热图层分离、PNG/HTML 可见产物。
- 项目当前回放：`joint_palette_draw_20261025/joint_palette_draw.json`、`joint_palette_preview.png`、`index.html`。

## 设计判断

图片不是最终科研色板。它负责“抽卡”的视觉发现；SCI 色板负责分类、发散热图和验证状态的统计语义。两者只通过 CIE76 距离建立“气质接近度”，不跨语义拼色。对于当前环形图，分类环、signed LDSC 热图环、HDL/Genova 验证环仍分别使用定性、发散、中性 + 单一强调色。

匹配先限定在 SCI 候选池，再以视觉接近度进行卡片级排序。这样既保留 SCI 的应用筛选，又避免 10 张卡片全部退化到同一候选。

## 实测结果

- 10 张卡片按 `seed=20261025` 可复现；
- 分类候选池 12 套，signed heatmap 候选池 12 套；
- 当前 10 张卡片产生 5 个不同的分类候选和 2 个不同的热图候选；
- 右侧联合预览同时展示分类块、signed heatmap 和 circular heatmap 三种语义；
- `21` 个 Skill 单元测试通过；
- `py_compile` 通过；
- Qiaomu validator：`ok=true`；
- trigger evaluation：`15/15`，false positive `0`，false negative `0`。

## 使用边界

预览中的 SCI 分数、CIE76、CVD、明度和白底对比度是诊断证据，不是期刊接受保证。最终选色仍需要在真实图形、目标尺寸、灰度和导出格式下人工复核。当前不提交图片资产到公共 Skill，只提交流程、契约和测试。
