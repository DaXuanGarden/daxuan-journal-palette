# Daxuan Journal Palette

一个面向科研论文图表的配色 Skill：把图表语义、艺术风格和出版可读性连接起来，输出可复用的 HEX、R/ggplot2、Python 映射以及色盲、灰度、印刷和多面板一致性审查。当前版本为 0.4.0。

## Prerequisites

- [ ] Python 3.10+（仅用于生成静态画廊）
- [ ] Pillow（仅在需要从本地图像自动提色时需要；可改用人工取色）
- [ ] R 或 Python 绘图环境（仅在实际绘图时需要）
- [ ] 已确定图表类型、类别顺序、目标栏宽和输出介质

开放公共领域抽卡需要网络；内置色板、静态画廊和生成式卡片提示不依赖网络。

## 你可以直接这样说

- “给 GO-BP 富集图设计中国水墨加矿物色，输出 HEX 和 ggplot2 映射。”
- “给五组科研柱状图选不太浅、适合期刊投稿的高级配色，检查色盲和灰度。”
- “比较宋韵、敦煌矿物和北欧矿物三种论文配色，告诉我哪一种适合白底多面板图。”
- “把水墨、文人纸本、青花瓷、草木土色、海岸矿物和现代编辑部风格列成风格地图，给出适用图形和风险。”
- “审查这张热图的连续色带和中点设置，给出印刷和最终尺寸风险。”
- “把所有分面中同一通路固定为同一种颜色，并生成 R 和 Python 代码。”
- “在内置风格之外，随机抽 5 张公共领域的蓝绿色作品，让我选一张，再提取配色做 GO 富集图。”
- “生成 5 张没有文字的现代水墨视觉卡片，我选一张后，把它转成适合白底论文图的 5 色方案。”

## 输出

默认给一套主方案和不超过两套备选方案。每套包括风格家族、风格理由、语义映射、精确 HEX、文字/背景/描边建议、R/ggplot2 与 Python 示例、可访问性检查、假设和来源记录。风格总表见 [references/style-taxonomy.md](references/style-taxonomy.md)，具体配方见 [references/palette-atlas.md](references/palette-atlas.md)。需要直观看颜色时，打开 [assets/palette-gallery/index.html](assets/palette-gallery/index.html) 或 [assets/palette-gallery/palette-atlas.svg](assets/palette-gallery/palette-atlas.svg)。

当前用户选定的 A 风格经过白底和缩印优化，默认使用 `ink-mineral-a-sunlit`：

```text
#6D98AF  #7DACA3  #CBA064  #CE8793  #A28BAF
```

它适合白底的富集图、机制图和五组以内的定性分类。它是设计色板，不是历史色彩复原；较深的 `ink-mineral-a` 仍可用于深色底图或需要更强重量感的图。

可用的艺术家族包括：水墨矿物、文人纸本、江南烟雨、宋韵青瓷、青花瓷、敦煌矿物、朱砂宫墙、草木土色、茶褐植物、北欧矿物、海岸矿物、沙漠陶土、高山湖泊、现代编辑部、临床冷暖、石墨铜色、单色强调、柔和补充图，以及印象派大气、梵高式强调、马蒂斯式平面、Rothko 式色域、浮世绘靛蓝和现代水墨矿物。它们是视觉设计标签，不代表任何期刊官方色板或历史色彩复原。艺术来源和公开仓库见 [references/artistic-inspiration.md](references/artistic-inspiration.md)。

画廊由 [scripts/build_palette_gallery.py](scripts/build_palette_gallery.py) 从 `palettes.json` 生成。HTML 用于筛选和复制，SVG 用于矢量查看，CSV 用于 R/Python 整理；灰度代理仅用于快速发现明度风险。

如果内置风格不够开放，可以使用 [开放抽卡工作流](references/card-draw-workflow.md)：用 [scripts/draw_art_cards.py](scripts/draw_art_cards.py) 抽取公共领域候选图，用 [scripts/extract_palette.py](scripts/extract_palette.py) 提取候选色，或调用本机 `imagegen` 生成 3–5 张视觉卡片。必须先让作者选图，再做语义映射和实际图形审查；抽卡来源、生成 prompt、版权状态和提色方法都要进入 `provenance`。

仓库包含 MIT LICENSE 和 GitHub Actions 校验，可作为 public GitHub skill 发布；具体发布和版本标签顺序见 [references/github-publishing.md](references/github-publishing.md)。

## 使用边界

本 Skill 负责色彩方案和图形可读性审查，不负责统计检验、数据清洗、期刊投稿保证、品牌识别、网页 UI 主题或照片调色。色盲/灰度检查只能说明当前图形在给定尺寸和导出格式下的风险，不能替代人工查看。

可选地结合本机 `easyplot` 的 palette audit、`nature-figure` 的图形契约和 `journal-ggplot-stylebook` 的期刊导出规则；这些依赖不由本 Skill 自动安装。自动诊断只能提供当前图形的风险信号，不能证明色盲认证、印刷无风险或期刊接受。

## 本地验证

本地目录可直接被 Codex 读取；需要用 Skills CLI 安装到另一个环境时，可使用 npx skills add /home/daxuan/.codex/skills/daxuan-journal-palette，再按目标环境的安装提示确认目录。

上游参考：qiaomu-meta-skill; K-Dense-AI/scientific-agent-skills scientific-visualization; local easyplot; local nature-figure; local journal-ggplot-stylebook。

```bash
python3 /home/daxuan/.codex/skills/qiaomu-meta-skill/scripts/validate_skill.py /home/daxuan/.codex/skills/daxuan-journal-palette
python3 /home/daxuan/.codex/skills/qiaomu-meta-skill/scripts/trigger_eval.py /home/daxuan/.codex/skills/daxuan-journal-palette --output /home/daxuan/.codex/skills/daxuan-journal-palette/reports/trigger-eval.json
```

## Troubleshooting

- 颜色太浅：先保留色相，降低 LCH/OKLCH 明度；同步增加填充描边和文字对比，不要只把所有颜色变成黑色。
- 分类过多：改用直接标签、形状或分面；不要继续添加相近的浅色。
- 灰度下难以区分：用明度层次重排，并补充线型、形状或标签。
- 热图中点不明确：使用发散色带并明确中点的统计含义；没有有意义的中点时改用连续色带。
- 多面板颜色漂移：建立一个全局命名映射，在每个面板中按同一键值调用。

<!-- qiaomu-profile:start -->
## 关于向阳乔木

向阳乔木（乔向阳 / Joe）是一位实践型 AI 产品与内容创作者，长期把前沿 AI 变化转译成可复用的工作流、产品判断、AI 编程实践、AI 搜索实践和 GEO/AI 营销方法。

- 个人网站: https://qiaomu.ai
- 博客: https://blog.qiaomu.ai
- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
- 微信公众号: 向阳乔木推荐看

### 支持与关注

| 打赏支持 | 微信公众号 |
|---|---|
| <img src="assets/qiaomu-profile/qiaomu_reward_qr.png" alt="向阳乔木打赏二维码" width="180" /> | <img src="assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg" alt="向阳乔木推荐看公众号二维码" width="180" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

<!-- qiaomu-profile:end -->

## License

MIT. See [LICENSE](LICENSE).

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/
