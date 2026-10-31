#!/usr/bin/env python3
"""Generate a self-hosted ASCII avatar and profile stats SVGs."""
import html, json, os, urllib.request
from datetime import date, timedelta
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

USER = "abinash123hg"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
if TOKEN:
    HEADERS["Authorization"] = "Bearer " + TOKEN

def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)

def svg_text(x, y, text, size=18, color="#DDF7FF", weight="400"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(str(text))}</text>'

def generate_portrait():
    # Use the user's public GitHub avatar as the input; no image is committed.
    req = urllib.request.Request(f"https://github.com/{USER}.png?size=800", headers={"User-Agent": "profile-readme-generator"})
    with urllib.request.urlopen(req, timeout=30) as response:
        from io import BytesIO
        image = Image.open(BytesIO(response.read())).convert("RGB")
    image = ImageOps.fit(image, (90, 45), method=Image.Resampling.LANCZOS, centering=(0.5, 0.42))
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(1.7)
    ramp = " .:-=+*#%@"
    pixels = list(image.getdata())
    rows = []
    for y in range(45):
        row = "".join(ramp[min(len(ramp)-1, int(pixels[y*90+x] / 256 * len(ramp)))] for x in range(90))
        rows.append(row)
    # Each line is revealed once with a staggered SMIL wipe; no JavaScript.
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 470" role="img" aria-label="Self-typing ASCII portrait of Abinash Swain">']
    out.append('<rect width="900" height="470" rx="22" fill="#050B16"/>')
    out.append('<defs><linearGradient id="accent"><stop stop-color="#38BDF8"/><stop offset="1" stop-color="#10B981"/></linearGradient></defs>')
    out.append('<text x="30" y="30" fill="#38BDF8" font-family="monospace" font-size="13" letter-spacing="3">ABINASH SWAIN / PROFILE PORTRAIT</text>')
    for i, row in enumerate(rows):
        y = 65 + i*8.3
        # Character grid uses monospace; color stays consistent with repo palette.
        out.append(f'<defs><clipPath id="line{i}"><rect x="28" y="{y-7:.1f}" width="0" height="10"><animate attributeName="width" from="0" to="800" dur="0.45s" begin="{i*0.075:.3f}s" fill="freeze"/></rect></clipPath></defs>')
        out.append(f'<text x="30" y="{y:.1f}" clip-path="url(#line{i})" font-family="monospace" font-size="8.8" xml:space="preserve" fill="#7DD3FC">{html.escape(row)}</text>')
    out.append('<text x="30" y="450" fill="#94A3B8" font-family="monospace" font-size="12">PYTHON · RAG · MCP · AI/ML</text></svg>')
    (ASSETS / "portrait.svg").write_text("".join(out), encoding="utf-8")

def generate_stats():
    user = api(f"/users/{USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&type=public&sort=updated")
    repos = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    lang_bytes = {}
    for repo in repos:
        try:
            languages = api(f"/repos/{USER}/{repo['name']}/languages")
            for name, count in languages.items():
                lang_bytes[name] = lang_bytes.get(name, 0) + count
        except Exception:
            continue
    top = sorted(lang_bytes.items(), key=lambda item: item[1], reverse=True)[:5]
    total = sum(v for _, v in top) or 1
    width = 900
    bar_x, bar_y, bar_w = 40, 180, 820
    colors = ["#38BDF8", "#10B981", "#818CF8", "#F59E0B", "#22D3EE"]
    segments, labels = [], []
    cursor = bar_x
    for i, (name, amount) in enumerate(top):
        segment = bar_w * amount / total
        segments.append(f'<rect x="{cursor:.1f}" y="{bar_y}" width="{segment:.1f}" height="14" rx="4" fill="{colors[i]}"/>')
        labels.append(svg_text(40, 235+i*30, f"{name}  ·  {amount/total*100:.1f}%", 17, colors[i], "600"))
        cursor += segment
    body = [
        svg_text(40, 55, "GITHUB SNAPSHOT", 14, "#38BDF8", "700"),
        svg_text(40, 105, f"{user.get('public_repos', 0)} public repos", 28, "#F1F5F9", "700"),
        svg_text(440, 105, f"{stars} stars", 28, "#F1F5F9", "700"),
        svg_text(40, 145, f"Updated {date.today().isoformat()} · original repositories only", 14, "#94A3B8"),
        "".join(segments), "".join(labels),
    ]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 390"><rect width="1000" height="390" rx="22" fill="#050B16" stroke="#26364D"/><g font-family="Arial, sans-serif">{"".join(body)}</g></svg>'
    (ASSETS / "stats-dark.svg").write_text(svg, encoding="utf-8")

if __name__ == "__main__":
    generate_portrait()
    generate_stats()
