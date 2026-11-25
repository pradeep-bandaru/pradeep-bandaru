"""GitHub profile graphics, v2: one design system, light + dark variants of every panel.

Usage: py -3 make_profile_v2.py <assets_dir>
Everything is static-visible; motion is decorative only (knee pulse, flow dashes) and respects reduced motion.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
FF = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
W = 1200

THEMES = {
    "dark": dict(bg0="#0B1020", bg1="#111833", bg2="#17113A", card="#111827", card2="#0F172A", line="#263043", txt="#F1F5F9",
                 sub="#CBD5E1", mut="#8B98AE", faint="#FFFFFF", faint_op=".06", cyan="#22D3EE", violet="#A78BFA", pink="#F472B6",
                 green="#34D399", amber="#FBBF24", blue="#60A5FA", pill="#1E293B", pill_t="#E2E8F0", glow=".30"),
    "light": dict(bg0="#FFFFFF", bg1="#F6F7FF", bg2="#EFEAFF", card="#FFFFFF", card2="#F8FAFC", line="#D8DEE8", txt="#0F172A",
                  sub="#334155", mut="#5B6577", faint="#0F172A", faint_op=".06", cyan="#0E7490", violet="#6D28D9", pink="#BE185D",
                  green="#047857", amber="#B45309", blue="#1D4ED8", pill="#EEF2F7", pill_t="#1E293B", glow=".16"),
}


def width(text, size, bold=False):
    return len(text) * size * (0.585 if bold else 0.53)


def wrap(text, size, maxw):
    lines, cur = [], ""
    for w_ in text.split():
        t = (cur + " " + w_).strip()
        if width(t, size) > maxw and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = t
    return lines + [cur]


def svg(h, body, label, t, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(label)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg0']}"/><stop offset=".6" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
  <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['cyan']}"/><stop offset=".55" stop-color="{t['violet']}"/><stop offset="1" stop-color="{t['pink']}"/></linearGradient>
  <style>text{{font-family:{FF}}} {extra_css}
  @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
</defs>
{body}
</svg>'''


def frame(h, t, grad=True):
    fill = "url(#bg)" if grad else t["card"]
    return (f'<rect width="{W}" height="{h}" rx="20" fill="{fill}"/>'
            f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="20" fill="none" stroke="{t["line"]}"/>')


def T(x, y, s, size, fill, weight=400, anchor="start", extra=""):
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'


def kicker(x, y, s, t, color=None):
    return T(x, y, s, 15, color or t["cyan"], 700, extra='letter-spacing="2.4"')


# ------------------------------------------------------------------------------------------------ 1. header
def header(t):
    H = 360
    x0, x1, y0, y1 = 790, 1136, 292, 74
    pts = []
    for i in range(121):
        u = 0.04 + 0.915 * i / 120
        r = 1 / (1 - u)
        pts.append((x0 + (x1 - x0) * i / 120, y0 - min(r, 12.5) / 12.5 * (y0 - y1)))
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = path + f" L{x1},{y0} L{x0},{y0} Z"
    sla = y0 - 4.0 / 12.5 * (y0 - y1)
    kx = next(x for x, y in pts if y <= sla)
    grid = "".join(f'<line x1="{x0}" y1="{y:.0f}" x2="{x1}" y2="{y:.0f}" stroke="{t["faint"]}" stroke-opacity="{t["faint_op"]}"/>' for y in [y1 + k * (y0 - y1) / 4 for k in range(5)])
    grid += "".join(f'<line x1="{x:.0f}" y1="{y1}" x2="{x:.0f}" y2="{y0}" stroke="{t["faint"]}" stroke-opacity="{t["faint_op"]}"/>' for x in [x0 + k * (x1 - x0) / 4 for k in range(5)])
    css = (f".pulse{{transform-origin:{kx:.1f}px {sla:.1f}px;animation:pulse 2.2s ease-out infinite;opacity:0}}"
           "@keyframes pulse{0%{transform:scale(1);opacity:.65}100%{transform:scale(3.4);opacity:0}}")
    body = frame(H, t) + f'''
<radialGradient id="glow" cx=".82" cy=".25" r=".55"><stop offset="0" stop-color="{t['violet']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['violet']}" stop-opacity="0"/></radialGradient>
<rect width="{W}" height="{H}" rx="20" fill="url(#glow)"/>
{kicker(64, 92, "PERFORMANCE ENGINEERING  ·  ML FOR SYSTEMS", t)}
<text x="61" y="166" font-size="70" font-weight="800" fill="{t['txt']}" letter-spacing="-1">Pradeep Bandaru</text>
{T(64, 214, "Senior Performance Engineer", 30, t['txt'], 600)}
<rect x="64" y="236" width="88" height="4" rx="2" fill="url(#acc)"/>
{T(64, 278, "Capgemini  ·  Royal Bank of Canada  ·  8+ years in banking & financial services", 19, t['sub'])}
{T(64, 308, "MSc Data Science & AI, BITS Pilani  ·  Hyderabad, India", 19, t['mut'])}
{grid}
<line x1="{x0}" y1="{sla:.1f}" x2="{x1}" y2="{sla:.1f}" stroke="{t['amber']}" stroke-width="1.6" stroke-dasharray="6 6"/>
{T(x1, sla - 10, "SLA", 15, t['amber'], 700, "end")}
<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['violet']}" stop-opacity=".30"/><stop offset="1" stop-color="{t['violet']}" stop-opacity="0"/></linearGradient>
<path d="{area}" fill="url(#ar)"/>
<path d="{path}" fill="none" stroke="url(#acc)" stroke-width="4.5" stroke-linecap="round"/>
<circle cx="{kx:.1f}" cy="{sla:.1f}" r="7" fill="{t['pink']}" class="pulse"/>
<circle cx="{kx:.1f}" cy="{sla:.1f}" r="6.5" fill="{t['bg1']}" stroke="{t['pink']}" stroke-width="3"/>
{T(kx - 16, sla - 16, "find the knee before users do", 16, t['pink'], 700, "end")}
{T(x0, y0 + 30, "load  →", 15, t['mut'], 600)}
{T(x0 - 14, (y0 + y1) / 2, "p95 latency", 15, t['mut'], 600, "middle", f'transform="rotate(-90 {x0 - 14} {(y0 + y1) / 2:.0f})"')}'''
    return svg(H, body, "Pradeep Bandaru, Senior Performance Engineer at Capgemini for Royal Bank of Canada", t, css)


# ------------------------------------------------------------------------------------------------ 2. impact strip
def impact(t):
    H = 214
    tiles = [("98%", "less manual effort", "multi-region test orchestration", "cyan"),
             ("4h → 5m", "load-generator analysis", "25+ generators, one dashboard", "violet"),
             ("85–90%", "faster test-data prep", "bulk banking test data", "pink"),
             ("4", "innovation awards", "2024 – 2026", "green")]
    n, gap, pad = len(tiles), 18, 28
    tw = (W - 2 * pad - (n - 1) * gap) / n
    body = frame(H, t, grad=False)
    for i, (v, l, s, c) in enumerate(tiles):
        x = pad + i * (tw + gap)
        col = t[c]
        body += (f'<rect x="{x:.0f}" y="{pad}" width="{tw:.0f}" height="{H - 2 * pad}" rx="14" fill="{t["card2"]}" stroke="{t["line"]}"/>'
                 f'<rect x="{x + 24:.0f}" y="{pad + 26}" width="34" height="4" rx="2" fill="{col}"/>'
                 + T(x + 24, pad + 84, v, 46, col, 800, extra='letter-spacing="-1"')
                 + T(x + 24, pad + 117, l, 19, t["txt"], 600)
                 + T(x + 24, pad + 143, s, 16, t["mut"]))
    return svg(H, body, "Impact: 98% less manual effort, load-generator analysis from 4 hours to 5 minutes, 85-90% faster test-data preparation, 4 innovation awards", t)


# ------------------------------------------------------------------------------------------------ 3. PerfOracle card
def perforacle(t):
    H = 520
    steps = [("Connect", "20 tool formats"), ("Align", "one clock"), ("Understand", "test phases"), ("Correlate", "every layer"),
             ("Predict", "1.5–7× load"), ("Experiment", "rank the fixes"), ("Decide", "cited verdict")]
    cols = ["cyan", "cyan", "blue", "blue", "violet", "violet", "pink"]
    body = frame(H, t)
    body += kicker(64, 74, "FEATURED PROJECT  ·  BAMS HACKATHON 2026", t, t["violet"])
    body += f'<text x="62" y="128" font-size="46" font-weight="800" fill="{t["txt"]}" letter-spacing="-.5">PerfOracle</text>'
    body += T(64, 168, "Will your application survive 3× the users? Know before your customers find out.", 22, t["sub"])
    chips = ["Python", "Queueing theory", "Conformal prediction", "JVM & G1 GC", "Dynatrace · OpenShift · Oracle"]
    cx = 64
    for c in chips:
        w = width(c, 15, True) + 30
        body += (f'<rect x="{cx:.0f}" y="192" width="{w:.0f}" height="32" rx="16" fill="{t["pill"]}" stroke="{t["line"]}"/>'
                 + T(cx + w / 2, 213, c, 15, t["pill_t"], 600, "middle"))
        cx += w + 10
    sx0, sx1, sy = 120, 1080, 290
    gap = (sx1 - sx0) / (len(steps) - 1)
    body += f'<line x1="{sx0}" y1="{sy}" x2="{sx1}" y2="{sy}" stroke="url(#acc)" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round" class="dash"/>'
    for i, ((s, d), c) in enumerate(zip(steps, cols)):
        x = sx0 + i * gap
        body += (f'<circle cx="{x:.0f}" cy="{sy}" r="24" fill="{t["card"]}" stroke="{t[c]}" stroke-width="2.5"/>'
                 + T(x, sy + 7, str(i + 1), 18, t[c], 800, "middle")
                 + T(x, sy + 56, s, 18, t["txt"], 700, "middle")
                 + T(x, sy + 79, d, 15, t["mut"], 400, "middle"))
    mets = [("2.7%", "median capacity error", "vs 45% linear baseline", "cyan"), ("93.8%", "go / no-go accuracy", "60 held-out scenarios", "violet"),
            ("85%", "calibrated band coverage", "split-conformal", "pink"), ("~3 s", "per investigation", "from files to decision", "green")]
    n, g, pad = 4, 16, 64
    tw = (W - 2 * pad - (n - 1) * g) / n
    for i, (v, l, s, c) in enumerate(mets):
        x = pad + i * (tw + g)
        body += (f'<rect x="{x:.0f}" y="398" width="{tw:.0f}" height="92" rx="14" fill="{t["card"]}" fill-opacity=".7" stroke="{t["line"]}"/>'
                 + T(x + 20, 440, v, 32, t[c], 800) + T(x + 20, 464, l, 16, t["txt"], 600) + T(x + 20, 482, s, 14, t["mut"]))
    css = ".dash{animation:flow 1.4s linear infinite}@keyframes flow{to{stroke-dashoffset:-22}}"
    return svg(H, body, "PerfOracle: predicts whether an application survives 3x load. 2.7% median capacity error, 93.8% go/no-go accuracy", t, css)


# ------------------------------------------------------------------------------------------------ 4. accelerators
def accelerators(t):
    items = [("SATM-E2E-Utility", "Innovator of the Quarter · 2026", "cyan",
              "Automates multi-region execution setup, dynamic region consolidation, hourly SMM collection, artifact management and run orchestration.",
              "98% less manual effort"),
             ("LG-Metrics-Extractor", "RBC CAA Award · 2024", "violet",
              "Monitors 25+ load generators from one place: health checks, service management, saturation detection and consolidated reporting.",
              "Analysis time: 4+ hours → under 5 minutes"),
             ("Copilot AI agents", "AI Innovator Award · 2026", "pink",
              "Agents for production log analysis, workload modelling, LoadRunner script review, report generation and executive performance insights.",
              "Faster turnaround on recurring analysis"),
             ("Cheque-Generation-Utility", "RBC Rising Star Award · 2025", "green",
              "Generates bulk, realistic banking test data on demand, so test cycles no longer wait on manual data preparation.",
              "85–90% less test-data effort")]
    pad, g = 28, 18
    cw = (W - 2 * pad - g) / 2
    ch = 262
    H = pad * 2 + ch * 2 + g
    body = frame(H, t, grad=False)
    for i, (name, award, c, desc, metric) in enumerate(items):
        x = pad + (i % 2) * (cw + g)
        y = pad + (i // 2) * (ch + g)
        col = t[c]
        body += (f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="{ch}" rx="14" fill="{t["card2"]}" stroke="{t["line"]}"/>'
                 f'<rect x="{x:.0f}" y="{y + 22}" width="4" height="62" rx="2" fill="{col}"/>'
                 + T(x + 28, y + 42, "★  " + award.upper(), 13.5, col, 700, extra='letter-spacing="1.4"')
                 + T(x + 28, y + 78, name, 25, t["txt"], 700))
        for k, ln in enumerate(wrap(desc, 17, cw - 56)[:3]):
            body += T(x + 28, y + 118 + k * 26, ln, 17, t["sub"])
        body += (f'<line x1="{x + 28:.0f}" y1="{y + ch - 58}" x2="{x + cw - 28:.0f}" y2="{y + ch - 58}" stroke="{t["line"]}"/>'
                 + T(x + 28, y + ch - 24, metric, 19, col, 700))
    return svg(H, body, "Award-winning engineering accelerators: SATM-E2E-Utility, LG-Metrics-Extractor, Copilot AI agents, Cheque-Generation-Utility", t)


# ------------------------------------------------------------------------------------------------ 5. experience
def experience(t):
    roles = [("2022 – PRESENT", "Senior Consultant", "Capgemini", "Royal Bank of Canada · CCTMP, DCP", "cyan",
              "End-to-end performance engineering for multiple lines of business: NFRs, workload models, Dynatrace root cause and production sign-off."),
             ("2017 – 2019", "Senior Software Engineer", "Capgemini", "Royal Bank of Canada · Wealth Management", "violet",
              "Performance testing for the Canadian and US wealth-management suite before UAT, with sign-off reports and tuning advice."),
             ("2015 – 2017", "Software Engineer", "Capgemini", "Associated Bank · MGM Resorts", "pink",
              "LoadRunner scripting, workload design and SLA triage for a US regional bank and a global booking platform.")]
    pad, g = 28, 18
    cw = (W - 2 * pad - 2 * g) / 3
    H = 336
    body = frame(H, t, grad=False)
    for i, (yrs, role, co, client, c, desc) in enumerate(roles):
        x = pad + i * (cw + g)
        col = t[c]
        body += (f'<rect x="{x:.0f}" y="{pad}" width="{cw:.0f}" height="{H - 2 * pad}" rx="14" fill="{t["card2"]}" stroke="{t["line"]}"/>'
                 f'<rect x="{x:.0f}" y="{pad}" width="{cw:.0f}" height="4" rx="2" fill="{col}"/>'
                 + T(x + 24, pad + 42, yrs, 14, col, 700, extra='letter-spacing="1.6"')
                 + T(x + 24, pad + 76, role, 23, t["txt"], 700)
                 + T(x + 24, pad + 103, co, 17, t["sub"], 600)
                 + T(x + 24, pad + 126, client, 15.5, t["mut"]))
        for k, ln in enumerate(wrap(desc, 16, cw - 48)[:5]):
            body += T(x + 24, pad + 164 + k * 24, ln, 16, t["sub"])
    return svg(H, body, "Experience: Capgemini, Royal Bank of Canada, 2015 to present", t)


# ------------------------------------------------------------------------------------------------ 6. toolbox
def toolbox(t):
    rows = [("Performance testing", ["LoadRunner Enterprise", "Apache JMeter", "k6", "Postman", "SoapUI"], "cyan"),
            ("Monitoring & APM", ["Dynatrace", "AppDynamics", "Grafana", "PerfMon"], "blue"),
            ("Languages", ["Python", "SQL", "PowerShell", "JavaScript", "VBScript", "C", "SAP ABAP"], "violet"),
            ("Data & AI", ["pandas", "NumPy", "Power BI", "Tableau", "Excel", "Copilot AI agents"], "pink"),
            ("Databases", ["Oracle", "SQL Server", "IBM Db2", "MySQL"], "amber"),
            ("Diagnostics", ["Fiddler", "Wireshark", "Chrome DevTools"], "green"),
            ("Delivery", ["Git", "GitHub", "Jira", "Confluence", "qTest", "CI/CD"], "mut")]
    pad, rh = 40, 54
    H = pad * 2 + rh * len(rows) - 14
    body = frame(H, t, grad=False)
    for i, (cat, tools, c) in enumerate(rows):
        y = pad + i * rh
        col = t[c]
        body += f'<circle cx="{pad + 6}" cy="{y + 18}" r="5" fill="{col}"/>' + T(pad + 24, y + 24, cat, 18, t["txt"], 700)
        x = 290
        for tool in tools:
            w = width(tool, 16, False) + 32
            body += (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="36" rx="10" fill="{t["pill"]}" stroke="{t["line"]}"/>'
                     + T(x + w / 2, y + 24, tool, 16, t["pill_t"], 500, "middle"))
            x += w + 10
        if i < len(rows) - 1:
            body += f'<line x1="{pad}" y1="{y + rh - 9}" x2="{W - pad}" y2="{y + rh - 9}" stroke="{t["line"]}" stroke-opacity=".6"/>'
    return svg(H, body, "Toolbox: LoadRunner Enterprise, JMeter, k6, Dynatrace, AppDynamics, Grafana, Python, SQL, Oracle and more", t)


for name, fn in (("header", header), ("perforacle", perforacle), ("accelerators", accelerators),
                 ("experience", experience), ("toolbox", toolbox)):
    for th, pal in THEMES.items():
        (OUT / f"{name}-{th}.svg").write_text(fn({**pal, "mut": pal["mut"]}), encoding="utf-8")
print("ok", sorted(p.name for p in OUT.glob("*.svg")))
