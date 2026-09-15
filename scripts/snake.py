"""Cobrinha que come o gráfico de contribuições, em SVG animado (SMIL) no estilo VGUI."""
from vgui import *

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
PALETTE = ["#353C2F", "#5A6A4C", "#7A8458", "#A09A48", "#C4B550"]


def render_snake(grid, login="jvpts11", duration=36, length=6):
    """grid: lista de semanas; cada semana é uma lista de (weekday, level 0-4)."""
    W = 860
    step, cell = 14, 11
    cols = len(grid)
    gw = cols * step
    ox = (W - gw) / 2 + (step - cell) / 2
    oy = 84

    b = text(20, 60, "] snake", 13, Y, mono=True)
    b += panel(16, 70, W - 32, 7 * step + 28, "#2F352A")

    # caminho em serpentina: desce numa semana, sobe na seguinte
    path = []
    for x in range(cols):
        rows = range(7) if x % 2 == 0 else range(6, -1, -1)
        path += [(x, y) for y in rows]
    idx = {p: i for i, p in enumerate(path)}
    n = len(path)

    for x, week in enumerate(grid):
        for wd, lvl in week:
            px, py = ox + x * step, oy + wd * step
            b += f'<rect x="{px:.1f}" y="{py}" width="{cell}" height="{cell}" fill="{PALETTE[0]}"/>'
            if lvl:
                f = min(idx[(x, wd)] / n, 0.994)
                b += (f'<rect x="{px:.1f}" y="{py}" width="{cell}" height="{cell}" fill="{PALETTE[lvl]}">'
                      f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{f:.4f};{f+0.004:.4f};1" '
                      f'dur="{duration}s" repeatCount="indefinite"/></rect>')

    # trajetória da cobra (centro das células)
    pts = [(ox + x * step + cell / 2, oy + y * step + cell / 2) for x, y in path]
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    seg = duration / n
    for k in range(length):
        size = cell - k * 1.2
        color = Y if k == 0 else ("#A09A48" if k < 3 else "#7A8458")
        begin = 0 if k == 0 else -(duration - k * seg)
        b += (f'<rect x="{-size/2:.1f}" y="{-size/2:.1f}" width="{size:.1f}" height="{size:.1f}" fill="{color}">'
              f'<animateMotion path="{d}" dur="{duration}s" begin="{begin:.3f}s" repeatCount="indefinite" '
              f'calcMode="linear"/></rect>')

    h = 70 + 7 * step + 28
    b += text(16, h + 22, "contributions eaten in real time · updated daily", 11, DIM)
    b += text(W - 16, h + 22, "hp 100  ·  armor 100", 11, DIM, anchor="end")
    return window(W, h + 34, f"snake — {login}", b)
