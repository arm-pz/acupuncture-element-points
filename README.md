# Shu Atlas

Interactive atlas of the five Shu points across the twelve primary channels of acupuncture. Each channel page is a self-contained HTML reference: an authentic anatomy chart with clickable dots on the five Shu points, and a panel showing the point's Shu category, Five Shu element, pinyin/English name, and textbook location.

**Status: private working repository.** Only the Lung page has cleared imagery for public release (see [Licensing](#licensing)). Do not publish or deploy this repository until the remaining image licences are settled.

## Pages

| Route | File | Channel |
|---|---|---|
| `/` | `index.html` | App home — the Five Elements ring, linking into each element's channels |
| `/channels` | `channels.html` | Twelve-channel launcher, filterable by element |
| `/points` | `points.html` | Searchable index of all sixty Shu points |
| `/learn` | `learn.html` | Ten-module course and reference: the five names (with the Lung hand figure and Nan Jing indications), the element cycle, an element per module, cun, landmarks and a closing read |
| `/basics` | `basics.html` | Redirect into `/learn` (old section anchors map to the matching module) |
| `/study` | `study.html` | Recall quiz: Shu category, element and finding the point |
| `/lu` | `lung-meridian-chart.html` | Lung (LU) — arm, palm view |
| `/li` | `li-v4-meridian-chart.html` | Large Intestine (LI) — arm, side view with the thumb forward |
| `/st` | `st-v4-meridian-chart.html` | Stomach (ST) — leg, front view |
| `/sp` | `sp-v4-meridian-chart.html` | Spleen (SP) — leg, inner side |
| `/ht` | `ht-v4-meridian-chart.html` | Heart (HT) — arm, palm view |
| `/si` | `si-v4-meridian-chart.html` | Small Intestine (SI) — arm, back view |
| `/bl` | `bl-v4-meridian-chart.html` | Bladder (BL) — leg, outer side |
| `/ki` | `ki-v4-meridian-chart.html` | Kidney (KI) — leg, inner side |
| `/pc` | `pc-v4-meridian-chart.html` | Pericardium (PC) — arm, palm view |
| `/tb` | `tb-v4-meridian-chart.html` | Triple Burner (TB) — arm, back view |
| `/gb` | `gb-v4-meridian-chart.html` | Gallbladder (GB) — leg, outer side |
| `/lr` | `lr-v4-meridian-chart.html` | Liver (LR) — leg, front view |

## Footer and favicon

Every scrolling page ends in the Caffeinity wordmark only. Edit `tools/footer-snippet.html` and run `python3 tools/sync-footer.py`. The yin-yang tab icon lives in `favicon.svg`; run `python3 tools/sync-favicon.py` to inline it into every page.

## Deploy

Production is the Cloudflare Worker `shu-atlas`, which serves <https://acu.caffeinity.com>. The build is `python3 tools/build-site.py` (pages, short routes, 404 and favicon embedded in `.build/worker.js`; `wrangler.jsonc` points at it) and the deploy is `npx wrangler deploy`.

**Auto-deploy on merge** uses Cloudflare's Git integration, so no credentials live in GitHub: in the Cloudflare dashboard open Workers & Pages → `shu-atlas` → Settings → Builds → Connect, choose `arm-pz/acupuncture-element-points`, production branch `main`, build command `python3 tools/build-site.py`, deploy command `npx wrangler deploy`. Every merge to `main` then deploys.

**Manual deploy** from a trusted machine: `tools/deploy.sh`, with `CLOUDFLARE_API_TOKEN` (Workers Scripts → Edit) and `CLOUDFLARE_ACCOUNT_ID` in `~/.config/shu-atlas/cf.env`, never in the repo.

## Shared styling

The twelve chart pages share one stylesheet, `tools/chart.css`, in the same midnight shell as Channels, Points, Learn and Study (Jost and IBM Plex Mono, element inks, the anatomy plate on a cream card). After editing it, run `python3 tools/sync-chart-style.py` to copy it into each chart.

## Run

```
node shu-serve.js
```

Then open <http://127.0.0.1:4174>. The server maps the routes above to files and also serves each page under its file name, which is how the app pages link to one another. Pages are self-contained (styles and images embedded; the app pages load their fonts from Google Fonts), so they also open directly from disk.

The twelve chart pages are the V4 pages plus Lung; the older V1–V3 charts were removed (they remain in git history). The `/lr4`-style routes still work as aliases. A point code after `#` opens the chart with that point selected, e.g. `gb-v4-meridian-chart.html#GB34`.

## Data

- **Single source:** all sixty points (code, pinyin, hanzi, English name, category, element, location, Lung cun notes) and the twelve channels live in `data/points.json`. Pages stay self-contained, so the data is copied into them: after editing the JSON, run
  ```
  python3 tools/sync-points.py
  ```
  It rewrites the marked `/* points:start … */` blocks in the app chart pages (V4 + Lung), Study, Points and the home page, and the `data-pt` / `data-f` tagged names, elements and locations in Learn. It refuses to write if a channel breaks the station or element sequence, or doesn't have exactly one horary point. `python3 tools/sync-points.py --check` reports any page that is out of date without changing it.
- Five Shu assignments verified against classical 五輸穴 tables and WHO-standard point lists.
- Yin channels follow Wood → Fire → Earth → Metal → Water; Yang channels follow Metal → Water → Wood → Fire → Earth. Luo-Connecting and Xi-Cleft points are always skipped.
- Named traps confirmed: TE Sea = TE10, LR River = LR4 and Sea = LR8, GB set = GB44/43/41/38/34.
- Every chart's details panel has a **Cun** row (`cun` in `data/points.json`): the cun distance from a named landmark, or, for points found by a joint, bone or crease, that landmark. The distances (GB38, HT4, PC5, TB6, TB10, KI7, ST36, the 0.1-cun Wells and KI1's proportion) were checked against meandqi, acufinder and americandragon. `/learn` explains the five Shu categories, element mapping and cun measurement.
- **Glossary tooltips:** anatomical and Shu terms (cun, proximal, malleolus, Jing-Well, horary point…) get a dotted underline and a hover/tap definition in chart-panel locations, Learn and Study. The terms live in one place, `tools/glossary-snippet.html`; after editing it, run `python3 tools/sync-glossary.py` to copy it into every page (pages stay self-contained).
- No per-point outbound links, by design.

## Licensing

- **Lung (LU):** based on [“Points of lung channel” by Dimitrius, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Points_of_lung_channel.svg), CC BY-SA 3.0. Relabelled P → LU and non-Shu points removed. That derivative imagery remains CC BY-SA 3.0.
- **Arm plates (`/ht4`, `/pc4`, `/si4`, `/tb4`):** reuse the same Dimitrius arm drawing (mirrored for the back view, palm creases removed there), CC BY-SA 3.0. Channel lines and Shu points are drawn for this project.
- **Leg plates (`/st4`, `/sp4`, `/lr4`, `/gb4`, `/bl4`, `/ki4`):** line art traced from the user-supplied leg charts (Kidney chart for the inner side, Gallbladder chart for the outer side, Stomach charts for the front bones and foot; provenance to be confirmed). The front-view shin outline is traced from “Homo sapiens” by Ivy Livingstone, BIODIDAC (https://omeka.uottawa.ca/biodidac/items/show/5101), CC BY-NC 4.0 — non-commercial use only. Channel lines and Shu points are drawn for this project.
- **LI arm plate (`/li4`):** side-view line art made from a user-supplied LI illustration, provenance to be confirmed.
- **`commons/`:** standalone SVG files of the arm plates built on the CC BY-SA lung drawing (LU, HT, PC, SI, TB), with sources and licences in `commons/README.md`.
- **All other channel charts:** user-supplied, provenance to be confirmed. Not licensed for redistribution.
- **Per-point location diagrams:** nalaayan.com, provisional source; licensing review pending.
- Point categories were cross-checked against nalaayan.com per-point badges (provisional source).
- No blanket licence is granted for this repository. Code and design © 2026 Abdul Rahman P Z; third-party imagery remains the property of its respective sources.

## Related

- [`arm-pz/shu-points`](https://github.com/arm-pz/shu-points) — the public, LU-only predecessor.
