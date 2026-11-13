---
name: Five Shu Atlas
description: A midnight enamel transit strip map for launching the twelve primary-channel Shu charts.
colors:
  ground: "#10131f"
  ink: "#f2f0ea"
  ink-2: "#9aa4bb"
  hair: "rgba(242, 240, 234, 0.13)"
  hair-strong: "rgba(242, 240, 234, 0.26)"
  row-hover: "rgba(242, 240, 234, 0.038)"
  wood-deep: "#3e7d5a"
  wood-tint: "#83c7a3"
  fire-deep: "#d23b2e"
  fire-tint: "#f2968a"
  earth-deep: "#d99a2b"
  earth-tint: "#e8c273"
  metal-deep: "#dfd9cb"
  metal-tint: "#f2f0ea"
  water-deep: "#3c6fbd"
  water-tint: "#93b8f0"
typography:
  display:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "clamp(24px, 2.4vw, 31px)"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.18em"
  title:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "16.5px"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "0.005em"
  body:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: "normal"
    letterSpacing: "0.015em"
  label:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.16em"
  mono:
    fontFamily: '"Plex Mono", ui-monospace, monospace'
    fontSize: "11px"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.02em"
  han:
    fontFamily: '"Classic", "Songti SC", "SimSun", serif'
    fontSize: "12px"
    fontWeight: 500
    lineHeight: "normal"
    letterSpacing: "0.02em"
rounded:
  badge: "3px"
spacing:
  row: "56px"
  field-mobile: "52px"
  term: "clamp(230px, 20vw, 288px)"
  pad: "clamp(16px, 3vw, 48px)"
  chevron: "30px"
components:
  route-row:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "0"
    height: "{spacing.row}"
    padding: "0"
  route-row-hover:
    backgroundColor: "{colors.row-hover}"
  station:
    textColor: "{colors.ink}"
    typography: "{typography.mono}"
    height: "{spacing.row}"
  phase-badge-wood:
    backgroundColor: "{colors.wood-tint}"
    textColor: "{colors.ground}"
    rounded: "{rounded.badge}"
    height: "26px"
    padding: "0 6px"
  phase-badge-fire:
    backgroundColor: "{colors.fire-tint}"
    textColor: "{colors.ground}"
    rounded: "{rounded.badge}"
    height: "26px"
    padding: "0 6px"
  phase-badge-earth:
    backgroundColor: "{colors.earth-tint}"
    textColor: "{colors.ground}"
    rounded: "{rounded.badge}"
    height: "26px"
    padding: "0 6px"
  phase-badge-metal:
    backgroundColor: "{colors.metal-tint}"
    textColor: "{colors.ground}"
    rounded: "{rounded.badge}"
    height: "26px"
    padding: "0 6px"
  phase-badge-water:
    backgroundColor: "{colors.water-tint}"
    textColor: "{colors.ground}"
    rounded: "{rounded.badge}"
    height: "26px"
    padding: "0 6px"
  quick-launch:
    textColor: "{colors.ground}"
    rounded: "{rounded.badge}"
    height: "30px"
    padding: "0 6px"
  column-header:
    textColor: "{colors.ink-2}"
    padding: "12px 0 9px"
---

# Design System: Five Shu Atlas

## Overview

**Creative North Star: "The Meridian Network"**

The Five Shu homepage is a transit strip map rendered in midnight enamel. Twelve channel routes enter from a single terminus column at the left, each bending 45 degrees into a shared five-column field of Shu stations and running on to Sea. Nothing is a card: rows are separated by hairlines, stations by ticks, and the only bright surfaces are the phase-tinted code badges. The map is the navigation, the lesson, and the product's front door at once.

The stance is Operate, not persuade. This is a channel launcher: a practitioner recognizes a channel at the left terminus, reads its five stations left to right, registers whether the phase cycle starts from yin or yang, and opens that channel's chart in one click. The design refuses the incumbent TCM study-atlas grid of boxed tables in favor of a strip-map topology that makes alignment and sequence visible. The route rows carry the content; the page adds no marketing prose.

Visual authority is code-led. The page is one self-contained HTML file with embedded WOFF2 subsets, inline SVG marks, no scripts, no rasters, no shadows, and no external requests. The world borrows transit-signage discipline—fixed rhythm, monospaced codes, terminal chevrons—without literal signage colors or iconography. Scope honesty is part of the visual contract: this is a public teaching surface; only the Lung page is public, the other channel pages remain blocked from publication, the provisional-source credit stays visible, and per-point outbound links are deliberately absent. Shu assignments are verified against classical 五輸穴 tables and WHO-standard point lists, including the yin-channel skips; any data change must be re-verified before it ships.

**Key Characteristics:**
- **Midnight enamel field.** A full-bleed #10131f ground; porcelain text; no light mode, no cards, no panels.
- **Five doubled phase inks.** Wood, Fire, Earth, Metal, and Water each ship a deep route ink and a tint; color is a pair, not a single accent.
- **Strip-map topology.** A 45° lead-in, a 3px route, five station ticks, and a terminus chevron replace the atlas table.
- **Fixed 56px rhythm.** Twelve rows share one grid and one density; the station field is always five equal columns.
- **Solid/hollow polarity.** Yang is a solid 3px line; yin is a 5px line split by a 2px midnight core, mirrored in the bend and the polarity key.
- **Type as infrastructure.** Jost for voice, IBM Plex Mono for codes, a 30-glyph Noto Serif SC subset for classical names; 11px is the functional floor.
- **One row, one link.** The whole route is the hit target; hover or keyboard focus energizes one route and recedes the other eleven to 52%.
- **Hairlines, not cards.** No box-shadow, no gradient, no raster; separation is a 1px 13%-porcelain rule or a 2px focus ring.
- **Motion with an off switch.** The route draws in 0.65s on a 45ms stagger; reduced motion renders the map static.

## Colors

A midnight field, five mineral inks, and porcelain type. Every phase is a pair—a deep route ink and a tint—so color carries both the line and its label.

### Primary
- **Wood Route Ink** (#3e7d5a): the deep green for Wood tracks, ticks, and 45° lead-ins; 3.78:1 against midnight.
- **Fire Route Ink** (#d23b2e): the deep vermilion for Fire routes; 3.88:1 against midnight.
- **Earth Route Ink** (#d99a2b): the ochre for Earth routes; the highest-chroma warm ink in the map.
- **Metal Route Ink** (#dfd9cb): a deliberately dimmed porcelain route ink, not a metallic gold; 13.15:1 against midnight, the quietest deep ink.
- **Water Route Ink** (#3c6fbd): the lifted blue for Water routes, raised from #2f5fa8 (2.93:1) to 3.70:1 so it holds 3:1 against midnight.

### Secondary
- **Wood Tint** (#83c7a3): fills Wood code badges and colors Wood station phase words.
- **Fire Tint** (#f2968a): fills Fire badges and Fire phase words.
- **Earth Tint** (#e8c273): fills Earth badges and Earth phase words.
- **Metal Tint** (#f2f0ea): fills Metal badges; the one tint identical to Porcelain, making Metal badges the brightest in the map.
- **Water Tint** (#93b8f0): fills Water badges and Water phase words; all five tints clear 8.37:1 against midnight.

### Neutral
- **Midnight Enamel** (#10131f): the page ground, fixed by the `color-scheme: dark` declaration and theme color.
- **Porcelain** (#f2f0ea): primary text, channel names, station codes, chevrons, the yang polarity bar, and the focus ring.
- **Slate Porcelain** (#9aa4bb): metadata, key labels, column heads, and the colophon; 7.40:1 against midnight.
- **Hairline** (rgba(242, 240, 234, 0.13)): row dividers and the masthead/footer rules.
- **Hairline Strong** (rgba(242, 240, 234, 0.26)): the heavier rule under the column header only, where the map's coordinate system needs a stronger edge.
- **Row Wash** (rgba(242, 240, 234, 0.038)): the hover and keyboard-focus background wash; a state, not a surface.

### Named Rules
**The Phase-Pair Rule.** Every phase ships as a deep route ink and a tint. Deep ink draws the track, tick, and bend; tint fills the code badge and colors the station phase word. Never use a tint for a route line or a deep ink for a badge.

**The Metal-Is-Porcelain Rule.** Metal uses #dfd9cb route ink and #f2f0ea tint—a dimmed porcelain route, never gold, brass, or silver. Its restraint is what keeps the five-ink system from becoming a rainbow.

**The Water-Lift Rule.** Water route ink is #3c6fbd, lifted from #2f5fa8 to hold 3.7:1 against midnight, with #93b8f0 tint. Treat the lift as an accessibility invariant, not a color preference; do not revert to the darker blue.

## Typography

**Display Font:** Jost (with system-ui, sans-serif)
**Body Font:** Jost
**Label/Mono Font:** IBM Plex Mono (with ui-monospace, monospace)
**Classical Font:** Noto Serif SC 500, embedded under the local family name `Classic` (with Songti SC, SimSun, serif)

**Character:** A geometric sans that behaves like signage, a documentary mono for point codes, and a 30-glyph classical serif that gives the Chinese names their own voice without turning them into ornament. The pairing reads as a working chart, not a wellness brochure.

### Hierarchy
- **Display** (500, clamp(24px, 2.4vw, 31px), line-height 1, letter-spacing .18em, uppercase): the FIVE SHU wordmark; the 五輸 suffix is 13px at .08em in Slate Porcelain.
- **Title** (500, 16.5px desktop / 15.5px at ≤480px, line-height 1.15, letter-spacing .005em): channel names at the row terminus; no wrap on desktop.
- **Body** (400, 13.5px, normal line-height): the masthead tagline; the colophon steps down to 11.5px at 1.7.
- **Meta** (400, 11px, line-height 1.4): the `Yin · Wood · 足厥陰肝經` line; its Han segment is 11.5px.
- **Label** (400, 11px, .08–.16em, uppercase): phase inks, polarity, column heads, the term head, and station phase words.
- **Mono** (500, 11–12.5px, .02–.04em): station codes at 11px, code badges at 12.5px, quick-launch chips at 12px.
- **Han** (500, 11.5–13px): wordmark suffix 13, column headers 12, meta 11.5; always marked `lang="zh-Hant"`.

**The 11px Floor Rule.** No functional text sits below 11px. Metadata, codes, station phases, headers, key labels, and the colophon all meet the floor; 11.5px is the next step for notes and Han meta. Shrinking type is not an acceptable way to fit the map.

**The Code-Is-Mono Rule.** IBM Plex Mono is reserved for point codes, channel abbreviations, and quick-launch chips. Body copy, functional labels, and Chinese names never use it.

**The Classical-Han Rule.** Chinese channel and Shu names use the embedded Noto Serif SC subset at weight 500 and carry `lang="zh-Hant"`. Do not substitute a system display face or faux-serif when the subset is available.

### Embedded faces and provenance
- **Jost**—OFL; variable 400–600 WOFF2 subset embedded as a base64 data URI (26,576 bytes); display and body sans.
- **IBM Plex Mono**—OFL; 500 WOFF2 subset embedded as a base64 data URI (14,888 bytes); station codes and badges.
- **Noto Serif SC**—OFL; 500 WOFF2 subset embedded as a base64 data URI (7,388 bytes) under the local family name `Classic`; exactly 30 CJK glyphs: 三 五 井 包 厥 合 大 太 小 少 心 手 明 滎 焦 穴 經 肝 肺 胃 胱 脾 腎 腸 膀 膽 足 輸 陰 陽.
- All faces are self-hosted data URIs; the page makes no font network requests. This surface ships no rasters: the wordmark, five-tick route mark, 45° bends, ticks, and chevrons are inline SVG or CSS.

## Layout

The page is one full-bleed map inside a 1440px frame. Horizontal padding is clamp(16px, 3vw, 48px); the masthead sits 30px from the top and closes on a hairline. Below it, a fixed three-column grid repeats for the column header and every route: a clamp(230px, 20vw, 288px) terminus column, a flexible station field, and a 30px chevron column. The station field is five equal columns, so the Well / Spring / Stream / River / Sea heads sit exactly over their ticks.

Rows are 56px high with 1px hairline separators; twelve rows produce a 672px map body before the column header and masthead. The track begins 22px into the field, ends at the Sea tick (10% from the right edge), and runs at a constant 3px. Station codes sit 4px from the top, ticks at 19px, phase words at 41px, giving every row the same three-band read.

At ≤820px the grid collapses to one column: the terminus sits above a 52px field, the 45° bend and chevron disappear, the column header becomes sticky at top 0, and a twelve-chip quick launcher appears beneath the key. At ≤480px the channel name drops to 15.5px, row padding tightens to 9px/7px, and station phase tracking narrows to .06em. At ≤374px the quick-launcher label takes its own line and the chip gap tightens to 4px, so the twelve chips break 6/6 instead of leaving one orphaned. The 480px rule carries the verified 390×844 view. The colophon is capped at 88ch and sets at 11.5px/1.7.

### Named Rules
**The Five-Column Rule.** The station field is always five equal columns in Well → Spring → Stream → River → Sea order. Never add, drop, or reorder a station; the phase ink rotates around the fixed station, not the station around the ink.

**The 56px Rhythm Rule.** Desktop routes stay 56px high and share one grid with the column header. Density comes from repetition and hairlines, not from shrinking rows or type.

## Elevation & Depth

Flat by construction. The page has no box-shadow, no gradient, no card, and no backdrop blur. Depth is tonal and cartographic: the midnight ground recedes, porcelain text advances, phase inks sit between them, and a 13%-porcelain hairline does the separating work. The only "raised" state is interaction: a 3.8%-porcelain row wash on hover or focus and a 2px porcelain focus ring. The stronger 26%-porcelain rule appears only under the column header, where the coordinate system needs a heavier edge.

### Shadow Vocabulary
- **None.** `box-shadow` count in the shipped CSS is zero. Do not add ambient, inset, or glow shadows; the focus ring and row wash are outlines and backgrounds, not elevation.

### Named Rules
**The Hairline-Only Rule.** Separation is one 1px hairline at 13% porcelain (26% under the column header) or a 2px focus ring. No cards, shadows, gradients, or filled panels.

## Shapes

Form is orthogonal and diagrammatic. Rows and fields are square; the only radius is the 3px cut on code badges and quick-launch chips. The route lead-in is a hard 45° bend (22×28px box, path `M1 7 L22 28`), not a curve. Station ticks are 3×18px; the Sea end is marked by the same tick as every other station, not a terminus blob. The chevron is an 8×14px inline stroke. The masthead mark is an 88×14px five-tick ruler: a hairline rail with five 2.5px ticks in the five phase deep inks.

Yin and yang are drawn as line grammar, not labels. Yang routes use a solid 3px track and a solid 3px bend. Yin routes use a 5px track split by a 2px midnight core and a hollow 5px bend cut by a 2px midnight diagonal, so the route reads as a double stripe. The polarity key mirrors the grammar: a solid 24×5px porcelain bar for yang, the same bar with a 1.5px midnight stripe for yin.

### Named Rules
**The 45-Degree Rule.** Every route enters the station field on a hard 45° lead-in (22×28px, dx = dy = 21). Never soften it into a curve or a rounded corner.

**The Solid/Hollow Rule.** Yang is solid (3px); yin is hollow (5px with a 2px midnight core). The distinction must survive at a glance without reading the yin/yang meta text.

## Components

### Route Row (Signature)
The row is the product's atom: one channel, one link, one 56px band.

- **Shape:** grid of 230–288px / 1fr / 30px; min-height 56px; 1px hairline between rows; zero radius; full-bleed within the frame.
- **Terminus:** a stretched link covers the entire row via an absolutely positioned `::after`; inside, a 46×26px code badge (3px radius, phase tint, midnight text, Plex Mono 12.5px), the channel name at 16.5px, and an 11px meta line (polarity · phase · Han name).
- **Field:** a 45° phase-ink bend, a 3px phase track, and five stations. Each station stacks an 11px mono code, a 3×18px phase tick, and an 11px uppercase phase word. A yin route swaps to the 5px/2px stripe grammar.
- **Chevron:** 8×14px inline SVG at 30% opacity; hover or focus raises it to 100% and translates it 2px.
- **Hover:** row wash at 3.8% porcelain; on hover-capable devices the other eleven routes recede to 52% opacity.
- **Focus:** the row gets a single 2px porcelain ring inset 2px; the link's own focus ring is suppressed. The other eleven routes recede to 52%.
- **Reduced motion:** no draw or bend animation; hover and focus state changes are instantaneous.

### Column Header
Five Shu names aligned to the station grid, not a table head.

- Shares the route's 230–288px / 1fr / 30px columns; 12px top / 9px bottom padding; 1px 26%-porcelain bottom rule.
- The left cell reads "Channel · terminus" at 11px .16em uppercase Slate Porcelain.
- Each Shu cell pairs the English station name (11px .15em uppercase) with its Han character (12px Noto Serif SC), baseline-aligned with a 7px gap.
- At ≤820px the header becomes sticky at top 0 with a midnight background; the term cell hides.

### Phase & Polarity Key
The legend is a grammar reference, not decoration.

- Top right of the masthead on desktop; moves left and stacks at ≤820px.
- Phase inks: five 18×3px deep-ink swatches with 11px .12em uppercase labels.
- Polarity: a 24×5px solid porcelain bar for yang; a 1.5px midnight stripe inside the same bar for yin.
- Labels are Slate Porcelain; the swatches are the only place the deep inks appear without a route.

### Quick Launcher (≤820px)
A compact channel index for touch.

- Appears only at ≤820px beneath the masthead key, above the map.
- Twelve links, one per channel, in the phase tint with midnight text; 44×30px minimum, 3px radius, Plex Mono 12px, 6px gap, wrapping.
- Hover brightens by 8%; keyboard focus uses the global 2px porcelain ring at 2px offset.
- Each link carries the channel abbreviation and an `aria-label` with the full channel name.

### Footer Colophon
The map's footnotes, kept as part of the system.

- Starts on a 13% hairline 26px below the map, with 20px top / 40px bottom padding and a max width of 88ch.
- Sets at 11.5px/1.7 in Slate Porcelain.
- The first line states both phase cycles in their phase tints: Yin Wood → Fire → Earth → Metal → Water; Yang Metal → Water → Wood → Fire → Earth; both skip the Luo-Connecting and Xi-Cleft points.
- The second line explains the Well → Sea route span and the split between eight interactive overlay channels (LI, HT, SP, ST, LR, GB, KI, BL) and four earlier-format pages (LU, SI, PC, TB).
- The third line retains the classical-table verification and the nalaayan provisional-source credit, and states that point-location charts are user-supplied with licensing review pending.

### States
- **Hover:** row wash at rgba(242, 240, 234, 0.038); other routes recede to 0.52; chevron reaches opacity 1 and shifts 2px. Hover recede is gated behind `@media (hover: hover)`.
- **Keyboard focus:** the full row takes the same wash plus one 2px Porcelain ring, inset 2px; the link-level ring is suppressed; other routes recede to 0.52; the chevron reaches opacity 1 and shifts 2px.
- **Focus recede:** any route focus recedes all non-focused routes to 0.52 regardless of hover.
- **Reduced motion:** `prefers-reduced-motion: reduce` removes the track draw and bend fade and removes the route/chevron transitions; the map renders static.

### Named Rules
**The One-Link Row Rule.** Each route is one link. The `::after` overlay stretches the hit target across the full row; never add a second interactive element inside a route.

**The Energize-and-Recede Rule.** Hover or keyboard focus energizes exactly one route and recedes the other eleven to 52% opacity; nothing else on the page changes.

**The Single-Ring Rule.** Keyboard focus draws one 2px porcelain ring around the whole route, inset 2px. The link-level ring is suppressed. Never stack a second outline on the badge or channel name.

## Do's and Don'ts

### Do:
- **Do** keep twelve routes and five stations in fixed Well → Spring → Stream → River → Sea order; the phase ink rotates, the station never does.
- **Do** use each phase as a pair: deep ink for track, tick, and bend; tint for badge and station phase word.
- **Do** keep Water at #3c6fbd with #93b8f0 tint; the lift from #2f5fa8 is an accessibility invariant.
- **Do** keep Metal porcelain at #dfd9cb deep and #f2f0ea tint; never gold, brass, or silver.
- **Do** keep the 56px desktop row, 52px mobile field, 230–288px terminus column, and 30px chevron column.
- **Do** keep every functional text size at or above the 11px floor; 11.5px for notes and Han meta, 16.5px/15.5px for channel names.
- **Do** keep one stretched link per route and the single full-row 2px focus ring with the link-level ring suppressed.
- **Do** keep the solid/hollow yin-yang grammar and the hard 45° lead-in; both must read at a glance.
- **Do** keep reduced motion static and gate hover recede behind `@media (hover: hover)`.
- **Do** retain the provisional-source credit, the licensing note, the classical-table verification, and the absence of per-point outbound links.
- **Do** keep the surface self-contained: embedded OFL subsets, inline SVG or CSS marks, no scripts, no rasters.

### Don't:
- **Don't** add cards, shadows, gradients, filled panels, or backdrop blur; the world is hairlines over midnight.
- **Don't** add rasters or external font/image requests to this surface.
- **Don't** drop functional text below 11px or shrink type to fit the map.
- **Don't** add a second focus ring or restyle the row focus as a badge ring.
- **Don't** mix a deep ink from one phase with a tint from another.
- **Don't** use gold, brass, or silver for Metal, or revert Water to #2f5fa8.
- **Don't** publish non-LU pages, remove the provisional-source credit, or imply that licensing is cleared.
- **Don't** add per-point outbound links.
- **Don't** substitute icon fonts or glyph characters for the chevron, ticks, or wordmark; use inline SVG or CSS.
- **Don't** add narrow-screen rules beyond the ≤374px quick-launcher rule; test the 480px rule at 390px.

## One scene, every screen (2026-11)

The system above was written for the launcher map. The app now reads as one place from the ring to a point:

- **The scene carries through.** The element chosen on the ring stays behind Channels, Points and each chart page, full height, blurred and dimmed. Panels over it are glass (a translucent midnight fill with a backdrop blur and a hairline), so the Hairline-Only rule still governs the map rows while panels that float over the scene may blur what is behind them.
- **The plate is the page.** A chart opens on its anatomy plate. Text about the channel is folded away until asked for, and the channel is summarised by one line drawn to scale.
- **Two pictures per point.** The channel map shows order and direction and is labelled “not to scale”; the location diagram shows where the point is. Location and cun text stay beside whichever is showing.
- **Thumb reach.** On phones the tabs are a dock at the bottom and a chart's details are a sheet that pulls up.
- **Motion still has an off switch.** Weather, parallax, the card turn and the zoom between views are all removed under reduced motion.
