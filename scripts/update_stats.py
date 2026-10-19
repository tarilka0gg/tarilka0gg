#!/usr/bin/env python3
"""Writes assets/stats.svg: repository, star and follower counts and a language bar for the public, non-fork repositories of a user.
Standard library only. GITHUB_TOKEN (optional) raises the API rate limit.   usage: update_stats.py [user]"""
import json, os, sys, urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "tarilka0gg"
COLORS = {"Rust": "#dea584", "Shell": "#89e051", "Python": "#3572A5", "Zig": "#ec915c", "JavaScript": "#f1e05a", "CSS": "#663399",
          "HTML": "#e34c26", "Go": "#00ADD8", "C": "#555555", "Nix": "#7e7eff", "Makefile": "#427819"}

def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

user = api(f"/users/{USER}")
repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
langs = {}
for r in repos:
    for name, n in api(f"/repos/{USER}/{r['name']}/languages").items():
        langs[name] = langs.get(name, 0) + n
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda kv: -kv[1])
shown, rest = top[:6], sum(n for _, n in top[6:])
if rest:
    shown.append(("Other", rest))
stars = sum(r["stargazers_count"] for r in repos)

W, H, PAD = 760, 230, 28
font = 'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"'
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub statistics of {USER}">',
     '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f1722"/><stop offset="1" stop-color="#1a1530"/></linearGradient>',
     f'<clipPath id="bar"><rect x="{PAD}" y="118" width="{W-2*PAD}" height="14" rx="7"/></clipPath></defs>',
     f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>']
for i, (label, value) in enumerate([("public repos", len(repos)), ("stars earned", stars), ("followers", user["followers"])]):
    x = PAD + i * 240
    o.append(f'<text x="{x}" y="62" {font} font-size="38" font-weight="700" fill="#e6edf3">{value}</text>')
    o.append(f'<text x="{x}" y="86" {font} font-size="14" fill="#8b949e">{label}</text>')
x = PAD
for name, n in shown:
    w = (W - 2 * PAD) * n / total
    o.append(f'<rect x="{x:.1f}" y="118" width="{w:.1f}" height="14" fill="{COLORS.get(name, "#8b949e")}" clip-path="url(#bar)"/>')
    x += w
for i, (name, n) in enumerate(shown):
    cx = PAD + (i % 4) * 178
    cy = 166 + (i // 4) * 26
    o.append(f'<circle cx="{cx+6}" cy="{cy-5}" r="6" fill="{COLORS.get(name, "#8b949e")}"/>')
    o.append(f'<text x="{cx+18}" y="{cy}" {font} font-size="13" fill="#c9d1d9">{name} {100*n/total:.1f}%</text>')
o.append(f'<text x="{PAD}" y="{H-12}" {font} font-size="11" fill="#6e7681">top languages across my public repositories, updated daily</text>')
o.append("</svg>")
open(os.path.join(os.path.dirname(__file__), "..", "assets", "stats.svg"), "w").write("\n".join(o))
print(f"{len(repos)} repos, {stars} stars, {user['followers']} followers; " + ", ".join(f"{k} {100*v/total:.0f}%" for k, v in shown))
