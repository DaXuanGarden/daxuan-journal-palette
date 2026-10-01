# Palette Atlas

本图谱给出可直接起步的科研图表色板。HEX 是设计输入，不是任何期刊的官方规范。中国/东方风格名称表示视觉语汇；除非另有原始来源，不把它们写成历史色彩复原。定性色板应保持组别顺序；连续和发散色带应按数值方向生成，而不是把色板当作分类色。

## 选择规则

| 图形语义 | 首选色族 | 说明 |
|---|---|---|
| 组别、通路、组织 | 定性 | 4–6 组优先；超过 7 组使用标签、形状或分面 |
| 强度、显著性、计数 | 连续 | 保持明度单调；避免把红色单独当作“更重要” |
| 正负效应、富集方向 | 发散 | 先定义中点，通常为 0 或无效值 |
| 环形、相位、时间角度 | 循环 | 起点和终点同色；不用于普通分类 |
| 机制图底图或对照 | 中性灰 + 强调色 | 用灰色承载背景，用一个颜色承载主结论 |

## A. Ink and mineral

### `ink-mineral-a-sunlit` (recommended for white-background figures)

适合白底机制图、GO-BP 富集图和 5 组以内的定性分类。它保留水墨矿物的色相关系，但降低过暗区域，适合缩印和长条形富集图。

```text
ink_blue       #6D98AF
mineral_teal   #7DACA3
ochre          #CBA064
cinnabar_rose  #CE8793
ink_plum       #A28BAF
```

建议：背景 `#FFFFFF`，正文/轴线 `#263238`，浅背景描边 `#FFFFFF` 或 `#263238`，图例按语义而不是按颜色深浅排序。

### `ink-mineral-a`

较深的 A 版本，适合深色底图、需要更强视觉重量的机制图，或白底中只使用少量大面积色块的图。

```text
ink_blue       #527A8F
mineral_teal   #5B8C85
ochre          #B7833F
cinnabar_rose  #A75A66
ink_plum       #8A6F99
```

### `ink-cinnabar`

适合突出一个主结论并保留东方墨色的图。不要同时把朱砂和绿色解释成两个方向，以免造成红绿依赖。

```text
ink           #27343B
indigo        #3F6078
celadon       #709B91
cinnabar      #B94E52
ochre         #C28A3A
```

## B. Chinese and oriental muted

### `jiangnan-muted`

低饱和青绿、藕粉、黛蓝、茶褐和灰紫，适合多面板和组织/细胞分类。浅色填充需要加深文字或描边。

```text
river_teal    #4F8A83
lotus_pink    #C98291
dai_blue      #4D6680
tea_brown     #9B7653
mist_plum     #806D88
```

### `dunhuang-mineral`

矿物蓝、朱红、石绿、金赭和沙紫，适合强调通路模块和富集类别。金赭适合条形或点，不适合作为浅色大面积背景。

```text
lapis         #3E6E8F
vermilion     #B65B50
malachite     #5C8D78
gilded_ochre  #C28B3C
desert_lilac  #8B7190
```

### `songyun-celadon`

更克制的青瓷、墨蓝、枣红、米灰和梅紫，适合正文图和补充图保持统一。

```text
celadon       #6E9B96
deep_ink      #3D566C
date_red      #9D5B5C
paper_gray    #B7B8B1
plum          #76677E
```

### `gugong-muted`

适合少量高亮和分类标签。明黄色只作为小面积强调，不用于大面积背景。

```text
palace_red    #A94B4A
jade          #578B83
imperial_ochre #C0903A
ink_blue      #49647B
stone         #86847D
```

## C. Journal mineral and clinical

### `nature-muted`

白底、低饱和、清晰层次，适合生物医学多面板图。强调色数不超过 5 个，正文使用深灰。

```text
deep_blue     #365C78
teal          #4F8A86
amber         #B9833B
rose          #A75F70
lavender      #81759A
```

### `clinical-cool-warm`

适合病例/对照、组织和生物标志物分组。蓝绿承载主要组别，珊瑚和芥末只用于强调。

```text
navy          #304F68
slate         #607D8B
teal          #4B918A
coral         #C46F6A
mustard       #B68B3D
```

### `botanical-earth`

适合代谢、肝脏、炎症和生态类机制图；用土色表达模块，不暗示统计方向。

```text
forest        #3F6B5A
leaf          #729B72
ochre         #B58A43
terracotta    #B66956
plum          #765E78
```

### `nordic-mineral`

冷静的蓝灰与苔绿配一枚暖色强调，适合白底、高密度图和缩印。

```text
fjord         #416A80
ice           #79A9B3
moss          #718B70
ochre         #B58C4E
dusty_rose    #AD7180
```

## D. Structure-preserving styles

### `monochrome-accent`

用于多个对照组或需要突出一个结果的图。先用灰阶区分背景，再用一个蓝、朱砂或青绿强调主组；不适合需要五组都同等突出的图。

```text
ink           #27343B
slate         #63717A
silver        #A9B0B3
paper         #E6E7E3
accent_teal   #4B918A
```

### `cvd-high-contrast`

适合重要分组和审查图。它借鉴常见色觉可区分原则，但仍需对实际图形做检查；不要仅凭色板名称声称安全。

```text
blue          #0072B2
orange        #E69F00
green         #009E73
vermillion    #D55E00
purple        #CC79A7
sky           #56B4E9
```

### `pastel-journal`

可用于轻量补充图或需要柔和语气的图。它不是默认主方案：浅背景上的文字和灰度区分可能不足，应增加深色描边并在最终尺寸审查。

```text
lavender      #C6B3DA
blue          #6986B6
cyan          #B0DCE5
rose          #E3A9B5
apricot       #F3C77A
```

## E. Continuous and diverging ramps

### `paper-blue-sequential`

从纸白到深蓝，用于计数、显著性或强度。示例锚点按低到高排列；实际绘图时让中间值保持足够明度差。

```text
#F3F5F3  #C9D9D8  #8FB8BB  #527A8F  #263F55
```

### `jade-ochre-sequential`

适合代谢或组织强度，不表达正负方向。

```text
#F5F1E9  #D6DDD1  #A8BDA7  #728F79  #3F6B5A
```

### `ink-cinnabar-diverging`

用于有明确中心值的正负效应。中点为纸白；蓝和朱砂是两个方向，不能把颜色方向写成未经检验的生物学好坏。

```text
#3F6078  #94AFB8  #F5F2EC  #D89A91  #A94B4A
```

### `qingzhu-diverging`

青竹到暖赭的东方风格发散色带；仍需明确中点和数值方向。

```text
#3F7180  #9BBCC0  #F5F1E8  #E0B18A  #B66A4A
```

## F. Expanded artistic families

这些配方用于补充风格谱系。它们是设计输入，不代表历史色彩复原；默认仍需按实际图形做灰度、色觉、缩印和印刷检查。

### `ink-paper-literati`

纸本、石墨和灰青构成安静的主体，茶褐和枣红只做少量节点或结果强调。适合注释密集的网络图、线图和机制图。

```text
graphite       #34444D
slate_ink      #607D86
paper_celadon  #8EA8A8
tea_brown      #B8A58F
date_red       #A46C6C
```

### `qinghua-porcelain`

深钴与釉蓝保持冷静层级，青白和暖米作为浅色承载。适合热图注释、空间图和分组气泡；蓝色类别较多时必须用明度或形状补充。

```text
cobalt         #2F5D7E
glaze_blue     #4A82A3
celadon_white  #8FB6C1
warm_kaolin    #D8B98A
porcelain      #F3F0E8
```

### `tea-earth-botanical`

茶褐、苔绿和米纸组成低饱和的草木语汇，果实红只用于重点。适合生物过程、器官来源和实验流程图。

```text
tea            #85664D
moss           #718B70
leaf           #98AA83
paper          #D8D0BD
berry          #A96868
```

### `coastal-mineral`

海蓝和孔雀青承载主体，珊瑚与沙金提供暖色锚点。适合环境、空间和单细胞分群图；青绿和蓝色相邻时需加深其中一色。

```text
deep_coast     #245C73
peacock        #4A8E91
shell_gray     #AAB8B2
coral          #C97868
sand_gold      #C59B69
```

### `desert-clay`

赭红、陶土和沙金构成温暖但克制的矿物风格，烟灰用于对照。适合空间热点、模块和地理图，不宜将全部暖色解释为风险。

```text
smoke          #56666A
clay           #A96E58
terracotta     #C68B67
desert_gold    #D3B083
date           #7A4E45
```

### `alpine-lake`

深湖蓝、雾青、松绿和岩石金提供冷暖平衡，莓紫可作少量分组或节点。适合纵向队列、生态图、网络和轨迹。

```text
lake           #365B69
mist           #6E9293
pine           #A9C3B2
rock_gold      #C49A68
berry_plum     #8B6F72
```

### `editorial-jewel`

以深蓝和青绿做出版型主体，以琥珀、玫瑰和紫灰做有限强调。它表达“现代编辑部”的克制感，不是任何期刊的官方色板。

```text
editorial_blue #274C77
editorial_teal #4F8C8C
amber          #D07C4A
rose           #9A596B
violet_gray    #7C6A9A
```

### `graphite-copper`

石墨和银灰先建立结构，再以铜和砖红突出主结果。适合模型比较、结构图和对照组 + 单一主结论；多于四个同等重要类别时改用定性色板。

```text
graphite       #30343B
silver         #8F9BA3
slate          #5A6470
copper         #B57F55
brick          #A85F59
```

### `impressionist-muted`

以低饱和蓝、绿、赭、玫瑰和紫构成柔和的艺术化层次，适合低密度示意图和补充图。小点、细线和灰度打印需重点检查。

```text
blue_gray      #496A81
sage           #7F9E93
ochre          #C8A77C
rose           #BA7A85
lavender       #8C7A9A
```

## G. 配方使用规则

- `qualitative` 配方按语义顺序直接分配，不按色相、明度或字母顺序自动重排。
- `sequential` 配方从低到高排列；需要更多等级时在同一色相路径中插值，并检查明度单调性。
- `diverging` 配方必须写出中点、两端含义和是否对称；若中点没有统计含义，改用 `sequential`。
- 浅色配方用于白底时默认加 `#263238` 文字或细描边；深色配方用于深底时先测试局部对比和透明叠加。
- 若要把一套定性色板改成深/浅版，只调整明度和饱和度并保留色相关系；调整后应记录原 ID、变换和新 HEX。

## 语义和来源边界

- 以上命名色板是为论文图表整理的设计配方，可从同一配方生成深/浅版本；名称不等于历史、地域或文化的严格出处。
- “Nature 风格”“Cell 风格”等表示常见的克制、白底、高可读性视觉目标，不表示来自这些期刊的官方色板。
- 若用户提供已有色板，默认保留其语义和顺序，只在获得同意后调整明度、饱和度或对比度。
- 颜色不能替代直接标签、形状、线型和统计注释；显著性仍由数据和统计方法定义。
