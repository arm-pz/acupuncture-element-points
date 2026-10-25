# Shu Atlas

Interactive atlas of the five Shu points across the twelve primary channels of acupuncture. Each channel page is a self-contained HTML reference: an authentic anatomy chart with clickable dots on the five Shu points, and a panel showing the point's Shu category, Five Shu element, pinyin/English name, and textbook location.

**Status: private working repository.** Only the Lung page has cleared imagery for public release (see [Licensing](#licensing)). Do not publish or deploy this repository until the remaining image licences are settled.

## Pages

| Route | File | Channel |
|---|---|---|
| `/` | `index.html` | Homepage — twelve-channel launcher |
| `/lu` | `lung-meridian-chart.html` | Lung (LU) |
| `/li` | `li-meridian-chart.html` | Large Intestine (LI) |
| `/li2` | `li-v2-meridian-chart.html` | Large Intestine (LI), V2 |
| `/li3` | `li-v3-meridian-chart.html` | Large Intestine (LI), V3 — one plate, two views |
| `/li4` | `li-v4-meridian-chart.html` | Large Intestine (LI), V4 — arm plate in the LU style (side view, thumb forward) |
| `/ht` | `ht-meridian-chart.html` | Heart (HT) |
| `/ht2` | `ht-v2-meridian-chart.html` | Heart (HT), V2 |
| `/ht4` | `ht-v4-meridian-chart.html` | Heart (HT), V4 — arm plate in the LU style (palm view) |
| `/sp2` | `sp-v2-meridian-chart.html` | Spleen (SP), V2 |
| `/sp3` | `sp-v3-meridian-chart.html` | Spleen (SP), V3 — one plate, two views |
| `/st2` | `st-v2-meridian-chart.html` | Stomach (ST), V2 |
| `/st3` | `st-v3-meridian-chart.html` | Stomach (ST), V3 — one plate, two views |
| `/bl2` | `bl-v2-meridian-chart.html` | Bladder (BL), V2 |
| `/bl3` | `bl-v3-meridian-chart.html` | Bladder (BL), V3 — one plate, two views |
| `/ki2` | `ki-v2-meridian-chart.html` | Kidney (KI), V2 |
| `/ki3` | `ki-v3-meridian-chart.html` | Kidney (KI), V3 — one plate, two views |
| `/gb2` | `gb-v2-meridian-chart.html` | Gallbladder (GB), V2 |
| `/gb3` | `gb-v3-meridian-chart.html` | Gallbladder (GB), V3 — one plate, two views |
| `/lr2` | `lr-v2-meridian-chart.html` | Liver (LR), V2 |
| `/lr3` | `lr-v3-meridian-chart.html` | Liver (LR), V3 — one plate, two views |
| `/si` | `si-meridian-chart.html` | Small Intestine (SI) |
| `/si4` | `si-v4-meridian-chart.html` | Small Intestine (SI), V4 — arm plate in the LU style (back view) |
| `/pc` | `pc-meridian-chart.html` | Pericardium (PC) |
| `/pc4` | `pc-v4-meridian-chart.html` | Pericardium (PC), V4 — arm plate in the LU style (palm view) |
| `/tb` | `tb-meridian-chart.html` | Triple Burner (TB) |
| `/tb4` | `tb-v4-meridian-chart.html` | Triple Burner (TB), V4 — arm plate in the LU style (back view) |

## Run

```
node shu-serve.js
```

Then open <http://127.0.0.1:4174>. The server maps the routes above to files. Pages are self-contained (styles, fonts, and images embedded), so individual pages also open directly, but the `/li2`-style links between them need the server.

## Data

- Five Shu assignments verified against classical 五輸穴 tables and WHO-standard point lists.
- Yin channels follow Wood → Fire → Earth → Metal → Water; Yang channels follow Metal → Water → Wood → Fire → Earth. Luo-Connecting and Xi-Cleft points are always skipped.
- Named traps confirmed: TE Sea = TE10, LR River = LR4 and Sea = LR8, GB set = GB44/43/41/38/34.
- On the V2 and V3 charts, only the five Shu points are interactive; other printed dots mark non-Shu points.
- No per-point outbound links, by design.

## Licensing

- **Lung (LU):** based on [“Points of lung channel” by Dimitrius, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Points_of_lung_channel.svg), CC BY-SA 3.0. Relabelled P → LU and non-Shu points removed. That derivative imagery remains CC BY-SA 3.0.
- **Arm plates (`/ht4`, `/pc4`, `/si4`, `/tb4`):** reuse the same Dimitrius arm drawing (mirrored for the back view, palm creases removed there), CC BY-SA 3.0. Channel lines and Shu points are drawn for this project.
- **LI arm plate (`/li4`):** side-view line art made from a user-supplied LI illustration, provenance to be confirmed.
- **All other channel charts:** user-supplied, provenance to be confirmed. Not licensed for redistribution.
- **Per-point location diagrams:** nalaayan.com, provisional source; licensing review pending.
- Point categories were cross-checked against nalaayan.com per-point badges (provisional source).
- No blanket licence is granted for this repository. Code and design © 2026 Abdul Rahman P Z; third-party imagery remains the property of its respective sources.

## Related

- [`arm-pz/shu-points`](https://github.com/arm-pz/shu-points) — the public, LU-only predecessor.
