# import the necessary libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import unicodedata
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import sqlite3
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# class to get the datas pre formatted for the application graphics + leaderboard showing
class Race_Datas:
    
    # initialize the class with the file path
    def __init__(self, file_path: str) :
        # connect to the database
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # check if the 'runners' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='runners';")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            # load data from the database
            query = "SELECT * FROM runners"
            self.runners = pd.read_sql(query, conn)
        else:
            csv_path_input = "Data/Databases/raw_race_data.csv"
            csv_path_intermediate = "Data/Databases/treated_runners_data.csv"
            csv_path_output = "Data/Databases/analyzed_race_datas.csv"
            # load data from the CSV and insert into the database
            if os.path.exists(csv_path_input):
                # read and process the CSV file
                self.read_and_process_csv(csv_path_input, csv_path_intermediate)
                # add the clusterization datas to the runners data
                self.clusterize_datas(csv_path_intermediate, csv_path_output)
                # read the processed CSV file
                self.runners = pd.read_csv(csv_path_output, sep=";", header=0, dtype=str)
                # create the runners table
                cursor.execute("""
                    CREATE TABLE runners (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        Finish TEXT,
                        Rank TEXT,
                        Category TEXT,
                        Category_Rank TEXT
                    )
                """)
                # insert the data into the database
                self.runners.to_sql("runners", conn, if_exists="replace", index=False)
            else:
                raise FileNotFoundError(f"CSV file '{csv_path_input}' not found.")
        conn.close()

        # create the categories datas and pictures
        self.create_categories_datas()
        self.create_pre_computed_pictures()

    # function to create the categories datas
    def create_categories_datas(self):
        self.male_runners = self.runners[self.runners["Sex"] == "Homme"]
        self.female_runners = self.runners[self.runners["Sex"] == "Femme"]
        self.juh_runners = self.runners[self.runners["Category"] == "JUH"]
        self.juf_runners = self.runners[self.runners["Category"] == "JUF"]
        self.esh_runners = self.runners[self.runners["Category"] == "ESH"]
        self.esf_runners = self.runners[self.runners["Category"] == "ESF"]
        self.seh_runners = self.runners[self.runners["Category"] == "SEH"]
        self.sef_runners = self.runners[self.runners["Category"] == "SEF"]
        self.mah_1_runners = self.runners[self.runners["Category"] == "MAH1"]
        self.maf_1_runners = self.runners[self.runners["Category"] == "MAF1"]
        self.mah_2_runners = self.runners[self.runners["Category"] == "MAH2"]
        self.maf_2_runners = self.runners[self.runners["Category"] == "MAF2"]
    
    # function to get a Gaussian curve from a list of data
    def get_gaussienne_graph(self, list_data, name_fig: str, title: str, title_description: str, is_by_name: bool, own_time: str):
        
        list_data = list_data.dropna().apply(self.time_to_seconds).dropna().astype(float)

        # convert own_time to seconds if provided
        own_time = self.time_to_seconds(own_time)

        # create the Gaussian curve
        density = gaussian_kde(list_data)
        x = np.linspace(min(list_data), max(list_data), 1000)
        y = density(x)

        # create the graph
        plt.clf()
        plt.figure(figsize=(12, 5))
        plt.scatter(list_data, density(list_data), color="red", zorder = 2, marker="+", s=50)
        plt.plot(x, y, color="blue")

        if title_description != "": # we're in a general graph so we must precise the title catergory description
            # Using multiple lines with different font sizes to have the title and the title description on the same line
            if is_by_name:
                plt.text(0.55, 1.05, f"{title} -", fontsize=25, ha='right', transform=plt.gca().transAxes)
                plt.text(0.56, 1.055, title_description, fontsize=15, ha='left', transform=plt.gca().transAxes)
            else :
                plt.text(0.5, 1.05, f"{title} -", fontsize=25, ha='right', transform=plt.gca().transAxes)
                plt.text(0.51, 1.055, title_description, fontsize=15, ha='left', transform=plt.gca().transAxes)
        else : 
            plt.title(title, fontsize=20)

        # modify x-axis to show time in hh:mm format
        def format_time(value, _):
            hours = int(value // 3600)
            minutes = int((value % 3600) // 60)
            return f"{hours:02d}h{minutes:02d}"

        # set the x-axis to show time in hh:mm format
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
        plt.gca().invert_xaxis()
        plt.gca().xaxis.set_tick_params(labelsize=15)        
        plt.gca().yaxis.set_visible(False)

         # if is_by_name is True, draw the red arrow to show where the result is 
        if is_by_name and own_time != 0:
            # get the corresponding y-value for the team's time on the curve and then creating the arrow pointing toward the value
            y_own_time = density(own_time)
            plt.gca().annotate('', xy=(own_time, y_own_time), xytext=(own_time, -0.05), arrowprops=dict(facecolor='red', edgecolor='red', lw=2, linestyle='-'))

        plt.savefig(name_fig, dpi=500)

    # function to create the categories datas and the precomputed pictures for the graphics of those categories
    def create_pre_computed_pictures(self):
        if not os.path.exists("Data/Precomputed_graphs"):
            os.makedirs("Data/Precomputed_graphs")
        
        if not os.path.exists("Data/Precomputed_graphs/overall.png"):
            self.get_gaussienne_graph(self.runners["Finish"], "Data/Precomputed_graphs/overall.png", "OVERALL Results", "all runners", False, "")
            self.get_gaussienne_graph(self.male_runners["Finish"], "Data/Precomputed_graphs/men.png", "MEN Results", "all mens", False, "")
            self.get_gaussienne_graph(self.female_runners["Finish"], "Data/Precomputed_graphs/women.png", "WOMEN Results", "all womens", False, "")
            self.get_gaussienne_graph(self.juh_runners["Finish"], "Data/Precomputed_graphs/juh.png", "JUH Results", "mens born between 2006 and 2007", False, "")
            self.get_gaussienne_graph(self.juf_runners["Finish"], "Data/Precomputed_graphs/juf.png", "JUF Results", "womens born between 2006 and 2007", False, "")
            self.get_gaussienne_graph(self.esh_runners["Finish"], "Data/Precomputed_graphs/esh.png", "ESH Results", "mens born between 2003 and 2005", False, "")
            self.get_gaussienne_graph(self.esf_runners["Finish"], "Data/Precomputed_graphs/esf.png", "ESF Results", "womens born between 2003 and 2005", False, "")
            self.get_gaussienne_graph(self.seh_runners["Finish"], "Data/Precomputed_graphs/seh.png", "SEH Results", "mens born between 1991 and 2002", False, "")
            self.get_gaussienne_graph(self.sef_runners["Finish"], "Data/Precomputed_graphs/sef.png", "SEF Results", "womens born between 1991 and 2002", False, "")
            self.get_gaussienne_graph(self.mah_1_runners["Finish"], "Data/Precomputed_graphs/mah_1.png", "MAH 1 Results", "mens born between 1966 and 1990", False, "")
            self.get_gaussienne_graph(self.mah_2_runners["Finish"], "Data/Precomputed_graphs/mah_2.png", "MAH 2 Results", "mens born before 1965", False, "")
            self.get_gaussienne_graph(self.maf_1_runners["Finish"], "Data/Precomputed_graphs/maf_1.png", "MAF 1 Results", "womens born between 1966 and 1990", False, "")
            self.get_gaussienne_graph(self.maf_2_runners["Finish"], "Data/Precomputed_graphs/maf_2.png", "MAF 2 Results", "womens born before 1965", False, "")
 
    # function to get specific datas depending on the app queries (looking by name and getting its results by category results, then looking by category if the name is "", don't return anything is name is != "" and no results are found)
    # the function return the number of results found : 
    # 0 if no results are found
    # 1, category_datas
    # 2, name_datas (non finished runner)
    # 3, name_datas, overall_datas, category_datas (finished runner by found name)
    def get_specific_datas(self, name:str, category:str):
        if name == "": # we're looking for a category datas
            if category == "MEN":
                return 1, self.male_runners
            elif category == "WOMEN":
                return 1, self.female_runners
            elif category == "JUH":
                return 1, self.juh_runners
            elif category == "JUF":
                return 1, self.juf_runners
            elif category == "ESH":
                return 1, self.esh_runners
            elif category == "ESF":
                return 1, self.esf_runners
            elif category == "SEH":
                return 1, self.seh_runners
            elif category == "SEF":
                return 1, self.sef_runners
            elif category == "MAH1":
                return 1, self.mah_1_runners
            elif category == "MAH2":
                return 1, self.mah_2_runners
            elif category == "MAF1":
                return 1, self.maf_1_runners
            elif category == "MAF2":
                return 1, self.maf_2_runners
            else:
                return 1, self.runners
        else: # we're looking for a specific name and we must get its result by category results
            # split the input name into parts (e.g., "cuel tom" -> ["cuel", "tom"])
            name_parts = name.lower().split()
            # check if all parts are contained in the name, regardless of order
            def remove_accents(text):
                return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
            name_runner = self.runners[self.runners["Name"].apply(lambda x: 
                all(part in remove_accents(x.lower()) for part in map(remove_accents, name_parts)))]

            if len(name_runner) == 1: # we found an unique runner
                valid_finish_time_mask = ~self.runners['Finish'].isin(["Disqualifié", "None", "Abandon"]) & pd.notna(self.runners['Finish'])
                if not valid_finish_time_mask.loc[name_runner.index[0]]:  # The runner did not finish
                    return 2, name_runner
                
                else: # a finished runner
                    # left figure is the placement of the runner in the overall results
                    self.get_gaussienne_graph(self.runners["Finish"], "Data/left_figure.png", f"{name_runner["Name"].values[0]} - {name_runner["Rank"].values[0]} / {len(self.runners)} overall", "", True, name_runner["Finish"].values[0])
                    # right figure is the placement of the runner in the category results
                    runner_category = name_runner["Category"].values[0]
                    if runner_category == "JUH" :
                        self.get_gaussienne_graph(self.juh_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.juh_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.juh_runners
                    elif runner_category == "JUF" :
                        self.get_gaussienne_graph(self.juf_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.juf_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.juf_runners
                    elif runner_category == "ESH" :
                        self.get_gaussienne_graph(self.esh_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.esh_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.esh_runners
                    elif runner_category == "ESF" :
                        self.get_gaussienne_graph(self.esf_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.esf_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.esf_runners
                    elif runner_category == "SEH" :
                        self.get_gaussienne_graph(self.seh_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.seh_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.seh_runners
                    elif runner_category == "SEF" :
                        self.get_gaussienne_graph(self.sef_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.sef_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.sef_runners
                    elif runner_category == "MAH1" :
                        self.get_gaussienne_graph(self.mah_1_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.mah_1_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.mah_1_runners
                    elif runner_category == "MAH2" :
                        self.get_gaussienne_graph(self.mah_2_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.mah_2_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.mah_2_runners
                    elif runner_category == "MAF1" :
                        self.get_gaussienne_graph(self.maf_1_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.maf_1_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.maf_1_runners
                    elif runner_category == "MAF2" :
                        self.get_gaussienne_graph(self.maf_2_runners["Finish"], "Data/right_figure.png", f"{name_runner["Cluster_10_Label"].values[0]} - {name_runner["Category_Rank"].values[0]} / {len(self.maf_2_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.maf_2_runners
                
            else: # otherwise, we didn't find any or we found multiple runners, we return none, it will dealt by the graphical interface
                return 0

    # convert list_data from HH:MM:SS to total seconds
    def time_to_seconds(self, time_str):
        """Convert time from HH:MM:SS or MM:SS format to total seconds"""
        if pd.isna(time_str) or time_str == "":
            return None  # keep missing values as None
        
        parts = time_str.split(":")
        
        if len(parts) == 3:  # HH:MM:SS format
            h, m, s = map(int, parts)
        elif len(parts) == 2:  # MM:SS format (assume 0 hours)
            h, m, s = 0, int(parts[0]), int(parts[1])
        else:
            return None  # invalid format : DSQ, DNF, DNS, etc.

        return h * 3600 + m * 60 + s
          
    # function to get the average pace for the half marathon given the finish time
    def get_average_pace_str(self, finish_time, distance_km = 21.097):
        if pd.isna(finish_time) or finish_time == "" or finish_time == "Disqualifié" or finish_time == "None" or finish_time == "Abandon" or finish_time == None:
            return "None"
        
        # parse the finish time (e.g., "01:05:56")
        total_seconds = self.time_to_seconds(finish_time)
        
        # convert total time into minutes
        total_minutes = total_seconds / 60
        
        # calculate the pace (minutes per km) --> distance of the half marathon in kilometers (21.097 km)
        pace_minutes_per_km = total_minutes / distance_km
        
        # extract minutes and seconds from the pace
        pace_minutes = int(pace_minutes_per_km)
        pace_seconds = int((pace_minutes_per_km - pace_minutes) * 60)
        
        # format the pace as "X'XX"/km
        pace = f"{pace_minutes}'{pace_seconds:02d}\"/km"
        
        return pace

    # get the average pace in seconds per km
    def get_average_pace(self, time, distance = 21.097):
        if pd.isna(time) or time == "" or time == "Disqualifié" or time == "None" or time == "Abandon" or time == None: 
            return None
        
        time_sec = self.time_to_seconds(time)
        if time_sec is None:
            return None
        return time_sec / distance

    # function to read and process the CSV file by adding additional datas
    def read_and_process_csv(self, csv_path_input: str, csv_path_output : str):
        # read the CSV file
        runners = pd.read_csv(csv_path_input, sep=";", header=0, dtype=str)

        # add the average pace column
        runners["Avg_Pace"] = runners["Finish"].apply(self.get_average_pace)

        distance_intervals = [5, 5, 5, 6.097]  # km intervals
        pace_columns = ["0_5_pace", "5_10_pace", "10_15_pace", "15_end_pace"]
        for col in pace_columns:
            if col not in runners.columns:
                runners[col] = [np.nan] * len(runners)  # initialize with None or appropriate default
        # calculate the pace for each interval
        for runner_index in range(len(runners)):
            time5 = self.time_to_seconds(runners.loc[runner_index, "5km"])
            time10 = self.time_to_seconds(runners.loc[runner_index, "10km"])
            time15 = self.time_to_seconds(runners.loc[runner_index, "15km"])
            timeFinish = self.time_to_seconds(runners.loc[runner_index, "Finish"])

            # modify the times that are NaN to be a number
            if time5 == None:
                if time10 != None:
                    time5 = time10 / 2
                elif time15 != None:
                    time5 = time15 / 3
                    time10 = time5 * 2
                elif timeFinish != None:
                    time5 = 5*(timeFinish) / (distance_intervals[0]+distance_intervals[1]+distance_intervals[2]+distance_intervals[3])
                    time10 = time5 * 2
                    time15 = time5 * 3
            
            if time10 == None:
                if time5 != None and time15 != None:
                    time10 = time5 + (time15 - time5) / 2
                elif time5 != None and timeFinish != None:
                    time10 = time5 + 5*(timeFinish - time5) / (distance_intervals[1]+distance_intervals[2]+distance_intervals[3])
                    time15 = time5 + 10*(timeFinish - time5) / (distance_intervals[1]+distance_intervals[2]+distance_intervals[3])
                elif time15 != None:
                    time10 = (time15*2) / 3
                elif timeFinish != None:
                    time10 = (timeFinish*10) / (distance_intervals[0]+distance_intervals[1]+distance_intervals[2]+distance_intervals[3])

            if time15 == None:
                if time10 != None and timeFinish != None:
                    time15 = time10 + 5*(timeFinish - time10) / (distance_intervals[2]+distance_intervals[3])
                elif time5 != None and timeFinish != None:
                    time15 = time5 + 10*(timeFinish - time5) / (distance_intervals[1]+distance_intervals[2]+distance_intervals[3])

            runners.loc[runner_index, "0_5_pace"] = (time5) / distance_intervals[0] if pd.notna(time5) else np.nan
            runners.loc[runner_index, "5_10_pace"] = (time10 - time5) / distance_intervals[1] if pd.notna(time10) and pd.notna(time5) else np.nan
            runners.loc[runner_index, "10_15_pace"] = (time15 - time10) / distance_intervals[2] if pd.notna(time15) and pd.notna(time10) else np.nan
            runners.loc[runner_index, "15_end_pace"] = (timeFinish - time15) / distance_intervals[3] if pd.notna(timeFinish) and pd.notna(time15) else np.nan

        # adding the pace differences between each 5km interval
        runners["0_5_10_diff"] = runners["5_10_pace"] - runners["0_5_pace"]
        runners["5_10_15_diff"] = runners["10_15_pace"] - runners["5_10_pace"]
        runners["10_15_end_diff"] = runners["15_end_pace"] - runners["10_15_pace"]
        runners["start_end_diff"] = runners["15_end_pace"] - runners["0_5_pace"]
        runners["0_5_average_diff"] = runners["0_5_pace"] - runners["Avg_Pace"]
        runners["5_10_average_diff"] = runners["5_10_pace"] - runners["Avg_Pace"]
        runners["10_15_average_diff"] = runners["10_15_pace"] - runners["Avg_Pace"]
        runners["15_end_average_diff"] = runners["15_end_pace"] - runners["Avg_Pace"]
        runners["10k_diff"] = (runners["15_end_pace"] + runners["10_15_pace"])/2 - (runners["0_5_pace"] + runners["5_10_pace"])/2

        # adding the merged categories and changing the category ranks accordingly
        category_groups = {
            "MAH1": ["M0H", "M1H", "M2H", "M3H", "M4H"],
            "MAF1": ["M0F", "M1F", "M2F", "M3F", "M4F"],
            "MAH2": ["M5H", "M6H", "M7H", "M8H", "M9H", "M10H"],
            "MAF2": ["M5F", "M6F", "M7F", "M8F", "M9F", "M10F"]
        }

        # assign the merged category based on the mapping
        def get_merged_category(category):
            for merged_cat, original_cats in category_groups.items():
                if category in original_cats:
                    return merged_cat
            return category  # keep unchanged if not in the mapping
        
        # merge the columns that needs to be merged
        runners["Category"] = runners["Category"].apply(get_merged_category)

        # now we will rerank the runners in the merged categories but only those that have finished
        valid_finish_time_mask = ~runners['Finish'].isin(["Disqualifié", "None", "Abandon"]) & pd.notna(runners['Finish'])
        
        finishers = runners[valid_finish_time_mask].copy()
        non_finishers = runners[~valid_finish_time_mask].copy()

        mah1_index = 1
        mah2_index = 1
        maf1_index = 1
        maf2_index = 1
        for runner_index in range(len(finishers)):
            if finishers.loc[runner_index, "Category"] == "MAH1":
                finishers.loc[runner_index, "Category_Rank"] = str(mah1_index)
                mah1_index += 1
            elif finishers.loc[runner_index, "Category"] == "MAF1":
                finishers.loc[runner_index, "Category_Rank"] = str(maf1_index)
                maf1_index += 1
            elif finishers.loc[runner_index, "Category"] == "MAH2":
                finishers.loc[runner_index, "Category_Rank"] = str(mah2_index)
                mah2_index += 1
            elif finishers.loc[runner_index, "Category"] == "MAF2":
                finishers.loc[runner_index, "Category_Rank"] = str(maf2_index)
                maf2_index += 1
        
        # saving the runners data in a csv file
        runners = pd.concat([finishers, non_finishers], ignore_index=True)        
        runners.to_csv(csv_path_output, sep=";", index=False)

    # function to add clusterization datas to the runners data
    def clusterize_datas(self, csv_path_input: str, csv_path_output : str):
        # 1. Load the runners data
        runners = pd.read_csv(csv_path_input, sep=";", header=0, dtype=str)
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
            plt.savefig(f"Data/Precomputed_graphs/Kmeans_{nb_clusters}_clusters.png")

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
                    1: "Steady (+hills slowdown)", # small drop in pace in climbs (around the 10k mark)
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

        # applying this to the wanted categories
        apply_kmeans(X, 5)
        apply_kmeans(X, 8)
        apply_kmeans(X, 10)

        # 5. Save results 
        runners = pd.concat([df, non_finishers], ignore_index=True) 
        runners.to_csv(csv_path_output, sep=";", index=False)

