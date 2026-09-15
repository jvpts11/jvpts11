"""Gera assets/net_graph.svg com estatísticas reais do GitHub no estilo CS 1.6.

Uso: GH_TOKEN=... GH_USER=jvpts11 python scripts/net_graph.py
     python scripts/net_graph.py --sample   (dados falsos, para testar o visual)
"""
import json, os, sys, urllib.error, urllib.request
from collections import Counter
from pathlib import Path
from vgui import *

OUT = Path(__file__).resolve().parent.parent / "assets" / "net_graph.svg"
QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } }
    }
  }
}"""


def fetch(user, token):
    token = (token or "").strip()
    if not token:
        sys.exit("GH_TOKEN está vazio: confira o secret METRICS_TOKEN (nome exato, em Actions secrets).")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("401 Unauthorized: o token é inválido, expirou ou foi colado com erro. Gere outro e atualize o secret.")
        raise
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    u = data["data"]["user"]
    langs, colors = Counter(), {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
            colors[e["node"]["name"]] = e["node"]["color"] or "#A0AA95"
    cc = u["contributionsCollection"]
    return {
        "login": u["login"],
        "contrib": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "repos": u["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
        "langs": langs,
        "colors": colors,
        "weeks": [sum(d["contributionCount"] for d in w["contributionDays"])
                  for w in cc["contributionCalendar"]["weeks"]],
    }


def sample():
    import random
    random.seed(3)
    return {"login": "jvpts11", "contrib": 3893, "commits": 3120, "prs": 41, "repos": 37,
            "stars": 2, "followers": 6,
            "langs": Counter({"C#": 380, "Java": 240, "Python": 180, "C": 120, "JavaScript": 80}),
            "colors": {"C#": "#178600", "Java": "#B07219", "Python": "#3572A5", "C": "#555555", "JavaScript": "#F1E05A"},
            "weeks": [random.randint(0, 40) + (i > 38) * random.randint(30, 90) for i in range(53)]}


LANG_ICONS = {"C#": "csharp", "Java": "openjdk", "Python": "python", "C": "c", "C++": "cplusplus",
              "JavaScript": "javascript", "ShaderLab": "unity", "HLSL": "unity", "Dockerfile": "docker"}


# cores que combinam com os ícones (o verde do C# no GitHub destoa do resto)
BAR_COLORS = {"C#": "#9B4F96", "Java": "#E76F00"}


def render(d):
    W, H = 860, 330
    b = text(20, 60, "] net_graph 3", 13, Y, mono=True)

    # estatísticas
    b += panel(16, 70, 300, 170)
    stats = [("contributions (1y)", d["contrib"]), ("commits (1y)", d["commits"]),
             ("pull requests (1y)", d["prs"]), ("public repos", d["repos"]),
             ("stars earned", d["stars"]), ("followers", d["followers"])]
    for i, (k, v) in enumerate(stats):
        yy = 98 + i * 25
        b += text(30, yy, k, 13, DIM, mono=True) + text(302, yy, f"{v:,}", 13, TX, mono=True, anchor="end")

    # linguagens
    b += text(336, 60, "Most used languages", 12, DIM) + panel(332, 70, 512, 170)
    total = sum(d["langs"].values()) or 1
    shades = [Y, "#A09A48", "#7A8458", "#6A7650", "#5A6A4C"]
    for i, (name, size) in enumerate(d["langs"].most_common(5)):
        pct = size / total * 100
        yy = 100 + i * 28
        bw = 300 * pct / 100
        bar = shades[i] if COLOR_MODE == "mono" else tone(BAR_COLORS.get(name, d["colors"].get(name, "#A0AA95")), damp=0.75)
        b += (icon(LANG_ICONS.get(name, "file"), 346, yy - 12, 16) + text(370, yy, name, 13) + f'<rect x="450" y="{yy-11}" width="304" height="14" fill="{SH}"/>'
              + f'<rect x="452" y="{yy-9}" width="{bw:.1f}" height="10" fill="{bar}"/>'
              + text(830, yy, f"{pct:.1f}%", 13, TX, mono=True, anchor="end"))

    # gráfico estilo net_graph
    weeks = d["weeks"][-53:]
    peak = max(weeks) or 1
    b += panel(16, 250, W - 32, 58, "#353C2F")
    bw = (W - 40) / len(weeks)
    for i, v in enumerate(weeks):
        h = max(1, v / peak * 48)
        col = Y if v >= peak * .66 else "#A09A48" if v >= peak * .33 else "#7A8458"
        b += f'<rect x="{20 + i*bw:.1f}" y="{304-h:.1f}" width="{bw-1.5:.1f}" height="{h:.1f}" fill="{col}"/>'
    b += text(16, 324, "contributions per week · last 12 months", 11, DIM)
    b += text(W - 16, 324, f"peak {peak}/wk  ·  fps 144  ·  ping 12", 11, DIM, anchor="end")
    return window(W, H + 4, f"net_graph — {d['login']}", b)


if __name__ == "__main__":
    data = sample() if "--sample" in sys.argv else fetch(os.environ.get("GH_USER", "jvpts11"), os.environ.get("GH_TOKEN"))
    OUT.write_text(render(data), encoding="utf-8")
    print(f"wrote {OUT}")
