# GitHub Public Release

这个 Skill 可以作为普通 Git 仓库发布到 `DaXuanGarden/daxuan-journal-palette`。发布前应先完成本地验证，再由 `qiaomu-meta-skill` 创建 feature branch、Pull Request、版本 Release 和 clean install 证据。

## 仓库内容

- `SKILL.md`、`README.md`、`manifest.json`：入口、使用说明和版本元数据。
- `references/`、`scripts/`、`assets/palette-gallery/`：风格规则、生成器和可视化画廊。
- `LICENSE`：MIT 许可证。
- `.github/workflows/validate.yml`：验证 JSON、脚本语法、画廊可重复生成和必要文件。

## 推荐发布顺序

1. 确认 `manifest.json`、`SKILL.md` 和 `reports/skill-ir.json` 版本一致。
2. 运行 `python3 scripts/build_palette_gallery.py --overwrite`，确认生成文件没有未提交差异。
3. 确认 `gh auth status` 已登录 `DaXuanGarden`，并检查目标仓库是否已存在。
4. 运行 qiaomu publisher 的 dry-run；确认 owner、仓库名、分支、版本和文件变更正确。
5. 使用完整发布命令，让工具创建 feature branch、PR、合并、`v0.3.0` Release，并完成 `npx skills add --list` 和隔离安装验证。

不要把令牌写进远程 URL、脚本、CI 日志或提交历史。发布完成的判断包括：公开仓库可匿名访问、默认分支包含当前版本、GitHub Actions 通过、版本 Release 存在、技能可以被发现并完成干净安装。

## 内置发布命令

```bash
python3 /home/daxuan/.codex/skills/qiaomu-meta-skill/scripts/publish_skill.py \
  /home/daxuan/.codex/skills/daxuan-journal-palette \
  --github-user DaXuanGarden \
  --repo-name daxuan-journal-palette \
  --no-sync-local
```

只做读取审计时加 `--dry-run`；如果希望 PR 通过后由人工合并，加 `--no-merge`。版本标签应与 `manifest.json` 一致；本次修复使用 `v0.5.1`。
