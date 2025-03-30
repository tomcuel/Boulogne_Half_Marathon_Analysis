import pandas as pd
import numpy as np
import random
import math


# 1. Load the runners data
runners = pd.read_csv("treated_runners_data.csv", sep=";", header=0, dtype=str)
# filter out runners with invalid or missing finish times (handled separately)
valid_finish_time_mask = ~runners['Finish'].isin(["Disqualifié", "None", "Abandon"]) & pd.notna(runners['Finish'])
df = runners[valid_finish_time_mask].copy()
non_finishers = runners[~valid_finish_time_mask].copy()

# 2. Define relevant datas for clustering
# define the relevant columns 
learning_columns = ["0_5_average_diff", "5_10_average_diff", "10_15_average_diff", "15_end_average_diff", "0_5_10_diff", "5_10_15_diff", "10_15_end_diff", "start_end_diff", "10k_diff"]
# extract the features
data = df[learning_columns].apply(pd.to_numeric, errors='coerce').values

# 3. Define the K-means algorithm
def random_sample(low, high):
    return low + (high - low) * random.random()

def initialize_centroids(data, k):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    centroids = [random_sample(min_vals, max_vals) for _ in range(k)]
    return np.array(centroids)

def get_distance(point1, point2):
    return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))

def get_labels(data, centroids):
    labels = []
    for point in data:
        distances = [get_distance(point, centroid) for centroid in centroids]
        labels.append(np.argmin(distances))
    return labels

def update_centroids(data, labels, k):
    new_centroids = np.zeros((k, len(data[0])))
    counts = np.zeros(k)
    for point, label in zip(data, labels):
        new_centroids[label] += point
        counts[label] += 1
    for i in range(k):
        if counts[i] > 0:
            new_centroids[i] /= counts[i]
    return new_centroids

def should_stop(old_centroids, new_centroids, threshold=1e-5):
    total_movement = np.sum([get_distance(o, n) for o, n in zip(old_centroids, new_centroids)])
    return total_movement < threshold

def kmeans(data, k):
    centroids = initialize_centroids(data, k)
    while True:
        old_centroids = np.copy(centroids)
        labels = get_labels(data, centroids)
        centroids = update_centroids(data, labels, k)
        if should_stop(old_centroids, centroids):
            break
    return labels

# 4. Run K-means clustering
# for 5 clusters
df["Cluster_5"] = kmeans(data, 5)
df["Cluster_5"] = df["Cluster_5"].astype(str)
cluster_counts = df["Cluster_5"].value_counts()
print(df.head())  # Print first few rows with clusters
print("Cluster counts:")
print(cluster_counts)
print("\n")
# for 8 clusters
df["Cluster_8"] = kmeans(data, 8)
df["Cluster_8"] = df["Cluster_8"].astype(str)
cluster_counts = df["Cluster_8"].value_counts()
print(df.head())  # Print first few rows with clusters
print("Cluster counts:")
print(cluster_counts)   
print("\n")

# 5. Save the results
runners = pd.concat([df, non_finishers], ignore_index=True)
runners.to_csv("byhand_clustered_output.csv", sep=";", index=False)

