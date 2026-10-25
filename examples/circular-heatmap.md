# Circular heatmap example

This example uses the layer contract for the LDSC/Genova/HDL circular figure:

- `outcome_category_ring`: qualitative category colors
- `signed_ldsc_heat_ring`: diverging signed effect colors with a zero midpoint
- `validation_ring`: neutral gray plus one validation accent

Generate the small QA card from the repository root:

```bash
python3 scripts/render_palette_preview.py \
  --title "LDSC circular heatmap" \
  --colors '#6D98AF' '#7DACA3' '#CBA064' '#CE8793' '#A28BAF' \
  --output-dir /tmp/daxuan-circular-preview
```

The preview is a screening artifact. Review the final PNG/PDF/SVG at the intended figure size before submission.
