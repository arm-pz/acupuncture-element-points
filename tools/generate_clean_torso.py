import os

def generate_clean_chart():
    # Rib cage curves (smooth anatomical bezier paths)
    ribs_svg = """
    <!-- SKELETAL SYSTEM: STERNUM, CLAVICLES & RIB CAGE (Classic TCM anatomical styling) -->
    <g id="skeletal" style="fill:none;stroke:#9a9a9a;stroke-width:1.5px;stroke-linecap:round;stroke-linejoin:round;">
      <!-- Sternum: Manubrium & Gladiolus -->
      <path d="M 284,295 L 284,464 Q 288,468 292,464 L 292,295 Z" fill="#fff" stroke="#777" stroke-width="1.6"/>
      <!-- Sternal Angle (Angle of Louis at level of 2nd rib, CV20) -->
      <line x1="284" y1="332" x2="292" y2="332" stroke="#777" stroke-width="1.4"/>
      <!-- Xiphoid process (CV15 landmark) -->
      <path d="M 285,465 L 285,482 Q 288,487 291,482 L 291,465 Z" fill="#fff" stroke="#777" stroke-width="1.4"/>

      <!-- Clavicles (Collar bones meeting at Suprasternal Notch CV22) -->
      <path d="M 284,295 C 255,293 215,296 160,326" stroke="#666" stroke-width="2.2"/>
      <path d="M 292,295 C 321,293 361,296 416,326" stroke="#666" stroke-width="2.2"/>

      <!-- RIB CAGE ON ANATOMICAL RIGHT (Viewer's Left, matching reference diagram) -->
      <!-- Rib 1 -->
      <path d="M 284,302 C 260,304 225,310 195,332"/>
      <!-- Rib 2 (from Sternal Angle) -->
      <path d="M 284,332 C 252,336 212,342 180,362"/>
      <!-- Rib 3 -->
      <path d="M 284,360 C 248,366 200,375 168,400"/>
      <!-- Rib 4 (level with Nipple & CV17 Danzhong) -->
      <path d="M 284,388 C 244,396 192,408 158,438"/>
      <!-- Rib 5 -->
      <path d="M 284,414 C 240,424 186,440 152,476"/>
      <!-- Rib 6 -->
      <path d="M 284,440 C 236,452 182,472 150,514"/>
      <!-- Rib 7 (True Rib into Xiphisternal junction) -->
      <path d="M 284,464 C 232,480 180,505 152,552"/>

      <!-- Costal Margin (Anterior Inverted-V Rib Arch) -->
      <path d="M 288,466 C 265,492 232,525 192,562 C 180,574 165,584 154,588" stroke="#555" stroke-width="2.2"/>
      <!-- Right Costal Margin (Viewer's Right, muscle contour) -->
      <path d="M 288,466 C 311,492 344,525 384,562" stroke="#aaa" stroke-width="1.4" stroke-dasharray="4 3"/>

      <!-- Ribs 8, 9, 10 (False Ribs merging into Costal Arch) -->
      <path d="M 270,488 C 235,502 195,528 160,576"/>
      <path d="M 252,508 C 225,524 195,548 168,596"/>
      <path d="M 235,528 C 215,544 195,568 178,612"/>

      <!-- Floating Ribs 11 & 12 (tips) -->
      <path d="M 190,598 C 182,608 180,622 184,632"/>
      <path d="M 194,625 C 190,634 190,642 194,650"/>

      <!-- Pectoralis Major muscle outlines (Chest) -->
      <path d="M 284,388 C 255,392 225,405 210,425" stroke="#bbb" stroke-width="1.2"/>
      <path d="M 292,388 C 321,392 351,405 366,425" stroke="#888" stroke-width="1.5"/>
      <!-- Nipple (CV17 level on right) -->
      <circle cx="360" cy="420" r="3.5" fill="#444" stroke="#fff" stroke-width="1"/>
    </g>
    """

    # Pure smooth body contour and fill
    body_svg = """
    <!-- BODY SILHOUETTE & CONTOUR OUTLINE (Clean vector lines matching other charts) -->
    <g id="body-contour">
      <!-- White anatomical underlay silhouette -->
      <path d="
        M 288,95
        C 324,95 342,120 342,156
        C 342,188 334,222 318,244
        C 310,254 300,258 288,258
        C 276,258 266,254 258,244
        C 242,222 234,188 234,156
        C 234,120 252,95 288,95 Z
        M 264,258
        C 256,270 250,282 244,295
        C 212,299 168,310 142,328
        C 118,348 106,385 104,432
        C 102,480 106,545 110,615
        C 114,685 120,755 130,815
        C 134,838 140,865 148,890
        C 152,902 158,906 164,898
        C 170,890 172,870 174,845
        C 176,820 172,770 166,710
        C 162,650 162,590 166,530
        C 170,475 178,430 190,395
        C 188,430 186,480 188,540
        C 190,600 196,652 204,705
        C 212,752 222,792 232,828
        L 238,855
        L 338,855
        L 344,828
        C 354,792 364,752 372,705
        C 380,652 386,600 388,540
        C 390,480 388,430 386,395
        C 398,430 406,475 410,530
        C 414,590 414,650 410,710
        C 404,770 400,820 402,845
        C 404,870 406,890 412,898
        C 418,906 424,902 428,890
        C 436,865 442,838 446,815
        C 456,755 462,685 466,615
        C 470,545 474,480 472,432
        C 470,385 458,348 434,328
        C 408,310 364,299 332,295
        C 326,282 320,270 312,258 Z
      " fill="#ffffff" stroke="none"/>

      <!-- Head & Chin line -->
      <path d="M 248,138 C 244,175 248,215 258,238 C 266,252 276,256 288,256 C 300,256 310,252 318,238 C 328,215 332,175 328,138" fill="none" stroke="#222" stroke-width="2.2" stroke-linecap="round"/>
      <!-- Hair contour -->
      <path d="M 248,138 C 242,112 258,95 288,95 C 318,95 334,112 328,138 C 322,125 308,120 288,120 C 268,120 254,125 248,138 Z" fill="#222" stroke="#111" stroke-width="1.5"/>

      <!-- Neck & Trapezius sweeps -->
      <path d="M 264,256 C 258,272 252,284 244,295 Q 195,302 142,328" fill="none" stroke="#222" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M 312,256 C 318,272 324,284 332,295 Q 381,302 434,328" fill="none" stroke="#222" stroke-width="2.4" stroke-linecap="round"/>

      <!-- Arms and Flanks Contour Lines (Dark outer ink) -->
      <!-- Left outer arm -->
      <path d="M 142,328 C 120,346 106,380 104,432 C 102,480 106,545 110,615 C 114,685 120,755 130,815 C 134,838 140,865 148,890 C 152,902 158,906 164,898 C 170,890 172,870 174,845 C 176,820 172,770 166,710 C 162,650 162,590 166,530 C 170,475 178,430 190,395" fill="none" stroke="#222" stroke-width="2.4" stroke-linecap="round"/>
      <!-- Right outer arm -->
      <path d="M 434,328 C 456,346 470,380 472,432 C 474,480 470,545 466,615 C 462,685 456,755 446,815 C 442,838 436,865 428,890 C 424,902 418,906 412,898 C 406,890 404,870 402,845 C 400,820 404,770 410,710 C 414,650 414,590 410,530 C 406,475 398,430 386,395" fill="none" stroke="#222" stroke-width="2.4" stroke-linecap="round"/>

      <!-- Torso Flanks (Curving inward at waist, outward at hips) -->
      <path d="M 190,395 C 188,430 186,480 188,540 C 190,600 196,652 204,705 C 212,752 222,792 232,828 L 238,855" fill="none" stroke="#222" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M 386,395 C 388,430 390,480 388,540 C 386,600 380,652 372,705 C 364,752 354,792 344,828 L 338,855" fill="none" stroke="#222" stroke-width="2.4" stroke-linecap="round"/>

      <!-- Navel Landmark (CV8 Shenque, 0 cun reference at 632y) -->
      <ellipse cx="288" cy="632" rx="5.5" ry="4.5" fill="#e6d5b8" stroke="#333" stroke-width="1.8"/>
      <path d="M 284,632 Q 288,635 292,632" fill="none" stroke="#222" stroke-width="1.8"/>

      <!-- Inguinal Fold & Pubic Arch (CV2 level at 753y) -->
      <path d="M 216,732 Q 248,746 283,753" fill="none" stroke="#666" stroke-width="1.6"/>
      <path d="M 360,732 Q 328,746 293,753" fill="none" stroke="#666" stroke-width="1.6"/>
      <path d="M 282,753 L 294,753" stroke="#222" stroke-width="2.4"/>
      <!-- Lower pelvic base -->
      <path d="M 232,828 L 288,850 L 344,828" fill="none" stroke="#444" stroke-width="1.6"/>
    </g>
    """

    # Interactive elements, channel line, cun scale, and callouts
    interactive_svg = """
    <!-- CONCEPTION VESSEL ENERGETIC MIDLINE (Channel line #channel) -->
    <path id="channel" d="
      M 288,820
      L 288,753
      L 288,692
      L 288,668
      L 288,656
      L 288,632
      L 288,611
      L 288,527
      L 288,464
      L 288,388
      L 288,295
      L 288,256
    " style="fill:none;stroke:#ff8956;stroke-width:4px;stroke-linecap:round;stroke-linejoin:round;"/>

    <!-- PROPORTIONAL CUN RULER (Classical anatomical distance ticks) -->
    <g id="cun-scale" opacity="0.88">
      <!-- Upper abdomen ruler: 0 to 8 cun -->
      <line x1="324" y1="632" x2="324" y2="464" stroke="#8c6d48" stroke-width="1.2" stroke-dasharray="2.5 2"/>
      <line x1="320" y1="632" x2="328" y2="632" stroke="#8c6d48" stroke-width="1.5"/>
      <text x="332" y="635" font-family="'IBM Plex Mono',monospace" font-size="10" fill="#7a5c3a" font-weight="600">0 (Navel)</text>
      <!-- 1 cun tick (CV9) -->
      <line x1="321" y1="611" x2="327" y2="611" stroke="#8c6d48" stroke-width="1.2"/>
      <text x="332" y="614" font-family="'IBM Plex Mono',monospace" font-size="9" fill="#9c7a52">1 cun</text>
      <!-- 5 cun tick (CV13) -->
      <line x1="320" y1="527" x2="328" y2="527" stroke="#8c6d48" stroke-width="1.5"/>
      <text x="332" y="530" font-family="'IBM Plex Mono',monospace" font-size="10" fill="#7a5c3a" font-weight="600">5 cun</text>
      <!-- 8 cun tick (Xiphoid) -->
      <line x1="320" y1="464" x2="328" y2="464" stroke="#8c6d48" stroke-width="1.5"/>
      <text x="332" y="467" font-family="'IBM Plex Mono',monospace" font-size="10" fill="#7a5c3a" font-weight="600">8 cun (Xiphoid)</text>

      <!-- Lower abdomen ruler: 0 to 5 cun -->
      <line x1="324" y1="632" x2="324" y2="753" stroke="#8c6d48" stroke-width="1.2" stroke-dasharray="2.5 2"/>
      <!-- 1 cun tick (CV7) -->
      <line x1="321" y1="656" x2="327" y2="656" stroke="#8c6d48" stroke-width="1.2"/>
      <!-- 1.5 cun tick (CV6) -->
      <line x1="321" y1="668" x2="327" y2="668" stroke="#8c6d48" stroke-width="1.2"/>
      <!-- 2.5 cun tick (CV5) -->
      <line x1="320" y1="692" x2="328" y2="692" stroke="#8c6d48" stroke-width="1.5"/>
      <text x="332" y="695" font-family="'IBM Plex Mono',monospace" font-size="10" fill="#7a5c3a" font-weight="600">2.5 cun</text>
      <!-- 5 cun tick (Pubis) -->
      <line x1="320" y1="753" x2="328" y2="753" stroke="#8c6d48" stroke-width="1.5"/>
      <text x="332" y="756" font-family="'IBM Plex Mono',monospace" font-size="10" fill="#7a5c3a" font-weight="600">5 cun (Pubis)</text>
    </g>

    <!-- CALLOUT LEADER LINES (Connecting points to clean typography labels on the right) -->
    <!-- Pattern exactly matching st-meridian-chart and lung-meridian-chart -->
    <g id="callout-lines" style="fill:none;stroke:#555;stroke-width:1.2px;">
      <!-- CV13 (527y) -> right label at 527y -->
      <path d="M 288,527 L 430,527"/>
      <!-- CV9 (611y) -> right label at 611y -->
      <path d="M 288,611 L 430,611"/>
      <!-- CV7 (656y) -> right label at 656y -->
      <path d="M 288,656 L 430,656"/>
      <!-- CV6 (668y) -> right label angled down to 696y -->
      <path d="M 288,668 L 380,668 L 400,696 L 430,696"/>
      <!-- CV5 (692y) -> right label angled down to 736y -->
      <path d="M 288,692 L 360,692 L 390,736 L 430,736"/>
    </g>

    <!-- ANIMATED PULSE RINGS -->
    <g id="rings">
      <circle class="ring" id="ring-p13" cx="288.0" cy="527.0" r="14" stroke="var(--earth)"/>
      <circle class="ring" id="ring-p9" cx="288.0" cy="611.0" r="14" stroke="var(--metal)"/>
      <circle class="ring" id="ring-p7" cx="288.0" cy="656.0" r="14" stroke="var(--wood)"/>
      <circle class="ring" id="ring-p6" cx="288.0" cy="668.0" r="14" stroke="var(--water)"/>
      <circle class="ring" id="ring-p5" cx="288.0" cy="692.0" r="14" stroke="var(--fire)"/>
    </g>

    <!-- INTERACTIVE 5 ELEMENT POINTS (#points) -->
    <g id="points">
      <circle id="p13" cx="288.0" cy="527.0" r="6.75"/>
      <circle id="p9" cx="288.0" cy="611.0" r="6.75"/>
      <circle id="p7" cx="288.0" cy="656.0" r="6.75"/>
      <circle id="p6" cx="288.0" cy="668.0" r="6.75"/>
      <circle id="p5" cx="288.0" cy="692.0" r="6.75"/>
    </g>

    <!-- ACCESSIBILITY HIT TARGETS -->
    <circle class="hit" id="hit-p13" cx="288.0" cy="527.0" r="22" tabindex="0" role="button" aria-label="CV13 Shangwan (Earth Point)"/>
    <circle class="hit" id="hit-p9" cx="288.0" cy="611.0" r="22" tabindex="0" role="button" aria-label="CV9 Shuifen (Air / Metal Point)"/>
    <circle class="hit" id="hit-p7" cx="288.0" cy="656.0" r="22" tabindex="0" role="button" aria-label="CV7 Yinjiao (Wood Point)"/>
    <circle class="hit" id="hit-p6" cx="288.0" cy="668.0" r="22" tabindex="0" role="button" aria-label="CV6 Qihai (Water Point)"/>
    <circle class="hit" id="hit-p5" cx="288.0" cy="692.0" r="22" tabindex="0" role="button" aria-label="CV5 Shimen (Fire Point)"/>

    <!-- CLEAN TYPOGRAPHIC LABELS (Identical to other 12 meridian charts) -->
    <!-- font-size: 28px, clean point codes, ample spacing, no overlapping -->
    <g id="text-labels" style="font-family:ArialMT,Arial,sans-serif;font-size:28px;font-weight:700;fill:#555;cursor:pointer;">
      <text text-anchor="start" x="438" y="537" data-id="p13">CV13</text>
      <text text-anchor="start" x="438" y="621" data-id="p9">CV9</text>
      <text text-anchor="start" x="438" y="666" data-id="p7">CV7</text>
      <text text-anchor="start" x="438" y="706" data-id="p6">CV6</text>
      <text text-anchor="start" x="438" y="746" data-id="p5">CV5</text>
    </g>
    """

    full_svg = f"""<svg viewBox="0 0 576 1024" role="group" aria-label="Conception Vessel chart showing its 5 Element Points" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Warm anatomical body shadow -->
    <linearGradient id="bodyShade" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3d2d1d" stop-opacity="0.08"/>
      <stop offset="25%" stop-color="#3d2d1d" stop-opacity="0.02"/>
      <stop offset="50%" stop-color="#3d2d1d" stop-opacity="0.0"/>
      <stop offset="75%" stop-color="#3d2d1d" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#3d2d1d" stop-opacity="0.08"/>
    </linearGradient>
  </defs>

  <g>
    {body_svg}
    {ribs_svg}
    {interactive_svg}
  </g>
</svg>"""

    return full_svg

if __name__ == '__main__':
    svg = generate_clean_chart()
    with open('tools/clean_torso_perfect.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Wrote tools/clean_torso_perfect.svg successfully! Size:", len(svg))
