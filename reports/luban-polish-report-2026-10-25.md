# Daxuan Journal Palette · Luban Skill 打磨报告

审计日期：2026-10-25
对象：`/home/daxuan/.codex/skills/daxuan-journal-palette`
当前版本：0.5.6
本轮状态：完成验料、访行、过尺和方向设计；未修改 Skill 定位，等待用户选择下一轮打磨方向。

## 1. 验料结果（Skill 前提挑战）

挑战1 - 真实问题：**成立**。科研作者常常知道“想要高级、东方、克制或色彩丰富”，但不知道如何把这种审美要求转换成定性、连续、发散和中性强调色板，也缺少最终尺寸、色盲、灰度和打印审查。现有 Skill 正好覆盖这条从审美意图到科研图形的链路。

挑战2 - 独特角度：唯一性来自 **中文优先的视觉家族 + 语义色板契约 + 开放图片抽卡溯源 + SCI 应用场景审计**。目前差异点已经存在，但“Daxuan 自己的审美规则”仍主要散落在 `ink-mineral-a`、风格索引和 Router Rules 中，没有形成可执行的审美语法。

挑战3 - 安装理由：安装后可以得到可复制的 HEX、R/ggplot2、Python 映射、色板画廊、公共领域图片来源和 CVD/灰度/对比度审查，而不是每次重新向 Agent 描述“想要高级一点”。需要补强的地方是公共安装路径和一条不依赖本机目录的首跑命令。

挑战4 - 公共传播性：一句话钩子可以是：**“把‘我想要这种科研图质感’变成有语义、有来源、能复查的配色方案。”** 当前可展示产物包括 32 色板画廊、10 张高色彩图片卡片、SCI 分类/发散色板预览和 JSON 审计记录；缺少 20–30 秒的输入到结果 GIF，以及同一真实图形的打磨前/打磨后对比。

验料结论：**好料，继续打磨**。核心问题真实，差异化方向成立，下一步应把审美经验编码成规则并增强公共安装和展示证据。

## 2. 访行记录（同类 Skill 横向对标）

| 同类 Skill / 项目 | 链接 | 类型 | 一句话定位 | 可学的手艺 | 不能照搬的点 |
|---|---|---|---|---|---|
| K-Dense scientific-visualization | [GitHub SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) | 直接/手艺 | 先保护科学含义，再创建和审查期刊图 | 证据优先、期刊尺寸、导出后检查、颜色不能承担全部信息 | 范围比本 Skill 宽，不能吞并完整的图形设计工作流 |
| sci-color-palettes | [GitHub](https://github.com/Xiong-ding-kan/sci-color-palettes) | 直接 | 184 套科研色板、应用场景筛选和 CVD/对比度诊断 | `clinical/database/basic` 场景门、变体命名、可审计指标 | 不能把 SCI 分数当成期刊认证，也不能取代 Daxuan 的视觉家族 |
| cvd-accessible-visualization | [GitHub](https://github.com/gmontaletti/cvd-accessible-visualization) | 直接 | 为 R/Python 图形提供可执行的色觉缺陷检查 | 独立检查脚本、标准引用、可直接调用的 CLI | 重点是 CVD 安全，缺少中文艺术风格和图片溯源 |
| GPTomics color palettes | [Skill 页面](https://skills.homes/en/skills/gptomics-bioskills-data-visualization-color-palettes-skill-md) | 直接/生物信息 | 用 viridis、RColorBrewer 和自定义色板服务生物数据图 | 首屏短、场景尖锐、安装和调用简单 | 方案偏通用，缺少 Daxuan 的审美叙事和图像抽卡 |
| ColorCET | [官方站点](https://colorcet.com/) | 间接/手艺 | 提供感知均匀、连续、发散、循环和色盲地图 | 把连续、发散、循环语义写得非常明确，并提供测试图 | 不适合直接承担定性分类的中文视觉风格 |
| scico / Scientific Colour Maps | [CRAN scico](https://github.com/thomasp85/scico) / [Crameri](https://www.fabiocrameri.ch/colourmaps/) | 间接/手艺 | 提供感知均匀且可复现的科学连续色带 | 强调数据顺序、感知均匀、灰度和可引用版本 | 主要解决连续色带，不解决图片灵感和类别语义 |
| Accessible Color Cycles | [GitHub](https://github.com/mpetroff/accessible-color-cycles) | 间接/手艺 | 用感知距离、色觉模拟和偏好模型生成可区分的颜色循环 | 把“好看”和“可区分”分成可测指标，并保留生成过程 | 计算和数据规模较重，不适合作为 Daxuan 的默认首跑路径 |
| colorspace | [GitHub](https://github.com/cran/colorspace) | 间接/手艺 | 用 HCL 生成和交互选择定性、连续、发散色板 | 用颜色空间参数解释明度、色度、色相，而不是只列 HEX | R 生态交互工具，不能直接替代跨 runtime 的 Agent Skill |
| color-system | [GitHub SKILL.md](https://github.com/AntJanus/skillbox/blob/main/skills/color-system/SKILL.md) | 手艺/相邻 | 用语义角色、OKLCH 和可访问性管理多类颜色系统 | 角色先于 HEX、尺度和语义映射清楚 | 主要面向 UI/品牌/TUI，不能把其默认主题当成论文图规范 |

这些项目共同显示出三条传播规律：一句话定位要尖锐、首次调用要有可见产物、审查指标要与具体语义绑定。Daxuan 当前的中文审美和图片溯源是少见的优势，但首屏和可复现 showcase 还没有达到同样清晰的程度。

## 3. 生态位判断

纵向结论：这个 Skill 已从“个人配色经验”发展为“风格索引 + 色板画廊 + 抽卡脚本 + SCI 审计适配器”的小型工作流。下一阶段不是继续堆色板，而是把审美经验写成可执行规则，并让陌生用户在一分钟内跑出图形化结果。

横向结论：同类项目的立足点主要来自标准化色彩语义、独立审计脚本、清晰安装入口和可见的最终产物。Daxuan 的差异化来自中文优先的东方/矿物视觉谱系、图片卡片来源记录和科研语义映射；当前短板是公共路径可移植性、真实图形 benchmark 和审美规则的机器可读性。

交叉洞察：真正应该抢的生态位不是“又一个色板集合”，而是 **科研作者的审美意图编译器**：输入“东方纸墨、白底、五类、热图、需要色盲审查”，输出语义稳定、可追溯、可渲染、可复查的科研配色。

一句话新定位：**Daxuan Journal Palette 把中文优先的科研审美意图编译成跨 R/Python、带来源和可读性审计的期刊图配色。**

## 4. 过尺结果（活体检查 + 九维质量评分）

### 活体检查

- `python -m unittest discover -s tests -v`：19 个测试通过。
- `validate_skill.py`：结构验证通过，无 failure 或 warning。
- `trigger_eval.py`：15/15 通过，false positive 0，false negative 0。
- `build_palette_gallery.py --overwrite` 后，`git diff --exit-code -- assets/palette-gallery` 通过。
- `route_palette.py`、`draw_art_cards.py --help`、`extract_palette.py --help`、`sci_palette_bridge.py --figure circular --groups 5` 均实际运行成功。
- 真实桥接产物确认了三个语义层：分类环 `burgundy-clin-hi`、signed LDSC 发散环 `div-plum-sage-deep`、验证环中性灰 + 强调色。
- 发现一处验证流程竞态：测试与画廊重建并行时，测试曾读到重写中的空 HTML；顺序执行后 19/19 通过。这说明验证脚本应明确禁止共享生成目录的并行写入。
- 线上 CI 的最近运行记录和公共安装后的真实首跑尚未对账；当前证据来自本地结构、脚本和真实产物。

### 九维评分

| 维度 | 权重 | 得分 | 主要证据 | 最大短板 | 优先级 |
|---|---:|---:|---|---|---|
| Frontmatter 与触发条件 | 7 | 6 | 触发边界明确，15/15 trigger eval 通过 | 没有把“审美意图编译器”写进首屏描述 | P1 |
| 工作流清晰度 | 12 | 10 | Router Rules、Compact Workflow、Gate Ladder | 图片抽卡、SCI 适配和最终图形 QA 的决策树仍分散 | P1 |
| 失败模式编码 | 12 | 8 | 有抽卡降级、SCI 路径检查和审计边界 | 缺少统一的“输入缺失/网络失败/字体缺失/裁切/私有依赖”矩阵 | P0 |
| 检查点设计 | 6 | 5 | `sp.check`、`sp.report`、gallery test、输出契约 | 未自动检查最终 SVG/PDF 的裁切、字体和目标尺寸 | P1 |
| 可执行具体性 | 17 | 14 | 4 个脚本、19 个测试、复制命令 | SCI 默认路径仍是本机路径，公共安装需额外配置 | P0 |
| 资源整合度 | 4 | 4 | atlas、references、scripts、tests、SCI bridge | 资源齐全，尚缺一个统一 preview CLI | P1 |
| 整体架构 | 12 | 9 | 语义/风格/介质/角色/审计分层 | Daxuan 审美语法尚未独立成机器可读 schema | P1 |
| 实测表现 | 23 | 18 | 本地真实命令、gallery、SCI 推荐报告均可运行 | 缺少真实图形前后对比和公共 runtime 安装回放 | P0 |
| 反例与黑名单 | 7 | 5 | 明确不做 UI、品牌、统计和期刊保证 | 应明确禁止混合色带、颜色暗示统计结论、图片提色直接上图 | P1 |
| **总分** | **100** | **79** | 结构、实测和活体证据齐全 | 公共可移植性与视觉 benchmark 是主要损耗 |  |

79 分说明它已经是可用的生产型本地 Skill，但还没有成为“陌生用户装上就能信任和传播”的公共资产。

## 5. 差距清单

### P0：不补就无法放心公开

- `sci_palette_bridge.py` 的默认根路径是 `/home/daxuan/.codex/skills/sci-color-palettes`；虽然支持 `SCI_COLOR_PALETTES_ROOT`，但缺少公开安装后的自动发现、明确降级和错误示例。
- 没有公共安装后的首跑回放：当前验证证明“本地目录能跑”，没有证明 `npx skills add` 或复制到 `.agents/skills` 后能跑。
- 没有最终图形 benchmark：已有色板审计，但尚未对一个真实科研图完成“默认色板 → Daxuan 方案 → SCI/CVD/灰度/缩印”的可重复前后对比。

### P1：补上后明显提升理解和传播

- 把 Daxuan 审美写成五个可执行维度：底色、主色温度、色度上限、暖冷比例、深色文字/描边策略。
- 增加 `render_palette_preview.py` 或等价命令，一次生成 swatch、CVD、灰度和白底文字对比图。
- 增加 3 个公开测试 prompt 和真实输出样例，而不是只展示静态色板。
- README 首屏增加一张真实科研图的前后对比或 20 秒 GIF。
- 验证流程禁止测试与生成目录并行写入，或为每个运行分配临时输出目录。

### P2：锦上添花

- 增加 PDF/SVG 字体嵌入、透明度、裁切和目标尺寸检查。
- 增加用户选中的卡片和最终采用色板的反馈记录，形成审美偏好回流。
- 增加 `changelog.md` 和对标观察表，记录 SCI、Crameri、ColorCET 等上游的变化。

### 与同行相比，我们最缺的 3 件事

1. 一条跨环境、无私有路径的首跑路径。
2. 一个真实科研图的前后对比 benchmark。
3. 一套明确的 Daxuan 审美语法，而不是只靠色板 ID 和作者经验。

### 与同行相比，我们最有机会打穿的 3 件事

1. 中文/东方视觉语汇与科研语义、CVD 审计的结合。
2. 公共领域图片抽卡到最终 HEX 的完整来源链。
3. 把“好看”与“可解释、可复查、可跨面板复用”放进同一个输出契约。

## 6. 三个打磨方向

### 方案A：细修——把现在的 Skill 做成可移植的审美编译器

新定位：明确写出 Daxuan 五维审美语法，并把 SCI 根路径、降级策略、失败矩阵和 preview 命令标准化。
改动范围：`SKILL.md`、`README.md`、`sci_palette_bridge.py`、`manifest.json`、测试 prompt。
优点：风险最低，直接修复 P0，适合先做公共安装。
风险：showcase 变化有限，传播效果主要依赖文案和规则清晰度。
适合条件：优先保证稳定性和跨 runtime 兼容。

### 方案B：精雕——做出可见的科研配色 benchmark 工具包（推荐）

新定位：每个色板都能在一个真实科研图上生成“正常视觉 / CVD / 灰度 / 缩印”的对比卡，并输出选择理由。
改动范围：在方案A基础上新增 2–3 个无敏感数据的真实或合成科研图模板、`render_palette_preview.py`、before/after 图和可复现 showcase。
优点：最能证明 Daxuan 的审美不是主观口号，用户安装后立刻看到结果；也能直接回应当前环形热图的长期迭代需求。
风险：需要固定示例图和渲染后 QA，维护量高于方案A。
适合条件：希望提高传播力、安装率和用户信任。

### 方案C：开套件——从单 Skill 升级为小型配色套件

新定位：`daxuan-journal-palette` 负责路由，拆出 `daxuan-palette-audit`、`daxuan-card-draw` 和 `daxuan-figure-preview` 三个可选模块。
改动范围：新增多个 Skill 目录、跨 runtime 安装说明、共享输出 schema 和版本矩阵。
优点：职责清晰，适合长期维护和多种用户。
风险：会显著增加安装、版本同步和文档维护成本；当前尚未证明单 Skill 已达到需要拆分的复杂度。
适合条件：已有多个团队分别使用抽卡、审计和科研图预览，并愿意维护套件。

推荐选择：**方案B，但先完成方案A中的 P0 可移植性修复**。当前 Skill 已有足够基础，不需要重写成套件；最缺的是让审美和审计结果在真实科研图上可见。

## 7. 候选改写方案（本轮不直接落地）

本轮只刨：**公共可移植性 + Daxuan 审美语法 + 可见 benchmark 入口**。
改动边界：不改现有色板 HEX，不改变用户已经确认的环形热图生产图，不发布、不合并、不打 tag。
预期提升：首次安装能运行；陌生 Agent 能根据审美规则解释为什么选色；用户能看到真实图形审查而非只读 HEX。
验证方式：临时目录安装回放、3 个测试 prompt、真实图形四联预览、顺序执行测试和 gallery diff。

### 建议文件变更

| 文件 | 操作 | 原因 |
|---|---|---|
| `SKILL.md` | 修改 | 增加 Daxuan 五维审美语法和失败矩阵入口 |
| `README.md` | 修改 | 首屏加入一句话钩子、真实图形预览和一条首跑命令 |
| `scripts/sci_palette_bridge.py` | 修改 | 默认路径改为可配置发现；缺失时给出可执行降级信息 |
| `scripts/render_palette_preview.py` | 新增 | 统一生成正常/CVD/灰度/缩印预览 |
| `tests/test_prompts.json` | 新增 | 固化真实用户请求和预期字段 |
| `tests/test_preview.py` | 新增 | 检查生成图、尺寸、文字和审计 JSON |
| `assets/showcase/` | 新增 | 存放可复现的真实科研图 benchmark |
| `reports/changelog.md` | 新增 | 记录上游对标和每轮验证结果 |

### 可直接替换的首屏片段

```markdown
# Daxuan Journal Palette

> 把“我想要这种科研图质感”编译成有语义、有来源、能复查的期刊配色。

它先区分定性、连续、发散和中性强调，再把东方纸墨、矿物、青瓷或编辑部等视觉语汇映射到固定的科研角色；最后输出 HEX、R/Python 映射和正常视觉、CVD、灰度、缩印审查结果。
```

### 可直接加入 `SKILL.md` 的 Daxuan 审美语法

```markdown
## Daxuan Aesthetic Grammar

先写语义，再写审美。每次推荐至少记录以下五个轴：

1. substrate：白纸、冷白、暖纸或深底；它决定文字和浅色填充的安全范围。
2. temperature：冷、暖或冷暖平衡；默认用一个主温度和一个受控的对照温度。
3. chroma：低、中或高色度；密集论文图默认中等色度，只有用户明确要求多彩时才提高色度。
4. hierarchy：一个主色族、一个支持色族、一个强调色和中性灰；不要让所有颜色拥有同等视觉重量。
5. evidence cue：颜色之外至少保留标签、形状、线型、位置或星号中的一个证据线索。

风格名称只描述视觉设计，不代表期刊官方色板、历史复原或可访问性认证。
```

### 可直接加入 bridge 的公共路径降级片段

```python
def discover_sci_root(explicit=None):
    candidates = [
        explicit,
        os.environ.get("SCI_COLOR_PALETTES_ROOT"),
        Path(__file__).resolve().parents[3] / "sci-color-palettes",
    ]
    for candidate in candidates:
        if candidate and (Path(candidate) / "scripts" / "sci_palettes").is_dir():
            return Path(candidate).resolve()
    return None

root = discover_sci_root()
if root is None:
    # Continue with Daxuan-only routing and report the missing optional adapter.
    # Do not fail a basic palette request because an optional local library is absent.
    return {"sci_status": "unavailable", "fallback": "daxuan-atlas"}
```

## 8. README 与 Showcase 升级建议

README 首屏应在 10 秒内完成三件事：说明谁需要它、展示一张真实科研图、给出一条可运行命令。建议顺序：

1. 一句话钩子和 1 张“默认图 → Daxuan 图 → SCI/CVD/灰度”四联图。
2. 3 个真实请求：五类白底分类图、signed LDSC 热图、图片抽卡到科研色板。
3. 一条无网络的内置运行命令和一条可选 SCI 审计命令。
4. 直接链接到色板画廊、当前环形热图推荐报告和测试结果。
5. 明确“图片是灵感输入，最终颜色必须重新按科研语义分配”。

Showcase 不应只展示 HEX 色条；至少要展示一张真实图的正常视觉、CVD 模拟、灰度和最终尺寸版本。录制脚本、输入数据或合成数据和输出图应一起保存，保证 GIF/截图可复现。

## 9. 执行计划

### 24 小时内必须完成

- [ ] 选择 A/B/C 方向；推荐 B，先修 A 的 P0。
- [ ] 把 SCI 根路径和可选依赖降级规则改成跨环境配置。
- [ ] 写入 Daxuan 五维审美语法和 3 个测试 prompt。

### 3 天内完成

- [ ] 新增 `render_palette_preview.py` 和正常/CVD/灰度/缩印四联预览。
- [ ] 用当前环形热图的无敏感数据版本完成第一张 benchmark。
- [ ] 进行一次临时目录安装回放并保存命令、版本和产物清单。

### 7 天内完成

- [ ] README 首屏改成 showcase-first，并补充 before/after 图。
- [ ] 加入顺序执行的验证入口，禁止共享 gallery 目录并发写入。
- [ ] 建立 changelog 和对标观察清单。

### 本轮不做

- 不更改当前生产环形热图的配色。
- 不删除已有色板或复制第三方完整色板库。
- 不拆分成多个 Skill，不发布 GitHub/ClawHub 版本，不打 tag。

## 10. 出师证书

```text
┌─────────────────────────────────────────────┐
│             出师证书 · 鲁班工坊              │
│                                             │
│  作品：Daxuan Journal Palette 0.5.6         │
│  过尺：79 / 100（实测）                      │
│  定位：把科研审美意图编译成可复查的期刊配色  │
│  绝活：中文视觉语汇 + 语义映射 + SCI 审计     │
│  下一步：用真实科研图做四联 benchmark        │
│                                             │
│  验收师傅：鲁班                              │
└─────────────────────────────────────────────┘
```

## 11. 回炉清单

- 对标观察：持续关注 K-Dense scientific-visualization 的发布和验证资产、sci-color-palettes 的应用档案、Crameri/ColorCET 的连续色带更新、Accessible Color Cycles 的感知距离方法。
- 迭代纪律：每轮只改变一个面；先冻结当前版本和真实产物；脚本、测试、报告和 showcase 一起验证；未通过门槛就回刀；未获授权不 merge、push、打 tag 或发布。
- 下一轮入口：先实现 P0 路径降级和 Daxuan 五维审美语法，再制作第一张真实科研图 benchmark。

## 12. 需要用户确认的问题

1. 下一轮选择 **A（细修）/B（精雕，推荐）/C（开套件）**？
2. 是否同意把 `SCI_COLOR_PALETTES_ROOT` 作为可选依赖，并让 SCI 缺失时自动退回 Daxuan 内置色板？
3. 是否同意把“Daxuan 五维审美语法”作为正式公开定位，而不是继续只用色板 ID 和作者经验表达？

## 13. 附录：参考来源

- https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization
- https://github.com/Xiong-ding-kan/sci-color-palettes
- https://github.com/gmontaletti/cvd-accessible-visualization
- https://github.com/linjf15/bio-info-skills/blob/main/data-visualization/color-palettes/SKILL.md
- https://colorcet.com/
- https://github.com/thomasp85/scico
- https://www.fabiocrameri.ch/colourmaps/
- https://github.com/mpetroff/accessible-color-cycles
- https://github.com/cran/colorspace
- https://github.com/AntJanus/skillbox/blob/main/skills/color-system/SKILL.md
