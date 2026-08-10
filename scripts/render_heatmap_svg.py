import json
from pathlib import Path

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

days = data["days"]

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0"
]

CELL = 12
GAP = 4
LEFT = 30
TOP = 30

width = 53 * (CELL + GAP) + LEFT + 10
height = 7 * (CELL + GAP) + TOP + 45

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
)

svg.append("""
<style>
.cell {
    opacity: 0;
    animation: reveal 0.5s ease-out forwards;
}
@keyframes reveal {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""")

svg.append(
    '<rect width="100%" height="100%" rx="10" fill="#0d1117"/>'
)

for i, day in enumerate(days[-371:]):
    level = max(0, min(5, int(day["level"])))

    week = i // 7
    weekday = i % 7

    x = LEFT + week * (CELL + GAP)
    y = TOP + weekday * (CELL + GAP)

    delay = i * 0.008

    svg.append(
        f'<rect class="cell" '
        f'x="{x}" y="{y}" '
        f'width="{CELL}" height="{CELL}" '
        f'rx="3" '
        f'fill="{PALETTE[level]}" '
        f'style="animation-delay:{delay:.3f}s">'
        f'<title>{day["date"]}: level {level}</title>'
        f'</rect>'
    )

svg.append(
    f'<text x="{LEFT}" y="{height - 12}" '
    f'fill="#8b949e" font-family="monospace" font-size="11">'
    f'Less</text>'
)

svg.append(
    f'<text x="{width - 45}" y="{height - 12}" '
    f'fill="#8b949e" font-family="monospace" font-size="11">'
    f'More</text>'
)

svg.append("</svg>")

OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")

print(f"Saved: {OUTPUT_FILE}")