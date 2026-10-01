# 艺术灵感与公开来源

本参考页用于回答“想要某种艺术气质，应该从哪里获得视觉线索，以及怎样把线索翻译成论文图表配色”。它不把艺术家的作品、博物馆藏品或第三方色板当作期刊规范，也不主张直接复制一张画的颜色。

## 使用顺序

1. **先写视觉线索**：例如“相邻冷暖、宽阔色面、纸本中性、一个高饱和锚点”。不要先用艺术家名字替代图表需求。
2. **再确定数据语义**：定性、连续、发散、循环或中性灰 + 强调色。语义决定颜色数量、明度方向和中点，艺术线索只决定视觉语汇。
3. **最后做角色分配**：背景、文字、主色、支持色、中性、强调色和描边分别定义；同一变量跨面板固定同一颜色。
4. **在最终尺寸审查**：检查相邻色、灰度、常见色觉差异、黑白打印、文字对比和透明叠加。艺术感不能抵消小尺寸下的识别成本。

## 来源分层

### A. 可作为数据来源或程序参考的公开项目

| 来源 | 可借鉴内容 | 使用边界 |
|---|---|---|
| [MetBrewer](https://github.com/BlakeRMills/MetBrewer) | 以大都会艺术博物馆藏品为视觉起点的色板组织方式、作品元数据思路 | 复用前核对仓库许可证与每个来源作品的权利；本 Skill 中的配方仍是重新设计的期刊版本 |
| [scico](https://github.com/thomasp85/scico) | Crameri 科学色图的均匀明度、连续/发散语义和色觉友好思路 | 连续和发散图优先借鉴其结构；不要把“科学色图”当成艺术定性色板 |
| [accessible-color-cycles](https://github.com/mpetroff/accessible-color-cycles) | 颜色循环、感知距离、色觉差异模拟和审美筛选的联合思路 | 仍要在实际图形、尺寸和输出格式中复核；仓库中的数据和代码要按其许可证使用 |
| [PNWColors](https://github.com/jakelawlor/PNWColors) | 从摄影色彩中提取色板、再为数据可视化调整的工作流 | 摄影是灵感输入，不等于论文语义；记录提取与调整步骤 |
| [Color for geoscience](https://dominicroye.github.io/color-for-geoscience/) | 可浏览、筛选、导出科学色图的开放画廊，含均匀性和色觉元信息 | 用于比较连续色带和建立候选池；最终仍按图表语义选择 |
| [SciPalette](https://scipalette.fantasticjoe.com/) | 面向论文图表的公开色板目录和示例 | 借鉴组织方式，复用前查看仓库和具体色板的许可证 |

### B. 适合作为视觉提示的公开项目

| 来源 | 可提取的视觉原则 | 使用边界 |
|---|---|---|
| [wesanderson](https://github.com/karthik/wesanderson) | 电影画面中的有限色数、叙事性配色和成套命名 | 适合作为气质参考；不要把影视画面或未核对的调色板当作公共领域素材 |
| [MexBrewer](https://github.com/paezha/MexBrewer) | 从墨西哥画家与壁画家的作品得到强烈但有秩序的色彩组合 | 采用“平面色块、有限强调、文化语汇”这些原则，先核对项目许可证和作品权利 |

### C. 适合重新提取灵感的博物馆开放数据

需要从具体画作建立自己的色板时，优先使用有明确开放授权或公共领域标记的图像，并保存作品 ID、艺术家、图像 URL、授权状态和提取方法。

- [The Met Open Access API](https://metmuseum.github.io/)：提供大量藏品元数据和公共领域图像，可用作品 ID 追溯来源。
- [National Gallery of Art Open Access](https://www.nga.gov/artworks/free-images-and-open-access)：提供开放图像和数据，下载前仍应查看当前条款。
- [Art Institute of Chicago API](https://api.artic.edu/docs/)：提供 JSON/REST、IIIF 和公共领域筛选字段；不要默认所有图像都可再分发。
- [Rijksmuseum Data Services](https://data.rijksmuseum.nl/)：提供图像与元数据，记录每件对象显示的 CC0/PDM 或 CC-BY 状态。

**仓库内不存放第三方画作或截图。** 可以在来源表中保留链接、作品 ID 和提取参数；若授权不清楚，只做链接式灵感参考，不把图像或提取结果提交到仓库。

## 艺术原则到论文图表的翻译

下表是视觉翻译，不是对艺术史的严格归纳。艺术家名字只帮助作者快速找到观察对象；输出中应写“受某种视觉原则启发”，而不是声称颜色来自该艺术家的官方色板。

| 视觉参考 | 可观察的原则 | 论文图表翻译 | 推荐起点 |
|---|---|---|---|
| 莫奈式大气感 | 相邻冷暖、低到中饱和、色面之间柔和过渡 | 大面积填充、低密度分面、连续色带；细线和小点要加深 | `impressionist-muted`、`monet-atmospheric` |
| 梵高式互补强调 | 蓝与黄的张力、少量高饱和锚点 | 深蓝承载主体，黄/橙只标主结论或少数节点；不把所有类别都做高饱和 | `van-gogh-accent` |
| 马蒂斯/野兽派平面色 | 平面色块、强互补、轮廓清楚 | 流程图、机制图和分区示意；用标签/形状补足分类，不用于密集小点 | `matisse-flat` |
| Rothko 式色域 | 宽阔近邻色面、单一边界对比 | 中性底 + 一个强调色，适合对照与主结果叙事；避免把色块边界解释成统计方向 | `rothko-field`、`monochrome-accent` |
| Albers 的色彩关系 | 同一颜色受周围颜色影响 | 在白底、灰底和深底上做小型 surround test；色板选择不能只看孤立色块 | 任何主方案 + `accessibility-and-print` |
| Hokusai/浮世绘版画语汇 | 靛蓝、暖朱、稻草色、纸色、有限墨线 | 适合空间图、流程图和注释丰富图；纸色只做背景或大面积浅色 | `hokusai-indigo`、`qinghua-porcelain` |
| 现代水墨/矿物语汇 | 墨色结构 + 一到两枚矿物色锚点 | 以墨灰承载结构，矿物色表达类别或主节点；适合跨面板统一 | `modern-ink-mineral`、`ink-paper-literati` |
| Klee/几何构成 | 小范围几何色块与纸本中性并置 | 适合方法流程、网络节点和分区示意；用少量强调色保持层级 | `matisse-flat`、`graphite-copper` |

## 来源记录模板

每次采用外部灵感或提取色板，至少在交付说明中记录：

```yaml
source_url: https://...
source_type: repository | museum_api | artwork | visual_principle
artwork_id: optional
artist_or_collection: optional
rights: public-domain | CC0 | CC-BY | unclear
extraction: none | manual | k-means | median-cut | other
transformation: "降低饱和度；将最浅色替换为白底可读的中性"
final_palette_id: monet-atmospheric
audit_status: pending | reviewed
```

如果 `rights` 为 `unclear`，只输出来源链接和视觉描述，不分发原图、截图或未经核对的衍生资源。来源记录应与 `provenance`、`assumptions` 和 `visual_preview` 一起交付。

## 作者选择阶梯

当作者只说“想要高级、艺术、有审美”时，依次追问或合理假设：

1. 想要**气氛**（柔和、庄重、鲜明、克制）还是**对象语汇**（纸本、矿物、版画、植物）？
2. 图表是定性、连续还是发散？有多少组、是否需要跨面板固定？
3. 颜色承担数据语义，还是只承担背景/强调？
4. 目标是单栏缩印、屏幕展示、印刷，还是补充材料？
5. 最后给一套主方案和不超过两套备选，附颜色实例、适用场景、风险和来源记录。
