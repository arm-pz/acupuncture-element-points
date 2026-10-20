# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Students and practitioners of Traditional Chinese Medicine looking up the five Shu (jing-river) points of the twelve primary channels. Job on the homepage: get into any channel's interactive chart in one click. Job on a channel page: see exactly where each Shu point sits on an authentic anatomy chart and recall its category, element, and location.

## Product Purpose

An atlas of the five Shu points across all twelve channels. Each channel page is a self-contained interactive reference: a real anatomy chart with clickable overlay dots on the Shu points, and a per-point panel showing its Shu category, element, pinyin/English name, and location text. Success = an accurate, fast, trustworthy study reference that eventually serves public traffic.

## Positioning

Interactive authentic charts, not static tables: every point is shown on a real anatomical diagram (labels cleaned, dots overlaid), and every Shu assignment is verified against classical 五输穴 tables and WHO-standard point lists — including the Yin-channel skips (SP4, KI4/KI5, HT5/HT6, PC6) that trip up other references.

## Operating Context

Developed as a local prototype: static HTML pages with embedded base64 images, served by `shu-serve.js` at http://127.0.0.1:4174 (routes `/`, `/lu`, `/li`, `/li2`, `/ht`, `/ht2`, `/sp2`, `/st2`, `/bl2`, `/ki2`, `/gb2`, `/lr2`, `/si`, `/pc`, `/tb`). Lung is already published at github.com/arm-pz/shu-points; the rest stay local until licensing is settled. Homepage role confirmed by the owner: channel launcher first, minimal prose.

## Capabilities and Constraints

- All twelve channels have pages; eight carry the V2 interactive-chart pattern (LI/HT/SP/ST/BL/KI/GB/LR); SI/PC/TB are still V1; LU is its own public page.
- Verified Shu lists and element cycles are domain-critical: Yang Metal→Water→Wood→Fire→Earth, Yin Wood→Fire→Earth→Metal→Water, always skipping Luo/Xi-Cleft points. Any change must be re-verified against a fetched live source before shipping.
- Most chart and point images are provisional (nalaayan.com diagrams; user-supplied charts of unconfirmed provenance). Publishing non-LU pages is blocked until licensing is resolved; provisional images must keep their "provisional source" credit line.
- No per-point outbound links on any page (deliberately removed at the owner's request).
- Pages are single self-contained HTML fragments; the visualization snapshot surface caps files at 1 MB.

## Brand Commitments

Working name: the five Shu points atlas. Only the Lung page has a settled public identity (CC BY-SA chart on arm-pz/shu-points). No logo, palette, or type commitments made.

## Evidence on Hand

- Verified 60-point Shu table (chat record, `project-shu-atlas-data` memory) cross-checked against zh.wikipedia 五输穴, WHO codes, and nalaayan category badges.
- Twelve working channel pages + homepage served locally; LU page live in the public repo.
- Absences future work must not fabricate: licensed imagery for non-LU channels, named institutional users, testimonials, usage stats.

## Product Principles

1. Accuracy before beauty — a wrong point label is a worse failure than an ugly page; verify domain data against live sources before editing.
2. Authentic charts only — real anatomy diagrams with overlay interactivity, never hand-drawn approximations.
3. The chart is the product — pages exist to put a point on a body; chrome and prose stay minimal.
4. Provisional stays labeled — unlicensed assets are visibly credited until cleared.
5. Launch fast, land deep — navigation from homepage to a specific point should take two clicks.

## Accessibility & Inclusion

Open decision: no accessibility standard has been set yet; public teaching use implies keyboard-operable controls and text alternatives should be treated as a baseline.
