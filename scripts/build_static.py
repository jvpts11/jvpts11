"""Gera as janelas estáticas do README: status, servers e buy menu."""
from pathlib import Path
from vgui import *

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 860

# ---------- ] status ----------
rows = [("hostname", "jvpts11"), ("role", "AI Engineer"), ("map", "de_braga (Portugal)"),
        ("class", "fine-tuning · datasets · .NET"),
        ("side", "MSc Game Dev @ IPCA"), ("clan", "Skill Issue (guitar)")]
b = text(20, 60, "] status", 13, Y, mono=True)
b += panel(16, 70, 132, 200)
b += f'<circle cx="82" cy="140" r="48" fill="{TX}"/>' + pixel("j", 52, 110, 60, SH)
b += text(82, 214, "jvpts11", 13, TX, anchor="middle") + text(82, 232, "he/him", 11, DIM, anchor="middle")
b += icon("anvil", 40, 244, 14) + text(60, 256, "rank: AI Eng", 11, Y)
b += panel(160, 70, 416, 200)
for i, (k, v) in enumerate(rows):
    yy = 100 + i * 29
    b += text(176, yy, k, 13, DIM, mono=True) + text(262, yy, ":", 13, DIM, mono=True) + text(280, yy, v, 13, TX, mono=True)
# mapa
b += text(596, 60, "Map preview", 12, DIM) + panel(592, 70, 252, 200, "#353C2F")
for gx in range(592, 844, 28):
    b += f'<path d="M{gx+.5} 71V269" stroke="#3E4637"/>'
for gy in range(70, 270, 28):
    b += f'<path d="M593 {gy+.5}H843" stroke="#3E4637"/>'
b += (f'<rect x="620" y="98" width="84" height="56" fill="#5A6A4C"/><rect x="732" y="126" width="84" height="112" fill="#5A6A4C"/>'
      f'<rect x="648" y="182" width="56" height="56" fill="#5A6A4C"/><path d="M704 126H732M676 154V182" stroke="{DIM}" stroke-width="6"/>'
      + text(662, 131, "A", 18, Y, anchor="middle") + text(774, 187, "B", 18, Y, anchor="middle")
      + f'<circle cx="676" cy="210" r="5" fill="{Y}"><animate attributeName="opacity" values="1;.2;1" dur="1.2s" repeatCount="indefinite"/></circle>'
      + text(718, 262, "de_braga", 12, TX, anchor="middle"))
b += text(16, 292, "Players: 1 / 32  ·  Game: Counter-Strike  ·  VAC: secure", 11, DIM)
(OUT / "status.svg").write_text(window(W, 304, "Server Info", b), encoding="utf-8")

# ---------- ] find servers ----------
servers = [("bolt", "Polaron — systems language", "compiler", "live", "c", "Polaron / C", 12),
           ("robot", "agents.exe — LLM civ sim", "polaron · llm", "live", "bolt", "Polaron", 24),
           ("monitor", "js-tech-series — MC computers", "neoforge", "live", "openjdk", "Java", 31)]
tabs = ["Internet", "Favorites", "History", "Spectate", "Lan", "Friends"]
b, x = "", 16
for i, t in enumerate(tabs):
    tw = len(t) * 8 + 24
    if i == 0:
        b += f'<rect x="{x}" y="42" width="{tw}" height="26" fill="{BG}"/>' + f'<path d="M{x+.5} 68V42.5H{x+tw-.5}V68" stroke="{HI}" fill="none"/>' + text(x + 12, 60, t, 13, TX)
    else:
        b += f'<rect x="{x}" y="46" width="{tw}" height="22" fill="{DARK}"/>' + text(x + 12, 62, t, 13, DIM)
    x += tw + 2
b += panel(16, 68, W - 32, 26 + 26 * len(servers) + 20)
cols = [(28, f"Servers ({len(servers)})"), (360, "Game"), (520, "Status"), (620, "Lang"), (832, "Latency")]
b += f'<rect x="18" y="70" width="{W-36}" height="24" fill="{BG}"/>' + bevel(18, 70, W - 36, 24)
for cx, c in cols:
    b += text(cx, 87, c, 12, TX, anchor="end" if c == "Latency" else "start")
for i, (ic, n, m, s, li, l, p) in enumerate(servers):
    yy = 96 + i * 26
    if i == 0:
        b += f'<rect x="18" y="{yy}" width="{W-36}" height="26" fill="{SEL if COLOR_MODE == 'mono' else '#6B6A3A'}"/>'
    ty = yy + 18
    dot = Y if s == "live" else "#B0703A"
    fg = TX if i else "#FFFFFF"
    b += (icon(ic, 26, ty - 13, 16) + text(50, ty, n, 13, fg) + text(360, ty, m, 13, TX, mono=True)
          + f'<rect x="520" y="{ty-9}" width="8" height="8" fill="{dot}">'
          + (f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" begin="{i*.4}s" repeatCount="indefinite"/>' if s == "live" else "")
          + '</rect>' + text(534, ty, s, 13)
          + icon(li, 620, ty - 12, 14) + text(642, ty, l, 13)
          + text(832, ty, p, 13, TX, anchor="end"))
fy = 68 + 26 + 26 * len(servers) + 20
b += text(16, fy + 24, f"{len(servers)} servers  ·  filters: not full, has players", 12, DIM)
b += button(W - 334, fy + 8, 100, 26, "Refresh all") + button(W - 226, fy + 8, 100, 26, "Add server") + button(W - 118, fy + 8, 102, 26, "Connect", Y)
(OUT / "servers.svg").write_text(window(W, fy + 48, "Find Servers", b), encoding="utf-8")

# ---------- ] buy menu ----------
cats = [("1", "LANGUAGES", [("csharp", "C#", "AWP", 4750), ("dotnet", ".NET", "M4A1", 3100),
                            ("openjdk", "Java", "AK-47", 2500), ("python", "Python", "MP5", 1500),
                            ("cplusplus", "C / C++", "Deagle", 650)]),
        ("2", "AI / ML", [("pytorch", "PyTorch", "Scout", 2750),
                          ("sliders", "Fine-tuning", "Kevlar", 650), ("database", "Datasets", "HE Grenade", 300),
                          ("huggingface", "Hugging Face", "Smoke", 300)]),
        ("3", "GAME DEV", [("unity", "Unity 6", "P90", 2350), ("blender", "Blender", "Flashbang", 200),
                           ("anvil", "NeoForge", "Galil", 2000), ("espressif", "ESP32", "Defuse kit", 200)]),
        ("4", "TOOLS", [("git", "Git", "USP", 500), ("docker", "Docker", "Glock", 400),
                        ("linux", "Linux", "NVG", 1250), ("rider", "Rider", "Helmet", 350),
                        ("intellijidea", "IntelliJ", "Kevlar+H", 1000)])]
b = ""
cw = (W - 32 - 3 * 12) / 4
for i, (num, name, items) in enumerate(cats):
    x0 = 16 + i * (cw + 12)
    b += text(x0 + 4, 60, f"{num}. {name}", 13, Y) + panel(x0, 70, cw, 184)
    for j, (ic, it, wpn, price) in enumerate(items):
        yy = 96 + j * 32
        b += (icon(ic, x0 + 10, yy - 12, 20) + text(x0 + 40, yy, it, 13) + text(x0 + 40, yy + 13, wpn, 10, DIM)
              + text(x0 + cw - 10, yy, f"${price}", 13, Y, mono=True, anchor="end"))
b += text(16, 292, "$ 16000", 26, Y, mono=True) + text(150, 288, "Press 0 to exit", 12, DIM)
b += button(W - 118, 268, 102, 26, "Cancel")
(OUT / "buymenu.svg").write_text(window(W, 308, "Buy Menu — loadout", b), encoding="utf-8")
print("ok")
