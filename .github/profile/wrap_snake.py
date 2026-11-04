"""Puts the Platane/snk contribution snake into a profile-styled card.

    python .github/profile/wrap_snake.py dist

Reads dist/github-contribution-grid-snake.svg (light) and -dark.svg, removes
snk's progress bar under the grid (it reads as a rendering glitch), and writes
dist/snake-light.svg / dist/snake-dark.svg inside a titled panel.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from design import THEMES, W, panel, svg, text

SOURCES = {"light": "github-contribution-grid-snake.svg", "dark": "github-contribution-grid-snake-dark.svg"}


def inner(raw: str) -> tuple[str, list[float]]:
    """Return the snake's contents (without its <svg> wrapper or progress bar) and its viewBox."""
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', raw).group(1).split()]
    body = re.sub(r"^.*?<svg[^>]*>", "", raw, count=1, flags=re.S)
    body = re.sub(r"</svg>\s*$", "", body)
    body = re.sub(r"<desc>.*?</desc>", "", body, flags=re.S)
    body = re.sub(r'<rect class="u[ "][^>]*/>', "", body)  # progress bar segments
    # the bar sat in the bottom strip of the viewBox; crop that strip away
    vb[3] -= 24
    return body, vb


def card(t: dict, body: str, vb: list[float]) -> str:
    x0, top = 24, 46
    iw = W - 2 * x0
    ih = iw * vb[3] / vb[2]
    h = top + ih + 18
    content = (
        f'<g class="f d1">{text(28, 44, "CONTRIBUTION SNAKE", 11.5, t["accent"], 700, spacing=1.6)}</g>'
        f'<g class="f d1">{text(W - 28, 44, "Eating a year of commits", 13, t["text2"], 500, anchor="end")}</g>'
        f'<svg x="{x0}" y="{top}" width="{iw}" height="{ih:.1f}" viewBox="{" ".join(f"{v:g}" for v in vb)}">{body}</svg>'
    )
    return svg(W, round(h), panel(t, W, round(h), r=22) + content, "Contribution snake eating a year of contributions")


def main() -> None:
    dist = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    for mode, name in SOURCES.items():
        src = dist / name
        if not src.exists():
            sys.exit(f"missing {src}")
        body, vb = inner(src.read_text(encoding="utf-8"))
        (dist / f"snake-{mode}.svg").write_text(card(THEMES[mode], body, vb), encoding="utf-8")
    print("wrapped snake into snake-light.svg / snake-dark.svg")


if __name__ == "__main__":
    main()
