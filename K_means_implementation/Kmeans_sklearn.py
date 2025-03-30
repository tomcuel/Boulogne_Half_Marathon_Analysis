import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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
X = df[learning_columns]
# normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Apply K-Means clustering for n clusters
def apply_kmeans(X, nb_clusters):
    """Apply KMeans clustering to the data and return the cluster labels."""
    kmeans = KMeans(n_clusters=nb_clusters, init="k-means++", n_init=10, random_state=42)
    df.loc[X.index, f"Cluster_{nb_clusters}"] = kmeans.fit_predict(X_scaled)

    # associating each cluster with a label thanks to data visualization and my own knowledge and analysis
    # plot clustering results
    fig, axes = plt.subplots(3, 2, figsize=(12, 12)) 
    fig.suptitle(f"KMeans Clustering with {nb_clusters} Clusters", fontsize=16)

    # first plot: Difference between first5km and last5km pace
    scatter1 = axes[0, 0].scatter(X_scaled[:, 0], X_scaled[:, 3], c=df[f"Cluster_{nb_clusters}"].astype(int), cmap="viridis")
    axes[0, 0].set_xlabel(learning_columns[0])
    axes[0, 0].set_ylabel(learning_columns[3])
    axes[0, 0].set_title("First5km vs Last5km")

    # second plot: difference between the first10km-->last11km and the first5km-->last5km pace
    scatter2 = axes[0, 1].scatter(X_scaled[:, 7], X_scaled[:, 8], c=df[f"Cluster_{nb_clusters}"].astype(int), cmap="viridis")
    axes[0, 1].set_xlabel(learning_columns[7])
    axes[0, 1].set_ylabel(learning_columns[8])
    axes[0, 1].set_title("First5km-->Last5km vs First10km-->Last11km")

    # 1D projection plots with separate lines for each cluster
    for i, col_idx in enumerate([0, 1, 2, 3]):
        row = 1 + i // 2
        col = i % 2
        # assign unique y-values to each cluster
        cluster_labels = df[f"Cluster_{nb_clusters}"].astype(int)
        y_values = cluster_labels  # each cluster gets a different line
        scatter = axes[row, col].scatter(X_scaled[:, col_idx], y_values, c=cluster_labels, cmap="viridis")
        axes[row, col].set_xlabel(learning_columns[col_idx])
        axes[row, col].set_ylabel("Cluster Label (Separated)")
        axes[row, col].set_title(f"{learning_columns[col_idx]} vs Cluster")

    # create a separate axis for the colorbar on the far right
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(scatter2, cax=cbar_ax)
    cbar.set_label("Cluster Label")

    # adjust layout
    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  #lLeave space for suptitle and adjust for the colorbar
    plt.savefig(f"Kmeans_{nb_clusters}_clusters.png")

    if nb_clusters == 5:
        cluster_5_labels = {
            0: "Positive split", # slows down at each interval by a small amount
            3: "Strong starter", # starts really fast compared to the average
            1: "Negative split", # accelerates at each interval by a small amount
            4: "Fast finisher", # ends really fast compared to the average
            2: "Steady pace", # stays almost at the same pace at each interval
        }
        df["Cluster_5_Label"] = df["Cluster_5"].map(cluster_5_labels)

        # get the number of runners in each cluster
        cluster_counts = df["Cluster_5_Label"].value_counts()
        print("5 Clusters counts:")
        print(cluster_counts)
        print("\n")

    elif nb_clusters == 8: 
        cluster_8_labels = {
            3: "Steady Pace", # stays almost at the same pace at each interval
            0 : "Steady + hills struggles",  # small drop in pace in the climbs (around the 10k mark)
            2: "Mid-race slowdown", # first 10k fast compared to the last 11.097 km
            
            1: "Weak finisher", # ends really slow compared to the average and the first 15 km
            4: "Strong starter", # starts really fast compared to the average and the last 16 km
            7: "Positive split", # slows down at each interval by a small amount
            
            6: "Weak starter", # starts really slow compared to the average and the last 16 km
            5: "Negative split" # accelerates at each interval by a small amount
        }
        df["Cluster_8_Label"] = df["Cluster_8"].map(cluster_8_labels)
        # get the number of runners in each cluster
        cluster_counts = df[f"Cluster_8_Label"].value_counts()
        print(f"{nb_clusters} Clusters counts:")
        print(cluster_counts)
        print("\n")

    elif nb_clusters == 10: 
        cluster_10_labels = {
            4: "Steady pace", # stays almost at the same pace at each interval
            1: "Steady + hills struggles", # small drop in pace in climbs (around the 10k mark)
            5: "cautious start, get times back 5-10k then consistent", # cautious start, picks up speed, then steady
            6: "Mid-race slowdown", # first 10k fast compared to the last 11.097 km
    
            8: "Weak finisher", # ends really slow compared to the average and the first 15 km
            3: "Struggle at end", # ends slow compared to the average and the first 15 km
            2: "Strong starter", # starts really fast compared to the average and the last 16 km
            0: "Positive Split", # slows down at each interval by a small amount
            
            9: "Weak starter", # starts really slow compared to the average and the last 16 km
            7: "Negative split" # accelerates at each interval by a small amount
        }
        df["Cluster_10_Label"] = df["Cluster_10"].map(cluster_10_labels)
        # get the number of runners in each cluster
        cluster_counts = df[f"Cluster_10_Label"].value_counts()
        print(f"{nb_clusters} Clusters counts:")
        print(cluster_counts)
        print("\n")


# 4. Run K-means clustering for different numbers of clusters
apply_kmeans(X, 5)
apply_kmeans(X, 8)
apply_kmeans(X, 10)


# 5. Save the results
runners = pd.concat([df, non_finishers], ignore_index=True)
runners.to_csv("sklearn_clustered_output.csv", sep=";", index=False)

