import pandas as pd
import glob
import os


# Find the JSON file created by Task 1 inside the data folder.
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No Task 1 JSON file found in the data folder.")
    exit()

# Use the first matching JSON file.
json_file = json_files[0]

# Load the JSON data into a Pandas DataFrame.
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")


# ---------------------------------------------------------
# 1. Remove duplicate stories
# ---------------------------------------------------------

df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# ---------------------------------------------------------
# 2. Remove rows with missing required values
# ---------------------------------------------------------

df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# ---------------------------------------------------------
# 3. Clean the data types
# ---------------------------------------------------------

# Convert score to integer.
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# Convert number of comments to integer.
df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
)

# Remove rows where conversion created missing values.
df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# ---------------------------------------------------------
# 4. Remove low-quality stories
# ---------------------------------------------------------

df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# ---------------------------------------------------------
# 5. Remove extra whitespace from titles
# ---------------------------------------------------------

df["title"] = df["title"].str.strip()


# ---------------------------------------------------------
# 6. Save the cleaned data as CSV
# ---------------------------------------------------------

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print()
print(f"Saved {len(df)} rows to {output_file}")


# ---------------------------------------------------------
# 7. Print stories per category
# ---------------------------------------------------------

print()
print("Stories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")