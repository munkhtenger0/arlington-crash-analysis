import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Style
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

df = pd.read_csv("arlington_crashes_2019_2023.csv")
df["date"] = pd.to_datetime(df["date"])

print("=== Arlington County Crash Analysis 2019-2023 ===")
print(f"Total crashes: {len(df):,}")
print(f"Years covered: {df['year'].min()} to {df['year'].max()}")
print(f"Serious/Fatal: {len(df[df['severity'].isin(['Serious Injury','Fatal'])]):,} ({len(df[df['severity'].isin(['Serious Injury','Fatal'])])/len(df)*100:.1f}%)")
print()

# ── FIG 1: Crashes by Year
fig, ax = plt.subplots(figsize=(9, 5))
yearly = df.groupby("year").size().reset_index(name="crashes")
bars = ax.bar(yearly["year"], yearly["crashes"], color="#1F4E79", width=0.6, zorder=3)
ax.set_title("Total Crashes by Year — Arlington County", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Number of Crashes", fontsize=11)
ax.set_xticks(yearly["year"])
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            str(int(bar.get_height())), ha="center", va="bottom", fontsize=10, color="#333")
ax.grid(axis="y", alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig("fig1_crashes_by_year.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig1")

# ── FIG 2: Crashes by Hour of Day
fig, ax = plt.subplots(figsize=(11, 5))
hourly = df.groupby("hour").size().reset_index(name="crashes")
ax.fill_between(hourly["hour"], hourly["crashes"], alpha=0.25, color="#2E75B6")
ax.plot(hourly["hour"], hourly["crashes"], color="#1F4E79", linewidth=2.5, marker="o", markersize=4)
ax.axvspan(7, 9, alpha=0.08, color="red", label="Morning rush")
ax.axvspan(16, 19, alpha=0.08, color="orange", label="Evening rush")
ax.set_title("Crash Frequency by Hour of Day", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Hour of Day (24h)", fontsize=11)
ax.set_ylabel("Number of Crashes", fontsize=11)
ax.set_xticks(range(0, 24))
ax.legend(fontsize=10)
ax.grid(axis="y", alpha=0.4)
plt.tight_layout()
plt.savefig("fig2_crashes_by_hour.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig2")

# ── FIG 3: Top Streets by Crash Count
fig, ax = plt.subplots(figsize=(9, 6))
street_counts = df["street"].value_counts().head(10).sort_values()
colors = ["#1F4E79" if i >= len(street_counts) - 3 else "#AEC6E8" for i in range(len(street_counts))]
bars = ax.barh(street_counts.index, street_counts.values, color=colors, height=0.6)
ax.set_title("Top 10 Streets by Crash Frequency", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Number of Crashes", fontsize=11)
for bar in bars:
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            str(int(bar.get_width())), va="center", fontsize=10)
ax.grid(axis="x", alpha=0.4)
plt.tight_layout()
plt.savefig("fig3_top_streets.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig3")

# ── FIG 4: Severity Breakdown
fig, ax = plt.subplots(figsize=(8, 5))
sev_order = ["Property Damage Only", "Injury", "Serious Injury", "Fatal"]
sev_counts = df["severity"].value_counts().reindex(sev_order)
colors = ["#AEC6E8", "#2E75B6", "#1F4E79", "#8B0000"]
bars = ax.bar(sev_counts.index, sev_counts.values, color=colors, width=0.55, zorder=3)
ax.set_title("Crash Severity Distribution", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Number of Crashes", fontsize=11)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f"{int(bar.get_height())}\n({int(bar.get_height())/len(df)*100:.1f}%)",
            ha="center", va="bottom", fontsize=9.5)
ax.grid(axis="y", alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig("fig4_severity.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig4")

# ── FIG 5: Crash Type Breakdown
fig, ax = plt.subplots(figsize=(9, 5))
type_counts = df["crash_type"].value_counts().sort_values()
ax.barh(type_counts.index, type_counts.values, color="#2E75B6", height=0.55)
ax.set_title("Crashes by Type", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Number of Crashes", fontsize=11)
for i, v in enumerate(type_counts.values):
    ax.text(v + 1, i, str(v), va="center", fontsize=10)
ax.grid(axis="x", alpha=0.4)
plt.tight_layout()
plt.savefig("fig5_crash_type.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig5")

# ── FIG 6: Pedestrian & Cyclist Involvement by Street
fig, ax = plt.subplots(figsize=(10, 5))
vuln = df.groupby("street")[["pedestrians_involved", "cyclists_involved"]].sum().sort_values("pedestrians_involved", ascending=False)
x = range(len(vuln))
width = 0.35
ax.bar([i - width/2 for i in x], vuln["pedestrians_involved"], width, label="Pedestrians", color="#1F4E79")
ax.bar([i + width/2 for i in x], vuln["cyclists_involved"], width, label="Cyclists", color="#AEC6E8")
ax.set_title("Pedestrian & Cyclist Involvement by Street", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Count", fontsize=11)
ax.set_xticks(list(x))
ax.set_xticklabels(vuln.index, rotation=30, ha="right", fontsize=9)
ax.legend(fontsize=10)
ax.grid(axis="y", alpha=0.4)
plt.tight_layout()
plt.savefig("fig6_vulnerable_users.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig6")

print("\nAll figures saved successfully.")
print("\nKey Findings:")
print(f"  Peak crash hour: {hourly.loc[hourly['crashes'].idxmax(), 'hour']}:00")
print(f"  Most dangerous street: {df['street'].value_counts().index[0]}")
print(f"  Most common crash type: {df['crash_type'].value_counts().index[0]}")
print(f"  Pedestrian crashes: {df['pedestrians_involved'].sum()}")
print(f"  Cyclist crashes: {df['cyclists_involved'].sum()}")
