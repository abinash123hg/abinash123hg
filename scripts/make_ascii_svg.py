#!/usr/bin/env python3
"""
Avi ASCII Neon Batman — Professional Particle Assembly
Transparent background + Blue glowing ball + Live assembly
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import List, Tuple

from PIL import Image

# ──────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────
DEFAULT_INPUT = "source-prepped.png"
DEFAULT_OUTPUT = "avi-ascii.svg"
GRID_WIDTH = 95
BRIGHTNESS_THRESHOLD = 175
MAX_CONNECTION_DISTANCE = 5.5
CONNECTION_LOOKAHEAD = 12
DOT_SCALE = 10
SVG_WIDTH = 520
SVG_HEIGHT = 360

Point = Tuple[int, int, int]  # x, y, brightness


def load_and_sample(
    path: Path,
    grid_w: int = GRID_WIDTH,
    threshold: int = BRIGHTNESS_THRESHOLD,
) -> Tuple[List[Point], int, int]:
    if not path.exists():
        raise FileNotFoundError(f"Input image not found: {path}")

    img = Image.open(path).convert("L")
    ratio = img.height / img.width
    grid_h = max(38, int(grid_w * ratio * 0.48))
    img = img.resize((grid_w, grid_h), Image.Resampling.LANCZOS)
    pixels = img.load()

    points: List[Point] = []
    for y in range(grid_h):
        for x in range(grid_w):
            brightness = pixels[x, y]
            if brightness < threshold:
                probability = (threshold - brightness) / threshold
                if random.random() < probability:
                    points.append((x, y, brightness))

    return points, grid_w, grid_h


def build_svg(
    points: List[Point],
    grid_w: int,
    grid_h: int,
    seed: int = 42,
) -> str:
    random.seed(seed)
    view_w = grid_w * DOT_SCALE
    view_h = grid_h * DOT_SCALE

    # Center of the view (for blue ball)
    center_x = view_w / 2
    center_y = view_h / 2 + 25

    particles = []
    for x, y, brightness in points:
        final_x = x * DOT_SCALE + DOT_SCALE // 2
        final_y = y * DOT_SCALE + DOT_SCALE // 2
        radius = 1.1 + (BRIGHTNESS_THRESHOLD - brightness) / 95

        start_x = random.uniform(-100, view_w + 100)
        start_y = random.uniform(-80, view_h + 80)

        delay = random.uniform(0.0, 2.6)
        duration = random.uniform(1.5, 2.8)

        particles.append({
            "sx": start_x,
            "sy": start_y,
            "fx": final_x,
            "fy": final_y,
            "r": radius,
            "delay": delay,
            "dur": duration,
        })

    particles.sort(key=lambda p: (p["fy"], p["fx"]))

    lines: List[str] = []

    # ========== SVG START (NO BLACK RECTANGLE) ==========
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {view_w} {view_h}"
     width="{SVG_WIDTH}" height="{SVG_HEIGHT}">
  <defs>
    <!-- Neon gradient -->
    <linearGradient id="neon" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff2bd6">
        <animate attributeName="stop-color"
                 values="#ff2bd6;#ff65e8;#c44dff;#ff2bd6"
                 dur="3.5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#c44dff">
        <animate attributeName="stop-color"
                 values="#c44dff;#ff2bd6;#b83cff;#c44dff"
                 dur="3.5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#7b5cff">
        <animate attributeName="stop-color"
                 values="#7b5cff;#55b8ff;#c44dff;#7b5cff"
                 dur="3.5s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Blue glowing ball -->
    <radialGradient id="blueBall" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#3aa0ff" stop-opacity="0.58"/>
      <stop offset="55%" stop-color="#1a5cff" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#0a1a40" stop-opacity="0"/>
    </radialGradient>

    <!-- Glow filters -->
    <filter id="dotGlow" x="-90%" y="-90%" width="280%" height="280%">
      <feGaussianBlur stdDeviation="2.6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- ========== BLUE GLOWING BALL (behind everything) ========== -->
  <circle cx="{center_x:.1f}" cy="{center_y:.1f}" r="105" fill="url(#blueBall)">
    <animate attributeName="r" values="95;115;95" dur="5.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.65;1;0.65" dur="5.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{center_x:.1f}" cy="{center_y:.1f}" r="145" fill="#1a5cff" opacity="0.07">
    <animate attributeName="r" values="135;160;135" dur="6.5s" repeatCount="indefinite"/>
  </circle>
''')

    # ── Connections ──
    for i, p1 in enumerate(particles):
        for j in range(i + 1, min(i + CONNECTION_LOOKAHEAD, len(particles))):
            p2 = particles[j]
            dx = p2["fx"] - p1["fx"]
            dy = p2["fy"] - p1["fy"]
            dist = math.hypot(dx, dy)

            if dist <= MAX_CONNECTION_DISTANCE * DOT_SCALE:
                line_dur = 2.0 + random.random() * 2.2
                line_delay = 2.5 + random.random() * 1.8

                lines.append(
                    f'''  <line x1="{p1['fx']:.1f}" y1="{p1['fy']:.1f}"
        x2="{p2['fx']:.1f}" y2="{p2['fy']:.1f}"
        stroke="url(#neon)" stroke-width="0.6" opacity="0">
    <animate attributeName="opacity"
             values="0;0.26;0.07;0.26;0"
             dur="{line_dur:.2f}s"
             begin="{line_delay:.2f}s"
             repeatCount="indefinite"/>
  </line>'''
                )

    # ── Particles (assembly animation) ──
    for p in particles:
        lines.append(
            f'''  <circle cx="{p['sx']:.1f}" cy="{p['sy']:.1f}"
          r="{p['r']:.2f}"
          fill="url(#neon)" filter="url(#dotGlow)" opacity="0.25">
    <animate attributeName="cx"
             from="{p['sx']:.1f}" to="{p['fx']:.1f}"
             dur="{p['dur']:.2f}s" begin="{p['delay']:.2f}s"
             fill="freeze" calcMode="spline"
             keySplines="0.22 0.1 0.25 1"/>
    <animate attributeName="cy"
             from="{p['sy']:.1f}" to="{p['fy']:.1f}"
             dur="{p['dur']:.2f}s" begin="{p['delay']:.2f}s"
             fill="freeze" calcMode="spline"
             keySplines="0.22 0.1 0.25 1"/>
    <animate attributeName="opacity"
             values="0.15;0.95;0.55;0.95"
             dur="{p['dur'] + 1.5:.2f}s"
             begin="{p['delay']:.2f}s"
             repeatCount="indefinite"/>
    <animate attributeName="r"
             values="{p['r']:.2f};{p['r'] * 1.5:.2f};{p['r']:.2f}"
             dur="{1.5 + random.random():.2f}s"
             begin="{p['delay'] + p['dur'] * 0.65:.2f}s"
             repeatCount="indefinite"/>
  </circle>'''
        )

    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate professional transparent neon Batman SVG with blue ball"
    )
    parser.add_argument("-i", "--input", type=Path, default=Path(DEFAULT_INPUT))
    parser.add_argument("-o", "--output", type=Path, default=Path(DEFAULT_OUTPUT))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"→ Loading: {args.input}")
    points, gw, gh = load_and_sample(args.input)
    print(f"  {len(points)} particles | grid {gw}×{gh}")

    print("→ Building transparent SVG with blue ball…")
    svg_content = build_svg(points, gw, gh, seed=args.seed)

    args.output.write_text(svg_content, encoding="utf-8")
    print(f"✓ Saved: {args.output}")
    print("  Transparent background + Blue glowing ball + Live assembly")


if __name__ == "__main__":
    main()