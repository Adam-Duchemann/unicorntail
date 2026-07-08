#!/usr/bin/env python3
"""Generate the README SVG charts (light + dark) from the measured results.

Reproducible: edit the DATA constants, re-run, commit the SVGs.
  python3 assets/make_charts.py

Palette: "Actual Unicorn" (schemecolor.com/actual-unicorn.php) —
Hot Pink #FD63B0 · Dark Orchid #8C3ED1 · Brilliant Azure #30A0F5 ·
Malachite #1EF361 · Chartreuse #ECFE0C · Rajah #FFAD65.
"""

import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))

FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

# Unicorn gradient in mane order (pink -> purple -> blue -> green -> yellow -> orange).
UNICORN = ["#FD63B0", "#8C3ED1", "#30A0F5", "#1EF361", "#ECFE0C", "#FFAD65"]

THEMES = {
    "light": {
        "bg": "#fcfcfb", "title": "#0b0b0b", "sub": "#898781", "label": "#52514e",
        "grid": "#e1e0d9", "axis": "#c3c2b7",
        "neutral": "#a8a49c", "pony": "#FFAD65", "uni_solid": "#8C3ED1",
        # chartreuse deepened for contrast on near-white
        "mane": ["#FD63B0", "#8C3ED1", "#30A0F5", "#17C94F", "#D9C400", "#FFAD65"],
        "grad": UNICORN,
        "onbar": "#1d2733",
    },
    "dark": {
        "bg": "#161b22", "title": "#e6edf3", "sub": "#8b949e", "label": "#c9d1d9",
        "grid": "#30363d", "axis": "#484f58",
        "neutral": "#6e7681", "pony": "#FFAD65", "uni_solid": "#A468E0",
        "mane": UNICORN,
        "grad": UNICORN,
        "onbar": "#10151c",
    },
}

# Measured 2026-07-05 — see README "Measured results". 24 runs per arm.
ARMS = [
    ("no tool · Haiku", "neutral", 14),
    ("ponytail v4.8.4 · Haiku", "pony", 19),
    ("unicorntail · Haiku", "grad", 22),
    ("unicorntail · Sonnet", "grad", 24),
]
TOTAL_RUNS = 24

# Rule tokens spent per session vs number of subagents spawned.
# ponytail: ~1,450 tok body x (1 session + N subagents). unicorntail: ~800 tok once (CLAUDE.md).
PONY_TOK = 1450
UNI_TOK = 800
AGENT_COUNTS = [0, 5, 10, 20, 30]

# Net-token measurement 2026-07-08 — output tokens generated per task, ladder-directed vs
# neutral, same Sonnet subject. See README "The net-token ledger". (name, with_tok, without_tok)
NET_TASKS = [
    ("store-theme", 263, 3099),
    ("debounce-search", 37, 830),
    ("validate-upload", 1366, 4031),
    ("retry-api", 191, 3330),
    ("relative-time", 69, 5004),
    ("feature-flag", 133, 3474),
    ("cache-user", 215, 2983),
    ("parse-tags", 22, 1938),
]
NET_WITH_TOTAL = sum(wt for _, wt, _ in NET_TASKS)      # 2,296
NET_WITHOUT_TOTAL = sum(ot for _, _, ot in NET_TASKS)   # 24,689


def gradient_def(t, gid, x1, x2):
    stops = "".join(
        f'<stop offset="{i / (len(t["grad"]) - 1) * 100:.0f}%" stop-color="{c}"/>'
        for i, c in enumerate(t["grad"])
    )
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{x1}" y1="0" x2="{x2}" y2="0">{stops}</linearGradient>')


def svg_results(t):
    w, h = 780, 340
    bar_h, gap, x0, xmax = 40, 24, 250, 730
    scale = (xmax - x0) / TOTAL_RUNS
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" role="img" '
        f'aria-label="Eval runs passed out of 24: no tool 14 and ponytail 19 on Haiku; unicorntail 22 on Haiku and 24 of 24 on Sonnet.">',
        f"<defs>{gradient_def(t, 'unigrad', x0, xmax)}</defs>",
        f'<rect width="{w}" height="{h}" rx="10" fill="{t["bg"]}"/>',
        f'<text x="40" y="36" font-size="19" font-weight="600" fill="{t["title"]}">Eval runs passed — 8 cases × 3 runs, same rubrics, same judge</text>',
        f'<text x="40" y="57" font-size="13" fill="{t["sub"]}">rules injected identically per arm · same rubrics, same judge · higher is better ↑</text>',
    ]
    y = 90
    for name, key, val in ARMS:
        bw = val * scale
        pct = round(val / TOTAL_RUNS * 100)
        fill = "url(#unigrad)" if key == "grad" else t[key]
        label_fill = t["onbar"] if key == "grad" else t["bg"]
        parts += [
            f'<text x="{x0 - 14}" y="{y + bar_h / 2 + 5}" font-size="14" text-anchor="end" fill="{t["label"]}">{name}</text>',
            f'<rect x="{x0}" y="{y}" width="{xmax - x0}" height="{bar_h}" rx="6" fill="{t["grid"]}" opacity="0.35"/>',
            f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="{bar_h}" rx="6" fill="{fill}"/>',
            f'<text x="{x0 + bw - 12:.1f}" y="{y + bar_h / 2 + 5}" font-size="15" font-weight="600" text-anchor="end" '
            f'fill="{label_fill}" font-variant-numeric="tabular-nums">{val}/24</text>',
            f'<text x="{xmax + 8}" y="{y + bar_h / 2 + 5}" font-size="12" fill="{t["sub"]}" font-variant-numeric="tabular-nums"> {pct}%</text>' if val < TOTAL_RUNS else
            f'<text x="{xmax + 8}" y="{y + bar_h / 2 + 5}" font-size="12" font-weight="600" fill="{t["grad"][1]}" font-variant-numeric="tabular-nums">100%</text>',
        ]
        y += bar_h + gap
    parts.append("</svg>")
    return "\n".join(parts)


def svg_tokens(t):
    w, h = 780, 340
    x0, y0, x1, y1 = 90, 80, 740, 280  # plot box
    max_tok = PONY_TOK * (1 + AGENT_COUNTS[-1])  # 44,950
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" role="img" '
        f'aria-label="Rule tokens spent per session as subagents scale: ponytail grows to about 45,000 tokens at 30 subagents; unicorntail stays flat at about 800.">',
        f'<rect width="{w}" height="{h}" rx="10" fill="{t["bg"]}"/>',
        f'<text x="40" y="36" font-size="19" font-weight="600" fill="{t["title"]}">Rule tokens spent per session — hooks multiply, CLAUDE.md doesn\'t</text>',
        f'<text x="40" y="57" font-size="13" fill="{t["sub"]}">ponytail re-injects ~1,450 tok into the session + every subagent · unicorntail rides CLAUDE.md once (~800 tok) · lower is better ↓</text>',
    ]
    # gridlines
    for tok in (0, 15000, 30000, 45000):
        gy = y1 - (tok / max_tok) * (y1 - y0)
        parts += [
            f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{t["grid"]}" stroke-width="1"/>',
            f'<text x="{x0 - 10}" y="{gy + 4:.1f}" font-size="11" text-anchor="end" fill="{t["sub"]}" font-variant-numeric="tabular-nums">{tok // 1000}k</text>',
        ]
    parts.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{t["axis"]}" stroke-width="1.5"/>')
    # grouped bars
    group_w = (x1 - x0) / len(AGENT_COUNTS)
    bw = 34
    for i, n in enumerate(AGENT_COUNTS):
        cx = x0 + group_w * (i + 0.5)
        pony = PONY_TOK * (1 + n)
        for dx, val, key in ((-bw - 3, pony, "pony"), (3, UNI_TOK, "uni_solid")):
            bh = (val / max_tok) * (y1 - y0)
            parts.append(f'<rect x="{cx + dx:.1f}" y="{y1 - bh:.1f}" width="{bw}" height="{bh:.1f}" rx="4" fill="{t[key]}"/>')
            label = f"{round(val / 1000, 1):g}k" if val >= 1000 else str(val)
            parts.append(
                f'<text x="{cx + dx + bw / 2:.1f}" y="{y1 - bh - 6:.1f}" font-size="11" text-anchor="middle" '
                f'fill="{t["label"]}" font-variant-numeric="tabular-nums">{label}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{y1 + 20}" font-size="12" text-anchor="middle" fill="{t["sub"]}" font-variant-numeric="tabular-nums">{n}</text>')
    parts += [
        f'<text x="{(x0 + x1) / 2}" y="{y1 + 42}" font-size="12" text-anchor="middle" fill="{t["sub"]}">subagents spawned in the session</text>',
        f'<rect x="{x0}" y="66" width="12" height="12" rx="2" fill="{t["pony"]}"/>',
        f'<text x="{x0 + 18}" y="76" font-size="13" fill="{t["label"]}">ponytail (hook re-injection)</text>',
        f'<rect x="{x0 + 230}" y="66" width="12" height="12" rx="2" fill="{t["uni_solid"]}"/>',
        f'<text x="{x0 + 248}" y="76" font-size="13" fill="{t["label"]}">unicorntail (CLAUDE.md, once)</text>',
        "</svg>",
    ]
    return "\n".join(parts)


def svg_nettokens(t):
    """Per-task output tokens: gradient = written with the ladder, gray = over-build avoided."""
    w = 780
    x0, xmax = 172, 690
    bar_h, gap, top = 20, 13, 92
    max_val = 5100
    scale = (xmax - x0) / max_val
    h = top + len(NET_TASKS) * (bar_h + gap) + 82
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" role="img" '
        f'aria-label="Output tokens generated per task, ladder vs neutral: the ladder writes about 11 times '
        f'less code, 2,296 tokens across 8 tasks versus 24,689 without it.">',
        f"<defs>{gradient_def(t, 'netgrad', x0, xmax)}</defs>",
        f'<rect width="{w}" height="{h}" rx="10" fill="{t["bg"]}"/>',
        f'<text x="40" y="36" font-size="19" font-weight="600" fill="{t["title"]}">Code written vs code skipped — 8 tasks, same model</text>',
        f'<text x="40" y="57" font-size="13" fill="{t["sub"]}">gradient = tokens generated with the ladder · gray = extra tokens the neutral run spent · lower total is better ↓</text>',
    ]
    y = top
    for name, wtok, otok in NET_TASKS:
        full = otok * scale
        seg = max(2.5, wtok * scale)
        parts += [
            f'<text x="{x0 - 12}" y="{y + bar_h / 2 + 5}" font-size="13" text-anchor="end" fill="{t["label"]}">{name}</text>',
            f'<rect x="{x0}" y="{y}" width="{full:.1f}" height="{bar_h}" rx="4" fill="{t["neutral"]}"/>',
            f'<rect x="{x0}" y="{y}" width="{seg:.1f}" height="{bar_h}" rx="4" fill="url(#netgrad)"/>',
            f'<text x="{x0 + full + 8:.1f}" y="{y + bar_h / 2 + 5}" font-size="12" fill="{t["sub"]}" font-variant-numeric="tabular-nums">{otok:,}</text>',
        ]
        y += bar_h + gap
    ly = y + 8
    parts += [
        f'<rect x="{x0}" y="{ly}" width="12" height="12" rx="2" fill="url(#netgrad)"/>',
        f'<text x="{x0 + 18}" y="{ly + 10}" font-size="13" fill="{t["label"]}">written with the ladder</text>',
        f'<rect x="{x0 + 188}" y="{ly}" width="12" height="12" rx="2" fill="{t["neutral"]}"/>',
        f'<text x="{x0 + 206}" y="{ly + 10}" font-size="13" fill="{t["label"]}">over-build the ladder refused</text>',
    ]
    sy = ly + 40
    saved = NET_WITHOUT_TOTAL - NET_WITH_TOTAL
    parts += [
        f'<text x="40" y="{sy}" font-size="15" font-weight="600" fill="{t["title"]}" font-variant-numeric="tabular-nums">'
        f'Total: <tspan fill="{t["uni_solid"]}">{NET_WITH_TOTAL:,}</tspan> written vs {NET_WITHOUT_TOTAL:,} — '
        f'<tspan fill="{t["mane"][3]}">{saved:,} output tokens saved (−91%)</tspan></text>',
        "</svg>",
    ]
    return "\n".join(parts)


def svg_banner(t):
    """Six-strand unicorn mane weaving, then merging into one rainbow line."""
    w, h, mid = 880, 120, 60
    merge_x = 685
    paths = []
    for i, color in enumerate(t["mane"]):
        phase = i * math.pi / 3.2
        amp0 = 34 - 2.5 * i  # slightly varied amplitudes so strands interleave
        pts = []
        for x in range(30, merge_x + 1, 5):
            u = (x - 30) / (merge_x - 30)
            decay = max(0.0, 1.0 - u) ** 1.15  # converge to the midline at the merge point
            y = mid + amp0 * decay * math.sin(2 * math.pi * (x - 30) / 300 + phase)
            pts.append(f"{x},{y:.1f}")
        d = "M " + " L ".join(pts)
        opacity = 0.95 - 0.06 * i
        paths.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3.2" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity:.2f}"/>')
    stops = "".join(
        f'<stop offset="{i / (len(t["grad"]) - 1) * 100:.0f}%" stop-color="{c}"/>'
        for i, c in enumerate(t["grad"])
    )
    merged = (f'<defs><linearGradient id="manegrad" gradientUnits="userSpaceOnUse" '
              f'x1="{merge_x}" y1="0" x2="850" y2="0">{stops}</linearGradient></defs>\n'
              f'<line x1="{merge_x}" y1="{mid}" x2="850" y2="{mid}" stroke="url(#manegrad)" '
              f'stroke-width="3.6" stroke-linecap="round"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" role="img" '
            f'aria-label="A six-strand unicorn mane weaving into a single rainbow line — many rule sources merged into one.">\n'
            f'<rect width="{w}" height="{h}" rx="10" fill="{t["bg"]}"/>\n'
            f"{merged}\n" + "\n".join(paths) + "\n</svg>")


CHARTS = {"results": svg_results, "tokens": svg_tokens, "net-tokens": svg_nettokens, "banner": svg_banner}

for name, fn in CHARTS.items():
    for theme, tokens in THEMES.items():
        path = os.path.join(OUT, f"{name}-{theme}.svg")
        with open(path, "w") as f:
            f.write(fn(tokens))
        print(f"wrote {os.path.relpath(path)}")
