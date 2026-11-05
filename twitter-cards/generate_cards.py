import os
import subprocess

cards_dir = os.path.dirname(os.path.abspath(__file__))

# Path to styles.css
css_path = os.path.join(cards_dir, "styles.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# CARD 1: OVERVIEW / SPECIMEN
card1_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Collab Sans — Card 01 Overview</title>
<link rel="stylesheet" href="styles.css">
<style>
{css_content}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans &nbsp;/&nbsp; 01 Overview</div>
  <div class="header-meta">SIL Open Font License 1.1</div>
</div>

<div class="main">
  <div>
    <h1 class="card-title hero">Collab Sans</h1>
    <p class="card-subhead">Inter's optical rigor, softened into warmth.</p>
  </div>

  <div class="glyph-block">
    <div class="glyph-row caps">ABCDEFGHIJKLMNOPQRSTUVWXYZ</div>
    <div class="glyph-row lower">abcdefghijklmnopqrstuvwxyz</div>
    <div class="glyph-row numbers">0123456789 &amp; — % $ ( ) [ ] /</div>
  </div>
</div>

<div class="footer">
  <div>18 Styles: 9 Weights (Thin to Black) + Matching Italics</div>
  <div>Derived from Inter by Rasmus Andersson</div>
</div>
</body>
</html>
"""

# CARD 2: TERMINAL GEOMETRY (Comparison)
card2_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Collab Sans — Card 02 Terminals</title>
<link rel="stylesheet" href="styles.css">
<style>
{css_content}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans &nbsp;/&nbsp; 02 Terminals</div>
  <div class="header-meta">Optical Geometry</div>
</div>

<div class="main">
  <div class="card-title">Terminal Geometry</div>

  <div class="comparison-grid">
    <div class="comparison-col">
      <div class="col-header">Inter (Original)</div>
      <div class="col-sample inter-sample">C r t &amp;</div>
      <p class="col-note">Sharp 90° cut terminals designed for screen micro-legibility and mathematical precision.</p>
    </div>

    <div class="comparison-col">
      <div class="col-header active">Collab Sans (Derivative)</div>
      <div class="col-sample collab-sample">C r t &amp;</div>
      <p class="col-note active">Tangent-continuous circular caps that introduce organic warmth without optical distortion.</p>
    </div>
  </div>
</div>

<div class="footer">
  <div>Maintains identical metrics, kerning pairs, and layout tables</div>
  <div>Zero compromise on micro-typography</div>
</div>
</body>
</html>
"""

# CARD 3: WEIGHT SPECTRUM (Aligned with Live Website Copy)
card3_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Collab Sans — Card 03 Weights</title>
<link rel="stylesheet" href="styles.css">
<style>
{css_content}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans &nbsp;/&nbsp; 03 Weights</div>
  <div class="header-meta">100 to 900</div>
</div>

<div class="main">
  <div class="card-title">The Weight Progression</div>

  <div class="weight-stack">
    <div class="weight-row">
      <div class="weight-num">100</div>
      <div class="weight-sample" style="font-weight: 100;">The lightest whisper of form, maintaining optical clarity.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">200</div>
      <div class="weight-sample" style="font-weight: 200;">Delicate structure preserved across large display sizes.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">300</div>
      <div class="weight-sample" style="font-weight: 300;">Clean and gentle rhythm for relaxed reading measures.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">400</div>
      <div class="weight-sample" style="font-weight: 400;">The optical workhorse: balanced UI and editorial prose.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">500</div>
      <div class="weight-sample" style="font-weight: 500;">Mathematical precision softened into approachable warmth.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">600</div>
      <div class="weight-sample" style="font-weight: 600;">Tangent-continuous terminals with preserved optical ink-traps.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">700</div>
      <div class="weight-sample" style="font-weight: 700;">Sub-contour adaptive scaling across small symbols and punctuation.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">800</div>
      <div class="weight-sample" style="font-weight: 800;">Derived from Inter, engineered with Antigravity.</div>
    </div>
    <div class="weight-row">
      <div class="weight-num">900</div>
      <div class="weight-sample" style="font-weight: 900;">Solid impact with rounded warmth for identity and posters.</div>
    </div>
  </div>
</div>

<div class="footer">
  <div>18 Styles total (9 Upright + 9 Matching Italics)</div>
  <div>TTF • OTF • WOFF2 • SIL Open Font License 1.1</div>
</div>
</body>
</html>
"""

# CARD 4: INTERFACE TYPOGRAPHIC HIERARCHY
card4_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Collab Sans — Card 04 In Use</title>
<link rel="stylesheet" href="styles.css">
<style>
{css_content}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans &nbsp;/&nbsp; 04 In Use</div>
  <div class="header-meta">Data &amp; Interface Legibility</div>
</div>

<div class="main">
  <div class="card-title">Interface Typographic Hierarchy</div>

  <div class="ui-metrics-row">
    <div>
      <div class="metric-label">Monthly Processed</div>
      <div class="metric-val">$482,950.00</div>
      <div class="metric-sub">+14.2% monthly operational flow</div>
    </div>
    <div>
      <div class="metric-label">Active Workflows</div>
      <div class="metric-val">1,248</div>
      <div class="metric-sub">99.98% runtime consistency</div>
    </div>
    <div>
      <div class="metric-label">Automated Records</div>
      <div class="metric-val">84,392</div>
      <div class="metric-sub">Zero structural dropped frames</div>
    </div>
  </div>

  <div class="ui-table-wrap">
    <div class="ui-table">
      <div class="ui-table-head">
        <div>Record ID</div>
        <div>Operational Workflow</div>
        <div>Timestamp</div>
        <div class="num-col">Amount</div>
      </div>
      <div class="ui-table-row">
        <div class="row-id">#ORD-90241</div>
        <div class="row-desc">Inventory Ledger Allocation</div>
        <div class="row-date">2026-11-04 12:45</div>
        <div class="row-val num-col">$14,250.00</div>
      </div>
      <div class="ui-table-row">
        <div class="row-id">#BOM-48192</div>
        <div class="row-desc">Multi-Tiered Assembly Run</div>
        <div class="row-date">2026-11-04 12:30</div>
        <div class="row-val num-col">$8,940.50</div>
      </div>
    </div>
  </div>
</div>

<div class="footer">
  <div>Tabular figures (<code class="inline-code">tnum</code>) preserve vertical column alignment</div>
  <div>Engineered for enterprise dashboards and financial systems</div>
</div>
</body>
</html>
"""

files = [
    ("card1.html", card1_html, "card-1-hero.png"),
    ("card2.html", card2_html, "card-2-comparison.png"),
    ("card3.html", card3_html, "card-3-weights.png"),
    ("card4.html", card4_html, "card-4-ui.png")
]

chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

for html_name, content, png_name in files:
    html_path = os.path.join(cards_dir, html_name)
    png_path = os.path.join(cards_dir, png_name)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    cmd = [
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--allow-file-access-from-files',
        f'--screenshot={png_path}',
        '--window-size=1600,900',
        '--hide-scrollbars',
        f'file://{html_path}'
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Generated Aligned Card: {png_name} ({os.path.getsize(png_path)} bytes)")
