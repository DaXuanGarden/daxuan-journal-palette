# SCI palette integration report — circular heatmap

Date: 2026-10-25. This is a recommendation/audit record; it does not recolour the production figure.

## Layer contract

| Layer | SCI role | Selection rule |
|---|---|---|
| Outcome category ring | `database` categorical | `sp.select()` from one fitted ramp; preserve category order |
| Signed LDSC heat ring | `diverging` | `sp.ramp()`; retain the pale zero centre at index 3 of 7 |
| HDL/Genova validation ring | Daxuan `neutral-accent` | neutral gray + one accent; independent of the heat scale |

## outcome_category_ring

| Rank | Palette | SCI score | Fit | Selected colours |
|---:|---|---:|:---:|---|
| 1 | `burgundy-clin-hi` | 68 | yes | `#38091E #C08E9A #FFECF2 #859AA8 #DABC90` |
| 2 | `burgundy-clin` | 67 | yes | `#3B1022 #C0929D #FFECF2 #889CAA #DABD94` |
| 3 | `lilac_garden-clin-hi` | 65 | yes | `#1C104B #A48F63 #688A6F #B68390 #F2F0F5` |
| 4 | `lilac_garden-h270` | 65 | yes | `#0096A8 #F5B5CA #DFB79F #B0C8EE #EEF5F7` |
| 5 | `burgundy-light` | 63 | yes | `#764355 #D9A7B3 #FFECF2 #9EB3C3 #E8CA9E` |

## signed_ldsc_heat_ring

| Rank | Palette | Full-ramp CVD ΔE | Best-5 ΔE | Min best-5 ΔE | Span8 | Selected colours |
|---:|---|---:|---:|---:|---:|---|
| 1 | `div-plum-sage-deep` | 15.5 | 15.5 | 20.5 | 0.813 | `#2C203B #6F6479 #B8B0BE #F6EAD3 #BDB199 #828B70 #476553` |
| 2 | `div-plum-sage` | 11.8 | 14.1 | 14.2 | 0.724 | `#655675 #968AA1 #C9C1CF #F6EAD3 #CFC2AA #A0A98D #6F8F7B` |
| 3 | `div-plum-blue` | 8.7 | 14.0 | 14.2 | 0.757 | `#713E50 #A17C88 #D2BFC5 #F3E7FC #CCBFD5 #9F9ABD #6978A6` |
| 4 | `div-plum-blue-soft` | 8.6 | 8.6 | 8.8 | 0.595 | `#AE7688 #C8A1AD #E1CED4 #F3E7FC #DBCEE4 #BCB7DB #93A2D2` |
| 5 | `div-plum-blue-deep` | 8.2 | 20.5 | 20.5 | 0.826 | `#2E0115 #75535E #C0AEB4 #F3E7FC #BAAEC3 #7E799B #394A74` |

## Audit limits

- one ramp per semantic layer; never splice members from unrelated ramps
- preserve category order across panels and legend
- pale SCI members are fills/bands only; use dark members for text and outlines
- retain labels/geometry/markers because color is not the sole evidence cue
- run sp.report or sp.check again after the final figure is rendered
- SCI scores are library diagnostics; final review must use the rendered figure at the target size and export format.
