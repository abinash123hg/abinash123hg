#!/usr/bin/env python3
"""
Fixed + Updated Professional RGB Info Card
- Fixed ready_ overlapping
- Added Internship (TutorialsPoint Certificate Verified)
"""

from pathlib import Path

OUTPUT = Path("info-card.svg")

svg = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 620" width="560" height="620">
  <defs>
    <!-- FULL RGB FLOW - Left Labels -->
    <linearGradient id="rgbLeft" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff2bd6">
        <animate attributeName="stop-color" 
                 values="#ff2bd6;#ff0040;#ff6b00;#ffe600;#00ff88;#00e5ff;#2979ff;#d500f9;#ff2bd6" 
                 dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#ff4d6d">
        <animate attributeName="stop-color" 
                 values="#ff4d6d;#ff6b00;#ffe600;#00ff88;#00e5ff;#2979ff;#d500f9;#ff2bd6;#ff4d6d" 
                 dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#c44dff">
        <animate attributeName="stop-color" 
                 values="#c44dff;#00e5ff;#2979ff;#d500f9;#ff2bd6;#ff0040;#ff6b00;#ffe600;#c44dff" 
                 dur="8s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- FULL RGB FLOW - Right Values -->
    <linearGradient id="rgbRight" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#00e5ff">
        <animate attributeName="stop-color" 
                 values="#00e5ff;#2979ff;#d500f9;#ff2bd6;#ff0040;#ff6b00;#00ff88;#00e5ff" 
                 dur="7.5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#2979ff">
        <animate attributeName="stop-color" 
                 values="#2979ff;#d500f9;#ff2bd6;#ff0040;#ff6b00;#00ff88;#00e5ff;#2979ff" 
                 dur="7.5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#d500f9">
        <animate attributeName="stop-color" 
                 values="#d500f9;#ff2bd6;#ff0040;#ff6b00;#00ff88;#00e5ff;#2979ff;#d500f9" 
                 dur="7.5s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Border -->
    <linearGradient id="borderRGB" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff2bd6">
        <animate attributeName="stop-color" 
                 values="#ff2bd6;#ff0040;#ff6b00;#00ff88;#00e5ff;#2979ff;#d500f9;#ff2bd6" 
                 dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#00e5ff">
        <animate attributeName="stop-color" 
                 values="#00e5ff;#2979ff;#d500f9;#ff2bd6;#ff0040;#ff6b00;#00ff88;#00e5ff" 
                 dur="6s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Status green -->
    <linearGradient id="status" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00e676"/>
      <stop offset="100%" stop-color="#69f0ae"/>
    </linearGradient>

    <!-- Glow -->
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3.6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="560" height="620" rx="24" fill="#06060c"/>

  <!-- Animated RGB Border -->
  <rect x="5" y="5" width="550" height="610" rx="20" fill="none"
        stroke="url(#borderRGB)" stroke-width="2.8" filter="url(#glow)">
    <animate attributeName="stroke-width" values="2.3;3.5;2.3" dur="2.8s" repeatCount="indefinite"/>
  </rect>

  <!-- HEADER -->
  <text x="32" y="48" font-family="'Courier New', monospace" font-size="21" font-weight="700"
        fill="url(#rgbLeft)" filter="url(#textGlow)">
    abinash@github:~$
  </text>

  <text x="32" y="78" font-family="'Courier New', monospace" font-size="16.5" fill="#eaeaf2">
    whoami
  </text>

  <!-- Divider -->
  <line x1="32" y1="96" x2="528" y2="96" stroke="url(#rgbLeft)" stroke-width="1.2" opacity="0.55">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.5s" repeatCount="indefinite"/>
  </line>

  <!-- ========== INFO SECTION ========== -->
  <g font-family="'Courier New', monospace" font-size="16.5">

    <text x="34" y="140" fill="url(#rgbLeft)" filter="url(#textGlow)">Name</text>
    <text x="190" y="140" fill="url(#rgbRight)">Abinash Swain</text>

    <text x="34" y="178" fill="url(#rgbLeft)" filter="url(#textGlow)">Role</text>
    <text x="190" y="178" fill="url(#rgbRight)">B.Tech CSE (AIML)</text>

    <text x="34" y="216" fill="url(#rgbLeft)" filter="url(#textGlow)">Year</text>
    <text x="190" y="216" fill="url(#rgbRight)">3rd Year</text>

    <text x="34" y="254" fill="url(#rgbLeft)" filter="url(#textGlow)">Focus</text>
    <text x="190" y="254" fill="url(#rgbRight)">AI / ML / Deep Learning</text>

    <text x="34" y="292" fill="url(#rgbLeft)" filter="url(#textGlow)">Vision</text>
    <text x="190" y="292" fill="url(#rgbRight)">Computer Vision</text>

    <text x="34" y="330" fill="url(#rgbLeft)" filter="url(#textGlow)">Build</text>
    <text x="190" y="330" fill="url(#rgbRight)">Generative AI</text>

    <text x="34" y="368" fill="url(#rgbLeft)" filter="url(#textGlow)">University</text>
    <text x="190" y="368" fill="url(#rgbRight)">CUTM Bhubaneswar</text>

    <!-- NEW: Internship -->
    <text x="34" y="406" fill="url(#rgbLeft)" filter="url(#textGlow)">Internship</text>
    <text x="190" y="406" fill="url(#rgbRight)">TutorialsPoint (Verified)</text>
  </g>

  <!-- Divider 2 -->
  <line x1="32" y1="435" x2="528" y2="435" stroke="url(#rgbRight)" stroke-width="1.1" opacity="0.45">
    <animate attributeName="opacity" values="0.25;0.7;0.25" dur="2.6s" repeatCount="indefinite"/>
  </line>

  <!-- TECH STACK -->
  <text x="34" y="470" font-family="'Courier New', monospace" font-size="15.5"
        fill="url(#rgbLeft)" filter="url(#textGlow)">
    Stack
  </text>

  <g font-family="'Courier New', monospace" font-size="13.5">
    <rect x="34" y="488" width="84" height="27" rx="7" fill="#10101a" stroke="#ff2bd6" stroke-width="1.5" filter="url(#textGlow)"/>
    <text x="48" y="507" fill="#ff6be9">Python</text>

    <rect x="130" y="488" width="78" height="27" rx="7" fill="#10101a" stroke="#c44dff" stroke-width="1.5" filter="url(#textGlow)"/>
    <text x="144" y="507" fill="#d07dff">AI/ML</text>

    <rect x="220" y="488" width="64" height="27" rx="7" fill="#10101a" stroke="#00e5ff" stroke-width="1.5" filter="url(#textGlow)"/>
    <text x="236" y="507" fill="#65c7ff">CV</text>

    <rect x="296" y="488" width="80" height="27" rx="7" fill="#10101a" stroke="#ff4d6d" stroke-width="1.5" filter="url(#textGlow)"/>
    <text x="310" y="507" fill="#ff7a9a">GenAI</text>

    <rect x="388" y="488" width="60" height="27" rx="7" fill="#10101a" stroke="#00e676" stroke-width="1.5" filter="url(#textGlow)"/>
    <text x="402" y="507" fill="#69f0ae">Git</text>
  </g>

  <!-- STATUS -->
  <text x="34" y="555" font-family="'Courier New', monospace" font-size="15.5"
        fill="url(#rgbLeft)" filter="url(#textGlow)">
    Status
  </text>

  <circle cx="195" cy="549" r="7.5" fill="#00e676" filter="url(#glow)">
    <animate attributeName="r" values="6.5;9;6.5" dur="1.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.65;1;0.65" dur="1.4s" repeatCount="indefinite"/>
  </circle>

  <text x="215" y="555" font-family="'Courier New', monospace" font-size="16"
        fill="url(#status)">
    Building &amp; Learning
  </text>

  <!-- FOOTER (Fixed - no overlap) -->
  <line x1="32" y1="580" x2="528" y2="580" stroke="#222233" stroke-width="0.9"/>

  <rect x="34" y="595" width="13" height="16" rx="2" fill="#ff2bd6" filter="url(#glow)">
    <animate attributeName="opacity" values="1;0;1" dur="0.7s" repeatCount="indefinite"/>
  </rect>

  <text x="56" y="608" font-family="'Courier New', monospace" font-size="14" fill="#8888a0">
    ready_
  </text>

</svg>'''

OUTPUT.write_text(svg, encoding="utf-8")
print("✓ Fixed version generated → info-card.svg")
print("  • ready_ overlapping fixed")
print("  • Internship (TutorialsPoint Verified) added")