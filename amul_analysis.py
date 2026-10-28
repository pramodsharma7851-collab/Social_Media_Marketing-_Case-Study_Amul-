import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "amul_social_media_dataset.csv")
CHART_DIR = os.path.join(BASE_DIR, "charts")
REPORT_DIR = os.path.join(BASE_DIR, "report")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["date"])

df["engagements"] = df[["likes", "comments", "shares", "saves"]].sum(axis=1)
df["engagement_rate_pct"] = (df["engagements"] / df["reach"] * 100).round(2)

# Platform performance
platform_summary = (
    df.groupby("platform")
    .agg(
        posts=("date", "count"),
        total_reach=("reach", "sum"),
        total_engagements=("engagements", "sum"),
        avg_engagement_rate=("engagement_rate_pct", "mean"),
    )
    .round(2)
    .sort_values("avg_engagement_rate", ascending=False)
)

# Post format performance
format_summary = (
    df.groupby("post_type")
    .agg(
        posts=("date", "count"),
        avg_reach=("reach", "mean"),
        avg_engagement_rate=("engagement_rate_pct", "mean"),
        avg_shares=("shares", "mean"),
        avg_saves=("saves", "mean"),
    )
    .round(2)
    .sort_values("avg_engagement_rate", ascending=False)
)

# Content theme performance
theme_summary = (
    df.groupby("topic_category")
    .agg(
        posts=("date", "count"),
        avg_reach=("reach", "mean"),
        avg_engagement_rate=("engagement_rate_pct", "mean"),
        avg_shares=("shares", "mean"),
        avg_saves=("saves", "mean"),
    )
    .round(2)
    .sort_values("avg_engagement_rate", ascending=False)
)

platform_summary.to_csv(os.path.join(REPORT_DIR, "platform_summary.csv"))
format_summary.to_csv(os.path.join(REPORT_DIR, "format_summary.csv"))
theme_summary.to_csv(os.path.join(REPORT_DIR, "theme_performance.csv"))

# Chart 1: Engagement by content theme
plt.figure(figsize=(10, 6))
theme_summary["avg_engagement_rate"].sort_values().plot(kind="barh", color="#1f77b4")
plt.title("Average Engagement Rate by Content Theme")
plt.xlabel("Engagement Rate (%)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "engagement_by_theme.png"), dpi=160)
plt.close()

# Chart 2: Engagement by post format
plt.figure(figsize=(10, 6))
format_summary["avg_engagement_rate"].sort_values().plot(kind="barh", color="#2ca02c")
plt.title("Average Engagement Rate by Post Format")
plt.xlabel("Engagement Rate (%)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "engagement_by_format.png"), dpi=160)
plt.close()

# Chart 3: Engagements by platform
plt.figure(figsize=(10, 6))
platform_summary["total_engagements"].sort_values().plot(kind="barh", color="#ff7f0e")
plt.title("Total Engagements by Platform")
plt.xlabel("Engagements")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "engagements_by_platform.png"), dpi=160)
plt.close()

# Chart 4: Instagram engagement trend
instagram = df[df["platform"] == "Instagram"].sort_values("date")
plt.figure(figsize=(12, 6))
plt.plot(instagram["date"], instagram["engagement_rate_pct"], marker="o")
plt.title("Instagram Engagement Rate Over Time")
plt.ylabel("Engagement Rate (%)")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "instagram_engagement_trend.png"), dpi=160)
plt.close()

print("Analysis completed successfully.")
print("\nPlatform Summary:")
print(platform_summary)
print("\nFormat Summary:")
print(format_summary)
print("\nTheme Summary:")
print(theme_summary)
