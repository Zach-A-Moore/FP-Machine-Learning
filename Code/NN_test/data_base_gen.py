import pandas as pd
import numpy as np

# Function to generate binary data with some pattern
def generate_data(n_samples, pattern_shift=0):
    data = []
    for i in range(n_samples):
        f1 = np.random.randint(0, 2)
        f2 = np.random.randint(0, 2)
        f3 = np.random.randint(0, 2)
        # Label: simple pattern (e.g., majority vote with a shift)
        label = 1 if (f1 + f2 + f3 + pattern_shift) % 2 == 0 else 0
        data.append({"feature1": f1, "feature2": f2, "feature3": f3, "label": label})
    return pd.DataFrame(data)

# Generate datasets
train_df = generate_data(10, pattern_shift=0)  # Training set
test1_df = generate_data(5, pattern_shift=0)   # Test set 1 (similar pattern)
test2_df = generate_data(5, pattern_shift=1)   # Test set 2 (shifted pattern)

# Save to CSV
train_df.to_csv("train_data.csv", index=False)
test1_df.to_csv("test_data1.csv", index=False)
test2_df.to_csv("test_data2.csv", index=False)

print("Datasets created: train_data.csv, test_data1.csv, test_data2.csv")