"""
Graphical Abstract — Operability Analysis of a Natural Gas Processing Plant
===========================================================================
Generates a 1328x531 px (2x=2656x1062) graphical abstract using PIL.

Layout:
  Col 1: Process flowsheet (DWSIM)
  Col 2: LPG_C5 x NG_RVP trade-off with DOS boundary (Fig 4a)
  Col 3: LPG_C2 x NG_RVP feasible region with SLSQP at active constraints (Fig 5)
  Bottom: 4 Key Findings cards

Requirements:
    pip install Pillow matplotlib numpy pandas

Usage:
    - Adjust FLOWSHEET_PATH, AOS_PLOT_PATH, and DATASET_PATH below
    - Run: python graphical_abstract.py

Authors: Gabriel F. Ferraz, Roymel R. Carpio, Nicolas Spogis
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

# ============================================================
# PATHS — adjust to your local files
# ============================================================
FLOWSHEET_PATH = "graphical_abstract/flowsheet.png"
AOS_PLOT_PATH  = "figures/fig8_lpgc5_ngrvp_tradeoff.png"
DATASET_PATH   = "../datasets/dataset_clean.csv"
OUTPUT_DIR     = "graphical_abstract"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# CONFIG
# ============================================================
SCALE = 2
W, H = 1328 * SCALE, 531 * SCALE

# Colors (RGB)
C_BG      = (250, 251, 253)
C_DARK    = (26, 26, 46)
C_TEAL    = (13, 115, 119)
C_ACCENT  = (214, 39, 40)
C_BLUE    = (31, 119, 180)
C_GREEN   = (44, 160, 44)
C_PURPLE  = (123, 45, 142)
C_LGRAY   = (237, 242, 247)
C_WHITE   = (255, 255, 255)
C_TEXT    = (50, 50, 50)
C_SUBTEXT = (74, 85, 104)

C_ACCENT_LIGHT = (254, 235, 235)
C_BLUE_LIGHT   = (230, 242, 255)
C_GREEN_LIGHT  = (230, 252, 237)
C_PURPLE_LIGHT = (243, 232, 250)

# Layout
H_TITLE = int(H * 0.11)
H_MID   = int(H * 0.58)
H_GAP1  = int(H * 0.015)

COL_PAD  = int(W * 0.012)
COL_GAP  = int(W * 0.04)  # Wide gap for visible arrows
USABLE_W = W - 2 * COL_PAD
COL_W1   = int((USABLE_W - 2 * COL_GAP) * 0.30)
COL_W2   = int((USABLE_W - 2 * COL_GAP) * 0.37)
COL_W3   = USABLE_W - COL_W1 - COL_W2 - 2 * COL_GAP


# ============================================================
# HELPERS
# ============================================================
def get_font(size, bold=False):
    candidates = ([
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "C:/Windows/Fonts/timesbd.ttf",
        "C:/Windows/Fonts/georgiabd.ttf",
    ] if bold else [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/georgia.ttf",
    ])
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            pass
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, fill, radius=8, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, text, x_center, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x_center - tw // 2, y), text, font=font, fill=fill)


def fit_image(img, max_w, max_h):
    ratio = min(max_w / img.width, max_h / img.height)
    return img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)


def auto_crop(img, margin=15):
    arr = np.array(img)
    gray = np.mean(arr, axis=2)
    rows = np.where(gray < 250)[0]
    cols = np.where(gray < 250)[1]
    if len(rows) > 0 and len(cols) > 0:
        return img.crop((max(0, cols.min() - margin), max(0, rows.min() - margin),
                         min(img.width, cols.max() + margin),
                         min(img.height, rows.max() + margin)))
    return img


def draw_arrow(draw, x1, x2, y, color):
    """Draw a proper arrow with long shaft + triangular head."""
    head_w = 24   # triangle depth (pixels)
    head_h = 18   # triangle half-height
    shaft_h = 5   # shaft half-thickness
    shaft_end = x2 - head_w
    # Shaft
    draw.rectangle([(x1, y - shaft_h), (shaft_end, y + shaft_h)], fill=color)
    # Arrowhead
    draw.polygon([(x2, y), (shaft_end, y - head_h), (shaft_end, y + head_h)], fill=color)


def make_fig5_plot(dataset_path):
    """
    Generate Figure 5 from the paper: LPG_C2 vs NG_RVP for feasible points
    with SLSQP optimal at the intersection of active constraints.
    
    Column mapping from dataset_clean.csv:
        GVC1     = SG_C1   (methane in SG, mol%)
        GVC2     = LPG_C2  (ethane in LPG, mol%)
        GVC5     = LPG_C5  (C5+ in LPG, mol%)
        GVC5_PVR = NG_RVP  (Reid Vapour Pressure of NG, kPa)
        Sales_Price = Revenue ($/h)
    """
    df = pd.read_csv(dataset_path)
    feas = df[
        (df["GVC1"] >= 80) &
        (df["GVC2"] <= 12) &
        (df["GVC5"] <= 2) &
        (df["GVC5_PVR"] <= 76)
    ]

    fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    sc = ax.scatter(feas["GVC2"], feas["GVC5_PVR"], c=feas["Sales_Price"],
                    cmap="viridis", s=20, alpha=0.8, edgecolors="none", zorder=2)
    ax.axhline(76, color="#d62728", ls="--", lw=1.5, label="NG_RVP = 76", zorder=1)
    ax.axvline(12, color="#1f77b4", ls="--", lw=1.5, label="LPG_C2 = 12", zorder=1)

    # SLSQP optimal at constraint intersection
    ax.scatter([12.0], [76.0], marker="*", s=250, c="#ff7f0e",
              edgecolors="black", linewidths=0.8, zorder=5,
              label="SLSQP (663.85 $/h)")

    ax.set_xlabel("LPG_C2 (Ethane in LPG, mol%)", fontsize=9, fontfamily="serif")
    ax.set_ylabel("NG_RVP (kPa)", fontsize=9, fontfamily="serif")
    ax.set_title("Active constraints at optimal", fontsize=9,
                 fontfamily="serif", fontweight="bold")
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=6.5, loc="lower left", framealpha=0.9)

    cb = fig.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label("Revenue ($/h)", fontsize=8, fontfamily="serif")
    cb.ax.tick_params(labelsize=7)

    plt.tight_layout()
    tmp = os.path.join(OUTPUT_DIR, "_tmp_fig5.png")
    fig.savefig(tmp, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    return Image.open(tmp)


# ============================================================
# BUILD CANVAS
# ============================================================
canvas = Image.new("RGB", (W, H), C_BG)
draw = ImageDraw.Draw(canvas)

# Fonts
f_title  = get_font(int(22 * SCALE), bold=True)
f_sub    = get_font(int(11 * SCALE))
f_sec    = get_font(int(16 * SCALE), bold=True)
f_kf_t   = get_font(int(18 * SCALE), bold=True)
f_kf_d   = get_font(int(14 * SCALE))

# ── TITLE BAR ──
draw_rounded_rect(draw, (0, 0, W, H_TITLE), fill=C_DARK, radius=0)
center_text(draw,
    "Operability Analysis of a Natural Gas Processing Plant",
    W // 2, int(H_TITLE * 0.15), f_title, C_WHITE)
center_text(draw,
    "DWSIM Simulation  |  LHS Sampling (2000 pts)  |  SLSQP Constrained Optimization",
    W // 2, int(H_TITLE * 0.60), f_sub, (170, 180, 190))

# ── MIDDLE SECTION ──
y_mid = H_TITLE + H_GAP1
col_hdr_h = int(H_MID * 0.09)

# ── COL 1: Process Simulation (flowsheet only) ──
x1 = COL_PAD
draw_rounded_rect(draw, (x1, y_mid, x1 + COL_W1, y_mid + col_hdr_h),
                  fill=C_TEAL, radius=6)
center_text(draw, "1. Process Simulation",
            x1 + COL_W1 // 2, y_mid + int(col_hdr_h * 0.12), f_sec, C_WHITE)

flow = Image.open(FLOWSHEET_PATH)
flow_avail_h = H_MID - col_hdr_h - 16
flow_fit = fit_image(flow, COL_W1 - 16, flow_avail_h)
flow_x = x1 + (COL_W1 - flow_fit.width) // 2
flow_y = y_mid + col_hdr_h + 8
draw_rounded_rect(draw, (flow_x - 4, flow_y - 4,
                          flow_x + flow_fit.width + 4, flow_y + flow_fit.height + 4),
                  fill=C_WHITE, outline=(200, 200, 200), radius=6, width=2)
canvas.paste(flow_fit, (flow_x, flow_y))

# ── ARROW 1→2 ──
arrow_y = y_mid + H_MID // 2
draw_arrow(draw, x1 + COL_W1 + 8, x1 + COL_W1 + COL_GAP - 8, arrow_y, C_TEAL)

# ── COL 2: Operability & Trade-off (Fig 4a — LPG_C5 vs NG_RVP) ──
x2 = x1 + COL_W1 + COL_GAP
draw_rounded_rect(draw, (x2, y_mid, x2 + COL_W2, y_mid + col_hdr_h),
                  fill=C_TEAL, radius=6)
center_text(draw, "2. Operability & Trade-off",
            x2 + COL_W2 // 2, y_mid + int(col_hdr_h * 0.12), f_sec, C_WHITE)

aos = auto_crop(Image.open(AOS_PLOT_PATH))
aos_fit = fit_image(aos, COL_W2 - 16, H_MID - col_hdr_h - 16)
aos_x = x2 + (COL_W2 - aos_fit.width) // 2
aos_y = y_mid + col_hdr_h + 8
draw_rounded_rect(draw, (aos_x - 4, aos_y - 4,
                          aos_x + aos_fit.width + 4, aos_y + aos_fit.height + 4),
                  fill=C_WHITE, outline=(200, 200, 200), radius=6, width=2)
canvas.paste(aos_fit, (aos_x, aos_y))

# ── ARROW 2→3 ──
draw_arrow(draw, x2 + COL_W2 + 8, x2 + COL_W2 + COL_GAP - 8, arrow_y, C_TEAL)

# ── COL 3: Constrained Optimum (Fig 5 — LPG_C2 vs NG_RVP feasible) ──
x3 = x2 + COL_W2 + COL_GAP
draw_rounded_rect(draw, (x3, y_mid, x3 + COL_W3, y_mid + col_hdr_h),
                  fill=C_TEAL, radius=6)
center_text(draw, "3. Constrained Optimum",
            x3 + COL_W3 // 2, y_mid + int(col_hdr_h * 0.12), f_sec, C_WHITE)

fig5_img = make_fig5_plot(DATASET_PATH)
fig5_fit = fit_image(fig5_img, COL_W3 - 16, H_MID - col_hdr_h - 16)
fig5_x = x3 + (COL_W3 - fig5_fit.width) // 2
fig5_y = y_mid + col_hdr_h + 8
draw_rounded_rect(draw, (fig5_x - 4, fig5_y - 4,
                          fig5_x + fig5_fit.width + 4, fig5_y + fig5_fit.height + 4),
                  fill=C_WHITE, outline=(200, 200, 200), radius=6, width=2)
canvas.paste(fig5_fit, (fig5_x, fig5_y))

# ══════════════════════════════════════════════════════
# KEY FINDINGS — colored cards with accent bars
# ══════════════════════════════════════════════════════
y_bot = y_mid + H_MID + H_GAP1
draw_rounded_rect(draw, (0, y_bot, W, H), fill=C_LGRAY, radius=0)

findings = [
    ("OI = 14.1%",
     "Only 281/2000 samples",
     "satisfy all ANP specs",
     C_ACCENT, C_ACCENT_LIGHT),
    ("|r| = 0.97-0.98",
     "Strong DV-constraint",
     "correlations with real T",
     C_BLUE, C_BLUE_LIGHT),
    ("+7.1% Revenue",
     "SLSQP: 663.85 $/h",
     "2 active constraints = fragile",
     C_GREEN, C_GREEN_LIGHT),
    ("RVP bottleneck",
     "NG_RVP <= 76 kPa",
     "dominant constraint (+21.4 pp)",
     C_PURPLE, C_PURPLE_LIGHT),
]

card_gap = 18
total_card_w = W - 2 * COL_PAD - 3 * card_gap
card_w = total_card_w // 4
card_margin_top = 10
card_y = y_bot + card_margin_top
card_h = H - y_bot - card_margin_top - 10

for i, (title, line1, line2, color, bg_color) in enumerate(findings):
    cx = COL_PAD + i * (card_w + card_gap)

    # Card background with colored border
    draw_rounded_rect(draw, (cx, card_y, cx + card_w, card_y + card_h),
                      fill=bg_color, outline=color, radius=10, width=3)

    # Accent bar at top
    bar_inset = 20
    draw_rounded_rect(draw, (cx + bar_inset, card_y + 8,
                              cx + card_w - bar_inset, card_y + 14),
                      fill=color, radius=3)

    # Title (large, colored)
    center_text(draw, title, cx + card_w // 2, card_y + 24, f_kf_t, color)

    # Description lines
    desc_y1 = card_y + int(card_h * 0.48)
    desc_y2 = desc_y1 + int(22 * SCALE / 2)
    center_text(draw, line1, cx + card_w // 2, desc_y1, f_kf_d, C_TEXT)
    center_text(draw, line2, cx + card_w // 2, desc_y2, f_kf_d, C_SUBTEXT)

# ── SAVE ──
out_full = os.path.join(OUTPUT_DIR, "graphical_abstract_2656x1062.png")
out_spec = os.path.join(OUTPUT_DIR, "graphical_abstract_1328x531.png")

canvas.save(out_full, dpi=(300, 300))
canvas.resize((1328, 531), Image.LANCZOS).save(out_spec, dpi=(150, 150))

# Cleanup temp file
tmp = os.path.join(OUTPUT_DIR, "_tmp_fig5.png")
if os.path.exists(tmp):
    os.remove(tmp)

print(f"Saved: {out_full} ({canvas.size[0]}x{canvas.size[1]})")
print(f"Saved: {out_spec} (1328x531)")
print("Done!")
