import subprocess
import os

cards_dir = os.path.dirname(os.path.abspath(__file__))
# Check fonts path from collab-sans or yugal.one
fonts_dir = "/Users/yugal/Desktop/collab-sans/fonts/woff2"
if not os.path.exists(fonts_dir):
    fonts_dir = "/Users/yugal/Desktop/yugal.one/fonts/woff2"

font_face_css = f"""
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 100;
  src: url('{fonts_dir}/CollabSans-Thin.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 200;
  src: url('{fonts_dir}/CollabSans-ExtraLight.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 300;
  src: url('{fonts_dir}/CollabSans-Light.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 400;
  src: url('{fonts_dir}/CollabSans-Regular.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 500;
  src: url('{fonts_dir}/CollabSans-Medium.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 600;
  src: url('{fonts_dir}/CollabSans-SemiBold.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 700;
  src: url('{fonts_dir}/CollabSans-Bold.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 800;
  src: url('{fonts_dir}/CollabSans-ExtraBold.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-weight: 900;
  src: url('{fonts_dir}/CollabSans-Black.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-style: italic;
  font-weight: 400;
  src: url('{fonts_dir}/CollabSans-Italic.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Collab Sans';
  font-style: italic;
  font-weight: 700;
  src: url('{fonts_dir}/CollabSans-BoldItalic.woff2') format('woff2');
}}
"""

common_css = f"""
{font_face_css}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 1600px;
  height: 900px;
  background: #ffffff;
  color: #111111;
  font-family: 'Collab Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 85px 110px;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
.header {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}}
.header-meta {{
  font-size: 13.5px;
  font-weight: 500;
  color: #6e6e73;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}
.footer {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 15px;
  color: #6e6e73;
  font-weight: 400;
  letter-spacing: -0.01em;
}}
"""

# CARD 1: OVERVIEW / SPECIMEN
card1_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
{common_css}
.main {{
  display: flex;
  flex-direction: column;
  gap: 36px;
}}
.title {{
  font-size: 92px;
  font-weight: 400;
  letter-spacing: -0.03em;
  line-height: 1.1;
  color: #111111;
}}
.subhead {{
  font-size: 30px;
  font-weight: 400;
  color: #6e6e73;
  margin-top: 8px;
  letter-spacing: -0.015em;
  line-height: 1.4;
}}
.glyph-block {{
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 8px;
}}
.glyph-row {{
  font-size: 42px;
  line-height: 1.35;
}}
.glyph-row.caps {{
  font-weight: 500;
  letter-spacing: 0.08em;
  color: #111111;
}}
.glyph-row.lower {{
  font-weight: 400;
  letter-spacing: 0.06em;
  color: #2e2e2e;
}}
.glyph-row.numbers {{
  font-weight: 400;
  letter-spacing: 0.1em;
  color: #6e6e73;
}}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans  /  01 Overview</div>
  <div class="header-meta">SIL Open Font License 1.1</div>
</div>

<div class="main">
  <div>
    <h1 class="title">Collab Sans</h1>
    <p class="subhead">Inter's optical rigor, softened into warmth.</p>
  </div>
  
  <div class="glyph-block">
    <div class="glyph-row caps">ABCDEFGHIJKLMNOPQRSTUVWXYZ</div>
    <div class="glyph-row lower">abcdefghijklmnopqrstuvwxyz</div>
    <div class="glyph-row numbers">0123456789  &amp;  —  %  $  ( )  [ ]  /</div>
  </div>
</div>

<div class="footer">
  <div>18 Styles: 9 Weights (Thin to Black) + Matching Italics</div>
  <div>Derived from Inter by Rasmus Andersson</div>
</div>
</body>
</html>"""

# CARD 2: TERMINALS (Side-by-side comparison without boxes)
card2_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
{common_css}
.main {{
  display: flex;
  flex-direction: column;
  gap: 40px;
}}
.section-title {{
  font-size: 42px;
  font-weight: 400;
  letter-spacing: -0.025em;
  color: #111111;
}}
.comparison-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 88px;
}}
.col-label {{
  font-size: 13.5px;
  font-weight: 500;
  color: #6e6e73;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 24px;
}}
.col-glyphs {{
  font-size: 136px;
  line-height: 1;
  letter-spacing: 8px;
  margin-bottom: 24px;
}}
.col-desc {{
  font-size: 19px;
  line-height: 1.6;
  color: #6e6e73;
  max-width: 540px;
}}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans  /  02 Terminals</div>
  <div class="header-meta">Optical Geometry</div>
</div>

<div class="main">
  <div class="section-title">Terminal Geometry</div>

  <div class="comparison-grid">
    <div>
      <div class="col-label">Inter (Original)</div>
      <div class="col-glyphs" style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; font-weight: 700; color: #6e6e73;">
        C r t &amp;
      </div>
      <div class="col-desc">
        Sharp 90° cut terminals designed for screen micro-legibility and mathematical precision.
      </div>
    </div>

    <div>
      <div class="col-label" style="color: #111111;">Collab Sans (Derivative)</div>
      <div class="col-glyphs" style="font-weight: 700; color: #111111;">
        C r t &amp;
      </div>
      <div class="col-desc" style="color: #2e2e2e;">
        Tangent-continuous circular caps that introduce organic warmth without optical distortion.
      </div>
    </div>
  </div>
</div>

<div class="footer">
  <div>Maintains identical metrics, kerning pairs, and layout tables</div>
  <div>Zero compromise on micro-typography</div>
</div>
</body>
</html>"""

# CARD 3: WEIGHTS (Pure Typographic Cascade)
card3_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
{common_css}
.main {{
  display: flex;
  flex-direction: column;
  gap: 16px;
}}
.section-title {{
  font-size: 42px;
  font-weight: 400;
  margin: 0 0 10px 0;
  letter-spacing: -0.025em;
  color: #111111;
}}
.weight-stack {{
  display: flex;
  flex-direction: column;
  gap: 11px;
}}
.row {{
  display: flex;
  align-items: baseline;
  gap: 36px;
}}
.w-num {{
  width: 50px;
  font-size: 14px;
  font-weight: 500;
  color: #999999;
  font-variant-numeric: tabular-nums;
}}
.w-text {{
  font-size: 27px;
  color: #111111;
  letter-spacing: -0.015em;
}}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans  /  03 Weights</div>
  <div class="header-meta">100 to 900</div>
</div>

<div class="main">
  <div class="section-title">The Weight Progression</div>

  <div class="weight-stack">
    <div class="row">
      <div class="w-num">100</div>
      <div class="w-text" style="font-weight: 100;">Every complex system began as a simple system that worked.</div>
    </div>
    <div class="row">
      <div class="w-num">200</div>
      <div class="w-text" style="font-weight: 200;">Minimalism is not a design preference—it is a way of living.</div>
    </div>
    <div class="row">
      <div class="w-num">300</div>
      <div class="w-text" style="font-weight: 300;">Balancing clean, accessible design with enterprise governance.</div>
    </div>
    <div class="row">
      <div class="w-num">400</div>
      <div class="w-text" style="font-weight: 400;">Clarity over noise, intent over decoration, function over abstraction.</div>
    </div>
    <div class="row">
      <div class="w-num">500</div>
      <div class="w-text" style="font-weight: 500;">Mathematical precision softened into approachable warmth.</div>
    </div>
    <div class="row">
      <div class="w-num">600</div>
      <div class="w-text" style="font-weight: 600;">Tangent-continuous terminals with preserved optical ink-traps.</div>
    </div>
    <div class="row">
      <div class="w-num">700</div>
      <div class="w-text" style="font-weight: 700;">Sub-contour adaptive scaling across small symbols and punctuation.</div>
    </div>
    <div class="row">
      <div class="w-num">800</div>
      <div class="w-text" style="font-weight: 800;">Derived from Inter, engineered with Antigravity.</div>
    </div>
    <div class="row">
      <div class="w-num">900</div>
      <div class="w-text" style="font-weight: 900;">Collab Sans — Free for personal and commercial use.</div>
    </div>
  </div>
</div>

<div class="footer">
  <div>18 Styles total (9 Upright + 9 True Italics)</div>
  <div>TTF • OTF • WOFF2</div>
</div>
</body>
</html>"""

# CARD 4: IN USE (Clean Interface Hierarchy - No Fake Dashboard Boxes)
card4_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
{common_css}
.main {{
  display: flex;
  flex-direction: column;
  gap: 36px;
}}
.section-title {{
  font-size: 42px;
  font-weight: 400;
  letter-spacing: -0.025em;
  color: #111111;
}}
.metrics-row {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  padding-bottom: 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}}
.metric-label {{
  font-size: 13px;
  font-weight: 500;
  color: #6e6e73;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 10px;
}}
.metric-value {{
  font-size: 52px;
  font-weight: 600;
  color: #111111;
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}}
.metric-sub {{
  font-size: 15px;
  color: #6e6e73;
  margin-top: 6px;
}}
.data-table {{
  display: flex;
  flex-direction: column;
  gap: 16px;
}}
.table-head {{
  display: grid;
  grid-template-columns: 180px 1fr 200px 160px;
  font-size: 12.5px;
  font-weight: 500;
  color: #999999;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}}
.table-row {{
  display: grid;
  grid-template-columns: 180px 1fr 200px 160px;
  font-size: 19px;
  color: #2e2e2e;
  align-items: baseline;
  padding: 4px 0;
}}
.table-row .id {{
  font-weight: 500;
  color: #111111;
  font-variant-numeric: tabular-nums;
}}
.table-row .desc {{
  color: #2e2e2e;
}}
.table-row .date {{
  color: #6e6e73;
  font-size: 16px;
  font-variant-numeric: tabular-nums;
}}
.table-row .val {{
  font-weight: 600;
  color: #111111;
  font-variant-numeric: tabular-nums;
  text-align: right;
}}
</style>
</head>
<body>
<div class="header">
  <div class="header-meta">Collab Sans  /  04 In Use</div>
  <div class="header-meta">Data &amp; Interface Legibility</div>
</div>

<div class="main">
  <div class="section-title">Interface Typographic Hierarchy</div>

  <div class="metrics-row">
    <div>
      <div class="metric-label">Monthly Processed</div>
      <div class="metric-value">$482,950.00</div>
      <div class="metric-sub">+14.2% monthly operational flow</div>
    </div>
    <div>
      <div class="metric-label">Active Workflows</div>
      <div class="metric-value">1,248</div>
      <div class="metric-sub">99.98% runtime consistency</div>
    </div>
    <div>
      <div class="metric-label">Automated Records</div>
      <div class="metric-value">84,392</div>
      <div class="metric-sub">Zero structural dropped frames</div>
    </div>
  </div>

  <div class="data-table">
    <div class="table-head">
      <div>Record ID</div>
      <div>Operational Workflow</div>
      <div>Timestamp</div>
      <div style="text-align: right;">Amount</div>
    </div>
    <div class="table-row">
      <div class="id">#ORD-90241</div>
      <div class="desc">Inventory Ledger Allocation</div>
      <div class="date">2026-11-04 12:45</div>
      <div class="val">$14,250.00</div>
    </div>
    <div class="table-row">
      <div class="id">#BOM-48192</div>
      <div class="desc">Multi-Tiered Assembly Run</div>
      <div class="date">2026-11-04 12:30</div>
      <div class="val">$8,940.50</div>
    </div>
  </div>
</div>

<div class="footer">
  <div>Tabular figures (`tnum`) preserve numerical column alignment</div>
  <div>Optimized for data dashboards and financial systems</div>
</div>
</body>
</html>"""

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
    with open(html_path, "w") as f:
        f.write(content)
    
    cmd = [
        chrome,
        '--headless=new',
        '--disable-gpu',
        f'--screenshot={png_path}',
        '--window-size=1600,900',
        '--hide-scrollbars',
        f'file://{html_path}'
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Generated Consistent Minimal {png_name}: {os.path.getsize(png_path)} bytes")
