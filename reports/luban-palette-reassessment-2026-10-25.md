# Daxuan Journal Palette · Luban 回炉审查报告

审查日期：2026-10-25
对象：`daxuan-journal-palette` 0.6.0
活体样本：LDSC–GNOVA–HDL 21 结局环形遗传相关性热图
本轮状态：已完成方案 B 与方案 A 的 P0 落地；完成真实预览卡、可移植路径回退、层间契约和用户偏好约束；未发布或合并。

## 1. 验料结果（Skill 前提挑战）

挑战1 - 真实问题：**成立**。作者需要同时处理分类色、正负相关热图、验证状态、白底缩印和个人审美反馈；单独列 HEX 不能解决这些层之间的冲突。

挑战2 - 独特角度：唯一性来自中文优先的东方/矿物视觉家族、科研语义映射、图片抽卡溯源和 SCI 审计的组合。当前仍缺少“层间协调”和“用户审美反馈可复用”两条机器可执行规则。

挑战3 - 安装理由：可以得到 HEX、R/Python 映射、图片卡片、SCI 候选和审计结果；公共安装理由还需要一条不依赖本机路径的首跑命令。

挑战4 - 公共传播性：一句话钩子是“把科研图的审美意图编译成有语义、有来源、能复查的配色”。已有真实环形图和多种色板输出，但缺少可复现的 before/after benchmark 和 20–30 秒首跑展示。

验料结论：**好料，继续打磨**。

## 2. 访行记录（同类Skill横向对标）

| 同类项目 | 链接 | 类型 | 可学的手艺 | 当前不能照搬的点 |
|---|---|---|---|---|
| pypubfigs | https://github.com/JLSteenwyk/pypubfigs | 直接/手艺 | 期刊主题、色盲友好色板、Python/Seaborn 直接调用 | 主要面向 Python 主题，不处理中文审美和图片溯源 |
| PubChroma + FigureLint-Bio | https://github.com/tyuan2024/pubchroma | 直接 | 把字段、图形类型、色板和投稿前 QA 放入同一规则系统 | 其 lint 是规格级检查，不能直接替代真实渲染审查 |
| SSCI-Plots | https://github.com/O0000-code/SSCI-Plots | 直接/手艺 | 期刊预设、可见产物、统一导出和独立图例 | 不能把期刊预设名称当作官方配色保证 |
| sci-color-palettes | https://github.com/Xiong-ding-kan/sci-color-palettes | 直接 | 按 clinical/database/basic 场景评分，并提供 CVD/对比度诊断 | 诊断分数不是期刊认证；需要保留 Daxuan 的语义层设计 |
| scico | https://github.com/thomasp85/scico | 间接/手艺 | 感知均匀的连续和发散色带、明确 R API | 主要解决连续色带，不解决分类环和图片灵感 |
| ClawHub Color | https://clawhub.ai/ivangdavila/skills/color | 间接/手艺 | 按 data-viz、print、color-space 分文件加载，避免所有请求走同一套规则 | 重点是通用颜色系统，缺少科研图形的语义层和 R/Python 复现契约 |

交叉观察：成熟同行都把“色板选择”和“最终渲染审查”分开；医疗/科研工具还会把字段、图形类型、打印介质和色盲检查纳入规则。Daxuan 的优势是审美语言和图片来源链，但需要把真实图形回放提升为一等产物。

## 3. 生态位判断

纵向结论：Skill 已从色板索引发展为“路由 + 抽卡 + SCI 桥接 + 审计”的工作流；下一阶段应从“推荐色板”升级为“多语义层配色编译器”。

横向结论：同类项目的信任来自可复现代码、实际预览、字段化规则和打印/CVD 证据，而不是色名本身。

一句话新定位：**Daxuan Journal Palette 把科研图的审美意图和数据语义编译成分层配色，并在真实渲染、CVD、灰度和缩印条件下复查。**

## 4. 过尺结果（活体检查 + 九维评分）

### 活体检查

- 当前真实环形图已生成 PNG、PDF、SVG 和 700-dpi TIFF；蓝紫正相关版本已实际查看。
- `python -m unittest discover -s tests -p 'test_*.py' -q`：25/25 通过。
- `check-skill-repo.sh`：10 PASS、3 WARN、0 FAIL。
- 3 条 WARN 为：缺 `.claude-plugin/marketplace.json`、缺 demo GIF/视频、缺 skills.sh 徽章；它们属于发布包装项，不影响本地工作流。
- 当前蓝紫热图审计：分类环无 ΔE<12 近邻；Plum–Blue 热图有 1 对浅色近邻，说明最终尺寸审查仍然必要。
- 真实回放暴露的问题：`div-plum-sage` 的绿色正相关端与分类环黄橄榄色发生视觉冲突；替换为 `div-plum-blue` 后，三层语义更容易分辨。

### 九维评分

| 维度 | 权重 | 得分 | 证据 | 最大短板 |
|---|---:|---:|---|---|
| Frontmatter 与触发条件 | 7 | 6 | 触发评估和排除边界完整 | 缺少“绿色/过暗/过灰”等审美反馈词典 |
| 工作流清晰度 | 12 | 10 | Router、抽卡、SCI bridge、输出契约 | 三层环形图合同仍分散在不同文件 |
| 失败模式编码 | 12 | 8 | 有路径检查和抽卡降级 | 缺少字体、裁切、缩印、渲染失败矩阵 |
| 检查点设计 | 6 | 5 | CVD、灰度、对比度和真实图审查 | 缺少统一图形 benchmark 命令 |
| 可执行具体性 | 17 | 14 | 脚本、R/Python 映射、21 个测试 | SCI 默认路径仍需显式配置 |
| 资源整合度 | 4 | 4 | atlas、gallery、references、bridge、tests | 缺少统一 preview CLI |
| 整体架构 | 12 | 9 | 语义/风格/介质/角色分层 | 缺少机器可读的层间协调 schema |
| 实测表现 | 23 | 21 | 真实环形图、四种导出、25/25 测试、仓库内五联预览卡 | 尚未完成公共安装回放 |
| 反例与黑名单 | 7 | 5 | 已禁止红绿单独表达和图片色直接上图 | 需要加入“同一图内禁止混用多个发散色带” |
| **总分** | **100** | **86** | 结构、测试、真实图形证据和五联预览齐全 | 公共可移植性和发布包装仍是主要损耗 |

## 5. 差距清单

### P0（已完成）

- 增加 `circular_heatmap` 层间合同：分类环、signed heat ring、验证环分别声明 `palette_type`、零点、状态色和文字策略。
- 为 SCI bridge 增加自动发现、环境变量、缺失时的 Daxuan-only fallback 和清晰错误信息；三种 figure 模式都返回结构化缺省结果。
- 把正常视觉、灰度、protanopia、deuteranopia 和 target-size 纳入一次性 preview 命令，并保存 PNG/JSON 示例。

### P1（本轮已完成核心项）

- 把“不要绿色”“不要黑压感”“浅色但不能灰”“保留暖黄橄榄”等用户反馈编码为可组合的 `preference_constraints`，加入 `chroma_target`。
- 增加当前环形热图的五联 benchmark 预览卡：`assets/showcase/circular-palette-preview/`。
- README 补充可移植的 SCI bridge 与 preview 命令、缺失依赖行为和示例链接。

### P2

- 增加 CMYK/打印证明和 SVG 字体嵌入检查。
- 保存用户选中的方案、拒绝理由和最终采用方案，形成审美反馈回流。
- 增加 `changelog.md` 与同行对标观察清单。

## 6. 三个打磨方向

### 方案A：细修——分层配色合同和反馈约束

修改 `SKILL.md`、`sci_palette_bridge.py`、输出契约和测试。加入 `layer_mapping`、`preference_constraints`、`fallback` 和失败矩阵。风险低，优先解决重复调色和层间冲突。

### 方案B：精雕——真实科研图配色 benchmark（推荐）

在 A 的基础上增加 `render_palette_preview.py`，对同一真实图输出 normal/CVD/grayscale/target-size 五联预览，并记录选择理由。最能证明 Skill 的判断来自实际图形，而不是 HEX 直觉。

### 方案C：开套件——拆分路由、抽卡、审计和图形预览

把当前 Skill 拆成可选模块。长期扩展性好，但会增加安装和版本同步成本，当前没有必要马上拆分。

推荐：**B，先完成 A 的 P0 项**。

## 7. 可直接替换的改写片段

### 加入 `SKILL.md` 的分层合同

```markdown
## Circular figure contract

当图形包含多个环层时，先声明每层的语义，再选择色板：

- `outcome_category_ring`: qualitative；固定类别顺序；不得使用连续渐变。
- `signed_effect_ring`: diverging；明确负端、零点和正端；零点必须位于色带中心。
- `validation_ring`: neutral-accent；验证状态与效应方向分离；不得复用热图色阶。

同一图形内不得拼接不同发散色带的成员。若用户反馈“太绿、太暗、太灰”，先在同一家族内调整明度和色相，并重新渲染整图，再决定是否换家族。
```

### 加入 `SKILL.md` 的审美反馈约束

```markdown
## Preference constraints

把用户审美反馈转成可审计约束，而不是临时形容词：

- `avoid_hues`: 用户明确排斥的色相，如 `green`、`red-green`。
- `lightness_target`: `airy`、`balanced` 或 `ink-heavy`。
- `chroma_target`: `muted`、`moderate` 或 `colorful`。
- `preserve_cues`: 需要保留的视觉线索，如 `yellow/olive print cue`。
- `background`: 默认 `#FFFFFF`，白底图优先用中等明度填充。

推荐结果必须返回 `applied_constraints` 和 `rejected_candidates`，让作者知道为什么换色。
```

### 加入输出契约的字段

```yaml
layer_mapping:
  - layer: outcome_category_ring
    palette_type: qualitative
    palette_id: ink-mineral-a-sunlit
  - layer: signed_effect_ring
    palette_type: diverging
    palette_id: div-plum-blue
    zero_stop: 3
  - layer: validation_ring
    palette_type: neutral-accent
    validated_color: '#D37C70'
    unavailable_color: '#DDD9D0'
preference_constraints:
  avoid_hues: [green]
  lightness_target: airy
  preserve_cues: [yellow/olive]
rendered_preview:
  normal: required
  cvd: required
  grayscale: required
  target_size: required
```

## 8. README 与 Showcase 建议

首屏用一句话说明价值，并直接展示当前真实环形图的三种配色对比：绿色版、蓝紫版、灰度版。示例输入应包含：`21 outcomes + circular heatmap + white background + avoid green + signed LDSC + validation ring`。输出同时给 PNG、PDF、审计 JSON 和简短选择理由。

## 9. 执行结果与后续计划

### 已完成

- [x] 按用户授权采用方案 B，并先落地方案 A 的 P0 层间合同。
- [x] 固化 circular figure contract、preference constraints 和 `chroma_target`。
- [x] 把当前蓝紫环形图分类环作为首个 benchmark fixture。

### 后续可选

- [x] 新增统一 preview CLI 和五联图。
- [ ] 加入临时目录安装回放。
- [x] 增加反馈型测试：拒绝绿色、轻盈明度、保留黄橄榄线索。

### 7 天内

- [ ] README 改为 showcase-first。
- [ ] 增加 SVG/PDF 字体、裁切和目标尺寸检查。
- [ ] 建立 changelog 和回炉观察表。

本轮不做：不发布、不 merge、不拆分 Skill、不删除现有色板、不覆盖用户当前生产图。

## 10. 出师证书

```text
┌─────────────────────────────────────────────┐
│              出师证书 · 鲁班工坊             │
│                                             │
│  作品：Daxuan Journal Palette 0.6.0         │
│  过尺：81 → 86 / 100（本轮实测）             │
│  定位：科研审美意图的分层配色编译器          │
│  绝活：中文视觉语汇 + 语义层 + 真实图审查     │
│  下一步：完成公共安装回放与发布包装           │
│                                             │
│  验收师傅：鲁班                              │
└─────────────────────────────────────────────┘
```

## 11. 回炉清单

- 持续观察 `pubchroma` 的字段化 palette/figure lint、`SSCI-Plots` 的期刊预设和可见导出、`sci-color-palettes` 的应用场景门、`scico` 的感知均匀发散色带。
- 每次色板修改必须保存：输入语义、用户偏好、被拒绝色板、最终渲染图、审计 JSON 和导出格式。
- 下一轮优先从 P0 的层间合同和公共路径 fallback 开始；不继续无规则地试色。

## 12. 当前默认与边界

1. 当前 21 结局环形图作为第一张 benchmark；绿色禁用只在命令显式传入 `--avoid-hue green` 时生效，不改变全局色板默认值。
2. `chroma_target` 目前是约束记录字段；SCI 排序仍由外部库的 CVD、明度和应用评分驱动，避免把主观偏好伪装成客观认证。
3. 发布前仍应完成一次临时目录安装回放，并在最终 PNG/PDF/SVG 尺寸下复查标签、图例和字体嵌入。

## 13. 参考来源

- https://github.com/JLSteenwyk/pypubfigs
- https://github.com/tyuan2024/pubchroma
- https://github.com/O0000-code/SSCI-Plots
- https://github.com/Xiong-ding-kan/sci-color-palettes
- https://github.com/thomasp85/scico
- https://clawhub.ai/ivangdavila/skills/color
