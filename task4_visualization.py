import pandas as pd
import matplotlib.pyplot as plt
import os


# Load the analysed CSV created in Task 3.
df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs folder if it does not already exist.
os.makedirs("outputs", exist_ok=True)


# =========================================================
# Chart 1 — Top 10 Stories by Score
# =========================================================

# Select the 10 stories with the highest scores.
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters.
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Display the highest scoring story at the top.
plt.gca().invert_yaxis()

plt.tight_layout()

# Save before showing the chart.
plt.savefig("outputs/chart1_top_stories.png")

plt.show()
plt.close()


# =========================================================
# Chart 2 — Stories per Category
# =========================================================

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 6))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()

# Save before showing the chart.
plt.savefig("outputs/chart2_categories.png")

plt.show()
plt.close()


# =========================================================
# Chart 3 — Score vs Comments
# =========================================================

plt.figure(figsize=(9, 6))

# Separate popular and non-popular stories.
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    color="green"
)

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    color="red"
)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()

# Save before showing the chart.
plt.savefig("outputs/chart3_scatter.png")

plt.show()
plt.close()


# =========================================================
# Bonus — TrendPulse Dashboard
# =========================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 11))

# Overall dashboard title.
fig.suptitle("TrendPulse Dashboard", fontsize=18)


# -------------------------
# Dashboard Chart 1
# -------------------------

axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].invert_yaxis()


# -------------------------
# Dashboard Chart 2
# -------------------------

axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=[
        "steelblue",
        "orange",
        "green",
        "red",
        "purple"
    ]
)

axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")
axes[0, 1].set_title("Stories per Category")


# -------------------------
# Dashboard Chart 3
# -------------------------

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    color="green"
)

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    color="red"
)

axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].set_title("Score vs Comments")
axes[1, 0].legend()


# Leave the fourth dashboard area available for future analysis.
axes[1, 1].axis("off")


plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save the complete dashboard.
plt.savefig("outputs/dashboard.png")

plt.show()
plt.close()


print("\nVisualization complete!")
print("Saved:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png")