"""Shared design system for every SVG on the profile README.

Apple-style layout (monochrome, generous space, big type) with a small touch
of colour: one blue-to-teal accent gradient and Google's four dots as a
signature. Every asset is rendered twice, once per GitHub theme.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ICONS = json.loads((HERE / "icons.json").read_text(encoding="utf-8"))  # Simple Icons, CC0

W = 880  # README content width; every asset scales to 100% of it

FONT = (
    "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI Variable Display', "
    "'Segoe UI', Inter, Roboto, 'Helvetica Neue', Arial, sans-serif"
)
MONO = "'SF Mono', ui-monospace, 'JetBrains Mono', 'Cascadia Code', Consolas, monospace"

GOOGLE = ("#4285F4", "#EA4335", "#FBBC04", "#34A853")

THEMES = {
    "light": {
        "panel": "#f5f5f7",
        "panel_line": "#f5f5f7",
        "card": "#f5f5f7",
        "text": "#1d1d1f",
        "text2": "#6e6e73",
        "text3": "#86868b",
        "line": "#d2d2d7",
        "chip": "#ffffff",
        "chip_line": "#e5e5ea",
        "track": "#e8e8ed",
        "accent": "#0071e3",
        "grad": ("#0071e3", "#0d9488"),  # Apple blue -> teal
        "ramp": ("#0071e3", "#3d8ef0", "#73adf6", "#a4cafa", "#8e8e93", "#aeaeb2", "#c7c7cc", "#dcdce1"),
        "glow": 0.55,
    },
    "dark": {
        "panel": "#16181d",
        "panel_line": "#262931",
        "card": "#16181d",
        "text": "#f5f5f7",
        "text2": "#a1a1a6",
        "text3": "#6e6e73",
        "line": "#2c2f36",
        "chip": "#1f2228",
        "chip_line": "#2c2f36",
        "track": "#2a2d34",
        "accent": "#2997ff",
        "grad": ("#2997ff", "#2dd4bf"),  # bright blue -> aqua
        "ramp": ("#2997ff", "#4fa6ff", "#7cbcff", "#a9d3ff", "#8e8e93", "#6e6e73", "#55565c", "#3f4046"),
        "glow": 0.35,
    },
}

# --------------------------------------------------------------------------- text

_NARROW = set("iljtfrI.,:;'!|()[] ")
_WIDE = set("mwMW@%")


def text_width(s: str, size: float, weight: int = 400) -> float:
    """Rough rendered width of `s`. Good enough to size pills and wrap lines."""
    w = 0.0
    for ch in s:
        if ch in _NARROW:
            w += 0.30
        elif ch in _WIDE:
            w += 0.86
        elif ch.isupper():
            w += 0.66
        elif ch.isdigit():
            w += 0.58
        else:
            w += 0.54
    return w * size * (1.08 if weight >= 600 else 1.08 if weight >= 500 else 1.05)


def wrap(s: str, size: float, max_w: float, weight: int = 400) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and text_width(trial, size, weight) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def esc(s: str) -> str:
    return escape(str(s), quote=True)


def text(x, y, s, size, fill, weight=400, anchor="start", spacing=0, cls="", family=None, extra=""):
    attrs = [
        f'x="{x:.1f}"',
        f'y="{y:.1f}"',
        f'font-size="{size}"',
        f'font-weight="{weight}"',
        f'fill="{fill}"',
    ]
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if cls:
        attrs.append(f'class="{cls}"')
    if family:
        attrs.append(f'font-family="{family}"')
    if extra:
        attrs.append(extra)
    return f"<text {' '.join(attrs)}>{esc(s)}</text>"


# --------------------------------------------------------------------------- shapes


def icon(name: str, x: float, y: float, size: float, fill: str, opacity: float = 1.0) -> str:
    path = ICONS.get(name)
    if not path:
        r = size * 0.22
        return f'<circle cx="{x + size / 2:.1f}" cy="{y + size / 2:.1f}" r="{r:.1f}" fill="{fill}" opacity="{opacity}"/>'
    k = size / 24
    return (
        f'<path transform="translate({x:.1f} {y:.1f}) scale({k:.4f})" d="{path}" '
        f'fill="{fill}" opacity="{opacity}"/>'
    )


def google_dots(x: float, y: float, r: float = 4, gap: float = 13) -> str:
    """Google's four dots, doing a staggered bounce every few seconds."""
    return "".join(
        f'<circle class="gd gd{i + 1}" cx="{x + i * gap:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
        for i, c in enumerate(GOOGLE)
    )


def pulse(cx: float, cy: float, r: float, color: str) -> str:
    """A 'live' dot with an expanding ring, Material style."""
    return (
        f'<circle class="pl" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}" opacity="0"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"/>'
    )


def border_flow(uid: str, x: float, y: float, w: float, h: float, r: float, a: str, b: str,
                delay: float, period: float = 9.0):
    """A thin blue gradient light that slowly travels around a rounded rect's edge
    (Apple-Intelligence style, kept subtle). Returns (defs, body, css).

    It's a single dash on the outline, moved with stroke-dashoffset; at rest it simply sits
    as a short accent arc, so nothing depends on the animation running."""
    import math
    per = 2 * (w + h - 4 * r) + 2 * math.pi * r
    dash = per * 0.22
    defs = (
        f'<linearGradient id="bf{uid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        f'<filter id="bfg{uid}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.2"/></filter>'
    )
    shape = f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="none"'
    dash_attr = f'stroke-dasharray="{dash:.1f} {per - dash:.1f}" stroke-linecap="round"'
    body = (
        f'<rect class="bf{uid}" {shape} stroke="url(#bf{uid})" stroke-width="4" opacity=".35" '
        f'filter="url(#bfg{uid})" {dash_attr}/>'
        f'<rect class="bf{uid}" {shape} stroke="url(#bf{uid})" stroke-width="1.6" opacity=".9" {dash_attr}/>'
    )
    css = (
        f".bf{uid}{{animation:bf{uid} {period}s linear {delay:.2f}s infinite}}"
        f"@keyframes bf{uid}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-{per:.1f}}}}}"
    )
    return defs, body, css


def shifting_gradient(gid: str, a: str, b: str, dur: float = 6.0) -> str:
    """Accent gradient that slides a -> b -> a continuously (Apple-Intelligence style)."""
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0" spreadMethod="repeat">'
        f'<stop offset="0" stop-color="{a}"/><stop offset=".5" stop-color="{b}"/><stop offset="1" stop-color="{a}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" '
        f'from="0 0" to="1 0" dur="{dur}s" repeatCount="indefinite"/></linearGradient>'
    )


def panel(t: dict, w: float, h: float, x: float = 0.5, y: float = 0.5, r: float = 22) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w - 1}" height="{h - 1}" rx="{r}" '
        f'fill="{t["panel"]}" stroke="{t["panel_line"]}"/>'
    )


def chip(t: dict, x: float, y: float, label: str, size: float = 12.5, icon_name: str | None = None, h: float = 28):
    """Returns (svg, width)."""
    pad = 12
    iw = 0 if icon_name is None else size + 7
    w = pad * 2 + iw + text_width(label, size, 500)
    parts = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
        f'fill="{t["chip"]}" stroke="{t["chip_line"]}"/>'
    ]
    tx = x + pad
    if icon_name is not None:
        parts.append(icon(icon_name, tx, y + (h - size) / 2, size, t["text"], 0.9))
        tx += iw
    parts.append(text(tx, y + h / 2 + size * 0.36, label, size, t["text"], 500))
    return "".join(parts), w


# --------------------------------------------------------------------------- document

BASE_CSS = """
.f{animation:up .9s cubic-bezier(.2,.7,.2,1) backwards}
.d1{animation-delay:.08s}.d2{animation-delay:.18s}.d3{animation-delay:.28s}
.d4{animation-delay:.38s}.d5{animation-delay:.48s}.d6{animation-delay:.58s}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.gd{transform-box:fill-box;transform-origin:center;animation:gd 4.2s cubic-bezier(.3,0,.3,1) 1s infinite}
.gd2{animation-delay:1.1s}.gd3{animation-delay:1.2s}.gd4{animation-delay:1.3s}
@keyframes gd{0%,24%,100%{transform:none}8%{transform:translateY(-5px)}16%{transform:translateY(1px)}}
.pl{transform-box:fill-box;transform-origin:center;animation:pl 2.4s cubic-bezier(.2,.6,.3,1) infinite}
@keyframes pl{0%{transform:scale(1);opacity:.55}100%{transform:scale(3);opacity:0}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def svg(w: float, h: float, body: str, title: str, css: str = "", defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" '
        f'viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{esc(title)}" font-family="{esc(FONT)}">'
        f"<title>{esc(title)}</title>"
        f"<style>{BASE_CSS}{css}</style>"
        f"<defs>{defs}</defs>"
        f"{body}</svg>\n"
    )


def write_pair(out_dir: Path, name: str, render) -> None:
    """render(theme_dict, theme_name) -> svg string; writes name-light.svg / name-dark.svg."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for mode, t in THEMES.items():
        (out_dir / f"{name}-{mode}.svg").write_text(render(t, mode), encoding="utf-8")
