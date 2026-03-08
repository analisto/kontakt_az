"""
Kontakt.az Notebook Market — Chart Generator
Reads data/notebooks.csv and outputs business charts to charts/
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_FILE = Path(__file__).parent.parent / "data" / "notebooks.csv"
CHARTS_DIR = Path(__file__).parent.parent / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
BRAND_COLORS = {
    "Lenovo": "#E8274B",
    "Asus":   "#0078D7",
    "HP":     "#0096D6",
    "Apple":  "#555555",
    "Acer":   "#83B81A",
    "HUAWEI": "#CF0A2C",
    "HONOR":  "#1A1A2E",
    "MSI":    "#E60012",
    "Dell":   "#007DB8",
}

SEGMENT_COLORS = {
    "Budget (<1000 AZN)":      "#4CAF50",
    "Mid-Range (1000–2000)":   "#2196F3",
    "Premium (2000–3500)":     "#FF9800",
    "Luxury (3500+ AZN)":      "#9C27B0",
}

plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
    "xtick.labelsize":  10,
    "ytick.labelsize":  10,
    "figure.dpi":       130,
})


# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_price(p):
    if pd.isna(p):
        return None
    s = str(p).strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def add_bar_labels(ax, fmt="{:.0f}", pad=3, fontsize=9, color="black"):
    for patch in ax.patches:
        w = patch.get_width()
        h = patch.get_height()
        if w == 0 and h == 0:
            continue
        # Horizontal bars
        if patch.get_height() < patch.get_width() * 0.3 and w > 0 and h < 1:
            ax.text(
                w + pad,
                patch.get_y() + patch.get_height() / 2,
                fmt.format(w),
                va="center", ha="left", fontsize=fontsize, color=color,
            )
        else:
            if h > 0:
                ax.text(
                    patch.get_x() + patch.get_width() / 2,
                    h + pad,
                    fmt.format(h),
                    ha="center", va="bottom", fontsize=fontsize, color=color,
                )


def save(fig, name):
    path = CHARTS_DIR / name
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved → {path.name}")


# ── Load & prepare data ───────────────────────────────────────────────────────

def load_data():
    df = pd.read_csv(DATA_FILE)
    df["price_num"] = df["price"].apply(clean_price)
    df["orig_num"]  = df["original_price"].apply(clean_price)

    seg_order = [
        "Budget (<1000 AZN)",
        "Mid-Range (1000–2000)",
        "Premium (2000–3500)",
        "Luxury (3500+ AZN)",
    ]

    def segment(p):
        if pd.isna(p):    return None
        if p < 1_000:     return "Budget (<1000 AZN)"
        if p < 2_000:     return "Mid-Range (1000–2000)"
        if p < 3_500:     return "Premium (2000–3500)"
        return                   "Luxury (3500+ AZN)"

    df["segment"] = pd.Categorical(df["price_num"].apply(segment), categories=seg_order, ordered=True)

    disc = df[df["orig_num"].notna()].copy()
    disc["discount_pct"] = (
        (disc["orig_num"] - disc["price_num"]) / disc["orig_num"] * 100
    ).round(1)

    return df, disc


# ── Chart 1 ── Brand Portfolio Depth ─────────────────────────────────────────

def chart_brand_catalog(df):
    counts = df["brand"].value_counts().sort_values(ascending=True)
    colors = [BRAND_COLORS.get(b, "#999") for b in counts.index]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(counts.index, counts.values, color=colors, height=0.6)

    for bar, val in zip(bars, counts.values):
        ax.text(val + 0.4, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", ha="left", fontsize=10, fontweight="bold")

    ax.set_xlabel("Number of Models Listed")
    ax.set_title("Brand Catalog Depth — Number of Models Available on Kontakt.az")
    ax.set_xlim(0, counts.max() * 1.15)
    ax.axvline(counts.mean(), color="gray", linestyle="--", linewidth=1, alpha=0.6)
    ax.text(counts.mean() + 0.2, -0.6, f"Avg {counts.mean():.0f}", fontsize=8.5,
            color="gray", va="top")
    fig.tight_layout()
    save(fig, "01_brand_catalog_depth.png")


# ── Chart 2 ── Average Price by Brand ────────────────────────────────────────

def chart_avg_price_by_brand(df):
    avg = (df.groupby("brand")["price_num"]
             .mean()
             .sort_values(ascending=False)
             .round(0))
    colors = [BRAND_COLORS.get(b, "#999") for b in avg.index]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(avg.index, avg.values, color=colors, width=0.6)

    for bar, val in zip(bars, avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 30,
                f"{val:,.0f}", ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    ax.set_ylabel("Average Price (AZN)")
    ax.set_title("Average Notebook Price by Brand — Positioning in the Market")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_ylim(0, avg.max() * 1.15)
    fig.tight_layout()
    save(fig, "02_avg_price_by_brand.png")


# ── Chart 3 ── Price Segment Distribution (count) ────────────────────────────

def chart_segment_distribution(df):
    counts = df["segment"].value_counts().sort_index()
    colors = [SEGMENT_COLORS[s] for s in counts.index]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(counts.index, counts.values, color=colors, width=0.55)

    for bar, val in zip(bars, counts.values):
        pct = val / len(df) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1.2,
                f"{val}\n({pct:.0f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylabel("Number of Models")
    ax.set_title("Market Composition by Price Tier — Where Are Customers Being Served?")
    ax.set_ylim(0, counts.max() * 1.25)
    ax.tick_params(axis="x", labelsize=9.5)
    fig.tight_layout()
    save(fig, "03_price_segment_distribution.png")


# ── Chart 4 ── Brand × Segment Stacked Bar ───────────────────────────────────

def chart_brand_segment_stacked(df):
    seg_order = [
        "Budget (<1000 AZN)",
        "Mid-Range (1000–2000)",
        "Premium (2000–3500)",
        "Luxury (3500+ AZN)",
    ]
    cross = (df.groupby(["brand", "segment"], observed=True)
               .size()
               .unstack(fill_value=0)
               .reindex(columns=seg_order, fill_value=0))
    cross = cross.loc[cross.sum(axis=1).sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(11, 6))
    bottoms = np.zeros(len(cross))
    for seg in seg_order:
        vals = cross[seg].values
        bars = ax.bar(cross.index, vals, bottom=bottoms,
                      label=seg, color=SEGMENT_COLORS[seg], width=0.6)
        for bar, val, bot in zip(bars, vals, bottoms):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bot + val / 2,
                        str(val), ha="center", va="center",
                        fontsize=8.5, color="white", fontweight="bold")
        bottoms += vals

    ax.set_ylabel("Number of Models")
    ax.set_title("Brand Strategy by Price Tier — Portfolio Spread Across Market Segments")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax.set_ylim(0, cross.sum(axis=1).max() * 1.18)
    fig.tight_layout()
    save(fig, "04_brand_segment_stacked.png")


# ── Chart 5 ── Discount Depth by Brand ───────────────────────────────────────

def chart_discount_by_brand(disc):
    avg_disc = (disc.groupby("brand")["discount_pct"]
                    .mean()
                    .sort_values(ascending=False)
                    .round(1))
    disc_count = disc.groupby("brand").size().reindex(avg_disc.index)

    colors = [BRAND_COLORS.get(b, "#999") for b in avg_disc.index]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(avg_disc.index, avg_disc.values, color=colors, width=0.6, alpha=0.88)

    for bar, val, b in zip(bars, avg_disc.values, avg_disc.index):
        n = disc_count[b]
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
                f"{val}%\n({n} models)", ha="center", va="bottom",
                fontsize=9, fontweight="bold")

    ax.set_ylabel("Average Discount (%)")
    ax.set_title("Average Discount Depth by Brand — Who Is Competing on Price?")
    ax.set_ylim(0, avg_disc.max() * 1.3)
    ax.axhline(avg_disc.mean(), color="gray", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(len(avg_disc) - 0.45, avg_disc.mean() + 0.2,
            f"Avg {avg_disc.mean():.1f}%", fontsize=8.5, color="gray")
    fig.tight_layout()
    save(fig, "05_discount_depth_by_brand.png")


# ── Chart 6 ── Price Range (Min / Max) by Brand ──────────────────────────────

def chart_price_range_by_brand(df):
    rng = df.groupby("brand")["price_num"].agg(["min", "max", "median"])
    rng = rng.sort_values("median", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = range(len(rng))
    colors = [BRAND_COLORS.get(b, "#999") for b in rng.index]

    ax.barh([b + " (range)" for b in rng.index],
            rng["max"] - rng["min"],
            left=rng["min"],
            color=colors, alpha=0.35, height=0.55)

    for i, (brand, row) in enumerate(rng.iterrows()):
        ax.plot(row["median"], i, "D", color=BRAND_COLORS.get(brand, "#333"),
                markersize=8, zorder=5)
        ax.text(row["min"] - 30, i, f"{row['min']:,.0f}",
                va="center", ha="right", fontsize=8.5)
        ax.text(row["max"] + 30, i, f"{row['max']:,.0f}",
                va="center", ha="left", fontsize=8.5)

    ax.set_xlabel("Price (AZN)")
    ax.set_title("Price Range by Brand — Entry Price vs Ceiling & Median (◆)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_yticks(range(len(rng)))
    ax.set_yticklabels(rng.index)
    fig.tight_layout()
    save(fig, "06_price_range_by_brand.png")


# ── Chart 7 ── Category Mix (spec data) ──────────────────────────────────────

def chart_category_mix(df):
    cat_df = df[df["kateqoriya"].notna()]
    if len(cat_df) == 0:
        print("  [skip] No category data available.")
        return

    counts = cat_df["kateqoriya"].value_counts()
    cat_colors = ["#2196F3", "#FF9800", "#E8274B", "#4CAF50"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts.index, counts.values,
                  color=cat_colors[:len(counts)], width=0.5)

    for bar, val in zip(bars, counts.values):
        pct = val / len(cat_df) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5,
                f"{val} ({pct:.0f}%)", ha="center", va="bottom",
                fontsize=10, fontweight="bold")

    ax.set_ylabel("Number of Models")
    ax.set_title("Product Category Breakdown — Business, Premium, Gaming, Professional")
    ax.set_ylim(0, counts.max() * 1.25)
    fig.tight_layout()
    save(fig, "07_product_category_mix.png")


# ── Chart 8 ── Top 10 Models by Discount Amount (AZN) ────────────────────────

def chart_top_discounts(disc):
    disc = disc.copy()
    disc["discount_azn"] = (disc["orig_num"] - disc["price_num"]).round(0)
    top = disc.nlargest(10, "discount_azn")[
        ["name", "brand", "price_num", "orig_num", "discount_azn", "discount_pct"]
    ].copy()
    top["short_name"] = top["name"].str.replace("Notbuk ", "", regex=False).str[:38]
    top = top.sort_values("discount_azn")

    colors = [BRAND_COLORS.get(b, "#999") for b in top["brand"]]
    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(top["short_name"], top["discount_azn"], color=colors, height=0.6)

    for bar, row in zip(bars, top.itertuples()):
        ax.text(row.discount_azn + 10, bar.get_y() + bar.get_height() / 2,
                f"–{row.discount_azn:,.0f} AZN  ({row.discount_pct:.0f}%)",
                va="center", ha="left", fontsize=9, fontweight="bold")

    ax.set_xlabel("Discount Amount (AZN)")
    ax.set_title("Top 10 Models by Absolute Discount — Biggest Price Drops Available")
    ax.set_xlim(0, top["discount_azn"].max() * 1.35)
    fig.tight_layout()
    save(fig, "08_top_discount_models.png")


# ── Chart 9 ── Discount Coverage: Discounted vs Full-Price by Brand ───────────

def chart_discount_coverage(df, disc):
    all_counts   = df.groupby("brand").size().rename("total")
    disc_counts  = disc.groupby("brand").size().rename("on_sale")
    coverage = pd.concat([all_counts, disc_counts], axis=1).fillna(0)
    coverage["full_price"] = coverage["total"] - coverage["on_sale"]
    coverage = coverage.sort_values("total", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(coverage))
    bars1 = ax.bar(coverage.index, coverage["on_sale"],
                   color="#FF9800", label="On Discount", width=0.6)
    bars2 = ax.bar(coverage.index, coverage["full_price"],
                   bottom=coverage["on_sale"],
                   color="#2196F3", label="Full Price", width=0.6)

    for bar, b in zip(bars1, coverage.index):
        n = int(coverage.loc[b, "on_sale"])
        if n > 0:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    n / 2, str(n),
                    ha="center", va="center", fontsize=8.5,
                    color="white", fontweight="bold")

    totals = coverage["total"].values
    for i, (total, bar) in enumerate(zip(totals, bars2)):
        ax.text(bar.get_x() + bar.get_width() / 2,
                total + 0.4, str(int(total)),
                ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_ylabel("Number of Models")
    ax.set_title("Discount Coverage by Brand — How Many Models Are on Sale?")
    ax.legend(fontsize=10)
    ax.set_ylim(0, coverage["total"].max() * 1.2)
    fig.tight_layout()
    save(fig, "09_discount_coverage_by_brand.png")


# ── Chart 10 ── Price Trend Across Segments for Top 4 Brands ─────────────────

def chart_brand_price_segments(df):
    top4 = df["brand"].value_counts().head(4).index.tolist()
    seg_order = [
        "Budget (<1000 AZN)",
        "Mid-Range (1000–2000)",
        "Premium (2000–3500)",
        "Luxury (3500+ AZN)",
    ]

    plot_data = (df[df["brand"].isin(top4)]
                 .groupby(["brand", "segment"], observed=True)
                 .size()
                 .unstack(fill_value=0)
                 .reindex(columns=seg_order, fill_value=0))

    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(seg_order))
    width = 0.2
    offsets = [-1.5, -0.5, 0.5, 1.5]

    for brand, offset in zip(top4, offsets):
        vals = plot_data.loc[brand].values if brand in plot_data.index else np.zeros(4)
        bars = ax.bar(x + offset * width, vals,
                      width=width * 0.9,
                      color=BRAND_COLORS.get(brand, "#999"),
                      label=brand, alpha=0.9)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, val + 0.2,
                        str(val), ha="center", va="bottom", fontsize=8.5)

    ax.set_xticks(x)
    ax.set_xticklabels(seg_order, fontsize=9.5)
    ax.set_ylabel("Number of Models")
    ax.set_title("Top 4 Brands — How Each Positions Across Price Tiers")
    ax.legend(fontsize=10)
    ax.set_ylim(0, plot_data.values.max() * 1.25)
    fig.tight_layout()
    save(fig, "10_top4_brand_price_positioning.png")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Loading data from {DATA_FILE}…")
    df, disc = load_data()
    print(f"  {len(df)} products | {len(disc)} on discount\n")
    print("Generating charts…")
    chart_brand_catalog(df)
    chart_avg_price_by_brand(df)
    chart_segment_distribution(df)
    chart_brand_segment_stacked(df)
    chart_discount_by_brand(disc)
    chart_price_range_by_brand(df)
    chart_category_mix(df)
    chart_top_discounts(disc)
    chart_discount_coverage(df, disc)
    chart_brand_price_segments(df)
    print(f"\nAll charts saved to: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
