"""Helpers para desenhar janelas no estilo VGUI do Counter-Strike 1.6 em SVG."""
from html import escape

BG, DARK, SH, HI = "#4C5844", "#3E4637", "#292C21", "#8C9284"
TX, Y, DIM, SEL = "#DEDFD6", "#C4B550", "#A0AA95", "#958831"
SANS = "Tahoma,Verdana,'DejaVu Sans',sans-serif"
MONO = "'Lucida Console','Courier New','DejaVu Sans Mono',monospace"


def bevel(x, y, w, h, inset=False):
    a, b = (SH, HI) if inset else (HI, SH)
    return (f'<path d="M{x+.5} {y+h-.5}V{y+.5}H{x+w-.5}" stroke="{a}" fill="none"/>'
            f'<path d="M{x+.5} {y+h-.5}H{x+w-.5}V{y+.5}" stroke="{b}" fill="none"/>')


def panel(x, y, w, h, fill=DARK):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>' + bevel(x, y, w, h, inset=True)


def text(x, y, s, size=13, fill=TX, mono=False, anchor="start", extra=""):
    font = MONO if mono else SANS
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" xml:space="preserve" {extra}>{escape(str(s))}</text>')


def button(x, y, w, h, label, fill=TX):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BG}"/>' + bevel(x, y, w, h)
            + text(x + 8, y + h / 2 + 5, label, 13, fill))


def window(w, h, title, body, style=""):
    close = (f'<rect x="{w-34}" y="10" width="20" height="20" fill="{BG}"/>' + bevel(w - 34, 10, 20, 20)
             + f'<path d="M{w-29} 15L{w-19} 25M{w-19} 15L{w-29} 25" stroke="{TX}" stroke-width="1.5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{f"<style>{style}</style>" if style else ""}'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>' + bevel(0, 0, w, h)
            + text(16, 26, title, 14) + close + body + '</svg>')


# ---------------- ícones ----------------
import colorsys, os
from logos import LOGOS

# "brand" = cores oficiais · "muted" = cores oficiais puxadas para a paleta do CS · "mono" = tudo amarelo
COLOR_MODE = os.environ.get("ICON_COLORS", "muted")

# Grades de pixel art. "#" usa a cor principal do ícone; outras letras usam a paleta dele.
PIXELS = {
    "csharp": ["............", ".####.......", "#....#..w.w.", "#......wwwww",
               "#.......w.w.", "#......wwwww", "#....#..w.w.", ".####......."],
    "database": ["..######..", ".#ssssss#.", ".########.", ".#ssssss#.",
                 ".########.", ".#ssssss#.", "..######.."],
    "sliders": [".#....#....", ".#...ooo...", "ooo...#....", ".#....#..#.",
                ".#....#.ooo", ".#....#..#.", ".#....#..#."],
    "bolt": [".....###", "....###.", "...###..", "..######", "....###.",
             "...###..", "..###...", ".##....."],
    "robot": ["....rr....", ".########.", "#ssssssss#", "#sccsscc.#",
              "#ssssssss#", "#ss####ss#", ".########.", "..#....#.."],
    "monitor": ["##########", "#gggggggg#", "#g..ggggg#", "#gggggggg#",
                "#g....ggg#", "##########", "....##....", "..######.."],
    "skull": ["..######..", ".########.", "##########", "#rr####rr#", "#rr####rr#",
              "##########", ".###..###.", "..#.##.#..", "..######.."],
    "anvil": ["####oo####", ".########.", "...####...", "...####...",
              "..######..", ".########."],
    "file": ["######..", "#ssss##.", "#sssss#.", "#s##ss#.", "#sssss#.",
             "#s###s#.", "#sssss#.", "#######."],
    "j": [".....##", ".......", ".....##", ".....##", ".....##",
          ".....##", "##...##", ".##.##.", "..###.."],
}

PIXEL_COLORS = {
    "csharp": {"#": "#9B4F96", "w": "#DEDFD6"},
    "database": {"#": "#4F8FD6", "s": "#2E5A8C"},
    "sliders": {"#": "#A0AA95", "o": "#E8873A"},
    "bolt": {"#": "#F2C94C"},
    "robot": {"#": "#B8BDB0", "s": "#5E6557", "c": "#4FD1E0", "r": "#E0524A"},
    "monitor": {"#": "#B8BDB0", "g": "#2F6B3A", ".": None},
    "skull": {"#": "#E8E2CF", "r": "#C0392B"},
    "anvil": {"#": "#8A9199", "o": "#FF8C2A"},
    "file": {"#": "#A0AA95", "s": "#5A6A4C"},
    "j": {"#": SH},
}


def tone(hexcolor, damp=1.0):
    """Ajusta uma cor ao modo escolhido, garantindo contraste com o fundo oliva."""
    if COLOR_MODE == "mono":
        return Y
    r, g, b = (int(hexcolor.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if COLOR_MODE == "muted":
        s *= 0.72 * damp
    l = min(max(l, 0.62), 0.86)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))


MONO_ON = {"csharp": "#w", "sliders": "#o", "robot": "#r", "anvil": "#o"}


def pixel(name, x, y, size, fill=None):
    """Desenha um ícone pixel-art centrado num quadrado de lado `size`."""
    grid = PIXELS[name]
    pal = PIXEL_COLORS.get(name, {})
    if fill is None and COLOR_MODE == "mono":
        fill = Y
    cols = max(len(r) for r in grid)
    px = size / max(cols, len(grid))
    ox = x + (size - cols * px) / 2
    oy = y + (size - len(grid) * px) / 2
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch, s = row[c], c
            while c < len(row) and row[c] == ch:
                c += 1
            if ch == ".":
                continue
            if fill:
                if ch not in MONO_ON.get(name, "#"):
                    continue
                col = fill
            else:
                base = pal.get(ch, pal.get("#"))
                if base is None:
                    continue
                col = base if name == "j" else tone(base)
            out.append(f'<rect x="{ox+s*px:.2f}" y="{oy+r*px:.2f}" width="{(c-s)*px:.2f}" '
                       f'height="{px:.2f}" fill="{col}"/>')
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


def logo(name, x, y, size, fill=None):
    color = fill or tone(LOGOS[name]["hex"])
    return f'<path transform="translate({x} {y}) scale({size/24:.4f})" d="{LOGOS[name]["path"]}" fill="{color}"/>'


def icon(name, x, y, size=16, fill=None):
    """fill=None usa a cor do ícone conforme COLOR_MODE; um hex força a cor."""
    return pixel(name, x, y, size, fill) if name in PIXELS else logo(name, x, y, size, fill)
