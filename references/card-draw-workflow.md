# 开放抽卡与图像配色工作流

“抽卡”是本 Skill 的开放模式：先从图片获得视觉线索，再把线索转译成科研图配色。它与内置色板是两条并行路径。内置色板适合快速、稳定和跨项目复用；抽卡适合探索新的气质、建立作者自己的风格库。

## 三种抽卡模式

### 1. `open-public`：公共领域作品

使用 `scripts/draw_art_cards.py` 从 The Met Collection API 抽取 3–5 张候选图。脚本使用分页搜索、`hasImages=true` 和 `isPublicDomain=true`，返回作品标题、艺术家、对象 ID、缩略图 URL、作品页和权利说明。它只保存元数据，默认不把第三方图像复制进仓库。

适合的请求：

```text
随机抽 5 张公共领域的蓝绿色风景或版画，适合白底期刊图，先让我选一张。
```

### 2. `prompted-generated`：生成式视觉卡片

调用本机 `imagegen` Skill 的内置 `image_gen` 工具，一次生成 3–5 张独立卡片。每张卡片使用同一主题约束，但改变构图、色彩节奏或材质。生成图片的来源写为 `generated`，不能写成某位艺术家的原作，也不能自动加入公共领域来源清单。

适合的请求：

```text
请抽 5 张“现代水墨、矿物颜料、留白、低饱和、没有文字”的视觉卡片，先展示缩略图，我选一张再提取配色。
```

### 3. `hybrid`：公开作品 + 生成式变体

先抽 2–3 张公共领域作品，再为每张作品生成一个“结构相近但不复制原作”的抽象变体。候选卡片必须分别标明 `public-domain-reference` 和 `generated-variation`，用户可以选择原图灵感或生成式变体。

## 抽卡响应格式

先给卡片选择，不要直接把第一张图的颜色当作最终方案。每张卡片至少包含：

```yaml
draw_id: "2026-10-02-blue-ink-01"
card_id: "card-03"
image_url: "https://..."
thumbnail_url: "https://..."
source_type: public-domain | generated | generated-variation
source_url: "https://..."
title: "..."
artist: "..."
artwork_id: "..."
rights: public-domain | generated | unclear
palette_status: not-extracted
```

展示 3–5 张后，让作者选择 `card_id`。如果作者说“你来选”，选择依据仍应写清楚：图表语义、背景、图形密度、最终尺寸和颜色风险，而不是只说“最漂亮”。

## 选中后的提色流程

1. 保存所选卡片的来源 URL、作品 ID、权利状态和抽卡种子；生成式卡片保存完整 prompt 和生成时间。
2. 对本地图像运行 `scripts/extract_palette.py`，输出 4–8 个主色、面积占比、RGB/HEX、算法和参数。
3. 将原始主色分成背景、文字/描边、主体、支持色和强调色；不要按占比直接当成数据组顺序。
4. 根据图表语义重排或轻微调整明度/饱和度，记录 `transformation`，保留原始提取结果。
5. 生成实际科研图，再做灰度、色觉差异、文字对比、透明叠加和最终尺寸审查。
6. 只有作者确认且审查通过，才把结果加入 `palettes.json` 作为新内置配方。

推荐的提色命令：

```bash
python3 scripts/draw_art_cards.py \
  --query "blue landscape" --count 5 --seed 20261002 \
  --output cards.json

python3 scripts/extract_palette.py selected-card.jpg \
  --count 5 --seed 20261002 \
  --source-url "https://..." \
  --rights public-domain --output selected-palette.json
```

`extract_palette.py` 使用 Pillow 的 RGB k-means。Pillow 是可选依赖；没有安装时，Skill 应明确提示安装或改用人工取色，不应伪造提取结果。算法输出是候选色，不是最终科研色板。

## 何时允许内置

抽卡色板要进入内置库，至少满足：

- 有完整来源或生成记录；
- 有明确的 `source_type`、`rights`、`extraction` 和 `transformation`；
- 适合一种清楚的图表语义，而不只是“看起来漂亮”；
- 经过实际图形、灰度、色觉差异和缩印检查；
- 色板命名不冒充艺术家的官方色板、历史复原或期刊规范。

推荐 ID：`card-<source>-<visual-cue>`，例如 `card-met-indigo-paper` 或 `card-generated-mineral-mist`。原始图片和生成图片默认作为会话或外部资产保存；仓库只加入色板 JSON、来源元数据和必要的缩略色带。

## 版权与来源边界

- 公共领域只表示当前数据源对该对象的权利标记；仍保留机构、对象页和图像 URL。
- 生成式卡片标记为 `generated`，不附会艺术家姓名，不把生成结果写成公共领域作品。
- 版权不清楚的图片只作为链接式灵感，不下载、不提交到仓库、不把其颜色命名为作者原作色板。
- 抽卡结果用于科研配色时，最终交付应同时给出 `provenance` 和 `assumptions`。

## 交付给作者的最小结果

```yaml
draw_mode: open-public | prompted-generated | hybrid
selected_card: card-03
visual_cue: "靛蓝、纸色、有限朱砂、留白"
extracted_hex: ["#1E4C6B", "#5F8BA0", "#D8B16A", "#B9544A", "#E8DED0"]
palette_id: card-met-indigo-paper
semantic_mapping: qualitative | sequential | diverging | neutral-accent
audit: pending | reviewed
provenance: "source URL, artwork ID or generation prompt, extraction method, transformation"
```

抽卡的亮点是扩大探索空间；最终的出版质量仍来自语义映射、有限强调、可读性审查和可追溯来源。
