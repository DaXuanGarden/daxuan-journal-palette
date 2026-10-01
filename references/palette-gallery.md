# Palette Gallery Workflow

HEX 文本适合复制，但不适合比较。这个 Skill 使用“机器可读色板源 + 确定性渲染器 + 静态画廊”的方式让作者先看到颜色，再做选择。

## 交付物

- `assets/palette-gallery/palettes.json`：唯一的色板源文件，包含视觉家族、数据类型、关键词、适用场景、风险、颜色名称和 HEX。
- `assets/palette-gallery/index.html`：无需服务器和外部依赖的可检索画廊；可按家族/数据类型筛选，复制色板 ID，并查看灰度代理。
- `assets/palette-gallery/palette-atlas.svg`：矢量总览，适合 README、评审记录和快速打印比较。
- `assets/palette-gallery/palettes.csv`：适合 R/Python 或人工整理的长表。
- `assets/palette-gallery/manifest.json`：生成记录和输出清单。

## 生成命令

在 Skill 目录运行：

```bash
python3 scripts/build_palette_gallery.py --overwrite
```

脚本只使用 Python 标准库，不访问网络、不安装依赖、不修改原始参考文档。新增或调整色板时先修改 `palettes.json`，再重新生成四个输出文件。

## 如何给作者使用

1. 先打开 `assets/palette-gallery/index.html`，按视觉家族和 `qualitative / sequential / diverging / neutral-accent` 筛选。
2. 先比较卡片的整体明度、冷暖节奏和灰度代理，再回到图表语义确认颜色顺序。
3. 复制卡片中的色板 ID，在脚本中使用命名映射；不要从截图或浏览器吸取颜色。
4. 将实际图形以目标栏宽导出后，再做灰度、色觉、透明叠加和印刷检查。画廊不是最终图形的可读性证明。

## 技术选择

- **HTML**：适合作者选择和搜索；静态文件可直接打开，不依赖前端框架。
- **SVG**：适合矢量、缩放和版本审查；颜色与文字不会因位图缩放而模糊。
- **CSV/JSON**：适合可复现代码、跨语言映射和后续自动审查。
- **灰度代理**：按相对亮度生成快速预览，只是诊断信号，不等于完整灰度渲染。

未来如需增加色觉差异预览，可在同一生成器中加入明确标注的模拟行；不要把模拟图当作色盲安全认证。
