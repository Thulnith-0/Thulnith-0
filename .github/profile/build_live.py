"""Builds the live GitHub cards (stats, streak, languages, activity, achievements,
daily joke) from the GitHub GraphQL API. Run by .github/workflows/profile-cards.yml.

    GITHUB_TOKEN=... python .github/profile/build_live.py dist
    python .github/profile/build_live.py dist --sample     # offline preview data
"""

from __future__ import annotations

import json
import math
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import content as C
from design import W, esc, panel, pulse, svg, text, text_width, write_pair

API = "https://api.github.com/graphql"

# Build/config files that aren't really "languages I write".
IGNORED_LANGS = {"Batchfile", "Makefile", "Dockerfile", "Procfile", "CMake", "Inno Setup", "NSIS", "PowerShell"}

# ------------------------------------------------------------------------------- data

# `user(login:)` only lists public repos. When the token belongs to the profile
# owner, `viewer` also lists their private repos, so the build uses that instead.
PROFILE_FIELDS = """
    login
    createdAt
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, after: $after) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        isFork
        isPrivate
        stargazerCount
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
"""
Q_PROFILE = "query($login: String!, $after: String) { user(login: $login) {" + PROFILE_FIELDS + "} }"
Q_VIEWER = "query($after: String) { viewer {" + PROFILE_FIELDS + "} }"
Q_WHOAMI = "query { viewer { login } }"

Q_YEAR = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def gql(query: str, variables: dict, token: str) -> dict:
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-cards"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]


def fetch(login: str, token: str) -> dict:
    try:
        as_owner = gql(Q_WHOAMI, {}, token)["viewer"]["login"].lower() == login.lower()
    except Exception:  # the Actions bot token can't query viewer
        as_owner = False
    repos, after = [], None
    while True:
        if as_owner:
            u = gql(Q_VIEWER, {"after": after}, token)["viewer"]
        else:
            u = gql(Q_PROFILE, {"login": login, "after": after}, token)["user"]
        repos += u["repositories"]["nodes"]
        page = u["repositories"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        after = page["endCursor"]

    private = sum(r["isPrivate"] for r in repos)
    print(f"querying as {'owner (viewer)' if as_owner else 'public user'}: "
          f"{len(repos)} repos ({private} private)")
    created = datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    days: dict[str, int] = {}
    start = created
    while start < now:
        end = min(start + timedelta(days=365), now)
        cc = gql(Q_YEAR, {"login": login, "from": start.isoformat(), "to": end.isoformat()}, token)["user"][
            "contributionsCollection"
        ]
        for wk in cc["contributionCalendar"]["weeks"]:
            for d in wk["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        start = end

    langs: dict[str, int] = {}
    for r in repos:
        if r["isFork"]:
            continue
        for e in r["languages"]["edges"]:
            if e["node"]["name"] in IGNORED_LANGS:
                continue
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]

    last_year = [v for k, v in days.items() if k > (now - timedelta(days=365)).date().isoformat()]
    return {
        "created": created.date().isoformat(),
        "followers": u["followers"]["totalCount"],
        "prs": u["pullRequests"]["totalCount"],
        "issues": u["issues"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "langs": langs,
        "days": dict(sorted(days.items())),
        "year_total": sum(last_year),
    }


def sample() -> dict:
    """Plausible fake data for previews only; never published."""
    import random

    rnd = random.Random(7)
    today = date.today()
    days = {}
    for i in range(700, -1, -1):
        d = today - timedelta(days=i)
        days[d.isoformat()] = 0 if rnd.random() < 0.35 else int(rnd.expovariate(1 / 6)) + 1
    for i in range(9):
        days[(today - timedelta(days=i)).isoformat()] = rnd.randint(2, 14)
    return {
        "created": "2024-11-30",
        "followers": 12,
        "prs": 38,
        "issues": 9,
        "repos": 39,
        "stars": 21,
        "langs": {"Python": 900_000, "TypeScript": 520_000, "JavaScript": 410_000, "C#": 260_000,
                  "Java": 180_000, "HTML": 120_000, "CSS": 90_000, "Dart": 60_000, "Kotlin": 20_000},
        "days": days,
        "year_total": sum(v for k, v in days.items() if k > (today - timedelta(days=365)).isoformat()),
    }


# ------------------------------------------------------------------------------ helpers


def streaks(days: dict[str, int]) -> tuple[int, int]:
    """(current, longest). Today with no contributions yet doesn't break the streak."""
    items = sorted(days.items())
    longest = run = 0
    for _, v in items:
        run = run + 1 if v > 0 else 0
        longest = max(longest, run)
    current = 0
    rev = list(reversed(items))
    if rev and rev[0][1] == 0:
        rev = rev[1:]
    for _, v in rev:
        if v == 0:
            break
        current += 1
    return current, longest


def age(created: str) -> str:
    c = date.fromisoformat(created)
    t = date.today()
    months = (t.year - c.year) * 12 + t.month - c.month - (t.day < c.day)
    y, m = divmod(months, 12)
    parts = ([f"{y} yr"] if y else []) + ([f"{m} mo"] if m else [])
    return " ".join(parts) or "new"


def fmt(n: int) -> str:
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 10_000 else f"{n:,}"


def card(t, w, h, body, title):
    return svg(w, h, panel(t, w, h, r=22) + body, title)


# -------------------------------------------------------------------------------- cards

HALF = 433


def stats_card(d):
    def render(t, mode):
        w, h, x = HALF, 250, 28
        body = [
            f'<g class="f d1">{text(x, 44, "CONTRIBUTIONS · LAST 12 MONTHS", 11.5, t["accent"], 700, spacing=1.6)}</g>',
            f'<g class="f d1">{pulse(w - x - 40, 40, 3.5, "#34A853")}{text(w - x, 44, "Live", 12, t["text2"], 600, anchor="end")}</g>',
            f'<g class="f d2">{text(x - 2, 104, fmt(d["year_total"]), 56, t["text"], 700, spacing=-2)}</g>',
            f'<g class="f d2">{text(x, 130, "On GitHub for " + age(d["created"]) + ", since " + datetime.fromisoformat(d["created"]).strftime("%b %Y"), 13.5, t["text2"], 500)}</g>',
            f'<line x1="{x}" y1="152" x2="{w - x}" y2="152" stroke="{t["line"]}"/>',
        ]
        metrics = [("Repos", d["repos"]), ("Stars", d["stars"]), ("PRs", d["prs"]), ("Followers", d["followers"])]
        cw = (w - 2 * x) / 4
        for i, (label, v) in enumerate(metrics):
            mx = x + i * cw
            body.append(
                f'<g class="f d{i + 3}">'
                + text(mx, 196, fmt(v), 26, t["text"], 700, spacing=-0.8)
                + text(mx, 220, label, 12.5, t["text2"], 500)
                + "</g>"
            )
        return card(t, w, h, "".join(body), f'{d["year_total"]} contributions in the last year')

    return render


def streak_card(d):
    cur, best = streaks(d["days"])
    total = sum(d["days"].values())

    def render(t, mode):
        w, h, x = HALF, 250, 28
        cx, cy, r = w - 98, 125, 66
        frac = 1.0 if best == 0 else max(0.02, min(1.0, cur / best))
        circ = 2 * math.pi * r
        dash = circ * frac
        css_ring = (
            f".ring{{stroke-dasharray:{dash:.1f} {circ:.1f};animation:ring 1.6s cubic-bezier(.2,.7,.2,1) .3s backwards}}"
            f"@keyframes ring{{from{{stroke-dasharray:0 {circ:.1f}}}}}"
        )
        a, b = t["grad"]
        defs = f'<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        body = (
            f'<g class="f d1">{text(x, 44, "STREAK", 11.5, t["accent"], 700, spacing=1.6)}</g>'
            + f'<g class="f d2">{text(x - 2, 104, str(cur), 56, t["text"], 700, spacing=-2)}'
            + text(x + text_width(str(cur), 56, 700) - 2 + 8, 104, "days", 18, t["text2"], 600)
            + text(x, 130, "Current streak", 13.5, t["text2"], 500)
            + "</g>"
            + f'<line x1="{x}" y1="152" x2="{cx - r - 26}" y2="152" stroke="{t["line"]}"/>'
            + '<g class="f d3">'
            + text(x, 196, str(best), 26, t["text"], 700, spacing=-0.8)
            + text(x, 220, "Longest", 12.5, t["text2"], 500)
            + text(x + 96, 196, fmt(total), 26, t["text"], 700, spacing=-0.8)
            + text(x + 96, 220, "All-time", 12.5, t["text2"], 500)
            + "</g>"
            + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["track"]}" stroke-width="16"/>'
            + f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#rg)" stroke-width="16" '
            f'stroke-linecap="round" transform="rotate(-90 {cx} {cy})"/>'
            + f'<g class="f d4">{text(cx, cy + 6, f"{round(frac * 100)}%", 20, t["text"], 700, anchor="middle")}'
            + text(cx, cy + 25, "of best", 11, t["text2"], 500, anchor="middle")
            + "</g>"
        )
        return svg(w, h, panel(t, w, h, r=22) + body, f"Current streak {cur} days, longest {best}", css_ring, defs)

    return render


def languages_card(d):
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: -kv[1])
    shown = top[:7]
    rest = sum(v for _, v in top[7:])
    if rest:
        shown.append(("Other", rest))

    def render(t, mode):
        x, h = 28, 196
        bw = W - 2 * x
        body = [f'<g class="f d1">{text(x, 44, "LANGUAGES · BY CODE SIZE", 11.5, t["accent"], 700, spacing=1.6)}</g>']
        clip = f'<clipPath id="bar"><rect x="{x}" y="66" width="{bw}" height="14" rx="7"/></clipPath>'
        bx, segs = x, []
        for i, (name, v) in enumerate(shown):
            sw = bw * v / total
            segs.append(
                f'<rect x="{bx:.1f}" y="66" width="{max(sw - 2, 0.5):.1f}" height="14" fill="{t["ramp"][i % 8]}"/>'
            )
            bx += sw
        body.append(f'<g class="f d2" clip-path="url(#bar)">{"".join(segs)}</g>')
        cols, col_w = 4, bw / 4
        for i, (name, v) in enumerate(shown):
            lx = x + (i % cols) * col_w
            ly = 122 + (i // cols) * 36
            pct = f"{100 * v / total:.1f}%"
            body.append(
                f'<g class="f d{3 + i // cols}">'
                f'<circle cx="{lx + 5}" cy="{ly - 4.5}" r="5" fill="{t["ramp"][i % 8]}"/>'
                + text(lx + 18, ly, name, 14, t["text"], 600)
                + text(lx + 18 + text_width(name, 14, 600) + 8, ly, pct, 13, t["text2"], 500)
                + "</g>"
            )
        title = "Languages: " + ", ".join(f"{n} {100 * v / total:.1f}%" for n, v in shown)
        return svg(W, h, panel(t, W, h, r=22) + "".join(body), title, defs=clip)

    return render


def activity_card(d):
    today = date.today()
    series = [(today - timedelta(days=i)) for i in range(29, -1, -1)]
    vals = [d["days"].get(s.isoformat(), 0) for s in series]

    def render(t, mode):
        x, h = 28, 250
        top, bottom = 78, 200
        bw = W - 2 * x
        peak = max(vals) or 1
        step = bw / (len(vals) - 1)
        pts = [(x + i * step, bottom - (bottom - top) * v / peak) for i, v in enumerate(vals)]

        def smooth(points):
            p = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
            for (x0, y0), (x1, y1) in zip(points, points[1:]):
                mx = (x0 + x1) / 2
                p += f" C{mx:.1f},{y0:.1f} {mx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
            return p

        line = smooth(pts)
        area = line + f" L{pts[-1][0]:.1f},{bottom} L{pts[0][0]:.1f},{bottom} Z"
        a, b = t["grad"]
        defs = (
            f'<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
            f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}" stop-opacity=".22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>'
        )
        length = 2400
        css = (
            f".ln{{stroke-dasharray:{length};animation:draw 2s cubic-bezier(.2,.7,.2,1) .2s backwards}}"
            f"@keyframes draw{{from{{stroke-dashoffset:{length}}}}}"
        )
        grid = "".join(
            f'<line x1="{x}" y1="{gy:.1f}" x2="{W - x}" y2="{gy:.1f}" stroke="{t["line"]}" stroke-dasharray="2 5"/>'
            for gy in (top, (top + bottom) / 2, bottom)
        )
        month = f"{series[0].strftime('%b %d')}  –  {series[-1].strftime('%b %d')}"
        body = (
            f'<g class="f d1">{text(x, 44, "ACTIVITY · LAST 30 DAYS", 11.5, t["accent"], 700, spacing=1.6)}</g>'
            + f'<g class="f d1">{text(W - x, 44, f"{sum(vals)} contributions · peak {peak}/day", 13, t["text2"], 500, anchor="end")}</g>'
            + grid
            + f'<path d="{area}" fill="url(#ar)" class="f d2"/>'
            + f'<path class="ln" d="{line}" fill="none" stroke="url(#ln)" stroke-width="3" stroke-linecap="round"/>'
            + pulse(pts[-1][0], pts[-1][1], 5, b)
            + text(x, 230, series[0].strftime("%b %d"), 12, t["text3"], 500)
            + text(W - x, 230, "Today", 12, t["text3"], 500, anchor="end")
        )
        return svg(W, h, panel(t, W, h, r=22) + body, f"{sum(vals)} contributions in the last 30 days ({month})",
                   css, defs)

    return render


def heatmap_card(d):
    """Contribution calendar in the accent ramp, revealed by a diagonal wave."""
    today = date.today()
    start = today - timedelta(days=52 * 7 + (today.weekday() + 1) % 7)  # a Sunday ~1 year back
    days = [(start + timedelta(days=i)) for i in range((today - start).days + 1)]
    vals = [d["days"].get(x.isoformat(), 0) for x in days]
    nz = sorted(v for v in vals if v > 0)
    cuts = [nz[int(len(nz) * q)] for q in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]

    def level(v):
        if v == 0:
            return 0
        return 1 + sum(v > c for c in cuts)

    def render(t, mode):
        x0, y0, cell, gap = 52, 74, 12, 3.2
        a = t["accent"]
        shades = [t["track"]] + [f'{a}{op}' for op in ("55", "88", "c4", "")]
        weeks = (len(days) + 6) // 7
        h = y0 + 7 * (cell + gap) + 58
        cells, months, last_m = [], [], None
        for i, (dt, v) in enumerate(zip(days, vals)):
            col, row = i // 7, (dt.weekday() + 1) % 7
            x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
            delay = 0.2 + (col + row) * 0.018
            cells.append(
                f'<rect class="hc" style="animation-delay:{delay:.2f}s" x="{x:.1f}" y="{y:.1f}" width="{cell}" '
                f'height="{cell}" rx="3" fill="{shades[level(v)]}"/>'
            )
            if row == 0 and dt.month != last_m and dt.day <= 7:
                months.append(text(x, y0 - 12, dt.strftime("%b"), 11.5, t["text2"], 500))
                last_m = dt.month
        rows = "".join(text(x0 - 12, y0 + r * (cell + gap) + 10, n, 11, t["text3"], 500, anchor="end")
                       for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
        total = sum(vals)
        lx = W - 28 - 5 * (cell + 4) - 34
        legend = (text(lx - 8, h - 22, "Less", 11, t["text3"], 500, anchor="end")
                  + "".join(f'<rect x="{lx + k * (cell + 4):.1f}" y="{h - 32}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
                            for k, c in enumerate(shades))
                  + text(lx + 5 * (cell + 4) + 4, h - 22, "More", 11, t["text3"], 500))
        css = (".hc{transform-box:fill-box;transform-origin:center;animation:hc .6s cubic-bezier(.2,.8,.3,1.2) backwards}"
               "@keyframes hc{from{opacity:0;transform:scale(.3)}}")
        body = (
            f'<g class="f d1">{text(28, 44, "CONTRIBUTION CALENDAR", 11.5, t["accent"], 700, spacing=1.6)}</g>'
            + f'<g class="f d1">{text(W - 28, 44, "One square per day", 13, t["text2"], 500, anchor="end")}</g>'
            + "".join(months) + rows + "".join(cells) + legend
        )
        return svg(W, h, panel(t, W, h, r=22) + body, f"Contribution calendar: {total} contributions over the last 53 weeks", css)

    return render


TIERS = [("Bronze", "#c08457"), ("Silver", "#9aa3ad"), ("Gold", "#d4a72c"), ("Platinum", None)]


def achievements_card(d):
    years = (date.today() - date.fromisoformat(d["created"])).days / 365.25
    total = sum(d["days"].values())
    items = [
        ("Years", years, (1, 2, 3, 5), f"{years:.1f}"),
        ("Repos", d["repos"], (10, 25, 50, 100), fmt(d["repos"])),
        ("Contributions", total, (100, 500, 1000, 5000), fmt(total)),
        ("Pull requests", d["prs"], (5, 25, 100, 500), fmt(d["prs"])),
        ("Stars", d["stars"], (1, 10, 50, 100), fmt(d["stars"])),
        ("Followers", d["followers"], (1, 10, 50, 100), fmt(d["followers"])),
    ]

    def render(t, mode):
        x, h = 28, 230
        n = len(items)
        cw = (W - 2 * x) / n
        body = [f'<g class="f d1">{text(x, 44, "ACHIEVEMENTS", 11.5, t["accent"], 700, spacing=1.6)}</g>']
        for i, (label, v, steps, shown) in enumerate(items):
            tier = sum(v >= s for s in steps) - 1
            cx, cy, r = x + cw * i + cw / 2, 118, 40
            if tier < 0:
                ring, name = t["line"], "Locked"
            else:
                name, ring = TIERS[tier]
                ring = ring or t["accent"]
            body.append(
                f'<g class="f d{min(i + 1, 6)}">'
                f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{t["chip"]}" stroke="{ring}" stroke-width="4"/>'
                f'<circle cx="{cx:.1f}" cy="{cy}" r="{r - 9}" fill="none" stroke="{ring}" stroke-opacity=".35"/>'
                + text(cx, cy + 7, shown, 20 if len(shown) < 5 else 16, t["text"], 700, anchor="middle", spacing=-0.5)
                + text(cx, 186, label, 13, t["text"], 600, anchor="middle")
                + text(cx, 205, name, 11.5, ring if tier >= 0 else t["text3"], 600, anchor="middle")
                + "</g>"
            )
        return svg(W, h, panel(t, W, h, r=22) + "".join(body),
                   "Achievements: " + ", ".join(f"{l} {s}" for l, _, _, s in items))

    return render


JOKES = [
    ("There are 10 kinds of people:", "those who understand binary and those who don't."),
    ("A SQL query walks into a bar,", "goes up to two tables and asks: “Can I join you?”"),
    ("I would tell you a UDP joke,", "but you might not get it."),
    ("It works on my machine.", "Then we'll ship your machine."),
    ("Debugging: being the detective", "in a crime movie where you're also the murderer."),
    ("Why do programmers prefer dark mode?", "Because light attracts bugs."),
    ("A programmer's partner says “Get a loaf, and if they have eggs, get a dozen.”", "They come home with 12 loaves."),
    ("There are two hard things in computer science:", "cache invalidation, naming things, and off-by-one errors."),
    ("To understand recursion,", "you must first understand recursion."),
    ("Weeks of coding", "can save you hours of planning."),
    ("I don't always test my code,", "but when I do, I do it in production."),
    ("Why did the developer go broke?", "They used up all their cache."),
    ("!false", "— it's funny because it's true."),
    ("Git commit -m “final”,", "git commit -m “final final”, git commit -m “ok this one”."),
    ("Why do Java developers wear glasses?", "Because they don't C#."),
    ("The best thing about a Boolean:", "even if you're wrong, you're only off by a bit."),
    ("Programming is 10% writing code", "and 90% figuring out why it doesn't work."),
    ("Knock knock. Race condition.", "Who's there?"),
    ("My code doesn't have bugs.", "It has surprise features."),
    ("How many programmers does it take to change a light bulb?", "None. That's a hardware problem."),
]


def thought_card(_d):
    q, a = JOKES[date.today().toordinal() % len(JOKES)]

    def render(t, mode):
        x, h = 28, 132
        size = 18 if text_width(q, 18, 600) < W - 2 * x else 15.5
        body = (
            f'<g class="f d1">{text(x, 44, "TODAY’S DEV JOKE", 11.5, t["accent"], 700, spacing=1.6)}</g>'
            + f'<g class="f d2">{text(x, 78, q, size, t["text"], 600, spacing=-0.2)}</g>'
            + f'<g class="f d4">{text(x, 104, a, 15, t["text2"], 500)}</g>'
        )
        return svg(W, h, panel(t, W, h, r=22) + body, f"{q} {a}")

    return render


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "dist")
    if "--sample" in sys.argv:
        d = sample()
    else:
        token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN (or PROFILE_TOKEN) is required; use --sample for preview data")
        d = fetch(C.LOGIN, token)
    for name, fn in [
        ("stats", stats_card),
        ("streak", streak_card),
        ("languages", languages_card),
        ("activity", activity_card),
        ("heatmap", heatmap_card),
        ("achievements", achievements_card),
        ("joke", thought_card),
    ]:
        write_pair(out, name, fn(d))
    cur, best = streaks(d["days"])
    print(f"wrote cards to {out}: {d['year_total']} contributions/yr, streak {cur}/{best}, {len(d['langs'])} languages")


if __name__ == "__main__":
    main()
