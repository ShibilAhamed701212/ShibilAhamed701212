"""Regenerate assets/github-3d.svg from the GitHub API.

Env: GH_TOKEN (required), STATS_TOKEN_SET=1 when GH_TOKEN is a personal token that can see private repos.
"""
import collections, datetime, json, os, pathlib, re, urllib.request

LOGIN = "ShibilAhamed701212"
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN = os.environ["GH_TOKEN"]


def api(path, body=None):
    url = "https://api.github.com" + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "stats-graphic",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


QUERY = """query($login:String!){ user(login:$login){
  repositories(ownerAffiliations:OWNER){totalCount}
  contributionsCollection{
    totalCommitContributions totalPullRequestContributions
    contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount weekday } } }
  } } }"""
d = api("/graphql", {"query": QUERY, "variables": {"login": LOGIN}})["data"]["user"]
c = d["contributionsCollection"]
cal = c["contributionCalendar"]
weeks = cal["weeks"]

repos, page = [], 1
list_path = "/user/repos?affiliation=owner" if os.environ.get("STATS_TOKEN_SET") else f"/users/{LOGIN}/repos?type=owner"
while True:
    batch = api(f"{list_path}{'&' if '?' in list_path else '?'}per_page=100&page={page}")
    repos += batch
    if len(batch) < 100:
        break
    page += 1
tot = collections.Counter()
for r in repos:
    if r["fork"]:
        continue
    tot.update(api(f"/repos/{r['full_name']}/languages"))
total_bytes = sum(tot.values()) or 1
langs = [(k, round(v / total_bytes * 100, 2)) for k, v in tot.most_common(6)]
TODAY = datetime.date.today().isoformat()

T = 10.0                       # tile size
CX, CY = 0.866, 0.5
OX, OY = 104, 262
S = T * 0.86
HMAX = 78

counts = [x["contributionCount"] for w in weeks for x in w["contributionDays"]]
mx = max(counts)
nz = sorted(x for x in counts if x)
q = [nz[int(len(nz) * p)] for p in (0.25, 0.5, 0.75)]
def level(n):
    if n == 0: return 0
    return 1 + sum(n > t for t in q)
PAL = {1: (120, 18, 30), 2: (170, 22, 36), 3: (205, 28, 42), 4: (227, 25, 45)}
def hexc(rgb, k):
    return "#%02x%02x%02x" % tuple(min(255, int(v * k)) for v in rgb)
def P(x, y, z):
    return (OX + (x - y) * CX, OY + (x + y) * CY - z)
def poly(pts, fill, extra=""):
    return '<polygon points="%s" fill="%s"%s/>' % (" ".join("%.1f,%.1f" % p for p in pts), fill, extra)

cells = []
for i, w in enumerate(weeks):
    for x in w["contributionDays"]:
        j = x["weekday"]
        cells.append((i + j, i, j, x["contributionCount"]))
cells.sort()

flat, bars = [], []
tallest = (0, None)
for _, i, j, n in cells:
    x0, y0 = i * T, j * T
    lv = level(n)
    if lv == 0:
        pts = [P(x0, y0, 0), P(x0 + S, y0, 0), P(x0 + S, y0 + S, 0), P(x0, y0 + S, 0)]
        flat.append(poly(pts, "#131316", ' stroke="#1b1b1f" stroke-width=".5"'))
        continue
    h = 3 + n / mx * HMAX
    rgb = PAL[lv]
    top = [P(x0, y0, h), P(x0 + S, y0, h), P(x0 + S, y0 + S, h), P(x0, y0 + S, h)]
    right = [P(x0 + S, y0, 0), P(x0 + S, y0 + S, 0), P(x0 + S, y0 + S, h), P(x0 + S, y0, h)]
    left = [P(x0, y0 + S, 0), P(x0 + S, y0 + S, 0), P(x0 + S, y0 + S, h), P(x0, y0 + S, h)]
    g = '<g class="b" style="animation-delay:%dms">%s%s%s</g>' % (
        i * 28, poly(left, hexc(rgb, .5)), poly(right, hexc(rgb, .72)), poly(top, hexc(rgb, 1.0)))
    bars.append(g)
    if n > tallest[0]:
        tallest = (n, P(x0 + S / 2, y0 + S / 2, h))

active = sum(1 for x in counts if x)
tiles = [
    (str(c["totalCommitContributions"]), "COMMITS"),
    (str(c["totalPullRequestContributions"]), "PULL REQUESTS"),
    (str(d["repositories"]["totalCount"]), "REPOSITORIES"),
    (str(active), "ACTIVE DAYS"),
]
tile_svg = []
for k, (num, lab) in enumerate(tiles):
    x = 600 + (k % 2) * 162
    y = 44 + (k // 2) * 96
    tile_svg.append(f'''<g class="rise" style="animation-delay:{150+k*120}ms">
      <rect x="{x}" y="{y}" width="150" height="84" rx="10" fill="#0e0e11" stroke="#ece8e1" stroke-opacity=".12"/>
      <rect x="{x}" y="{y}" width="3" height="84" rx="1.5" fill="#e3192d"/>
      <text x="{x+20}" y="{y+50}" class="display" font-size="40" fill="#ece8e1">{num}</text>
      <text x="{x+20}" y="{y+70}" class="mono" font-size="9.5" letter-spacing="1.5" fill="#8d8a86">{lab}</text>
    </g>''')

RED = ["#e3192d", "#c11f25", "#9c1a22", "#7d1620", "#5f111b", "#4a0f18"]
lang_svg = []
top_pct = langs[0][1]
for k, (name, pct) in enumerate(langs):
    y = 292 + k * 44
    w = max(8, pct / top_pct * 290)
    x = 600
    col = RED[k]
    def sh(hx, f):
        r, g_, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
        return "#%02x%02x%02x" % (int(r * f), int(g_ * f), int(b * f))
    front = f'<rect x="{x}" y="{y+8}" width="{w:.1f}" height="12" fill="{col}"/>'
    topf = f'<polygon points="{x},{y+8} {x+7},{y+2} {x+w+7:.1f},{y+2} {x+w:.1f},{y+8}" fill="{sh(col,1.25)}"/>'
    endf = f'<polygon points="{x+w:.1f},{y+8} {x+w+7:.1f},{y+2} {x+w+7:.1f},{y+14} {x+w:.1f},{y+20}" fill="{sh(col,.6)}"/>'
    lang_svg.append(f'''<g class="rise" style="animation-delay:{500+k*90}ms">
      <text x="{x}" y="{y-4}" class="mono" font-size="11" fill="#ece8e1">{name}</text>
      <text x="912" y="{y-4}" class="mono" font-size="11" fill="#8d8a86" text-anchor="end">{pct:.1f}%</text>
      <g class="slab" style="animation-delay:{600+k*90}ms">{front}{topf}{endf}</g>
    </g>''')

# faint background grid
grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="600" />' for x in range(48, 960, 96)) + \
       "".join(f'<line x1="0" y1="{y}" x2="960" y2="{y}" />' for y in range(40, 600, 96))

tx, ty = tallest[1]
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600" role="img" aria-label="GitHub activity: {cal['totalContributions']} contributions in the last year, shown as a 3D isometric skyline with commit, pull request, repository and language stats">
  <defs>
    <radialGradient id="glow" cx="0.35" cy="0.6" r="0.6">
      <stop offset="0" stop-color="#e3192d" stop-opacity=".18"/>
      <stop offset="1" stop-color="#e3192d" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect width="960" height="600" rx="18"/></clipPath>
  </defs>
  <style>
    .display {{ font-family: Anton, Impact, 'Arial Narrow', sans-serif; }}
    .mono {{ font-family: 'JetBrains Mono', Menlo, Consolas, monospace; }}
    .b {{ transform-box: fill-box; transform-origin: 50% 100%; animation: grow 1s cubic-bezier(.2,.8,.2,1) both; }}
    .slab {{ transform-box: fill-box; transform-origin: 0 50%; animation: wide 1s cubic-bezier(.2,.8,.2,1) both; }}
    .sky {{ animation: float 7s ease-in-out infinite; }}
    .beacon {{ transform-box: fill-box; transform-origin: center; animation: ping 2.4s ease-out infinite; }}
    .rise {{ animation: rise .9s ease-out both; }}
    @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
    @keyframes wide {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-6px); }} }}
    @keyframes ping {{ 0% {{ transform: scale(.6); opacity: .9; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .b, .slab, .sky, .beacon, .rise {{ animation: none; }} }}
  </style>
  <g clip-path="url(#frame)">
    <rect width="960" height="600" fill="#09090b"/>
    <rect width="960" height="600" fill="url(#glow)"/>
    <g stroke="#ece8e1" stroke-opacity=".035">{grid}</g>

    <text x="48" y="58" class="mono" font-size="12" letter-spacing="2" fill="#e3192d">// GITHUB ACTIVITY</text>
    <text x="46" y="148" class="display" font-size="96" fill="#ece8e1">{cal['totalContributions']}</text>
    <text x="50" y="174" class="mono" font-size="11" letter-spacing="1.8" fill="#8d8a86">CONTRIBUTIONS · LAST 12 MONTHS</text>

    <g class="sky">
      {"".join(flat)}
      {"".join(bars)}
      <circle class="beacon" cx="{tx:.1f}" cy="{ty:.1f}" r="4" fill="#e3192d"/>
      <circle cx="{tx:.1f}" cy="{ty:.1f}" r="3" fill="#ffffff"/>
    </g>

    {"".join(tile_svg)}

    <text x="600" y="256" class="mono" font-size="10" letter-spacing="1.8" fill="#8d8a86">MOST USED LANGUAGES</text>
    <line x1="600" y1="264" x2="912" y2="264" stroke="#ece8e1" stroke-opacity=".12"/>
    {"".join(lang_svg)}

    <text x="48" y="580" class="mono" font-size="9.5" letter-spacing="1.2" fill="#4a4946">SOURCE: GITHUB API · SNAPSHOT {TODAY} · PEAK DAY {mx}</text>
  </g>
</svg>
'''
(ROOT / "assets" / "github-3d.svg").write_text(svg)
print("ok", len(svg), "bars", len(bars), "flat", len(flat), "peak", mx, "tallest at", tx, ty)

readme = ROOT / "README.md"
txt = readme.read_text()
txt = re.sub(r'assets/github-3d\.svg(\?v=\d+)?', "assets/github-3d.svg?v=" + TODAY.replace("-", ""), txt)
readme.write_text(txt)
