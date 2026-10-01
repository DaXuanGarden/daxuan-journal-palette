# Output Contract and Review Checklist

## Required response fields

    style_name: "ink-mineral-a-sunlit"
    style_family: "ink and mineral / low-saturation editorial"
    style_rationale: "中等明度的冷暖平衡适合白底密集图；赭石和藕红只作为有限强调。"
    palette_type: "qualitative"
    semantic_mapping:
      group_1: "primary module"
    hex:
      group_1: "#6D98AF"
    text_color: "#263238"
    background: "#FFFFFF"
    outline: "#263238"
    R: "c(group_1 = '#6D98AF')"
    Python: "{'group_1': '#6D98AF'}"
    audit:
      contrast: "pass / review / unavailable"
      grayscale: "pass / review / unavailable"
      color_vision: "pass / review / unavailable"
      print: "pass / review / unavailable"
      final_size: "pass / review / unavailable"
    assumptions: []
    provenance:
      palette_id: "ink-mineral-a-sunlit"
      adjustment: "none"
      audit_tool: "unavailable"
    visual_preview:
      html: "assets/palette-gallery/index.html"
      svg: "assets/palette-gallery/palette-atlas.svg"
    card_draw:
      mode: "open-public | prompted-generated | hybrid | none"
      cards: []
      selected_card: null
      extracted_palette: null
      selection_status: "not-requested | awaiting-selection | selected | reviewed"

## Review questions

- 颜色是按数据语义选择，还是只是按好看排序？
- 风格家族是否与图形密度、背景和输出介质匹配？
- 是否把风格名称误写成历史复原、期刊官方色板或审稿标准？
- 组别顺序是否在图例、面板、正文和补充图中固定？
- 关键区别在灰度、色觉差异和缩印后是否仍能表达？
- 文字、坐标轴、浅色背景和透明叠加是否有足够对比？
- 连续/发散色带的方向和中点是否写清楚？
- 色板是否把统计显著性、风险或生物学方向暗示成未经检验的结论？
- 自动化检查的工具、输入和局限是否记录？
- 哪些判断是设计建议，哪些是已运行的检查，哪些仍是 missing evidence？
- 是否记录了原始色板 ID、明度/饱和度调整和审查工具版本？
- 是否给作者提供了可直接查看的 HTML/SVG 预览，而不是只给 HEX 文本？
- 如果使用抽卡，作者是否先看过 3–5 张候选图并明确选择了 `card_id`？
- 抽卡来源、版权状态、生成 prompt、提色算法和明度/饱和度调整是否可追溯？
- 抽卡图片是否只作为视觉输入，最终颜色是否重新按图表语义分配？

## R/ggplot2 example

    palette_ink_mineral_a <- c(
      lipid = "#527A8F",
      mitochondrial = "#5B8C85",
      nucleotide = "#B7833F",
      stress_kinase = "#A75A66",
      support_lavender = "#8A6F99"
    )

    ggplot2::scale_fill_manual(values = palette_ink_mineral_a, drop = FALSE)

## Python example

    INK_MINERAL_A = {
        "lipid": "#527A8F",
        "mitochondrial": "#5B8C85",
        "nucleotide": "#B7833F",
        "stress_kinase": "#A75A66",
        "support_lavender": "#8A6F99",
    }
