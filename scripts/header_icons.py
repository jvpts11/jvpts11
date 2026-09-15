"""Recolore a barra de logos do header.svg com o ICON_COLORS atual."""
from pathlib import Path
import vgui

p = Path(__file__).resolve().parent.parent / "assets" / "header.svg"
h = p.read_text(encoding="utf-8")
anchor = '<path d="M16 327.5H844" stroke="#8C9284"/>'
i = h.index(anchor) + len(anchor)
j = h.index('<text x="844" y="343"')
names = ["csharp", "dotnet", "python", "pytorch", "openjdk", "c",
         "cplusplus", "unity", "blender", "espressif", "git", "docker", "linux"]
bar = "".join(vgui.icon(n, 16 + k * 24, 331, 15) for k, n in enumerate(names))
p.write_text(h[:i] + "\n  " + bar + "\n  " + h[j:], encoding="utf-8")
print("ok")
