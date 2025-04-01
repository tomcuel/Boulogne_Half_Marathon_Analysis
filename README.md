# Boulogne Half Marathon Analysis App in Python
> I’ve done an App in Python to show the different results linked to a Half Marathon I did back in November 2024 and from which I downloaded the results. This app is an upgraded version _(but also a different one)_ of the Ekiden App I previously did. The goal wasn't that much to just get used to Tkinter and the Python classes, but to add a runner race analyse, while still improving the functionnalities and the graphics for a better usage _(login, sign-up, buttons, search bar, …)_. Now everything rely on a SQL database, both datas that can still be loaded with the initial csv file but also client informations with crypted password _(no app security but an additional features)_. Datas are now handled through the pandas and numpy libraries, making it faster while handling 100x more datas. It allows me to pre-process the datas to then implement some machine learning tools. I need to start using these techniques with Python tools, as they will be useful later. I used the K-Means clustering algorithm in this project to categorize each runner's performance.


#### Tables of contents
* [Path tree](#path-tree)
* [Direct links to folders](#direct-links-to-folders) 
* [Runners categorization](#runners-categorization)
* [Virtual Environnment and Librairies](#virtual-environnment-and-librairies)  
* [App preview](#app-preview)


## Path tree
```
Boulogne_Half_Marathon_Analysis/
├── Data/
│   ├── Databases/              
│   ├── Pictures/    
│   ├── Precomputed_graphs/    
│   └── Treatment file and temporary datas 
│
├── K_means_implementation/
│   └── Treatment files, datas and results
│
└── main functions             
```


## Direct links to folders 
* [Data](./Data/) : contains the files related to the treatment of the results 
    * [Databases](./Data/Databases/) : contains all the csv and SQL files used during the datas treatment and the app use
    * [Pictures](./Data/Pictures/) : contains some useful picture to show in the app and the README
    * [Precomputed_graphs](./Data/Precomputed_graphs/) : contains the precomputed generic picture for overall rankings as well as K-means results
* [Test K_means_implementation](./K_means_implementation/) : contains the files to try the Kmeans clustering method


## Virtual Environnment and Librairies
Since the libraries are not installed on my Mac, I need to set up a virtual environment to access and use the required libraries, here is how to do :

Creating the virtual environnment
```
python3 -m venv path/to/venv
```
Activating the virtual environnment
```
source path/to/venv/bin/activate
```
Downloading the librairies you need in the virtual environnment
```
python3 -m pip install what_you_need
```
To temporarly deactivate the virtual environnment
```
deactivate 
```
To suppress it
```
rm -rf path/to/venv
```

I used those librairies for this project : 
```py
import os # searching paths
import matplotlib.pyplot as plt # to plot things
import matplotlib.ticker as ticker # plots customization
import tkinter as tk # tkinter 
from tkinter import ttk # for more modern and and customizable widgets 
from tkinter import messagebox # for errors messages
from tkinter import PhotoImage # for pictures 
from PIL import Image, ImageTk # a better rezising
import re # regular expression
import bcrypt # password crypting 
import sqlite3 # SQL database 
import numpy as np # numpy arrays
import pandas as pd # dataframe use
from scipy.stats import gaussian_kde # gaussian modelisation
from sklearn.cluster import KMeans # for clustering purpose
from sklearn.preprocessing import StandardScaler # prepare the datas
```


## Runners categorization


## App preview 
#### How to use it
Every button is clickable and will redirect you to the corresponding part of the App, you can use it like any app. For the login and the sign-up screens, the cursor is directly on the first entry, so we can type as soon as we wanted, and the tabulation and enter key does work here to move to the next entry to continue
Here is a preview of some screens you will encounter when lauching the app : 

#### Login screen render
<img src="./Data/Pictures/login_screen_render.png" alt="login_screen_render" width="350" height="225"/>

#### Sign-up screen render
<img src="./Data/Pictures/signup_screen_render.png" alt="signup_screen_render" width="350" height="225"/>

#### Home screen render
<img src="./Data/Pictures/home_app_screen_render.png" alt="home_app_screen_render" width="350" height="225"/>

#### Own results screen render
<img src="./Data/Pictures/own_results_screen_render.png" alt="own_results_screen_render" width="350" height="225"/>
