import pandas as pd

INPUT_FILE = "dns_preprocessed_dataset.csv"
OUTPUT_FILE = "dns_preprocessed_dataset_deduplicated.csv"

print("Loading dataset...")
df = pd.read_csv(INPUT_FILE)

original_count = len(df)

print(f"Original rows: {original_count}")

# Remove exact duplicate rows
df_clean = df.drop_duplicates()

cleaned_count = len(df_clean)
removed = original_count - cleaned_count

print(f"Rows after deduplication: {cleaned_count}")
print(f"Duplicate rows removed: {removed}")

# Save cleaned dataset
df_clean.to_csv(OUTPUT_FILE, index=False)

print(f"\n✅ Deduplicated dataset saved as: {OUTPUT_FILE}")
