"""Shared design system for every SVG on the profile README.

Apple-style layout (monochrome, generous space, big type) with a small touch
of colour: one blue-to-violet accent gradient and Google's four dots as a
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
        "grad": ("#0071e3", "#7c3aed"),
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
        "grad": ("#2997ff", "#a78bfa"),
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
    return "".join(
        f'<circle cx="{x + i * gap:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>' for i, c in enumerate(GOOGLE)
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
