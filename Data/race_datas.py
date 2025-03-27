# import the necessary libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import sqlite3
import os


# class to get the datas pre formatted for the application graphics + leaderboard showing
class Race_Datas:
    
    # initialize the class with the file path
    def __init__(self, file_path: str) :
        csv_path = "Data/raw_race_data.csv"
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
            # load data from the CSV and insert into the database
            if os.path.exists(csv_path):
                self.runners = pd.read_csv(csv_path, sep=";", header=0, dtype=str)
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
                raise FileNotFoundError(f"CSV file '{csv_path}' not found.")
        conn.close()

        # create the categories datas and pictures
        self.create_categories_datas()
        #self.create_pre_computed_pictures()

    # function to create the categories datas
    def create_categories_datas(self):
        self.male_runners = self.runners[self.runners.apply(lambda x: x["Category"] in ["JUH", "ESH", "SEH", "M0H", "M1H", "M2H", "M3H", "M4H", "M5H", "M6H", "M7H", "M8H", "M9H", "M10H"], axis=1)]
        self.female_runners = self.runners[self.runners.apply(lambda x: x["Category"] in ["JUF", "ESF", "SEF", "M0F", "M1F", "M2F", "M3F", "M4F", "M5F", "M6F", "M7F", "M8F", "M9F", "M10F"], axis=1)]
        self.juh_runners = self.runners[self.runners["Category"] == "JUH"]
        self.juf_runners = self.runners[self.runners["Category"] == "JUF"]
        self.esh_runners = self.runners[self.runners["Category"] == "ESH"]
        self.esf_runners = self.runners[self.runners["Category"] == "ESF"]
        self.seh_runners = self.runners[self.runners["Category"] == "SEH"]
        self.sef_runners = self.runners[self.runners["Category"] == "SEF"]
        self.mah_1_runners = self.runners[self.runners.apply(lambda x: x["Category"] in ["M0H", "M1H", "M2H", "M3H", "M4H"], axis=1)]
        self.mah_2_runners = self.runners[self.runners.apply(lambda x: x["Category"] in ["M5H", "M6H", "M7H", "M8H", "M9H", "M10H"], axis=1)]
        self.maf_1_runners = self.runners[self.runners.apply(lambda x: x["Category"] in ["M0F", "M1F", "M2F", "M3F", "M4F"], axis=1)]
        self.maf_2_runners = self.runners[self.runners.apply(lambda x: x["Category"] in ["M5F", "M6F", "M7F", "M8F", "M9F", "M10F"], axis=1)]
    
    # function to get a Gaussian curve from a list of data
    def get_gaussienne_graph(self, list_data, name_fig: str, title: str, title_description: str, is_by_name: bool, own_time: str):
        
        # Convert list_data from HH:MM:SS to total seconds
        def time_to_seconds(time_str):
            """Convert time from HH:MM:SS or MM:SS format to total seconds"""
            if pd.isna(time_str) or time_str == "":
                return None  # Keep missing values as None
            
            parts = time_str.split(":")
            
            if len(parts) == 3:  # HH:MM:SS format
                h, m, s = map(int, parts)
            elif len(parts) == 2:  # MM:SS format (assume 0 hours)
                h, m, s = 0, int(parts[0]), int(parts[1])
            else:
                return None  # Invalid format : DSQ, DNF, DNS, etc.

            return h * 3600 + m * 60 + s
        
        list_data = list_data.dropna().apply(time_to_seconds).dropna().astype(float)

        # Convert own_time to seconds if provided
        own_time = time_to_seconds(own_time)

        # Create the Gaussian curve
        density = gaussian_kde(list_data)
        x = np.linspace(min(list_data), max(list_data), 1000)
        y = density(x)

        # Create the graph
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

        # Modify x-axis to show time in hh:mm format
        def format_time(value, _):
            hours = int(value // 3600)
            minutes = int((value % 3600) // 60)
            return f"{hours:02d}h{minutes:02d}"

        # Set the x-axis to show time in hh:mm format
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
        plt.gca().invert_xaxis()
        plt.gca().xaxis.set_tick_params(labelsize=15)        
        plt.gca().yaxis.set_visible(False)

         # If is_by_name is True, draw the red arrow to show where the result is 
        if is_by_name and own_time != 0:
            # Get the corresponding y-value for the team's time on the curve and then creating the arrow pointing toward the value
            y_own_time = density(own_time)
            plt.gca().annotate('', xy=(own_time, y_own_time), xytext=(own_time, -0.05), arrowprops=dict(facecolor='red', edgecolor='red', lw=2, linestyle='-'))

        plt.savefig(name_fig, dpi=500)

    # function to create the categories datas and the precomputed pictures for the graphics of those categories
    def create_pre_computed_pictures(self):
        if not os.path.exists("Data/Precomputed_graphs"):
            os.makedirs("Data/Precomputed_graphs")
        
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
            name_runner = self.runners[self.runners["Name"].str.lower().apply(lambda x: all(part in x.lower() for part in name_parts))]
            if len(name_runner) == 1: # we found an unique runner
                # this person must have a rank in the overall results, otherwise we can't display the results, it just means that the person didn't finish the race
                no_rank_overall = name_runner['Rank'].str.contains(' -  ', na=False)
                no_rank_category = self.runners['Category_Rank'].isna() | (self.runners['Category_Rank'] == "")
                if no_rank_overall.any() or no_rank_category.any() : # a non finished runner
                    return 2, name_runner
                
                else: # a finished runner
                    # left figure is the placement of the runner in the overall results
                    self.get_gaussienne_graph(self.runners["Finish"], "left_figure.png", f"{name_runner["Name"].values[0]} - {name_runner["Rank"].values[0]} / {len(self.runners)} overall", "", True, name_runner["Finish"].values[0])
                    # right figure is the placement of the runner in the category results
                    runner_category = name_runner["Category"].values[0]
                    if runner_category == "JUH" :
                        self.get_gaussienne_graph(self.juh_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.juh_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.juh_runners
                    elif runner_category == "JUF" :
                        self.get_gaussienne_graph(self.juf_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.juf_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.juf_runners
                    elif runner_category == "ESH" :
                        self.get_gaussienne_graph(self.esh_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.esh_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.esh_runners
                    elif runner_category == "ESF" :
                        self.get_gaussienne_graph(self.esf_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.esf_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.esf_runners
                    elif runner_category == "SEH" :
                        self.get_gaussienne_graph(self.seh_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.seh_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.seh_runners
                    elif runner_category == "SEF" :
                        self.get_gaussienne_graph(self.sef_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.sef_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.sef_runners
                    elif runner_category in ["M0H", "M1H", "M2H", "M3H", "M4H"]:
                        self.get_gaussienne_graph(self.mah_1_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.mah_1_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.mah_1_runners
                    elif runner_category in ["M5H", "M6H", "M7H", "M8H", "M9H", "M10H"]:
                        self.get_gaussienne_graph(self.mah_2_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.mah_2_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.mah_2_runners
                    elif runner_category in ["M0F", "M1F", "M2F", "M3F", "M4F"]:
                        self.get_gaussienne_graph(self.maf_1_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.maf_1_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.maf_1_runners
                    elif runner_category in ["M5F", "M6F", "M7F", "M8F", "M9F", "M10F"]:
                        self.get_gaussienne_graph(self.maf_2_runners["Finish"], "right_figure.png", f"still to categorize - {name_runner["Category_Rank"].values[0]} / {len(self.maf_2_runners)} by category", "", True, name_runner["Finish"].values[0])
                        return 3, name_runner, self.runners, self.maf_2_runners
                
            else: # otherwise, we didn't find any or we found multiple runners, we return none, it will dealt by the graphical interface
                return 0

