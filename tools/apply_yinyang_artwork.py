import re, json

def build_svg():
    with open('tools/torso_yinyang_vector.svg', 'r', encoding='utf-8') as f:
        svg_raw = f.read()

    paths = re.findall(r'<path[^>]+/>', svg_raw)
    paths_str = "\n    ".join(paths)

    svg = f"""<svg viewBox="0 0 576 1024" role="group" aria-label="Conception Vessel chart showing its 5 Element Points" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Subtle drop shadow for interactive elements -->
    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#000" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- ANATOMICAL VECTOR ARTWORK (Traced from Reference Diagram) -->
  <g id="torso-art" transform="translate(66, 50) scale(1.48)" style="fill:#1a1d2e; opacity:0.92;">
    {paths_str}
  </g>

  <!-- Midline Meridian Pathway (CV / Ren Mai) -->
  <path id="channel" d="M288 267 L288 805" style="fill:none; stroke:#0284c7; stroke-width:3.5px; stroke-linecap:round; stroke-linejoin:round;"/>

  <!-- Proportional Anatomical Landmarks -->
  <!-- Landmark: CV16 Sternocostal Angle / Xiphisternal Joint (8 cun above navel) -->
  <g id="landmark-xiphoid">
    <line x1="175" y1="493" x2="280" y2="493" stroke="#64748b" stroke-dasharray="3 3" stroke-width="1.2"/>
    <text x="165" y="497" font-family="'IBM Plex Mono', monospace" font-size="11.5" font-weight="600" fill="#475569" text-anchor="end">CV16 · Xiphisternal (8 cun)</text>
  </g>

  <!-- Landmark: CV8 Navel (0 cun origin reference) -->
  <g id="landmark-navel">
    <line x1="175" y1="691.6" x2="280" y2="691.6" stroke="#64748b" stroke-dasharray="3 3" stroke-width="1.2"/>
    <text x="165" y="695.5" font-family="'IBM Plex Mono', monospace" font-size="11.5" font-weight="600" fill="#475569" text-anchor="end">CV8 · Navel (0 cun)</text>
    <circle cx="288" cy="691.6" r="4.5" fill="#0284c7" stroke="#faf6ee" stroke-width="1.5"/>
  </g>

  <!-- Landmark: CV2 Pubic Crest / Symphysis (5 cun below navel) -->
  <g id="landmark-pubic">
    <line x1="175" y1="805" x2="280" y2="805" stroke="#64748b" stroke-dasharray="3 3" stroke-width="1.2"/>
    <text x="165" y="809" font-family="'IBM Plex Mono', monospace" font-size="11.5" font-weight="600" fill="#475569" text-anchor="end">CV2 · Pubic Crest (5 cun)</text>
  </g>

  <!-- Callout Leader Lines (Connecting points to typographic labels) -->
  <g id="callout-lines" style="fill:none; stroke:#475569; stroke-width:1.2px;">
    <!-- CV13 -->
    <path d="M288 586.5 L400 586.5"/>
    <!-- CV9 -->
    <path d="M288 672.3 L400 672.3"/>
    <!-- CV7 -->
    <path d="M288 712.3 L400 712.3"/>
    <!-- CV6 -->
    <path d="M288 725.6 L340 725.6 L355 750 L400 750"/>
    <!-- CV5 -->
    <path d="M288 738.9 L330 738.9 L350 782 L400 782"/>
  </g>

  <!-- Animated Pulse Rings (Activated on point selection) -->
  <g id="rings">
    <circle class="ring" id="ring-p13" cx="288" cy="586.5" r="14" stroke="var(--earth)"/>
    <circle class="ring" id="ring-p9" cx="288" cy="672.3" r="14" stroke="var(--metal)"/>
    <circle class="ring" id="ring-p7" cx="288" cy="712.3" r="14" stroke="var(--wood)"/>
    <circle class="ring" id="ring-p6" cx="288" cy="725.6" r="14" stroke="var(--water)"/>
    <circle class="ring" id="ring-p5" cx="288" cy="738.9" r="14" stroke="var(--fire)"/>
  </g>

  <!-- Interactive Point Circles -->
  <g id="points">
    <circle id="p13" cx="288" cy="586.5" r="7"/>
    <circle id="p9" cx="288" cy="672.3" r="7"/>
    <circle id="p7" cx="288" cy="712.3" r="7"/>
    <circle id="p6" cx="288" cy="725.6" r="7"/>
    <circle id="p5" cx="288" cy="738.9" r="7"/>
  </g>

  <!-- Invisible Hit Targets (For precise cursor & accessibility click/tap/hover) -->
  <circle class="hit" id="hit-p13" cx="288" cy="586.5" r="20" tabindex="0" role="button" aria-label="CV13 Shangwan (Earth Point · 5 cun above navel)"/>
  <circle class="hit" id="hit-p9" cx="288" cy="672.3" r="20" tabindex="0" role="button" aria-label="CV9 Shuifen (Air / Metal Point · 1 cun above navel)"/>
  <circle class="hit" id="hit-p7" cx="288" cy="712.3" r="20" tabindex="0" role="button" aria-label="CV7 Yinjiao (Wood Point · 1 cun below navel)"/>
  <circle class="hit" id="hit-p6" cx="288" cy="725.6" r="20" tabindex="0" role="button" aria-label="CV6 Qihai (Water Point · 1.5 cun below navel)"/>
  <circle class="hit" id="hit-p5" cx="288" cy="738.9" r="20" tabindex="0" role="button" aria-label="CV5 Shimen (Fire Point · 2.5 cun below navel)"/>

  <!-- Clean Typographic Labels (Matching other meridian charts) -->
  <g id="text-labels" style="font-family:'IBM Plex Mono',monospace; cursor:pointer;">
    <!-- CV13 Earth -->
    <text x="410" y="583" font-size="14" font-weight="600" fill="#854d0e" data-id="p13">CV13 · Earth
      <tspan x="410" dy="16" font-size="11" font-weight="400" fill="#64748b">上脘 · Shangwan (5 cun)</tspan>
    </text>

    <!-- CV9 Metal -->
    <text x="410" y="669" font-size="14" font-weight="600" fill="#334155" data-id="p9">CV9 · Air / Metal
      <tspan x="410" dy="16" font-size="11" font-weight="400" fill="#64748b">水分 · Shuifen (1 cun)</tspan>
    </text>

    <!-- CV7 Wood -->
    <text x="410" y="709" font-size="14" font-weight="600" fill="#15803d" data-id="p7">CV7 · Wood
      <tspan x="410" dy="16" font-size="11" font-weight="400" fill="#64748b">陰交 · Yinjiao (1 cun)</tspan>
    </text>

    <!-- CV6 Water -->
    <text x="410" y="747" font-size="14" font-weight="600" fill="#0284c7" data-id="p6">CV6 · Water
      <tspan x="410" dy="16" font-size="11" font-weight="400" fill="#64748b">氣海 · Qihai (1.5 cun)</tspan>
    </text>

    <!-- CV5 Fire -->
    <text x="410" y="779" font-size="14" font-weight="600" fill="#b91c1c" data-id="p5">CV5 · Fire
      <tspan x="410" dy="16" font-size="11" font-weight="400" fill="#64748b">石門 · Shimen (2.5 cun)</tspan>
    </text>
  </g>
</svg>"""
    return svg

def apply():
    new_svg = build_svg()
    
    with open('tools/create_cv_chart.py', 'r', encoding='utf-8') as f:
        code = f.read()

    # Replace SVG_TORSO_ARTWORK
    pattern = r'SVG_TORSO_ARTWORK = """.*?"""'
    replacement = 'SVG_TORSO_ARTWORK = """' + new_svg + '"""'
    code = re.sub(pattern, replacement, code, flags=re.DOTALL)

    with open('tools/create_cv_chart.py', 'w', encoding='utf-8') as f:
        f.write(code)

    print("Updated tools/create_cv_chart.py with clean YinYang vector artwork!")

if __name__ == '__main__':
    apply()
