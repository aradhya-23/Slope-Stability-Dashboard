

import pandas as pd
import os

IN_PATH = "data/features.csv"
OUT_PATH = "data/labeled_data.csv"

def rule_based_label(df):
    # Add binary label: 1 = stable, 0 = unstable
    df["label"] = df.apply(
        lambda r: 1 if (r["slope"] > 25 and r["NDVI"] < 0.3 and r["rainfall"] > 500) else 0,
        axis=1
    )

    # Add human-readable text column for dashboard
    df["stability"] = df["label"].map({1: "Stable", 0: "Unstable"})

    return df

def main():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"{IN_PATH} not found. Run collect_ee.py first.")

    df = pd.read_csv(IN_PATH)
    df = rule_based_label(df)
    df.to_csv(OUT_PATH, index=False)
    print(f"✅ Labeled data saved to {OUT_PATH}")

if __name__ == "__main__":
    main()
