#!/usr/bin/env python3
# =====================================================================
#  FSO marketing site - static generator  (FSO 2.0 / Reset Plan, Nov 2026)
#  Edit shared head/header/footer and page bodies here, then run:
#     python3 build.py
#  Emits plain, deployable .html files. British English. No dashes in copy.
# =====================================================================
import os, math, shutil

SITE = "https://www.fsoworld.com"
APP  = "https://app.fsoworld.com"
SRC  = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(SRC, "public")   # Netlify publish directory (built output)
VER  = "5"   # asset cache-busting version

def prep_public():
    """Create a clean public/ folder with assets and loose static files."""
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    for f in ["sitemap.xml", "robots.txt", "site.webmanifest", "_redirects", ".htaccess"]:
        p = os.path.join(SRC, f)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(OUT, f))

def logo(variant="mark-blue", cls="logo-mark", label="FSO Financially Smart Organisation"):
    dims={"mark-blue":(231,96),"mark-white":(229,96),"lockup-blue":(272,140),"lockup-white":(275,140)}
    w,h=dims[variant]
    return (f'<img class="{cls}" src="assets/img/fso-{variant}.png" alt="{label}" '
            f'width="{w}" height="{h}" decoding="async">')

NAV = [
    ("index.html", "Home"),
    ("about.html", "About", [
        ("about.html", "About FSO"),
        ("founder.html", "About the Founder"),
    ]),
    ("standard.html", "The Standard"),
    ("services.html", "Services"),
    ("certification.html", "Certification"),
    ("contact.html", "Contact"),
]

def head(title, desc, path, og="assets/img/og-cover.png"):
    canonical = SITE + "/" + (path if path != "index.html" else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>document.documentElement.classList.add('js');</script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QH2W6MQ33L"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-QH2W6MQ33L');
</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#FFFFFF">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FSO Financially Smart Organisation">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/{og}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css?v={VER}">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>"""

def header(active):
    links = ""
    for item in NAV:
        if len(item) == 3:
            href, label, children = item
            child_hrefs = [c[0] for c in children]
            is_act = (href == active) or (active in child_hrefs)
            cls = "nav-link active" if is_act else "nav-link"
            aria = ' aria-current="page"' if is_act else ""
            sub = ""
            for chref, clabel in children:
                cur = ' aria-current="page"' if chref == active else ""
                sub += f'<li><a class="nav-dd-link" href="{chref}"{cur}>{clabel}</a></li>'
            links += (f'<li class="nav-item has-dd">'
                      f'<a class="{cls}" href="{href}" aria-haspopup="true"{aria}>{label} '
                      f'<span class="dd-caret" aria-hidden="true">&#9662;</span></a>'
                      f'<ul class="nav-dd-menu">{sub}</ul></li>')
        else:
            href, label = item
            cls = "nav-link active" if href == active else "nav-link"
            aria = ' aria-current="page"' if href == active else ""
            links += f'<li><a class="{cls}" href="{href}"{aria}>{label}</a></li>'
    return f"""
<header class="site-header" id="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="FSO home">{logo()}</a>
    <nav aria-label="Primary navigation">
      <ul class="nav-links" id="nav-links">
        {links}
        <div class="nav-drawer-cta">
          <a class="btn btn-ghost" href="{APP}" rel="noopener">Login / FSO Portal</a>
          <button class="btn btn-primary" type="button" data-open-diagnostic>Know Your FSO Score</button>
        </div>
      </ul>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-ghost btn-portal" href="{APP}" rel="noopener">Login</a>
      <button class="btn btn-primary btn-certify" type="button" data-open-diagnostic>Know Your FSO Score</button>
      <button class="hamburger" id="hamburger" aria-label="Open menu" aria-controls="nav-links" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>"""

MODAL = """
<div class="modal-overlay" id="diagnostic-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-label="FSO Diagnostic">
  <div class="modal-box">
    <button class="modal-close" type="button" data-close-modal aria-label="Close diagnostic">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="5" y1="5" x2="19" y2="19"/><line x1="19" y1="5" x2="5" y2="19"/></svg>
    </button>
    <div id="diagnostic-modal-root"></div>
  </div>
</div>"""

def footer():
    return f"""
<footer class="site-footer">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        {logo("lockup-blue","footer-logo")}
        <p>An independent assessment, on evidence, of how well a business plans, controls, reports and protects its money, and a certificate for those who clear the line.</p>
        <p style="margin-top:12px;font-size:13px;color:var(--muted);">Issued by the FSO Council</p>
        <div class="footer-social">
          <a href="{APP}" rel="noopener" aria-label="FSO Portal"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></a>
          <a href="https://www.linkedin.com" rel="noopener" aria-label="LinkedIn"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14zM8.34 17V10.2H6.06V17h2.28zM7.2 9.24a1.32 1.32 0 1 0 0-2.64 1.32 1.32 0 0 0 0 2.64zM18 17v-3.73c0-1.99-.43-3.52-2.75-3.52-1.12 0-1.87.61-2.18 1.2h-.03v-1.02H10.9V17h2.28v-3.37c0-.89.17-1.75 1.27-1.75 1.08 0 1.1 1.01 1.1 1.81V17H18z"/></svg></a>
          <a href="mailto:connect@fsoworld.com" aria-label="Email FSO"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/></svg></a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="about.html">About FSO</a></li>
          <li><a href="founder.html">About the Founder</a></li>
          <li><a href="standard.html">The FSO Standard</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="certification.html">Certification</a></li>
          <li><a href="diagnostic.html">FSO Diagnostic</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Get started</h4>
        <ul>
          <li><a href="diagnostic.html">Know Your FSO Score</a></li>
          <li><a href="contact.html">Book a Discovery Call</a></li>
          <li><a href="certification.html">Apply for Certification</a></li>
          <li><a href="{APP}" rel="noopener">FSO Portal</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:connect@fsoworld.com">connect@fsoworld.com</a></li>
          <li><a href="tel:+919311646714">+91 93116 46714</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="{APP}" rel="noopener">Login</a></li>
        </ul>
      </div>
    </div>
    <p class="footer-disc">
      <strong style="color:var(--ink-blue);">Scope of certification.</strong>
      An FSO assessment evaluates the design, operation and effectiveness of an organisation's financial management system.
      It is not a statutory audit, a credit rating, a valuation or investment advice. FSO is not accredited by NABCB, QCI or any
      government body unless the certificate says so, and is not regulated by RBI or SEBI. Certification is of limited validity
      and reflects the assessment period only.
    </p>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> FSO Global Standards Private Limited. All rights reserved.</p>
      <div class="fb-links">
        <a href="index.html#privacy">Privacy Policy</a>
        <a href="index.html#terms">Terms of Use</a>
        <a href="{APP}" rel="noopener">Access Portal &#8599;</a>
      </div>
    </div>
  </div>
</footer>"""

SCRIPTS = f"""
<script src="assets/js/diagnostic.js?v={VER}" defer></script>
<script src="assets/js/main.js?v={VER}" defer></script>
</body>
</html>"""

def page(path, title, desc, body, active):
    html = head(title, desc, path) + header(active) + '\n<main id="main">\n' + body + '\n</main>\n' + footer() + MODAL + SCRIPTS
    with open(os.path.join(OUT, path), "w") as f:
        f.write(html)
    print("wrote", path, len(html), "bytes")

# =====================================================================
#  Inline icons (Tabler-style outline, FSO blue via currentColor)
# =====================================================================
def icon(name):
    P = {
      "cash":'<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
      "wc":'<path d="M21 12a9 9 0 1 1-9-9"/><polyline points="21 3 21 9 15 9"/>',
      "profit":'<path d="M3 3v18h18"/><path d="M19 9l-5 5-4-4-3 3"/>',
      "mis":'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 13v4M12 9v8M16 7v10"/>',
      "capital":'<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M7 8V6a5 5 0 0 1 10 0v2"/>',
      "gov":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
      "leader":'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
      "search":'<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
      "doc":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
      "shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
      "target":'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
      "users":'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13A4 4 0 0 1 16 11"/>',
      "chart":'<path d="M3 3v18h18"/><rect x="7" y="12" width="3" height="6"/><rect x="12" y="8" width="3" height="10"/><rect x="17" y="5" width="3" height="13"/>',
      "clock":'<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 16 14"/>',
      "phone":'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
      "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/>',
      "pin":'<path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
      "layers":'<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
      "award":'<circle cx="12" cy="8" r="6"/><path d="M8.2 13.9 7 22l5-3 5 3-1.2-8.1"/>',
      "book":'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
      "grow":'<path d="M23 6l-9.5 9.5-5-5L1 18"/><polyline points="17 6 23 6 23 12"/>',
      "bulb":'<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/>',
      "scale":'<path d="M12 3v18M7 21h10M5 7h14M7 7l-3 6a3 3 0 0 0 6 0zM17 7l-3 6a3 3 0 0 0 6 0z"/>',
      "refresh":'<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.5 9a9 9 0 0 1 14.9-3.4L23 10M1 14l4.6 4.4A9 9 0 0 0 20.5 15"/>',
      "check":'<path d="M20 6 9 17l-5-5"/>',
      "lock":'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

# =====================================================================
#  Four settled bands (Reset Plan, Nov 2026). No grades. No Elite.
# =====================================================================
BANDS_UI = [
  ("Financially Blind", "0 to 40", "var(--band-blind)", False),
  ("Reactive", "41 to 60", "var(--band-reactive)", False),
  ("Developing", "61 to 75", "var(--band-developing)", False),
  ("Certification ready", "76 and above", "var(--band-smart)", True),
]

def maturity_scale():
    rows = ""
    for name, rng, col, cert in BANDS_UI:
        tag = '<span class="ms-tag">The line</span>' if cert else ''
        rows += (f'<div class="ms-row{" is-line" if cert else ""}">'
                 f'<span class="ms-dot" style="background:{col};"></span>'
                 f'<span class="ms-name">{name}</span>'
                 f'<span class="ms-range">{rng}</span>{tag}</div>')
    return f"""
<div class="ms-card reveal" role="img" aria-label="The FSO maturity scale, from Financially Blind to Certification ready, with the certification line at 76.">
  <div class="ms-head">
    <span class="ms-kick">The FSO maturity scale</span>
    <span class="ms-sub">One score out of 100. One line to clear.</span>
  </div>
  {rows}
  <p class="ms-note">The Assessment score is private. Only a certificate says Financially Smart Organisation.</p>
</div>"""

MATURITY_CSS = """<style>
.ms-card{background:var(--canvas);border:1px solid var(--line);border-radius:var(--radius-panel);box-shadow:var(--shadow-lg);padding:26px 26px 20px;}
.ms-head{margin-bottom:16px;}
.ms-kick{display:block;font:700 12px var(--font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--fso);}
.ms-sub{display:block;margin-top:6px;font-family:var(--font-display);font-weight:800;font-size:19px;color:var(--ink-blue);letter-spacing:-.01em;}
.ms-row{display:flex;align-items:center;gap:12px;padding:12px 2px;border-top:1px solid var(--line);position:relative;}
.ms-row:first-of-type{border-top:0;}
.ms-dot{width:12px;height:12px;border-radius:50%;flex:none;}
.ms-name{font:600 15px var(--font-body);color:var(--ink-blue);flex:1;}
.ms-range{font-family:var(--font-display);font-weight:800;font-size:15px;color:var(--ink-soft);}
.ms-row.is-line{background:var(--green-tint);margin:4px -12px 0;padding-left:14px;padding-right:14px;border-radius:12px;border-top:0;}
.ms-row.is-line .ms-name{color:var(--green-text);}
.ms-row.is-line .ms-range{color:var(--green-text);}
.ms-tag{position:absolute;right:14px;top:-9px;font:700 9.5px var(--font-body);letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--green);padding:3px 9px;border-radius:99px;}
.ms-note{margin-top:16px;font-size:12.5px;line-height:1.5;color:var(--muted-2);}
</style>"""

FWCARD_CSS = """<style>
.fwc-wrap{text-align:center;}
.fwc-kick{display:block;font:700 12px var(--font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--fso);margin-bottom:12px;}
.fwc-wrap svg{display:block;width:100%;max-width:460px;height:auto;margin:0 auto;}
.fwc-note{margin-top:10px;font-size:12.5px;color:var(--muted-2);}
</style>"""

def _pt(cx, cy, r, ang):
    a = math.radians(ang)
    return (cx + r*math.cos(a), cy + r*math.sin(a))

FW_ICONS = {
  "assessment":'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9.5 4h5v2.4h-5z"/><path d="M8 11h8M8 14.5h5.5"/>',
  "report":'<rect x="5" y="3.5" width="14" height="17" rx="2"/><path d="M8.5 16v-3.4M12 16V9M15.5 16v-5"/>',
  "gear":'<path d="M10.3 3.3a1.9 1.9 0 0 1 3.4 0l.4 .9a1.9 1.9 0 0 0 2.3 1l1-.3a1.9 1.9 0 0 1 2.4 2.4l-.3 1a1.9 1.9 0 0 0 1 2.3l.9 .4a1.9 1.9 0 0 1 0 3.4l-.9 .4a1.9 1.9 0 0 0-1 2.3l.3 1a1.9 1.9 0 0 1-2.4 2.4l-1-.3a1.9 1.9 0 0 0-2.3 1l-.4 .9a1.9 1.9 0 0 1-3.4 0l-.4-.9a1.9 1.9 0 0 0-2.3-1l-1 .3a1.9 1.9 0 0 1-2.4-2.4l.3-1a1.9 1.9 0 0 0-1-2.3l-.9-.4a1.9 1.9 0 0 1 0-3.4l.9-.4a1.9 1.9 0 0 0 1-2.3l-.3-1a1.9 1.9 0 0 1 2.4-2.4l1 .3a1.9 1.9 0 0 0 2.3-1z"/><circle cx="12" cy="12" r="3"/>',
  "recheck":'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9.5 4h5v2.4h-5z"/><path d="M8.4 13.3l2.3 2.3 4.1-4.5"/>',
  "award":'<circle cx="12" cy="9" r="5"/><path d="M8.6 13.2 7 21l5-2.8L17 21l-1.6-7.8"/>',
  "shieldchart":'<path d="M12 3l7 3v5c0 4.6-3.1 7.7-7 9-3.9-1.3-7-4.4-7-9V6z"/><path d="M9.6 13.6v-2M12 13.6V9.6M14.4 13.6v-3"/>',
}

def flywheel_card():
    # (num, icon, light, base, label-lines)
    steps = [
        ("1","assessment","#4C74F2","#1E4FE0",["FSO","Assessment"]),
        ("2","report","#22C3B0","#0FA091",["Gap","Report"]),
        ("3","gear","#F0A836","#D9810C",["Improvement"]),
        ("4","recheck","#F2764C","#E2542B",["Reassessment"]),
        ("5","award","#8D5CE0","#6D3DC0",["Certification"]),
    ]
    cx = cy = 260; Ro = 238; Ri = 150; Rm = 194; gap = 3.0; n = len(steps)
    grads = ""; segs = ""; marks = ""
    for i,(num,ic,light,base,lines) in enumerate(steps):
        grads += (f'<radialGradient id="fwg{i}" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{Ro}">'
                  f'<stop offset="0.62" stop-color="{light}"/><stop offset="1" stop-color="{base}"/></radialGradient>')
        a0 = -90 + i*(360/n) + gap/2
        a1 = -90 + (i+1)*(360/n) - gap/2
        ox0,oy0 = _pt(cx,cy,Ro,a0); ox1,oy1 = _pt(cx,cy,Ro,a1)
        ix1,iy1 = _pt(cx,cy,Ri,a1); ix0,iy0 = _pt(cx,cy,Ri,a0)
        segs += (f'<path d="M{ox0:.1f} {oy0:.1f} A{Ro} {Ro} 0 0 1 {ox1:.1f} {oy1:.1f} '
                 f'L{ix1:.1f} {iy1:.1f} A{Ri} {Ri} 0 0 0 {ix0:.1f} {iy0:.1f} Z" '
                 f'fill="url(#fwg{i})" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/>')
        am = -90 + i*(360/n) + (360/n)/2
        mx,my = _pt(cx,cy,Rm,am)
        marks += (f'<circle cx="{mx:.1f}" cy="{my-35:.1f}" r="11" fill="#fff"/>'
                  f'<text x="{mx:.1f}" y="{my-30.5:.1f}" text-anchor="middle" font-family="Archivo,sans-serif" '
                  f'font-weight="800" font-size="13" fill="{base}">{num}</text>'
                  f'<g transform="translate({mx-11.5:.1f},{my-20.5:.1f}) scale(0.96)" fill="none" stroke="#fff" '
                  f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{FW_ICONS[ic]}</g>')
        for j,ln in enumerate(lines):
            marks += (f'<text x="{mx:.1f}" y="{my+16+j*16:.1f}" text-anchor="middle" '
                      f'font-family="Inter,sans-serif" font-weight="700" font-size="13.5" fill="#fff" '
                      f'letter-spacing="0.2">{ln}</text>')
    # directional arrow across the top
    ast,aen = -117, -63; Ra = Ro + 16
    sx,sy = _pt(cx,cy,Ra,ast); ex,ey = _pt(cx,cy,Ra,aen)
    dr = math.radians(aen+90); pr = math.radians(aen)
    tip=(ex+15*math.cos(dr), ey+15*math.sin(dr))
    b1=(ex+9.5*math.cos(pr), ey+9.5*math.sin(pr)); b2=(ex-9.5*math.cos(pr), ey-9.5*math.sin(pr))
    arrow = (f'<path d="M{sx:.1f} {sy:.1f} A{Ra} {Ra} 0 0 1 {ex:.1f} {ey:.1f}" fill="none" '
             f'stroke="#0A38C0" stroke-width="7" stroke-linecap="round"/>'
             f'<path d="M{tip[0]:.1f} {tip[1]:.1f} L{b1[0]:.1f} {b1[1]:.1f} L{b2[0]:.1f} {b2[1]:.1f} Z" fill="#0A38C0"/>')
    return f"""
<div class="fwc-wrap reveal" role="img" aria-label="The FSO Assessment Cycle: FSO Assessment, Gap Report, Improvement, Reassessment and Certification, repeating each year.">
  <span class="fwc-kick">The FSO Assessment Cycle</span>
  <svg viewBox="0 0 520 520">
    <defs>
      {grads}
      <filter id="fwsh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="7" stdDeviation="11" flood-color="#0B1B3F" flood-opacity="0.16"/></filter>
      <filter id="fwdrop" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="9" stdDeviation="13" flood-color="#0B1B3F" flood-opacity="0.17"/></filter>
    </defs>
    <g filter="url(#fwdrop)">{segs}</g>
    {arrow}
    <circle cx="{cx}" cy="{cy}" r="146" fill="#fff" filter="url(#fwsh)"/>
    <circle cx="{cx}" cy="{cy}" r="146" fill="none" stroke="#EDF1FC" stroke-width="1.5"/>
    <g transform="translate({cx-17},{cy-82}) scale(1.5)" fill="none" stroke="#0A38C0" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{FW_ICONS['shieldchart']}</g>
    <text x="{cx}" y="{cy-15}" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="800" font-size="22" fill="#0C1B36">FSO Assessment</text>
    <text x="{cx}" y="{cy+11}" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="800" font-size="22" fill="#0C1B36">Cycle</text>
    <rect x="{cx-29}" y="{cy+24}" width="58" height="3" rx="1.5" fill="#D9810C"/>
    <text x="{cx}" y="{cy+50}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="600" font-size="13.5" fill="#0A38C0">Assess &#8226; Improve</text>
    <text x="{cx}" y="{cy+69}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="600" font-size="13.5" fill="#0A38C0">Certify &#8226; Sustain</text>
    {marks}
  </svg>
  <p class="fwc-note">A cycle, not a one time event. Each round raises the baseline.</p>
</div>"""

BANDS_CSS = """<style>
.bands-card{background:var(--canvas);border:1px solid var(--line);border-radius:var(--radius-panel);box-shadow:var(--shadow-lg);padding:26px 26px 22px;}
.bands-kick{display:block;font:700 12px var(--font-body);letter-spacing:.14em;text-transform:uppercase;color:var(--fso);}
.bands-sub{display:block;margin-top:6px;font-family:var(--font-display);font-weight:800;font-size:19px;color:var(--ink-blue);letter-spacing:-.01em;}
.bands-card svg{display:block;width:100%;max-width:400px;height:auto;margin:8px auto 2px;}
.bands-legend{display:grid;grid-template-columns:1fr 1fr;gap:11px 16px;margin-top:8px;}
.bands-li{display:flex;align-items:center;gap:10px;}
.bands-li .bd{width:12px;height:12px;border-radius:50%;flex:none;}
.bands-li .bn{font:600 13.5px var(--font-body);color:var(--ink-blue);line-height:1.15;}
.bands-li .br{font:700 12px var(--font-display);color:var(--ink-soft);}
.bands-note{margin-top:16px;font-size:12.5px;line-height:1.5;color:var(--muted-2);}
</style>"""

def bands_graphic():
    bands = [("Financially Blind","0 to 40","#E15748",180,252),
             ("Reactive","41 to 60","#E39A2B",252,288),
             ("Developing","61 to 75","#3E8FD8",288,315),
             ("Certification ready","76 to 100","#18AE80",315,360)]
    cx, cy, R, sw, g = 230, 205, 165, 24, 1.8
    arcs = ""
    for name,rng,col,a0,a1 in bands:
        s = _pt(cx,cy,R,a0+g/2); e = _pt(cx,cy,R,a1-g/2)
        arcs += (f'<path d="M{s[0]:.1f} {s[1]:.1f} A{R} {R} 0 0 1 {e[0]:.1f} {e[1]:.1f}" '
                 f'fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>')
    t1 = _pt(cx,cy,R-16,315); t2 = _pt(cx,cy,R+18,315); lb = _pt(cx,cy,R+36,315)
    marker = (f'<line x1="{t1[0]:.1f}" y1="{t1[1]:.1f}" x2="{t2[0]:.1f}" y2="{t2[1]:.1f}" stroke="#0C1B36" stroke-width="2.5" stroke-linecap="round"/>'
              f'<circle cx="{t2[0]:.1f}" cy="{t2[1]:.1f}" r="3.2" fill="#0C1B36"/>'
              f'<text x="{lb[0]:.1f}" y="{lb[1]-5:.1f}" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="800" font-size="16" fill="#0C1B36">76</text>'
              f'<text x="{lb[0]:.1f}" y="{lb[1]+8:.1f}" text-anchor="middle" font-family="Inter,sans-serif" font-weight="700" font-size="9" letter-spacing="0.6" fill="#0F7A58">THE LINE</text>')
    legend = "".join(f'<div class="bands-li"><span class="bd" style="background:{col};"></span>'
                     f'<div><div class="bn">{name}</div><div class="br">{rng}</div></div></div>'
                     for name,rng,col,a0,a1 in bands)
    return f"""
<div class="bands-card reveal" role="img" aria-label="The four FSO bands: Financially Blind 0 to 40, Reactive 41 to 60, Developing 61 to 75, and Certification ready 76 and above. The certification line is at 76.">
  <span class="bands-kick">The FSO bands</span>
  <span class="bands-sub">One score out of 100. One line to clear.</span>
  <svg viewBox="0 0 460 236">{arcs}{marker}</svg>
  <div class="bands-legend">{legend}</div>
  <p class="bands-note">The score is private. Only a certificate says Financially Smart Organisation.</p>
</div>"""

def cta_band():
    return f"""
<section class="section">
  <div class="wrap">
    <div class="cta-band sec-brand reveal">
      <div class="emblem-bg" aria-hidden="true"></div>
      <div class="wrap-inner">
        <p class="eyebrow on-dark">Start with your score</p>
        <h2 class="h-lg">Know where your business stands, in about six minutes.</h2>
        <p class="lede mt-s">Take the free FSO Diagnostic for an indicative read across the areas FSO assesses, then book a Discovery Call to talk through the full Assessment and Certification.</p>
        <div class="btn-group mt-m">
          <button class="btn btn-light btn-lg" type="button" data-open-diagnostic>Know Your FSO Score <span class="ar">&#8594;</span></button>
          <a class="btn btn-ghost on-dark btn-lg" href="contact.html">Book a Discovery Call</a>
        </div>
      </div>
    </div>
  </div>
</section>"""

# =====================================================================
#  FSO Flywheel  (the perpetual FSO Assessment Cycle)
# =====================================================================
FLYWHEEL_CSS = """<style>
.fw-wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,60px);align-items:center;}
.fw-ring{position:relative;}
.fw-steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;}
.fw-step{display:flex;gap:16px;align-items:flex-start;background:var(--canvas);border:1px solid var(--line);border-left:3px solid var(--fso);border-radius:14px;padding:16px 18px;}
.fw-n{flex:none;width:30px;height:30px;border-radius:50%;background:var(--fso-wash);color:var(--fso);font-family:var(--font-display);font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;}
.fw-step h3{font-family:var(--font-display);font-weight:800;font-size:16px;color:var(--ink-blue);margin:2px 0 3px;}
.fw-step p{font-size:14px;line-height:1.5;color:var(--ink-soft);margin:0;}
.fw-core{text-align:center;background:var(--grad-brand);border-radius:var(--radius-panel);padding:40px 30px;color:#fff;position:relative;overflow:hidden;}
.fw-core .emblem-bg::before,.fw-core .emblem-bg::after{border-color:rgba(255,255,255,.14);}
.fw-core h3{font-family:var(--font-display);font-weight:800;font-size:clamp(24px,3vw,30px);color:#fff;line-height:1.14;margin:0 0 12px;position:relative;}
.fw-core p{color:rgba(255,255,255,.85);font-size:15px;line-height:1.6;margin:0 auto;max-width:34ch;position:relative;}
.fw-pills{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:18px;position:relative;}
.fw-pill{font:700 12px var(--font-body);letter-spacing:.06em;text-transform:uppercase;color:#fff;border:1px solid rgba(255,255,255,.4);border-radius:99px;padding:6px 13px;}
@media(max-width:820px){.fw-wrap{grid-template-columns:1fr;}.fw-core{order:-1;}}
</style>"""

def flywheel():
    return f"""
<section class="section" style="background:var(--wash);">
  <div class="wrap">
    <div class="center reveal" style="max-width:760px;margin-inline:auto;margin-bottom:clamp(26px,4vw,40px);">
      <p class="eyebrow center">The FSO Assessment Cycle</p>
      <h2 class="h-lg">Financial strength is not a one time event</h2>
      <p class="lede center mt-s">A single assessment tells you where you stand today. The FSO cycle keeps that strength current, year after year, so the discipline holds as the business grows. Assess, improve, certify, sustain.</p>
    </div>
    <div class="center reveal">
      <img src="assets/img/fso-flywheel.jpg?v=1" alt="The FSO Assessment Cycle: FSO Assessment, Gap Report, Improvement, Reassessment and Certification, repeating each year" width="1448" height="1086" style="width:100%;max-width:640px;height:auto;display:inline-block;" decoding="async">
    </div>
  </div>
</section>"""

# =====================================================================
#  Testimonials (clearly labelled placeholders)
# =====================================================================
TESTIMONIALS = [
  ("The FSO Assessment gave us a plain numbered view of exactly where our finances were fragile. Closing the top three gaps changed how we run the company.", "AK", "Managing Director", "Manufacturing SME"),
  ("For the first time we could show a lender something better than a balance sheet, an independent read on how our financial system actually works.", "RS", "Founder and CEO", "B2B Services"),
  ("We always thought we were doing fine because we were profitable. The Assessment showed us where cash and working capital were quietly costing us.", "MP", "Promoter", "Distribution and Trading"),
  ("Going through Certification forced a discipline we had been putting off for years. The score gave the whole leadership team one thing to rally around.", "VN", "Director", "Growth stage Manufacturer"),
]

def testimonials_block():
    slides = ""
    for quote, av, role, org in TESTIMONIALS:
        slides += f"""
      <div class="tcar-slide">
        <div class="tcar-card">
          <div class="tcar-stars" aria-label="Five out of five">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="tcar-quote">{quote}</p>
          <div class="tcar-who">
            <div class="tcar-av" aria-hidden="true">{av}</div>
            <div class="tcar-meta"><b>{role}</b><span>{org}</span></div>
          </div>
          <span class="placeholder-tag">Placeholder, replace with a real client</span>
        </div>
      </div>"""
    return f"""
<section class="section" aria-labelledby="tst-h">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:36px;">
      <p class="eyebrow center">Voices from the field</p>
      <h2 class="h-lg" id="tst-h">What FSO changes for the people who run the numbers</h2>
      <p class="lede center mt-s">The quotes below are illustrative placeholders. Send us your real testimonials and we will drop them straight in. No invented names or results are used.</p>
    </div>
    <div class="tcar reveal" data-carousel>
      <div class="tcar-track">{slides}
      </div>
      <div class="tcar-nav">
        <button class="tcar-btn" type="button" data-prev aria-label="Previous testimonial"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg></button>
        <div class="tcar-dots" role="tablist" aria-label="Choose testimonial"></div>
        <button class="tcar-btn" type="button" data-next aria-label="Next testimonial"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg></button>
      </div>
    </div>
  </div>
</section>"""

# =====================================================================
#  HOME
# =====================================================================
home = f"""
<section class="hero dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  {BANDS_CSS}
  <div class="wrap">
    <div class="hero-grid">
      <div class="hero-copy">
        <p class="eyebrow on-dark reveal">Assessment and Certification</p>
        <h1 class="reveal">Know how financially smart your organisation <span class="grad-text">really is.</span></h1>
        <p class="lede reveal">FSO is an independent assessment, on evidence, of how your business plans, controls, reports and protects its money. One private score out of 100, nine domains, 38 criteria, and a certificate for those who clear the line.</p>
        <div class="hero-badges reveal">
          <span class="pill"><span class="dot"></span> 38 criteria, scored on evidence</span>
          <span class="pill"><span class="dot"></span> Nine domains, four themes</span>
          <span class="pill"><span class="dot"></span> Independent certification</span>
        </div>
        <div class="btn-group hero-cta reveal">
          <button class="btn btn-primary btn-lg" type="button" data-open-diagnostic>Know Your FSO Score <span class="ar">&#8594;</span></button>
          <a class="btn btn-ghost on-dark btn-lg" href="contact.html">Book a Discovery Call</a>
        </div>
        <p class="hero-note reveal">Free six minute diagnostic. No sign up to see your score.</p>
      </div>
      <div class="hero-media">{bands_graphic()}</div>
    </div>
    <div class="trust-bar reveal">
      <p>Built on the FSO 2.0 standard. Issued by the FSO Council.</p>
      <div class="trust-logos">
        <span>DOCUMENT REVIEW</span><span>STRUCTURED INTERVIEWS</span><span>EVIDENCE SAMPLING</span><span>COUNCIL DECISION</span>
      </div>
    </div>
  </div>
</section>

<section class="section--tight" style="background:var(--wash);">
  <div class="wrap">
    <div class="stat-grid">
      <div class="stat reveal"><div class="n">100</div><div class="l">Point scale, from one assessment</div></div>
      <div class="stat reveal"><div class="n">38</div><div class="l">Criteria across nine domains</div></div>
      <div class="stat reveal"><div class="n">76</div><div class="l">The certification line, the same for every size of business</div></div>
      <div class="stat reveal"><div class="n">4</div><div class="l">Themes: Plan, Control, Report, Protect</div></div>
    </div>
  </div>
</section>

<section class="section dark" id="purpose">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="center reveal" style="max-width:840px;margin-inline:auto;margin-bottom:clamp(36px,5vw,52px);">
      <p class="eyebrow on-dark center">Why we exist</p>
      <h2 class="h-xl">World class enterprises are built on world class financial management.</h2>
      <p class="lede center mt-m">FSO exists for one reason, to make every business owner financially smart. We take the quiet advantage the biggest companies have always had, true command of their numbers, and put it within reach of every founder building something that matters.</p>
    </div>
    <div class="ripple reveal" role="list" aria-label="How FSO creates impact">
      <div class="ripple-step" role="listitem">
        <div class="rn">{icon('bulb')}</div>
        <div class="rbody"><h4>One owner sees clearly</h4><p>A founder finally understands what their numbers are telling them, and what to do about it.</p></div>
      </div>
      <div class="ripple-step" role="listitem">
        <div class="rn">{icon('grow')}</div>
        <div class="rbody"><h4>One business gets stronger</h4><p>More profitable, more resilient, and able to fund its own growth instead of hoping to survive it.</p></div>
      </div>
      <div class="ripple-step" role="listitem">
        <div class="rn">{icon('users')}</div>
        <div class="rbody"><h4>Livelihoods are protected</h4><p>The jobs, suppliers and families that depend on that business become far safer.</p></div>
      </div>
      <div class="ripple-step" role="listitem">
        <div class="rn">{icon('award')}</div>
        <div class="rbody"><h4>A world class enterprise is built</h4><p>The kind that lasts for generations, and lifts the economy around it.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Why FSO exists</p>
        <h2 class="h-lg">Judged on the numbers. Rarely on how they are managed.</h2>
        <p class="lede mt-s">An audit confirms the books are right. A credit assessment asks whether you can probably repay. A valuation asks what someone might pay. None of them answer the question a promoter actually asks, is my business financially sound as a system, or am I holding it together myself?</p>
        <p class="mt-m" style="color:var(--ink-soft);">FSO answers that question objectively, repeatably and comparably. We measure systems and practices, not profits, and score what your team actually does, not what the policy manual says.</p>
        <a class="btn btn-ghost mt-m" href="about.html">Read the FSO story <span class="ar">&#8594;</span></a>
      </div>
      <div class="reveal">
        <div class="card-grid cols-2">
          <div class="card card--soft"><div class="ic">{icon('search')}</div><h3>Unaware of the gap</h3><p>Owner led businesses rarely know whether their financial system is sound, only whether this year was good.</p></div>
          <div class="card card--soft"><div class="ic">{icon('users')}</div><h3>Accountants, not CFOs</h3><p>SMEs hire for compliance and bookkeeping, but seldom for the financial leadership that builds resilience.</p></div>
          <div class="card card--soft"><div class="ic">{icon('cash')}</div><h3>Cash runs the show</h3><p>Money that is not assigned a purpose the day it arrives gets consumed by the loudest demand.</p></div>
          <div class="card card--soft"><div class="ic">{icon('shield')}</div><h3>Key person exposure</h3><p>When the system lives in the promoter's head, capability is not maturity. It is risk.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section dark" id="what-we-assess">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:44px;max-width:760px;margin-inline:auto;">
      <p class="eyebrow on-dark center">What FSO assesses</p>
      <h2 class="h-lg">Nine domains, four themes, 38 criteria</h2>
      <p class="lede center mt-s">FSO examines how your whole financial system works, across every area that decides whether a business keeps the money it makes and keeps growing. Each criterion is scored on evidence an assessor can actually see.</p>
    </div>
    <div class="card-grid cols-4">
      <div class="card card--dark reveal"><div class="ic">{icon('target')}</div><h3>Plan</h3><p>How you forecast cash, fund the business and plan for growth.</p></div>
      <div class="card card--dark reveal"><div class="ic">{icon('layers')}</div><h3>Control</h3><p>How you manage working capital, costs and internal controls.</p></div>
      <div class="card card--dark reveal"><div class="ic">{icon('chart')}</div><h3>Report</h3><p>Whether your numbers are timely, reliable and used to decide.</p></div>
      <div class="card card--dark reveal"><div class="ic">{icon('shield')}</div><h3>Protect</h3><p>How you manage risk, compliance and the resilience of the system.</p></div>
    </div>
    <p class="center reveal mt-l" style="color:var(--ink-soft);max-width:660px;margin-inline:auto;">Each criterion is examined against a structured, points based rubric and scored on evidence, so the result is objective, consistent and comparable, not a matter of opinion.</p>
    <div class="center mt-m reveal"><a class="btn btn-light btn-lg" href="standard.html">How the FSO Standard works <span class="ar">&#8594;</span></a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:44px;">
      <p class="eyebrow center">How it works</p>
      <h2 class="h-lg">Six steps. The first two are free.</h2>
    </div>
    <div class="card-grid cols-3">
      <div class="card step reveal"><div class="num">1</div><h3>Diagnose</h3><p>Fifteen questions, about six minutes. An indicative read, with no sign up to see your score.</p></div>
      <div class="card step reveal"><div class="num">2</div><h3>Talk</h3><p>A 45 minute Discovery Call to agree scope and whether you are ready for a full Assessment.</p></div>
      <div class="card step reveal"><div class="num">3</div><h3>Assess</h3><p>An assessor reviews documents, interviews your team and samples real transactions across 38 criteria.</p></div>
      <div class="card step reveal"><div class="num">4</div><h3>Report</h3><p>A private Gap Report, with every gap ranked and a rupee value at stake on each one.</p></div>
      <div class="card step reveal"><div class="num">5</div><h3>Improve</h3><p>You close the gaps at your own pace, with the self use Improvement Guide.</p></div>
      <div class="card step reveal"><div class="num">6</div><h3>Certify</h3><p>Conformity checks, FSO 360 and the FSO Council decision. The certificate is renewed each year.</p></div>
    </div>
    <div class="center mt-l reveal"><a class="btn btn-ghost btn-lg" href="services.html">See the full path <span class="ar">&#8594;</span></a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:40px;max-width:700px;margin-inline:auto;">
      <p class="eyebrow center">Why you can trust it</p>
      <h2 class="h-lg">A certificate that cannot be bought</h2>
    </div>
    <div class="card-grid cols-2">
      <div class="card card--soft reveal"><div class="ic">{icon('lock')}</div><h3>Independence, in writing</h3><p>No assessor who advised you in the past 24 months, and a different lead assessor at Certification. The Council decides.</p></div>
      <div class="card card--soft reveal"><div class="ic">{icon('scale')}</div><h3>Fees never linked to outcome</h3><p>What you pay is never tied to your score or to whether you certify. The result reflects your business, nothing else.</p></div>
      <div class="card card--soft reveal"><div class="ic">{icon('target')}</div><h3>Objective and comparable</h3><p>The same evidence based framework, applied the same way every time, so progress is measurable year on year.</p></div>
      <div class="card card--soft reveal"><div class="ic">{icon('shield')}</div><h3>We do not sell the fix</h3><p>FSO measures and certifies. We can say what a gap is and why it matters, never how we would repair it for a fee.</p></div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--wash);">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:40px;">
      <p class="eyebrow center">Who it is for</p>
      <h2 class="h-lg">Four models by size, one standard</h2>
      <p class="lede center mt-s">FSO is designed to work across industries. The model is tuned to the size of the business, but the line at 76 is the same for everyone.</p>
    </div>
    <div class="card-grid cols-4">
      <div class="card reveal"><div class="ic">{icon('bulb')}</div><h3>Startup</h3><p>Early stage companies that want to build the financial discipline in from the start.</p></div>
      <div class="card reveal"><div class="ic">{icon('grow')}</div><h3>SME</h3><p>Promoter led companies that have outgrown gut feel finance and want a clear, honest read.</p></div>
      <div class="card reveal"><div class="ic">{icon('layers')}</div><h3>Mid Market</h3><p>Established businesses that want their financial management judged as a system.</p></div>
      <div class="card reveal"><div class="ic">{icon('target')}</div><h3>Large</h3><p>Groups preparing for funding, a lender, a buyer or succession who want an independent signal.</p></div>
    </div>
  </div>
</section>

{testimonials_block()}
{cta_band()}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Organization",
      "@id": "{SITE}/#organization",
      "name": "FSO Financially Smart Organisation",
      "legalName": "FSO Global Standards Private Limited",
      "url": "{SITE}/",
      "logo": "{SITE}/assets/img/icon-512.png",
      "description": "An independent assessment and certification of how well an organisation plans, controls, reports and protects its money.",
      "email": "connect@fsoworld.com",
      "telephone": "+91 93116 46714",
      "sameAs": ["{APP}"]
    }},
    {{
      "@type": "WebSite",
      "@id": "{SITE}/#website",
      "url": "{SITE}/",
      "name": "FSO Financially Smart Organisation",
      "publisher": {{ "@id": "{SITE}/#organization" }}
    }},
    {{
      "@type": "Service",
      "name": "FSO Assessment and Certification",
      "serviceType": "Financial management system assessment and certification",
      "provider": {{ "@id": "{SITE}/#organization" }},
      "areaServed": "IN",
      "description": "An independent, evidence based assessment of an organisation's financial management system across 38 criteria and nine domains, producing a private score out of 100 and, for organisations that clear the line and are decided by the FSO Council, certification as a Financially Smart Organisation."
    }}
  ]
}}
</script>
"""

# =====================================================================
#  ABOUT
# =====================================================================
about = f"""
<section class="page-hero dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div style="max-width:760px;">
      <p class="breadcrumbs reveal"><a href="index.html">Home</a><span>/</span>About</p>
      <p class="eyebrow on-dark reveal">About FSO</p>
      <h1 class="h-xl reveal">We believe every business owner deserves to be financially smart.</h1>
      <p class="lede reveal">Great products build companies. Great financial management builds companies that last. FSO exists to put that mastery within reach of every founder, by defining what it means to run your money as a designed system, and turning it into a score, a standard, and a certificate worth earning.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">The mission</p>
        <h2 class="h-lg">Financial literacy for every business owner</h2>
        <p class="lede mt-s">Too many capable businesses run on low profitability and thin liquidity, and some quietly slide into distress, not because the owners lack drive, but because no one ever assessed the system behind the numbers.</p>
        <p class="mt-m" style="color:var(--ink-soft);">FSO's purpose is to change that. To make good financial management measurable, teachable and recognisable, so that owners can see their gaps early, close them deliberately, and prove their progress to the people whose trust they need.</p>
      </div>
      <div class="reveal">
        <div class="card-grid cols-1" style="gap:16px;">
          <div class="card"><div class="ic">{icon('target')}</div><h3>Set the standard</h3><p>Establish a clear, objective benchmark for financial management in growth companies, one that different assessors apply consistently.</p></div>
          <div class="card"><div class="ic">{icon('bulb')}</div><h3>Build the literacy</h3><p>Give owners a plain language map of what good looks like across every domain of their finances.</p></div>
          <div class="card"><div class="ic">{icon('shield')}</div><h3>Reward the discipline</h3><p>Recognise the businesses that do the work, with a certificate that carries weight precisely because it cannot be bought.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="center reveal" style="max-width:720px;margin-inline:auto;margin-bottom:44px;">
      <p class="eyebrow on-dark center">Foundational principles</p>
      <h2 class="h-lg">The ideas that give the score its integrity</h2>
      <p class="lede center mt-s">You will not find our full methodology here, but these are the convictions that shape how every FSO assessment is done.</p>
    </div>
    <div class="card-grid cols-2">
      <div class="card card--dark reveal"><h3>Cash is the subject, profit is the evidence</h3><p>Profit is an accounting opinion. Cash is an observable fact. Where they diverge, the standard follows the cash.</p></div>
      <div class="card card--dark reveal"><h3>A system outranks a person</h3><p>Capability that lives in one individual is exposure, not maturity. The standard rewards documented, delegable, repeatable process.</p></div>
      <div class="card card--dark reveal"><h3>Decide before the money arrives</h3><p>Cash not assigned a purpose the day it lands gets consumed by the loudest demand. The strongest businesses decide first.</p></div>
      <div class="card card--dark reveal"><h3>Measured, or it does not exist</h3><p>A control that is not evidenced and a metric that is not tracked count as absent. Intention is not maturity.</p></div>
      <div class="card card--dark reveal"><h3>Rhythm beats intensity</h3><p>A modest review held without fail outperforms a brilliant one done once a year. Consistency counts.</p></div>
      <div class="card card--dark reveal"><h3>Reproducibility is the point</h3><p>The score is built so a different assessor would reach the same conclusion. A result that cannot be reproduced is not worth certifying.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split rev">
      <div class="reveal">
        <div class="card-grid cols-1" style="gap:16px;">
          <div class="card card--soft"><div class="ic">{icon('check')}</div><h3>What FSO is</h3><p>An independent assessment of the design, operation and effectiveness of a financial management system, and a certificate for those who clear the line.</p></div>
          <div class="card card--soft"><div class="ic">{icon('shield')}</div><h3>What FSO is not</h3><p>Not an audit, review or attest engagement. Not a credit rating, valuation or investment advice. Not accredited by NABCB, QCI or any government body unless the certificate says so, and not regulated by RBI or SEBI.</p></div>
        </div>
      </div>
      <div class="reveal">
        <p class="eyebrow">What FSO is, and is not</p>
        <h2 class="h-lg">Independence is the whole point</h2>
        <p class="lede mt-s">A certificate that can be bought is worthless to the lenders and buyers whose reliance gives it value. So the standard is deliberately held above any single engagement.</p>
        <ul class="check-list">
          <li>No assessor who advised you in the past 24 months.</li>
          <li>A different lead assessor at Certification, and the FSO Council decides.</li>
          <li>Fees are never linked to your score or outcome.</li>
          <li>FSO measures and certifies. It does not sell the fix.</li>
        </ul>
        <a class="btn btn-ghost mt-m" href="standard.html">See the methodology <span class="ar">&#8594;</span></a>
      </div>
    </div>
  </div>
</section>

{cta_band()}
"""

# =====================================================================
#  THE STANDARD
# =====================================================================
spectrum = ""
for _n,_r,_c,_cert in BANDS_UI:
    spectrum += f'<div class="spec-seg{" is-cert" if _cert else ""}" style="--c:{_c};"><i></i><span>{_n}</span><span style="display:block;font-weight:500;font-size:12px;color:var(--muted);margin-top:4px;">{_r}</span></div>'

standard = f"""
<section class="page-hero dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div style="max-width:780px;">
      <p class="breadcrumbs reveal"><a href="index.html">Home</a><span>/</span>The Standard</p>
      <p class="eyebrow on-dark reveal">The FSO Standard</p>
      <h1 class="h-xl reveal">A serious standard for a serious question.</h1>
      <p class="lede reveal">FSO turns is this business financially sound as a system into one objective, evidence based score. Rigorous enough to certify, clear enough to act on. Here is what makes it credible, without giving away the recipe.</p>
      <div class="btn-group mt-m reveal">
        <button class="btn btn-primary btn-lg" type="button" data-open-diagnostic>Try the free diagnostic <span class="ar">&#8594;</span></button>
        <a class="btn btn-ghost on-dark btn-lg" href="certification.html">Apply for Certification</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center reveal" style="max-width:700px;margin-inline:auto;margin-bottom:44px;">
      <p class="eyebrow center">What the FSO Standard is</p>
      <h2 class="h-lg">Built like a standard, not a checklist or an opinion</h2>
      <p class="lede center mt-s">FSO is a formal methodology, developed deliberately and applied by trained assessors. Four principles make its score something you can rely on and defend.</p>
    </div>
    <div class="card-grid cols-2">
      <div class="card reveal"><div class="ic">{icon('layers')}</div><h3>Structured and points based</h3><p>A defined framework converts the way your business runs its money into one clear, comparable score out of 100, across 38 criteria and nine domains.</p></div>
      <div class="card reveal"><div class="ic">{icon('doc')}</div><h3>Evidence based</h3><p>Every rating rests on things an assessor can actually see, documents, reports, reconciliations and live processes, not on assertions or good intentions.</p></div>
      <div class="card reveal"><div class="ic">{icon('target')}</div><h3>Objective and consistent</h3><p>The same method, applied the same way, to every organisation. The score is meant to reflect your business, not the assessor's mood or style.</p></div>
      <div class="card reveal"><div class="ic">{icon('shield')}</div><h3>Independently reproducible</h3><p>Designed so a different assessor would reach the same conclusion. A score that cannot be reproduced is not worth certifying.</p></div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  {MATURITY_CSS}
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow on-dark">One number, honestly earned</p>
        <h2 class="h-lg">One score out of 100. One line to clear.</h2>
        <p class="lede mt-s">The FSO Score, from 0 to 100, summarises how well your financial system works across every area that decides whether a business keeps its money and keeps growing, not just whether this year was profitable.</p>
        <p class="mt-m" style="color:var(--ink-soft);">At 76 and above an Assessment says Certification ready. That is not a certificate. Clear the line, meet every domain floor, carry no open red flag, and be decided by the FSO Council, and your business is recognised as a <b style="color:var(--fso);">Financially Smart Organisation</b>. The Assessment score itself stays private.</p>
      </div>
      <div class="reveal">{maturity_scale()}</div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--wash);" id="maturity">
  <div class="wrap">
    <div class="center reveal" style="max-width:720px;margin-inline:auto;margin-bottom:40px;">
      <p class="eyebrow center">The maturity scale</p>
      <h2 class="h-lg">Every business sits somewhere. Where do you?</h2>
      <p class="lede center mt-s">Your score places you on the FSO maturity scale. Certification begins where a business moves from doing okay to demonstrably in control of its numbers.</p>
    </div>
    <div class="spectrum reveal" role="img" aria-label="FSO maturity scale from Financially Blind, through Reactive and Developing, to Certification ready at 76 and above.">
      {spectrum}
    </div>
    <p class="center muted reveal mt-m" style="font-size:13.5px;">Certification ready is the point at which you may apply for Certification. The exact rubric behind the score is applied by trained assessors.</p>
    <div class="center mt-l reveal"><button class="btn btn-primary btn-lg" type="button" data-open-diagnostic>See where you would land, free <span class="ar">&#8594;</span></button></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center reveal" style="max-width:680px;margin-inline:auto;margin-bottom:44px;">
      <p class="eyebrow center">How an assessment works</p>
      <h2 class="h-lg">Thorough, structured, and the same every time</h2>
      <p class="lede center mt-s">A defined protocol, not a chat and a gut feel. Enough rigour to stand behind, without the paperwork of an audit.</p>
    </div>
    <div class="card-grid cols-4">
      <div class="card step reveal"><div class="num">1</div><h3>Scope</h3><p>We agree scope and timing on a Discovery Call, and set out exactly what the Assessment will look at.</p></div>
      <div class="card step reveal"><div class="num">2</div><h3>Assess</h3><p>Document review, structured interviews and sampling of real transactions across 38 criteria. Evidence, first hand.</p></div>
      <div class="card step reveal"><div class="num">3</div><h3>Report</h3><p>Your private score, a clear picture of strengths and gaps, and a rupee value at stake on every gap.</p></div>
      <div class="card step reveal"><div class="num">4</div><h3>Certify</h3><p>Conformity checks, FSO 360 and the FSO Council decision. The certificate is renewed each year.</p></div>
    </div>
  </div>
</section>

{cta_band()}
"""

# =====================================================================
#  SERVICES
# =====================================================================
services = f"""
<section class="page-hero dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div style="max-width:820px;">
      <p class="breadcrumbs reveal"><a href="index.html">Home</a><span>/</span>Services</p>
      <p class="eyebrow on-dark reveal">What we do</p>
      <h1 class="h-xl reveal">Two free steps, then two paid steps. Nothing else.</h1>
      <p class="lede reveal">FSO measures and certifies. Start with a free diagnostic and a Discovery Call, then the FSO Assessment and, for those who clear the line, FSO Certification. You close the gaps yourself, with a guide we provide.</p>
      <div class="btn-group mt-m reveal">
        <button class="btn btn-primary btn-lg" type="button" data-open-diagnostic>Know Your FSO Score <span class="ar">&#8594;</span></button>
        <a class="btn btn-ghost on-dark btn-lg" href="contact.html">Book a Discovery Call</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:44px;max-width:760px;margin-inline:auto;">
      <p class="eyebrow center">How we help</p>
      <h2 class="h-lg">One journey, from a quick score to an independent certificate</h2>
      <p class="lede" style="margin-top:12px;">Start wherever you are. The first two steps are free. The two paid steps are quoted on a Discovery Call, per legal entity, and exclude GST.</p>
    </div>
    <div class="card-grid cols-2">
      <div class="card reveal">
        <span class="placeholder-tag" style="background:var(--green-tint);color:var(--green-text);border-color:var(--green-border);">Free</span>
        <div class="ic" style="margin-top:12px;">{icon('mis')}</div>
        <h3>1 &middot; FSO Diagnostic</h3>
        <p>A free, six minute online check. Fifteen questions, one indicative score, and a view across the areas FSO assesses. No sign up needed.</p>
        <p style="margin-top:14px;"><a href="diagnostic.html" style="color:var(--fso);font-weight:600;text-decoration:none;">Take the diagnostic &#8594;</a></p>
      </div>
      <div class="card reveal">
        <span class="placeholder-tag" style="background:var(--green-tint);color:var(--green-text);border-color:var(--green-border);">Free</span>
        <div class="ic" style="margin-top:12px;">{icon('phone')}</div>
        <h3>2 &middot; Discovery Call</h3>
        <p>A 45 minute conversation to understand your business, agree scope and timing, and decide together whether you are ready for a full Assessment.</p>
        <p style="margin-top:14px;"><a href="contact.html" style="color:var(--fso);font-weight:600;text-decoration:none;">Book a Discovery Call &#8594;</a></p>
      </div>
      <div class="card reveal">
        <span class="placeholder-tag">Paid step</span>
        <div class="ic" style="margin-top:12px;">{icon('shield')}</div>
        <h3>3 &middot; FSO Assessment</h3>
        <p>The full, evidence based assessment by a trained assessor, across all 38 criteria and nine domains. It ends in a private Gap Report, with a rupee value at stake on every gap. Pricing is shared on a Discovery Call.</p>
        <p style="margin-top:14px;"><a href="contact.html" style="color:var(--fso);font-weight:600;text-decoration:none;">Start the Assessment &#8594;</a></p>
      </div>
      <div class="card reveal">
        <span class="placeholder-tag">Paid step</span>
        <div class="ic" style="margin-top:12px;">{icon('award')}</div>
        <h3>4 &middot; FSO Certification</h3>
        <p>A separate second step for businesses that clear the line. Conformity checks, FSO 360 and the FSO Council decision, then a one year certificate and the mark licence. Renewed each year. Pricing is shared on a Discovery Call.</p>
        <p style="margin-top:14px;"><a href="certification.html" style="color:var(--fso);font-weight:600;text-decoration:none;">Apply for Certification &#8594;</a></p>
      </div>
    </div>
    <div class="reveal" style="margin-top:22px;">
      <div class="card card--soft">
        <div class="ic">{icon('book')}</div>
        <h3>The FSO Improvement Guide</h3>
        <p>Between the Assessment and Certification, you close the gaps yourself. The Improvement Guide is a self use resource we provide to help you do that. It is a guide, not a service. FSO does not sell the fix, and does no improvement work for assessed clients.</p>
      </div>
    </div>
  </div>
</section>

{flywheel()}
{cta_band()}
"""

# =====================================================================
#  CERTIFICATION
# =====================================================================
faq_items = [
  ("Who can apply for FSO certification?", "FSO is designed for organisations across industries, from startups to large groups, that want their financial management assessed as a system. There is no minimum size. Certification sits on an FSO Assessment no older than 90 days, so you begin with an Assessment."),
  ("How is it priced?", "There are two paid steps, the FSO Assessment and FSO Certification, quoted per legal entity and exclusive of GST. We share pricing on a Discovery Call, once we understand your business. The free diagnostic and the Discovery Call cost nothing."),
  ("What does it take to be certified?", "You need to clear the line at 76 and above, meet every domain floor, and carry no open red flag. Certification is then a separate step, with conformity checks, FSO 360 and a decision by the FSO Council. We tell you clearly where you stand and what, if anything, is between you and the certificate."),
  ("What if we do not qualify the first time?", "You still receive your private Gap Report, with every gap ranked and a rupee value at stake on each one, so you know exactly what to close and in what order. Many organisations use the first Assessment as a baseline and certify on a later cycle."),
  ("Is the certificate permanent?", "No. The certificate is valid for one year, with 30 days of grace while a renewal is completed. Renewal is a fresh Assessment and Certification, applied for in the last two months, so the certificate always says something true about how the business runs today."),
  ("How is this different from our audit?", "An audit confirms your accounts are true and fair. FSO assesses whether the financial system behind those accounts is well designed and resilient. A different and complementary question. FSO is not an audit, a credit rating, a valuation or investment advice."),
]
faq_html = ""
for i,(q,a) in enumerate(faq_items):
    faq_html += f"""
      <div class="faq-item reveal">
        <button class="faq-q" type="button" aria-expanded="false">{q}</button>
        <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
      </div>"""

certification = f"""
<section class="page-hero dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div style="max-width:780px;">
      <p class="breadcrumbs reveal"><a href="index.html">Home</a><span>/</span>Certification</p>
      <p class="eyebrow on-dark reveal">FSO Certification</p>
      <h1 class="h-xl reveal">Turn financial discipline into a certificate you can show.</h1>
      <p class="lede reveal">Get an independent, evidence based read on how your business runs its money, and, if you clear the line, a certificate that tells lenders, boards and buyers your finances are built to last.</p>
      <div class="btn-group mt-m reveal">
        <a class="btn btn-primary btn-lg" href="contact.html">Apply for Certification <span class="ar">&#8594;</span></a>
        <button class="btn btn-ghost on-dark btn-lg" type="button" data-open-diagnostic>Know Your Score first</button>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:44px;max-width:720px;margin-inline:auto;">
      <p class="eyebrow center">Why get FSO certified</p>
      <h2 class="h-lg">What the Assessment, and the certificate, are worth to you</h2>
    </div>
    <div class="card-grid cols-3">
      <div class="card reveal"><div class="ic">{icon('profit')}</div><h3>Better profitability and cash flow</h3><p>A clear focus on the numbers that matter means you monitor and manage what actually drives profit and cash, deliberately rather than by guesswork.</p></div>
      <div class="card reveal"><div class="ic">{icon('grow')}</div><h3>A prioritised roadmap</h3><p>The highest leverage things to strengthen first, each with a rupee value at stake, not a long report no one actions.</p></div>
      <div class="card reveal"><div class="ic">{icon('shield')}</div><h3>Less key person risk</h3><p>Turn it is all in the promoter's head into a documented, resilient system.</p></div>
      <div class="card reveal"><div class="ic">{icon('cash')}</div><h3>Stronger footing with lenders</h3><p>An independent read on how you run your money strengthens your case and speeds up credit and funding conversations.</p></div>
      <div class="card reveal"><div class="ic">{icon('users')}</div><h3>Trust with buyers and boards</h3><p>An outside standard that reassures the people who decide whether to back you.</p></div>
      <div class="card reveal"><div class="ic">{icon('award')}</div><h3>A mark that is earned, not bought</h3><p>Financially Smart Organisation carries weight because it is assessed against a published standard and decided by the Council.</p></div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--wash);">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:44px;">
      <p class="eyebrow center">The path to certification</p>
      <h2 class="h-lg">Transparent, from first score to the public register</h2>
    </div>
    <div class="card-grid cols-4">
      <div class="card step reveal"><div class="num">1</div><h3>Assess</h3><p>Clear the line at an FSO Assessment, 76 and above, with every domain floor met and no open red flag.</p></div>
      <div class="card step reveal"><div class="num">2</div><h3>Conformity checks</h3><p>A different lead assessor confirms the practices scored at the Assessment still operate, and tests the signed declarations.</p></div>
      <div class="card step reveal"><div class="num">3</div><h3>Council decision</h3><p>The FSO Council reviews the file and decides. FSO 360 is applied at this step. The certificate shows no score.</p></div>
      <div class="card step reveal"><div class="num">4</div><h3>Certify and renew</h3><p>A one year certificate, the mark licence, and a place on the public register. Renewed each year with a fresh Assessment.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">What you walk away with</p>
        <h2 class="h-lg">Value whether or not you certify on day one</h2>
        <ul class="check-list">
          <li>A private, defensible score across every part of your finances.</li>
          <li>A Gap Report that ranks every gap, with a rupee value at stake on each.</li>
          <li>A closing meeting that walks your team through the findings.</li>
          <li>The FSO Improvement Guide, to close the gaps at your own pace.</li>
          <li>At Certification, a one year certificate, the mark licence and a place on the public register.</li>
        </ul>
        <a class="btn btn-primary mt-m" href="contact.html">Book a Discovery Call <span class="ar">&#8594;</span></a>
      </div>
      <div class="reveal">
        <div class="card-grid cols-1" style="gap:16px;">
          <div class="card card--soft"><div class="ic">{icon('lock')}</div><h3>The score stays private</h3><p>Your FSO Score is for you. It is never published, and the certificate itself shows no score. Only the fact of certification is public.</p></div>
          <div class="card card--soft"><div class="ic">{icon('refresh')}</div><h3>Valid one year, then renewed</h3><p>Certification sits on an Assessment no older than 90 days, is valid for one year, and is renewed through a fresh Assessment and Certification.</p></div>
          <div class="card card--soft"><div class="ic">{icon('scale')}</div><h3>Decided independently</h3><p>A different lead assessor at Certification, and the FSO Council decides. Fees are never linked to your score or outcome.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--wash);">
  <div class="wrap">
    <div class="center reveal" style="margin-bottom:40px;">
      <p class="eyebrow center">Questions, answered</p>
      <h2 class="h-lg">Frequently asked</h2>
    </div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

{cta_band()}
"""

# =====================================================================
#  CONTACT
# =====================================================================
contact = f"""
<section class="page-hero dark">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div style="max-width:720px;">
      <p class="breadcrumbs reveal"><a href="index.html">Home</a><span>/</span>Contact</p>
      <p class="eyebrow on-dark reveal">Let us talk</p>
      <h1 class="h-xl reveal">Book a Discovery Call, or start with your score.</h1>
      <p class="lede reveal">Whether you want to certify your business, understand your diagnostic result, or just understand where you stand, we are glad to help. Tell us a little and we will be in touch.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split" style="align-items:start;">
      <div class="reveal" id="enquiry">
        <div class="form-card">
          <h2 class="h-md" style="margin-bottom:6px;">Send us a message</h2>
          <p class="muted" style="font-size:14px;margin-bottom:22px;">We usually reply within one business day.</p>
          <form data-mock-form novalidate>
            <div class="grid2">
              <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="c-company">Company</label><input id="c-company" name="company" type="text" autocomplete="organization"></div>
            </div>
            <div class="grid2">
              <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
              <div class="field"><label for="c-phone">Mobile</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
            </div>
            <div class="field">
              <label for="c-topic">I am interested in</label>
              <select id="c-topic" name="topic">
                <option>The FSO Assessment</option>
                <option>FSO Certification</option>
                <option>Understanding my FSO diagnostic result</option>
                <option>Partnership or something else</option>
              </select>
            </div>
            <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" placeholder="Tell us a little about your business"></textarea></div>
            <div class="form-ok" role="status">Thanks, your message has been sent. We usually reply within one business day.</div>
            <button class="btn btn-primary btn-block btn-lg" type="submit">Send message <span class="ar">&#8594;</span></button>
          </form>
        </div>
      </div>
      <div class="reveal">
        <p class="eyebrow">Other ways to reach us</p>
        <h2 class="h-md" style="margin-bottom:22px;">Prefer to talk?</h2>
        <div class="contact-aside">
          <div class="contact-item"><div class="ic">{icon('phone')}</div><div><h4>Call us</h4><p><a href="tel:+919311646714" style="font-weight:600;">+91 93116 46714</a></p></div></div>
          <div class="contact-item"><div class="ic">{icon('mail')}</div><div><h4>Email</h4><p><a href="mailto:connect@fsoworld.com">connect@fsoworld.com</a></p></div></div>
          <div class="contact-item"><div class="ic">{icon('target')}</div><div><h4>Know your score first</h4><p>Not sure where you stand? <a href="#" data-open-diagnostic style="font-weight:600;">Take the six minute diagnostic &#8594;</a></p></div></div>
          <div class="contact-item"><div class="ic">{icon('doc')}</div><div><h4>Existing client?</h4><p>Access your assessment in the <a href="{APP}" rel="noopener" style="font-weight:600;">FSO Portal &#8594;</a></p></div></div>
        </div>
        <p class="muted" style="font-size:13px;margin-top:20px;">Issued by the FSO Council. FSO Global Standards Private Limited.</p>
      </div>
    </div>
  </div>
</section>
"""

# =====================================================================
#  DIAGNOSTIC (standalone)
# =====================================================================
diagnostic = f"""
<section class="page-hero dark" style="padding-bottom:clamp(30px,4vw,50px);">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="center" style="max-width:640px;margin-inline:auto;">
      <p class="eyebrow on-dark center reveal">Free. No sign up to see your score.</p>
      <h1 class="h-xl reveal">The FSO Diagnostic</h1>
      <p class="lede center reveal">Fifteen questions, about six minutes. One indicative score and a view across the areas FSO assesses. A quick reality check on how financially smart your company is, before the full FSO Assessment.</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:clamp(28px,4vw,44px);background:var(--wash);">
  <div class="wrap" style="max-width:720px;">
    <div id="diagnostic-page-root" class="reveal in"></div>
    <p class="center muted mt-m" style="font-size:13px;">An indicative self check, not the formal FSO Assessment. We will email your score and breakdown to the address you provide, and never share it.</p>
  </div>
</section>
"""

# =====================================================================
#  404
# =====================================================================
notfound = f"""
<section class="page-hero dark" style="min-height:70vh;display:flex;align-items:center;">
  <div class="emblem-bg" aria-hidden="true"></div>
  <div class="wrap center">
    <p class="eyebrow on-dark center">404</p>
    <h1 class="h-xl">This page took a different route.</h1>
    <p class="lede center mt-s" style="margin-inline:auto;">The page you are looking for is not here, but your FSO score is only six minutes away.</p>
    <div class="btn-group center mt-m">
      <a class="btn btn-light btn-lg" href="index.html">Back to home</a>
      <button class="btn btn-ghost on-dark btn-lg" type="button" data-open-diagnostic>Know Your FSO Score</button>
    </div>
  </div>
</section>
"""

# =====================================================================
#  FOUNDER
# =====================================================================
FOUNDER = """
<style>
  .fdr-eyebrow{font:700 12px Inter,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#0A38C0;display:flex;align-items:center;gap:10px;}
  .fdr-eyebrow::before{content:"";width:26px;height:2px;background:#0A38C0;display:inline-block;}
  .fdr-hero{padding:56px 0 26px;}
  .fdr-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:44px;align-items:center;}
  .fdr-hero h1{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-1px;font-size:46px;line-height:1.08;margin:16px 0 8px;color:#0C1B36;}
  .fdr-hero h1 em{font-style:normal;background:linear-gradient(90deg,#0A38C0,#19C2D6);-webkit-background-clip:text;background-clip:text;color:transparent;}
  .fdr-who{font-size:18px;color:#5A6B86;margin:14px 0 0;}
  .fdr-who b{color:#0C1B36;}
  .fdr-who .abbr{color:#8792A8;}
  .fdr-lede{font-size:18px;color:#5A6B86;margin:16px 0 0;max-width:42ch;}
  .fdr-portrait{position:relative;}
  .fdr-portrait img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:20px;border:1px solid #E7ECF5;display:block;box-shadow:0 30px 60px -30px rgba(10,56,192,.35);}
  .fdr-badge{position:absolute;left:-14px;bottom:22px;background:#fff;border:1px solid #E7ECF5;border-radius:14px;padding:12px 15px;box-shadow:0 18px 40px -20px rgba(12,27,64,.4);}
  .fdr-badge .n{font:800 20px Archivo,sans-serif;color:#0A38C0;}
  .fdr-badge .l{font:600 11px Inter,sans-serif;letter-spacing:.4px;color:#5A6B86;text-transform:uppercase;}
  .fdr-creds{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:30px 0 8px;}
  .fdr-cred{background:#fff;border:1px solid #E7ECF5;border-radius:14px;padding:18px 15px;text-align:center;}
  .fdr-cred .ic{width:34px;height:34px;border-radius:9px;background:#EEF3FD;color:#0A38C0;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;font-size:17px;}
  .fdr-cred .t{font:700 14px Inter,sans-serif;color:#0C1B36;}
  .fdr-cred .s{font:500 12.5px Inter,sans-serif;color:#5A6B86;margin-top:3px;}
  .fdr-note{padding:30px 0 8px;}
  .fdr-card{background:#fff;border:1px solid #E7ECF5;border-radius:20px;padding:40px 44px;max-width:820px;margin:0 auto;box-shadow:0 24px 60px -40px rgba(12,27,64,.28);}
  .fdr-card h2{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.5px;font-size:27px;line-height:1.2;margin:6px 0 18px;color:#0C1B36;}
  .fdr-card p{font-size:16.5px;line-height:1.7;color:#31425E;margin:0 0 18px;}
  .fdr-card p.big{font-size:19px;color:#0C1B36;font-weight:500;}
  .fdr-pull{border-left:3px solid #0A38C0;background:#F1F5FE;border-radius:12px;padding:18px 22px;margin:26px 0;font:600 18px/1.5 Archivo,sans-serif;color:#0C1B36;}
  .fdr-sign{margin-top:26px;padding-top:22px;border-top:1px solid #E7ECF5;}
  .fdr-sign .nm{font:800 16px Archivo,sans-serif;color:#0C1B36;}
  .fdr-sign .rl{font:500 13px Inter,sans-serif;color:#5A6B86;}
  .fdr-band{background:linear-gradient(120deg,#0A38C0,#123FC9);color:#fff;border-radius:22px;margin:44px auto;padding:40px;max-width:960px;text-align:center;}
  .fdr-band h2{font-family:Archivo,sans-serif;font-weight:800;font-size:27px;margin:0 0 8px;color:#fff;}
  .fdr-band p{color:#C9D6FA;margin:0 0 22px;}
  .fdr-band .row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
  .fdr-band .fbtn{display:inline-block;font:600 15px Inter,sans-serif;padding:13px 22px;border-radius:12px;border:1px solid transparent;cursor:pointer;text-decoration:none;}
  .fdr-band .fbtn.solid{background:#fff;color:#0A38C0;}
  .fdr-band .fbtn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.45);}
  @media(max-width:820px){
    .fdr-grid{grid-template-columns:1fr;}
    .fdr-hero h1{font-size:34px;}
    .fdr-portrait{max-width:330px;}
    .fdr-creds{grid-template-columns:repeat(2,1fr);}
    .fdr-card{padding:28px 22px;}
    .fdr-band{padding:30px 22px;}
  }
</style>

<section class="fdr-hero">
  <div class="wrap fdr-grid">
    <div>
      <p class="fdr-eyebrow">The Founder</p>
      <h1>Why I built <em>FSO.</em></h1>
      <p class="fdr-who"><b>Prashant Narang</b> <span class="abbr">(PRN)</span> &middot; Founder and Director</p>
      <p class="fdr-lede">A Chartered Accountant who spent 25 years watching good businesses run blind on their numbers, and decided to build the standard that fixes it.</p>
    </div>
    <div class="fdr-portrait">
      <img src="assets/img/founder.jpg?v=1" alt="Prashant Narang, Founder of FSO" width="1000" height="1250" decoding="async">
      <div class="fdr-badge"><div class="n">25+</div><div class="l">Years as a CA</div></div>
    </div>
  </div>

  <div class="wrap">
    <div class="fdr-creds">
      <div class="fdr-cred"><div class="ic">&#9670;</div><div class="t">Chartered Accountant</div><div class="s">All India Rank Holder, ICAI</div></div>
      <div class="fdr-cred"><div class="ic">&#9733;</div><div class="t">Founder and CEO</div><div class="s">Erito NXT</div></div>
      <div class="fdr-cred"><div class="ic">&#9998;</div><div class="t">Author</div><div class="s">Four Bucket Cash Flow</div></div>
      <div class="fdr-cred"><div class="ic">&#9673;</div><div class="t">TEDx Speaker</div><div class="s">The Power of Clarity</div></div>
    </div>
  </div>
</section>

<section class="fdr-note">
  <div class="wrap">
    <div class="fdr-card">
      <p class="fdr-eyebrow">Why I started FSO</p>
      <h2>Good businesses should not fail for reasons they never saw coming.</h2>
      <p class="big">For 25 years as a Chartered Accountant, I have sat across the table from hundreds of founders, brilliant at their craft, building real companies, yet flying blind on the one thing that quietly decides whether they survive and scale, how well they run their money.</p>
      <p>I kept seeing the same story. Profitable on paper, starved of cash. Growing in revenue, leaking in margin. Working harder every year with less and less to show for it. Not because these founders were not smart, but because no one had ever given them a clear, objective picture of what financially smart actually looks like, or an honest way to measure themselves against it.</p>
      <p>My whole career has been about turning that black box into something an owner can see and act on, from the <b>Four Bucket Cash Flow</b> method in my book, to the idea at the heart of my TEDx talk, clarity. Clarity about where your money sits, where it leaks, and where it should go next.</p>
      <div class="fdr-pull">World class enterprises are built on world class financial management. My mission is to make every business owner financially smart.</div>
      <p>FSO is that belief, made measurable. One clear score. The domains that decide whether you keep the money you make and grow with confidence. And a certificate your bank, your board and your buyers can trust, because it is measured against a real standard and decided by an independent Council, not an opinion.</p>
      <p>I built the standard I wish every founder I ever advised had been handed on day one. If it helps you run your business with more clarity and less fear, it will have done its job.</p>
      <div class="fdr-sign">
        <div class="nm">Prashant Narang</div>
        <div class="rl">Founder and Director, FSO Global Standards Private Limited &middot; Founder and CEO, Erito NXT &middot; <a href="https://www.linkedin.com/in/prashantnarang/" rel="noopener">LinkedIn &#8599;</a> &middot; <a href="https://youtu.be/dEXEKDNezqA" rel="noopener">Watch the TEDx talk &#8599;</a></div>
      </div>
    </div>
  </div>
</section>

<div class="wrap">
  <div class="fdr-band">
    <h2>See where your business stands</h2>
    <p>The same thinking I have brought to hundreds of founders, now a six minute score for you.</p>
    <div class="row">
      <button class="fbtn solid" type="button" data-open-diagnostic>Know Your FSO Score &#8594;</button>
      <a class="fbtn ghost" href="certification.html">Apply for Certification</a>
    </div>
  </div>
</div>
"""

# =====================================================================
#  BUILD
# =====================================================================
prep_public()

page("index.html", "FSO Financially Smart Organisation | Assessment and Certification",
     "FSO is an independent assessment and certification of how well a company plans, controls, reports and protects its money. A private score out of 100 across 38 criteria and nine domains.",
     home, "index.html")

page("about.html", "About FSO | Why the Financial Maturity Standard Exists",
     "FSO defines what it means to be financially smart, running your money as a designed system, and turns it into a measurable score, a maturity scale and an independent certificate.",
     about, "about.html")

page("founder.html", "About the Founder | Prashant Narang | FSO",
     "Why Prashant Narang, Chartered Accountant, All India rank holder, author of Four Bucket Cash Flow and TEDx speaker, built FSO, the Financially Smart Organisation standard.",
     FOUNDER, "founder.html")

page("standard.html", "The FSO Standard | An Objective Measure of Financial Maturity",
     "What makes the FSO Standard credible, a structured, objective, evidence based method that turns how a company runs its money into one comparable score out of 100 across 38 criteria.",
     standard, "standard.html")

page("services.html", "Services | FSO Diagnostic, Discovery Call, Assessment and Certification",
     "FSO services, a free six minute diagnostic and Discovery Call, then two paid steps, the FSO Assessment and FSO Certification. We measure and certify, and do not sell the fix.",
     services, "services.html")

page("certification.html", "FSO Certification | Independent Financial Maturity Certification",
     "Get an independent, evidence based FSO Assessment and, if you clear the line, a certificate decided by the FSO Council that shows your finances are built to last.",
     certification, "certification.html")

page("contact.html", "Contact FSO | Book a Discovery Call",
     "Talk to the FSO team about the Assessment, Certification, or understanding your diagnostic result. Call +91 93116 46714 or send a message. We usually reply within one business day.",
     contact, "contact.html")

page("diagnostic.html", "FSO Diagnostic | Know Your FSO Score in Six Minutes",
     "Take the free FSO Diagnostic for an indicative, no sign up read on how financially smart your company is, across the areas that matter most, before the full FSO Assessment.",
     diagnostic, "diagnostic.html")

page("404.html", "Page not found | FSO",
     "The page you are looking for is not here. Head back to FSO or take the six minute FSO Diagnostic.",
     notfound, "index.html")

print("\nAll pages generated.")
