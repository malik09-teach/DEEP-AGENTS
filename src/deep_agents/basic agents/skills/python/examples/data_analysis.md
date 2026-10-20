# Data Analysis Examples

## Data Processing with Pandas & NumPy

### 1. Loading and Cleaning Data
```python
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("dataset.csv")

# Clean missing values and format dates
df = df.dropna(subset=["id", "timestamp"])
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["amount"] = df["amount"].fillna(df["amount"].median())
```

### 2. Grouping and Aggregating
```python
# Aggregate sales and counts per category
summary = (
    df.groupby("category")
    .agg(
        total_sales=("amount", "sum"),
        avg_transaction=("amount", "mean"),
        transaction_count=("id", "count")
    )
    .reset_index()
    .sort_values(by="total_sales", ascending=False)
)

print(summary.head(10))
```

### 3. Statistical Analysis
```python
# Calculate descriptive metrics and percentiles
p25, p75 = np.percentile(df["amount"], [25, 75])
iqr = p75 - p25
outliers = df[(df["amount"] < (p25 - 1.5 * iqr)) | (df["amount"] > (p75 + 1.5 * iqr))]

print(f"Detected {len(outliers)} statistical outlier records.")
```
