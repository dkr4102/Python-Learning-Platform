"""
Project 8: Sales Analytics Dashboard
Ingests commercial sales records, performs Pandas aggregations, and generates Matplotlib charts.
"""
import io
import base64
from typing import Dict, Any, List
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt

SAMPLE_SALES_DATA = [
    {"Date": "2026-10-01", "Region": "West", "Category": "Hardware", "Product": "Laptops", "Units": 24, "Price": 850.0},
    {"Date": "2026-10-02", "Region": "North", "Category": "Hardware", "Product": "Monitors", "Units": 45, "Price": 220.0},
    {"Date": "2026-10-03", "Region": "South", "Category": "Software", "Product": "IDE Subscriptions", "Units": 120, "Price": 65.0},
    {"Date": "2026-10-04", "Region": "West", "Category": "Books", "Product": "Python Guides", "Units": 80, "Price": 35.0},
    {"Date": "2026-10-05", "Region": "East", "Category": "Hardware", "Product": "Mechanical Keyboards", "Units": 55, "Price": 95.0},
    {"Date": "2026-10-06", "Region": "North", "Category": "Software", "Product": "Cloud Compute Credits", "Units": 60, "Price": 140.0},
    {"Date": "2026-10-07", "Region": "West", "Category": "Software", "Product": "Analytics Licenses", "Units": 30, "Price": 300.0},
    {"Date": "2026-10-08", "Region": "South", "Category": "Hardware", "Product": "USB-C Hubs", "Units": 90, "Price": 38.0},
    {"Date": "2026-10-09", "Region": "East", "Category": "Books", "Product": "Algorithms Manuals", "Units": 40, "Price": 48.0},
    {"Date": "2026-10-10", "Region": "North", "Category": "Books", "Product": "Data Science Handbooks", "Units": 65, "Price": 42.0}
]

def run_sales_analysis(records: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not records:
        records = SAMPLE_SALES_DATA

    df = pd.DataFrame(records)
    # Vectorized Revenue
    df["Revenue"] = df["Units"] * df["Price"]

    total_revenue = float(df["Revenue"].sum())
    total_units = int(df["Units"].sum())
    average_order_value = float(df["Revenue"].mean())

    # Category Groupby
    cat_summary = df.groupby("Category").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Units=("Units", "sum"),
        Avg_Price=("Price", "mean")
    ).reset_index()

    # Region Groupby
    region_summary = df.groupby("Region")["Revenue"].sum().reset_index()

    # 1. Generate Matplotlib Category Bar Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), facecolor="#FBF8F3")
    
    # Palette styling
    colors = ["#23342B", "#6E8098", "#D8B6A3", "#8B9B82"]
    
    # Ax1: Category Revenue Bar Chart
    ax1.set_facecolor("#FBF8F3")
    bars = ax1.bar(
        cat_summary["Category"],
        cat_summary["Total_Revenue"],
        color=colors[:len(cat_summary)],
        edgecolor="#161616",
        width=0.55
    )
    ax1.set_title("Revenue by Product Category ($)", fontsize=11, fontweight="bold", pad=10, color="#161616")
    ax1.set_ylabel("Revenue ($)", fontsize=9, color="#5E5A55")
    ax1.grid(axis="y", linestyle="--", alpha=0.35)
    ax1.tick_params(colors="#161616", labelsize=9)
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f"${height:,.0f}",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=8, fontweight="bold", color="#23342B")

    # Ax2: Regional Revenue Distribution Pie Chart
    ax2.set_facecolor("#FBF8F3")
    ax2.pie(
        region_summary["Revenue"],
        labels=region_summary["Region"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[:len(region_summary)],
        wedgeprops={"edgecolor": "#161616", "linewidth": 0.8},
        textprops={"fontsize": 9, "color": "#161616"}
    )
    ax2.set_title("Regional Distribution", fontsize=11, fontweight="bold", pad=10, color="#161616")

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)

    chart_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return {
        "success": True,
        "total_revenue": round(total_revenue, 2),
        "total_units": total_units,
        "average_order_value": round(average_order_value, 2),
        "top_category": cat_summary.sort_values(by="Total_Revenue", ascending=False).iloc[0]["Category"],
        "top_region": region_summary.sort_values(by="Revenue", ascending=False).iloc[0]["Region"],
        "category_metrics": cat_summary.to_dict(orient="records"),
        "region_metrics": region_summary.to_dict(orient="records"),
        "chart_png_base64": chart_base64
    }
