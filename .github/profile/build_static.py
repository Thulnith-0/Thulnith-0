"""Renders the static profile artwork into /assets (light + dark versions).

    python .github/profile/build_static.py
"""

from __future__ import annotations

from pathlib import Path

import content as C
from design import (MONO, W, chip, esc, glint, google_dots, icon, panel, pulse, shifting_gradient, svg,
                    text, text_width, wrap, write_pair)

OUT = Path(__file__).resolve().parents[2] / "assets"


def grad_def(t, gid="g", x2="1"):
    a, b = t["grad"]
    return shifting_gradient(gid, a, b)


# --------------------------------------------------------------------------- hero


def hero(t, mode):
    h = 420
    a, b = t["grad"]
    defs = (
        grad_def(t)
        + '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>'
        + f'<clipPath id="clip"><rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="28"/></clipPath>'
    )
    css = (
        ".orb{animation:drift 14s ease-in-out infinite alternate}"
        ".o2{animation-duration:18s}.o3{animation-duration:22s}"
        "@keyframes drift{from{transform:translate(0,0)}to{transform:translate(-36px,22px)}}"
    )
    g = t["glow"]
    orbs = (
        f'<g clip-path="url(#clip)" filter="url(#blur)">'
        f'<circle class="orb" cx="760" cy="120" r="120" fill="{a}" opacity="{g}"/>'
        f'<circle class="orb o2" cx="690" cy="300" r="95" fill="{b}" opacity="{g * 0.85}"/>'
        f'<circle class="orb o3" cx="850" cy="320" r="70" fill="#34A853" opacity="{g * 0.45}"/>'
        f"</g>"
    )
    l1, l2a, l2b, l2c = C.HEADLINE
    x = 56
    body = [
        panel(t, W, h, r=28),
        orbs,
        f'<g class="f d1">{google_dots(x + 4, 74)}'
        + text(x + 62, 79, "HELLO, I'M", 13, t["text2"], 600, spacing=2.4)
        + "</g>",
        f'<g class="f d2">{text(x - 3, 170, C.NAME + ".", 76, t["text"], 700, spacing=-2.6)}</g>',
        f'<g class="f d3">{text(x, 228, l1, 27, t["text2"], 500, spacing=-0.4)}</g>',
        f'<g class="f d4"><text x="{x}" y="264" font-size="27" font-weight="500" letter-spacing="-0.4" '
        f'fill="{t["text2"]}">{esc(l2a)}<tspan fill="url(#g)" font-weight="700">{esc(l2b)}</tspan>{esc(l2c)}</text></g>',
    ]
    # meta row: one <text> so the browser lays it out (no width guessing)
    sep = f'<tspan fill="{t["text3"]}">  ·  </tspan>'
    meta = sep.join(esc(m) for m in C.META)
    body.append(f'<g class="f d5"><text x="{x}" y="345" font-size="15" font-weight="500" fill="{t["text2"]}" xml:space="preserve">{meta}</text></g>')
    body.append(
        f'<g class="f d6">{text(x, 378, "github.com/" + C.LOGIN, 13, t["text3"], 500, family=MONO)}</g>'
    )
    return svg(W, h, "".join(body), f"{C.NAME}. {l1} {l2a}{l2b}{l2c}", css, defs)


# --------------------------------------------------------------------------- section titles


def section(eyebrow, title):
    def render(t, mode):
        h = 96
        body = (
            f'<g class="f d1">{text(2, 30, eyebrow.upper(), 12.5, t["accent"], 700, spacing=2.2)}</g>'
            f'<g class="f d2">{text(0, 76, title, 40, t["text"], 700, spacing=-1.2)}</g>'
        )
        return svg(W, h, body, f"{eyebrow}: {title}")

    return render


SECTIONS = {
    "highlights": ("Highlights", "Numbers I'm proud of."),
    "work": ("Selected work", "Things I've built."),
    "stack": ("Toolkit", "What I build with."),
    "github": ("On GitHub", "The live numbers."),
    "connect": ("Say hello", "Let's connect."),
}


# --------------------------------------------------------------------------- highlights


def highlights(t, mode):
    n, gap, h = len(C.HIGHLIGHTS), 14, 176
    tw = (W - gap * (n - 1)) / n
    body, defs, css = [], [grad_def(t, x2="1")], []
    sheen, strength = ("#ffffff", 0.9) if mode == "light" else ("#ffffff", 0.07)
    for i, (big, l1, l2) in enumerate(C.HIGHLIGHTS):
        x = i * (tw + gap)
        size = 40 if text_width(big, 40, 700) < tw - 44 else 32
        fill = "url(#g)" if i == 0 else t["text"]
        gd, gb, gc = glint(f"h{i}", x + 0.5, 0.5, tw - 1, h - 1, 20, sheen, strength, 2.2 + i * 0.35, 10)
        defs.append(gd)
        css.append(gc)
        body.append(
            f'<g class="f d{i + 1}">'
            f'<rect x="{x + 0.5:.1f}" y="0.5" width="{tw - 1:.1f}" height="{h - 1}" rx="20" '
            f'fill="{t["card"]}" stroke="{t["panel_line"]}"/>'
            + gb
            + text(x + 24, 78, big, size, fill, 700, spacing=-1.4)
            + text(x + 24, 122, l1, 13.5, t["text2"], 500)
            + text(x + 24, 142, l2, 13.5, t["text2"], 500)
            + "</g>"
        )
    return svg(W, h, "".join(body), "Highlights: " + "; ".join(f"{a} {b} {c}" for a, b, c in C.HIGHLIGHTS),
               "".join(css), "".join(defs))


# --------------------------------------------------------------------------- project cards

CARD_W, CARD_H = 433, 286


def project(p, idx=0):
    def render(t, mode):
        w, h, x = CARD_W, CARD_H, 28
        sheen, strength = ("#ffffff", 0.9) if mode == "light" else ("#ffffff", 0.06)
        gd, gb, gc = glint("p", 0.5, 0.5, w - 1, h - 1, 22, sheen, strength, 1.6 + (idx // 2) * 0.5 + (idx % 2) * 0.25, 11)
        body = [
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="{t["card"]}" stroke="{t["panel_line"]}"/>',
            gb,
            f'<g class="f d1">{text(x, 44, p["area"].upper(), 11.5, t["accent"], 700, spacing=1.6)}</g>',
        ]
        # status pill, top right; public ones get a Material-style live dot
        public = p["kind"] == "public"
        label = "Public  ↗" if public else "Private"
        col = (t["chip"] if mode == "light" else "#0d1117") if public else t["text2"]
        dot = 14 if public else 0
        pw = text_width(label, 11.5, 600) + 24 + dot
        px = w - x - pw
        body.append(
            f'<g class="f d1"><rect x="{px:.1f}" y="26" width="{pw:.1f}" height="26" rx="13" '
            f'fill="{t["text"] if public else "none"}" stroke="{t["text"] if public else t["line"]}"/>'
            + (pulse(px + 15, 39, 3.2, "#34A853") if public else "")
            + text(px + dot + (pw - dot) / 2, 43.5, label, 11.5, col, 600, anchor="middle")
            + "</g>"
        )
        title_size = 27 if text_width(p["name"], 27, 700) < w - 2 * x else 23
        body.append(f'<g class="f d2">{text(x - 1, 92, p["name"], title_size, t["text"], 700, spacing=-0.7)}</g>')
        lines = wrap(p["desc"], 14.5, w - 2 * x)[:4]
        body.append(
            '<g class="f d3">'
            + "".join(text(x, 126 + i * 22, ln, 14.5, t["text2"], 400) for i, ln in enumerate(lines))
            + "</g>"
        )
        cx, chips = x, []
        for ic, label in p["tags"]:
            s, cw = chip(t, cx, h - 28 - 28, label, 12, ic, 28)
            if cx + cw > w - x:
                break
            chips.append(s)
            cx += cw + 8
        body.append(f'<g class="f d4">{"".join(chips)}</g>')
        return svg(w, h, "".join(body), f'{p["name"]} ({p["kind"]}): {p["desc"]}', gc, gd)

    return render


# --------------------------------------------------------------------------- stack


def stack(t, mode):
    row_h, label_w, pad = 52, 128, 30
    rows = []
    y = pad
    for gi, (group, items) in enumerate(C.STACK):
        cx, line_y, chips = pad + label_w, y, []
        for ic, label in items:
            s, cw = chip(t, 0, 0, label, 12.5, ic, 32)
            if cx + cw > W - pad:
                cx, line_y = pad + label_w, line_y + 42
            s, cw = chip(t, cx, line_y, label, 12.5, ic, 32)
            chips.append(s)
            cx += cw + 8
        rows.append(
            f'<g class="f d{min(gi + 1, 6)}">'
            + text(pad, y + 21, group, 14, t["text"], 600)
            + "".join(chips)
            + "</g>"
        )
        y = line_y + row_h
    h = y - row_h + 32 + pad
    sep = []
    return svg(W, h, panel(t, W, h, r=24) + "".join(sep) + "".join(rows),
               "Toolkit: " + "; ".join(f"{g}: {', '.join(l for _, l in it)}" for g, it in C.STACK))


# --------------------------------------------------------------------------- social buttons


def social(item, idx=0):
    ic, name, _handle, _url = item

    def render(t, mode):
        h, size, fs, pad = 40, 15, 13.5, 16
        w = pad + size + 8 + text_width(name, fs, 600) + pad
        bg = t["text"]
        fg = "#ffffff" if mode == "light" else "#0d1117"
        body = (
            f'<rect x="0.5" y="0.5" width="{w - 1:.1f}" height="{h - 1}" rx="{h / 2}" fill="{bg}"/>'
            + icon(ic, pad, (h - size) / 2, size, fg)
            + text(pad + size + 8, h / 2 + fs * 0.36, name, fs, fg, 600)
        )
        sheen, strength = ("#ffffff", 0.35) if mode == "light" else (t["accent"], 0.28)
        gd, gb, gc = glint("s", 0.5, 0.5, w - 1, h - 1, h / 2, sheen, strength, 2 + idx * 0.18, 8)
        return svg(round(w), h, body + gb, name, gc, gd)

    return render


# --------------------------------------------------------------------------- footer


def footer(t, mode):
    h = 110
    body = (
        f'<line x1="0" y1="1" x2="{W}" y2="1" stroke="{t["line"]}"/>'
        + f'<g class="f d1">{google_dots(W / 2 - 19.5, 52, 4, 13)}</g>'
        + f'<g class="f d2">{text(W / 2, 88, "Designed and built by Thulnith Perera. Cards refresh every 12 hours.", 13, t["text3"], 500, anchor="middle")}</g>'
    )
    return svg(W, h, body, "Designed and built by Thulnith Perera")


# --------------------------------------------------------------------------- README

RAW = f"https://raw.githubusercontent.com/{C.LOGIN}/{C.LOGIN}"
LIVE = f"{RAW}/output"
# Absolute URLs: GitHub doesn't reliably rewrite relative paths inside <source srcset>.
STATIC = f"{RAW}/main/assets"


def pic(path: str, alt: str, width: str | None = "100%", live: bool = False) -> str:
    base = LIVE if live else STATIC
    w = f' width="{width}"' if width else ""
    return (
        "<picture>"
        f'<source media="(prefers-color-scheme: dark)" srcset="{base}/{path}-dark.svg">'
        f'<img src="{base}/{path}-light.svg"{w} alt="{esc(alt)}">'
        "</picture>"
    )


def link(href: str, inner: str) -> str:
    return f'<a href="{href}">{inner}</a>'


def readme() -> str:
    l1, l2a, l2b, l2c = C.HEADLINE
    out = [
        "<!-- Generated by .github/profile/build_static.py. Edit content.py, then re-run it. -->",
        "",
        f'<p align="center">{pic("hero", f"{C.NAME}. {l1} {l2a}{l2b}{l2c}")}</p>',
        "",
        f'<p align="center">{pic("sections/highlights", "Highlights")}</p>',
        f'<p align="center">{pic("highlights", "; ".join(" ".join(h) for h in C.HIGHLIGHTS))}</p>',
        "",
        "<br>",
        "",
        f'<p align="center">{pic("sections/work", "Selected work")}</p>',
    ]
    for i in range(0, len(C.PROJECTS), 2):
        cells = []
        for p in C.PROJECTS[i:i + 2]:
            img = pic(f'projects/{p["slug"]}', f'{p["name"]}: {p["desc"]}', "49%")
            if p["kind"] == "public":
                img = link(f'https://github.com/{C.LOGIN}/{p["repo"]}', img)
            cells.append(img)
        out.append(f'<p align="center">{" ".join(cells)}</p>')
    out += [
        "",
        "<br>",
        "",
        f'<p align="center">{pic("sections/stack", "Toolkit")}</p>',
        f'<p align="center">{pic("stack", "; ".join(f"{g}: " + ", ".join(l for _, l in it) for g, it in C.STACK))}</p>',
        "",
        "<br>",
        "",
        f'<p align="center">{pic("sections/github", "On GitHub")}</p>',
        f'<p align="center">{pic("stats", "GitHub stats", "49%", True)} {pic("streak", "Contribution streak", "49%", True)}</p>',
        f'<p align="center">{pic("activity", "Activity over the last 30 days", live=True)}</p>',
        f'<p align="center">{pic("languages", "Top languages", live=True)}</p>',
        f'<p align="center">{pic("achievements", "Achievements", live=True)}</p>',
        "<p align=\"center\"><picture>"
        f'<source media="(prefers-color-scheme: dark)" srcset="{LIVE}/github-contribution-grid-snake-dark.svg">'
        f'<img src="{LIVE}/github-contribution-grid-snake.svg" width="100%" alt="Contribution snake">'
        "</picture></p>",
        f'<p align="center">{pic("joke", "Today’s dev joke", live=True)}</p>',
        "",
        "<br>",
        "",
        f'<p align="center">{pic("sections/connect", "Say hello")}</p>',
        '<p align="center">'
        + " ".join(link(url, pic(f"social/{ic}", f"{name}: {handle}", None)) for ic, name, handle, url in C.SOCIALS)
        + "</p>",
        "",
        f'<p align="center">{pic("footer", "Designed and built by " + C.NAME)}</p>',
        "",
    ]
    return "\n".join(out)


def main():
    (OUT.parent / "README.md").write_text(readme(), encoding="utf-8")
    write_pair(OUT, "hero", hero)
    write_pair(OUT, "highlights", highlights)
    write_pair(OUT, "stack", stack)
    write_pair(OUT, "footer", footer)
    for key, (eb, title) in SECTIONS.items():
        write_pair(OUT / "sections", key, section(eb, title))
    for i, p in enumerate(C.PROJECTS):
        write_pair(OUT / "projects", p["slug"], project(p, i))
    for i, s in enumerate(C.SOCIALS):
        write_pair(OUT / "social", s[0], social(s, i))
    print(f"wrote static assets to {OUT}")


if __name__ == "__main__":
    main()
