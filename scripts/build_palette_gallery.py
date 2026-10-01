#!/usr/bin/env python3
"""Build a self-contained visual gallery for the journal palette atlas.

The JSON file is the source of truth. Generated HTML is interactive and the
SVG is a crisp, dependency-free overview suitable for quick comparison or
embedding in documentation. No network access or third-party package is used.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "assets" / "palette-gallery" / "palettes.json"
DEFAULT_OUTPUT = ROOT / "assets" / "palette-gallery"


def rgb(hex_colour: str) -> tuple[float, float, float]:
    value = hex_colour.lstrip("#")
    return tuple(int(value[index : index + 2], 16) / 255 for index in (0, 2, 4))


def luminance(hex_colour: str) -> float:
    values = rgb(hex_colour)
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in values
    ]
    return sum(channel * weight for channel, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def text_colour(hex_colour: str) -> str:
    return "#000000" if luminance(hex_colour) > 0.179 else "#FFFFFF"


def grayscale(hex_colour: str) -> str:
    value = round(luminance(hex_colour) * 255)
    return f"#{value:02X}{value:02X}{value:02X}"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def card(palette: dict) -> str:
    swatches = "".join(
        f'<div class="swatch" style="background:{esc(colour)};color:{text_colour(colour)}">'
        f'<span>{esc(name)}</span><code>{esc(colour)}</code></div>'
        for colour, name in zip(palette["colors"], palette["names"])
    )
    gray_swatches = "".join(
        f'<div class="gray-swatch" style="background:{grayscale(colour)}" title="{esc(colour)}"></div>'
        for colour in palette["colors"]
    )
    search = " ".join(
        [
            palette["id"],
            palette["label"],
            palette["family"],
            palette["kind"],
            *palette.get("inspiration", []),
            *palette["keywords"],
            palette["best_for"],
            palette["avoid_for"],
        ]
    ).lower()
    return f'''<article class="card" data-family="{esc(palette["family"])}" data-kind="{esc(palette["kind"])}" data-search="{esc(search)}">
<div class="card-head"><div><h2>{esc(palette["label"])}</h2><code>{esc(palette["id"])}</code></div><span>{esc(palette["kind"])}</span></div>
<div class="swatches" aria-label="原色">{swatches}</div>
<div class="gray-label">灰度代理</div><div class="gray-swatches" aria-label="灰度代理">{gray_swatches}</div>
<dl><dt>关键词</dt><dd>{esc(" · ".join(palette["keywords"]))}</dd><dt>灵感</dt><dd>{esc(" · ".join(palette.get("inspiration", [])) or "本地设计配方")}</dd><dt>适合</dt><dd>{esc(palette["best_for"])}</dd><dt>注意</dt><dd>{esc(palette["avoid_for"])}</dd></dl>
<button type="button" class="copy" data-copy="{esc(palette["id"])}">复制色板 ID</button></article>'''


def html_page(palettes: list[dict]) -> str:
    families = sorted({palette["family"] for palette in palettes})
    cards = "\n".join(card(palette) for palette in palettes)
    options = "".join(f'<option value="{esc(family)}">{esc(family)}</option>' for family in families)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daxuan Journal Palette Gallery</title>
<style>
:root{{font-family:Arial,"Microsoft YaHei",sans-serif;color:#263238;background:#f5f7f8}}*{{box-sizing:border-box}}body{{margin:0}}
header,main,footer{{max-width:1500px;margin:auto;padding:28px 34px}}header{{padding-bottom:10px}}h1{{font-size:32px;margin:8px 0 12px}}p{{line-height:1.7;color:#5d6b73;max-width:1080px}}.eyebrow{{font-size:12px;letter-spacing:.14em;color:#70808a}}
.filters{{display:flex;gap:12px;flex-wrap:wrap;align-items:end;margin:14px 0 24px}}label{{display:flex;flex-direction:column;gap:6px;font-size:12px;color:#5d6b73}}input,select,button{{font:inherit;border:1px solid #cbd4d9;border-radius:5px;background:#fff;color:#263238;padding:9px 11px}}input{{width:300px;max-width:80vw}}button{{cursor:pointer}}button:hover{{background:#edf3f6}}button:focus-visible,input:focus-visible,select:focus-visible{{outline:3px solid #397c9d;outline-offset:2px}}
#status{{min-height:20px;color:#65747d;font-size:13px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;align-items:start}}.card{{background:#fff;border:1px solid #dee5e9;border-radius:7px;padding:18px;break-inside:avoid;min-width:0}}.card-head{{display:flex;justify-content:space-between;gap:12px;align-items:start;margin-bottom:15px}}h2{{font-size:17px;line-height:1.35;margin:0 0 7px;font-weight:600}}.card-head code{{font-size:11px;color:#66757d;overflow-wrap:anywhere}}.card-head>span{{font-size:11px;color:#78858d;white-space:nowrap}}.swatches,.gray-swatches{{display:grid;grid-template-columns:repeat(auto-fit,minmax(58px,1fr));gap:3px}}.swatch{{min-height:65px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:7px;padding:5px 2px}}.swatch span{{font-size:10px;text-align:center;line-height:1.35}}.swatch code{{font-size:9px}}.gray-label{{font-size:10px;color:#7a878e;margin:12px 0 5px}}.gray-swatch{{height:12px;border:1px solid #dbe1e4}}dl{{font-size:12px;line-height:1.55;margin:15px 0}}dt{{color:#69777f;font-weight:600;margin-top:7px}}dd{{margin:0;color:#53616a}}.copy{{font-size:11px;padding:6px 9px}}footer{{border-top:1px solid #dce4e8;margin-top:20px;font-size:12px}}footer a{{color:#245e7d}}#empty{{padding:40px 0;color:#68767e}}[hidden]{{display:none!important}}
@media(max-width:1050px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media(max-width:680px){{header,main,footer{{padding:20px}}.grid{{grid-template-columns:1fr}}h1{{font-size:27px}}}}
@media print{{.filters,.copy{{display:none}}body{{background:#fff}}.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}*{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
</style></head><body>
<header><div class="eyebrow">DAXUAN JOURNAL PALETTE / OFFLINE GALLERY</div><h1>先看色，再决定风格。</h1><p>这是一份面向期刊论文图表的艺术化配色图谱。色板是设计配方，不是期刊官方规范；灰度代理只提供快速信号，最终仍需结合实际图形、尺寸和输出介质检查。</p></header>
<main><section class="filters"><label>搜索风格、关键词或 ID<input id="search" type="search" placeholder="例如 敦煌、青花、sequential"></label><label>视觉家族<select id="family"><option value="">全部家族</option>{options}</select></label><label>数据类型<select id="kind"><option value="">全部类型</option><option value="qualitative">qualitative</option><option value="sequential">sequential</option><option value="diverging">diverging</option><option value="neutral-accent">neutral-accent</option></select></label><button id="reset" type="button">重置</button></section><div id="status" aria-live="polite"></div><section class="grid" id="cards">{cards}</section><p id="empty" hidden>没有匹配的色板。</p></main>
<footer><p><a href="palette-atlas.svg">打开 SVG 总览</a> · <a href="palettes.csv">下载 CSV</a> · 源文件：<code>palettes.json</code> · 可用脚本：<code>scripts/build_palette_gallery.py</code></p><div id="copy-status" role="status" aria-live="polite"></div></footer>
<script>
'use strict';
const cards=[...document.querySelectorAll('.card')], search=document.querySelector('#search'), family=document.querySelector('#family'), kind=document.querySelector('#kind');
function filter(){{const needle=search.value.trim().toLowerCase();let count=0;for(const card of cards){{const show=(!needle||card.dataset.search.includes(needle))&&(!family.value||card.dataset.family===family.value)&&(!kind.value||card.dataset.kind===kind.value);card.hidden=!show;if(show)count++;}}document.querySelector('#status').textContent=`显示 ${{count}} / ${{cards.length}} 套色板`;document.querySelector('#empty').hidden=count!==0;}}
[search,family,kind].forEach(field=>field.addEventListener('input',filter));document.querySelector('#reset').addEventListener('click',()=>{{search.value='';family.value='';kind.value='';filter();}});document.querySelector('#cards').addEventListener('click',async event=>{{const button=event.target.closest('[data-copy]');if(!button)return;try{{await navigator.clipboard.writeText(button.dataset.copy);document.querySelector('#copy-status').textContent='已复制：'+button.dataset.copy;}}catch(error){{document.querySelector('#copy-status').textContent='请手动复制：'+button.dataset.copy;}}}});filter();
</script></body></html>'''


def svg_page(palettes: list[dict]) -> str:
    columns = 3
    card_width, card_height = 500, 180
    margin_x, margin_y = 45, 65
    rows = math.ceil(len(palettes) / columns)
    width = columns * card_width + 2 * margin_x
    height = rows * card_height + 2 * margin_y + 75
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#F5F7F8"/>',
        '<style>text{font-family:Arial,"Microsoft YaHei",sans-serif;fill:#263238}.title{font-size:28px;font-weight:600}.subtitle{font-size:13px;fill:#66757D}.label{font-size:15px;font-weight:600}.id{font-size:10px;fill:#66757D}.hex{font-size:9px}</style>',
        '<text x="45" y="42" class="title">Daxuan Journal Palette · visual atlas</text>',
        '<text x="45" y="63" class="subtitle">艺术家族、定性/连续/发散语义与灰度代理；设计配方，不是期刊官方色板</text>',
    ]
    for index, palette in enumerate(palettes):
        column, row = index % columns, index // columns
        x = margin_x + column * card_width
        y = margin_y + 65 + row * card_height
        elements.append(f'<rect x="{x}" y="{y}" width="{card_width - 18}" height="{card_height - 18}" rx="7" fill="#FFFFFF" stroke="#DEE5E9"/>')
        elements.append(f'<text x="{x + 15}" y="{y + 25}" class="label">{esc(palette["label"])}</text>')
        elements.append(f'<text x="{x + 15}" y="{y + 42}" class="id">{esc(palette["id"])} · {esc(palette["family"])}</text>')
        swatch_width = (card_width - 48) / len(palette["colors"])
        for i, colour in enumerate(palette["colors"]):
            sx = x + 15 + i * swatch_width
            sy = y + 57
            elements.append(f'<rect x="{sx:.1f}" y="{sy}" width="{swatch_width - 2:.1f}" height="48" fill="{colour}"/>')
            elements.append(f'<text x="{sx + swatch_width / 2:.1f}" y="{sy + 67}" text-anchor="middle" class="hex">{colour}</text>')
            elements.append(f'<rect x="{sx:.1f}" y="{sy + 78}" width="{swatch_width - 2:.1f}" height="8" fill="{grayscale(colour)}" stroke="#DEE5E9"/>')
        elements.append(f'<text x="{x + 15}" y="{y + 112}" class="id">灰度代理</text>')
    elements.append("</svg>")
    return "\n".join(elements)


def write_outputs(output: Path, palettes: list[dict], overwrite: bool) -> None:
    output.mkdir(parents=True, exist_ok=True)
    targets = [output / name for name in ("index.html", "palette-atlas.svg", "palettes.csv", "manifest.json")]
    if not overwrite:
        existing = [path for path in targets if path.exists()]
        if existing:
            raise FileExistsError("outputs exist; pass --overwrite: " + ", ".join(map(str, existing)))
    (output / "index.html").write_text(html_page(palettes), encoding="utf-8")
    (output / "palette-atlas.svg").write_text(svg_page(palettes), encoding="utf-8")
    with (output / "palettes.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["id", "label", "family", "kind", "index", "name", "hex", "keywords", "inspiration", "best_for", "avoid_for"])
        for palette in palettes:
            for index, (name, colour) in enumerate(zip(palette["names"], palette["colors"]), start=1):
                writer.writerow([palette["id"], palette["label"], palette["family"], palette["kind"], index, name, colour, "|".join(palette["keywords"]), "|".join(palette.get("inspiration", [])), palette["best_for"], palette["avoid_for"]])
    manifest = {"schema_version": "1.0.0", "count": len(palettes), "source": "palettes.json", "outputs": [path.name for path in targets]}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    payload = json.loads(args.registry.read_text(encoding="utf-8"))
    palettes = payload["palettes"]
    required = {"id", "label", "family", "kind", "keywords", "best_for", "avoid_for", "colors", "names"}
    for palette in palettes:
        missing = required - set(palette)
        if missing:
            raise ValueError(f'{palette.get("id", "<unknown>")} missing {sorted(missing)}')
        if len(palette["colors"]) != len(palette["names"]):
            raise ValueError(f'{palette["id"]} has mismatched colors/names')
        for colour in palette["colors"]:
            if not isinstance(colour, str) or len(colour) != 7 or not colour.startswith("#"):
                raise ValueError(f'{palette["id"]} has invalid colour {colour!r}')
    write_outputs(args.output, palettes, args.overwrite)
    print(f"Built {len(palettes)} palette cards in {args.output}")


if __name__ == "__main__":
    main()
