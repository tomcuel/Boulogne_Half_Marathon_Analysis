# import the necessary libraries
import tkinter as tk
import pandas as pd
import os
import sqlite3


# import the class created in other files
from utility import Utility
from Data import Race_Datas


# screen 3: class to show the main app screen where the results are displayed
class App_Screen(tk.Frame):

    # initialize the app screen
    def __init__(self, master, navigate_callback, window_width, data : Race_Datas):
        super().__init__(master, bg="#282c34", highlightthickness=0, borderwidth=0, border=0)
        self.navigate_callback = navigate_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # ensure this frame expands within its parent
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.window_width = window_width
        # store the datas
        self.datas = data

    # header Section
        header_frame = tk.Frame(self, bg="#FFDB58", height=100, width = self.window_width)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

    # home Icon Button
        self.logo = Utility.load_resized_image("Data/Pictures/App_Icon.png", 75, 75)
        logo_button = tk.Button(
            header_frame, image= self.logo, compound="left", border=0, highlightthickness=0
        )
        logo_button.place(x=50, y=header_frame.winfo_reqheight() // 2, anchor="center")  
        logo_button.bind("<Button-1>", self.reset_screen)

    # home label/button
        home_button = tk.Label(
            header_frame, text="Home", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        home_button.place(x=200, y=header_frame.winfo_reqheight() // 2, anchor="center") 
        home_button.bind("<Enter>", lambda event: home_button.config(font=("Helvetica", 50, "bold"), fg="#000000", bg="#FFDB58"))
        home_button.bind("<Leave>", lambda event: home_button.config(font=("Helvetica", 40), fg="#000000", bg="#FFDB58"))
        home_button.bind("<Button-1>", self.reset_screen)
        
    # results label/button
        results_button = tk.Label(
            header_frame, text="Results", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        results_button.place(x=450, y=header_frame.winfo_reqheight() // 2, anchor="center")
        results_button.bind("<Button-1>", self.show_results_menu)

    # result sub-menu buttons
        # utility functions
        def show_submenu(event=None):
            # display the submenu when hovering over the results button.
            submenu.place(x=results_button.winfo_x(), y=results_button.winfo_y() + results_button.winfo_height())
            submenu.lift()
            for sub_button in submenu_buttons:
                sub_button.update_idletasks() # ensure the text on buttons is refreshed immediately
            results_button.config(font=("Helvetica", 50, "bold")) # Result button bigger when submenu is showing
        def hide_submenu(event=None):
            # hide the submenu if the mouse is not over the submenu or results button.
            widget_under_pointer = master.winfo_containing(event.x_root, event.y_root)
            if widget_under_pointer not in submenu.winfo_children() and widget_under_pointer != submenu and widget_under_pointer != results_button:
                submenu.place_forget()
            results_button.config(font=("Helvetica", 40)) # result button smaller when submenu isn't showing

        # submenu frame with fixed size
        submenu = tk.Frame(master, bg="#FFDB58", relief="raised", border=0, highlightthickness=0, width=350, height=100)
        submenu.place_forget()

        # add submenu buttons with place
        overall_result_sub_button = tk.Label(
                submenu, text="Overall Results",  font=("Helvetica", 30),  bg="#FFDB58", fg="#000000", padx=10, pady=5, anchor="center"
        )
        overall_result_sub_button.place(x=0, y=0, relwidth=1, height=50)
        overall_result_sub_button.bind("<Enter>", lambda event, b=overall_result_sub_button: self.on_submenu_button_hover(event, b, True))
        overall_result_sub_button.bind("<Leave>", lambda event, b=overall_result_sub_button: self.on_submenu_button_hover(event, b, False))
        overall_result_sub_button.bind("<Button-1>", self.show_overall_results_sub_menu)
        category_result_sub_button = tk.Label(
                submenu, text="Category Results", font=("Helvetica", 30), bg="#FFDB58", fg="#000000", padx=10, pady=5, anchor="center"
        )
        category_result_sub_button.place(x=0, y=50, relwidth=1, height=50)
        category_result_sub_button.bind("<Enter>", lambda event, b=category_result_sub_button: self.on_submenu_button_hover(event, b, True))
        category_result_sub_button.bind("<Leave>", lambda event, b=category_result_sub_button: self.on_submenu_button_hover(event, b, False))
        category_result_sub_button.bind("<Button-1>", self.show_category_results_sub_menu)
        submenu_buttons = [overall_result_sub_button, category_result_sub_button]

    # bind events to the results and submenu buttons
        results_button.bind("<Enter>", show_submenu)
        results_button.bind("<Leave>", hide_submenu)
        submenu.bind("<Enter>", show_submenu)
        submenu.bind("<Leave>", hide_submenu)

    # own person results button
        own_person_results_button = tk.Label(
            header_frame, text="My Results", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        own_person_results_button.place(x=750, y=header_frame.winfo_reqheight() // 2, anchor="center")
        own_person_results_button.bind("<Enter>", lambda event: own_person_results_button.config(font=("Helvetica", 50, "bold"), fg="#000000", bg="#FFDB58"))
        own_person_results_button.bind("<Leave>", lambda event: own_person_results_button.config(font=("Helvetica", 40), fg="#000000", bg="#FFDB58"))
        own_person_results_button.bind("<Button-1>", lambda event: self.show_results(self.get_own_person_results(), ""))

    # search bar
        self.search_var = tk.StringVar()
        search_bar = tk.Entry(
            header_frame, textvariable=self.search_var, font=("Helvetica", 20), background="#f7f7f7", highlightbackground="#282c34"
        )
        search_bar.place(x=self.window_width // 2 + 400, y=header_frame.winfo_reqheight() // 2, anchor="center")
        search_bar.bind("<Return>", self.perform_search)

    # deconnexion button
        self.logout_image = Utility.load_resized_image("Data/Pictures/Log_Out.png", 40, 40)
        logout_button = tk.Button(
            header_frame, image=self.logout_image, border=0, highlightthickness=0, compound="center"
        )
        logout_button.place(x=self.window_width - 75, y=header_frame.winfo_reqheight() // 2, anchor="center")
        logout_button.bind("<Button-1>", self.deconnexion)

    # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.bind("<Enter>", lambda event: self.scroll_canvas.focus_set())  # Focus the canvas when mouse enters
        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # home page content
        # title text
        self.description_title_text = (
            "Welcome to the Boulogne Half Marathon App!"
        )
        self.description_title_label = tk.Label(
            self.scrollable_frame, text=self.description_title_text, font=("Helvetica", 30), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_title_label.pack(padx=(50,50), pady=(10,10))
        # description text
        self.description_text = (
            "The Boulogne Half Marathon is a long-distance running event covering a distance of 21.0975 kilometers.\n"
            "The app is designed give access to essential race information, rankings and performance analysis.\n"
            "You can click on one of the results buttons or search for a specific runner or team in the search bar to access the results, both overall and by category"
        )
        self.description_half_label = tk.Label(
            self.scrollable_frame, text=self.description_text,font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_half_label.pack(padx=(50,50), pady=(0,10))
        # two buttons to redirect to the overall and category results
    # frame for result link buttons
        self.button_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.button_frame.pack(pady=(0, 10),)
        # buttons for overall results in the home page
        home_page_overall_results_button = tk.Label(
            self.button_frame, text="View Overall Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_overall_results_button.pack(padx=(50, 50), pady=(0, 10), side = "left")
        home_page_overall_results_button.bind("<Enter>", lambda event, b=home_page_overall_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_overall_results_button.bind("<Leave>", lambda event, b=home_page_overall_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_overall_results_button.bind("<Button-1>", self.show_overall_results_sub_menu)
    # buttons for overall results in the home page
        home_page_category_results_button = tk.Label(
            self.button_frame, text="View Category Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_category_results_button.pack(padx=(50, 50), pady=(0, 10), side = "right") 
        home_page_category_results_button.bind("<Enter>", lambda event, b=home_page_category_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_category_results_button.bind("<Leave>", lambda event, b=home_page_category_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_category_results_button.bind("<Button-1>", self.show_category_results_sub_menu)
    # race map 
        map_width, map_height = 850, 500
        self.parcours = Utility.load_resized_image("Data/Pictures/semi_parcours.png", map_width, map_height)
        self.race_map_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.race_map_frame.pack(pady=(0, 10), fill="x", side="bottom", anchor="s")
        map_label = tk.Label(self.race_map_frame, image=self.parcours, bg="#282c34")
        map_label.pack()

    # function to show the results menu in the scrollable frame
    def show_results_menu(self, event=None):   
        # destroy the old scrollable frame (clear old widgets)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # destroy all the previous informations on screen
        if hasattr(self, "results_header_frame"):
            self.results_header_frame.destroy()
        self.scrollable_frame.destroy()
        self.scroll_canvas.destroy()
        self.scrollbar.destroy()

    # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.bind("<Enter>", lambda event: self.scroll_canvas.focus_set())  # Focus the canvas when mouse enters
        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # creating the 3 buttons for the overall results
        # create a frame for organizing the buttons in a grid
        overall_button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        overall_button_grid_frame.pack(pady=(10, 0), padx=(200, 200), fill="x")
        # Add grid column configurations to ensure buttons are centered
        overall_button_grid_frame.grid_columnconfigure(0, weight=1)
        overall_button_grid_frame.grid_columnconfigure(1, weight=1)
        overall_button_grid_frame.grid_columnconfigure(2, weight=1)
        overall_results_label = tk.Label(
            overall_button_grid_frame, text="Overall Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        overall_results_label.grid(row=0, column=0, columnspan=3, padx=(50, 50), pady=(0, 10), sticky="nsew")
        # overall scratch 
        overall_results_button = tk.Button(
            overall_button_grid_frame, text="Overall", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda: self.show_results("", "OVERALL")
        )
        overall_results_button.grid(row=1, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # men
        men_results_button = tk.Button(
            overall_button_grid_frame, text="Men", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda: self.show_results("", "MEN")
        )
        men_results_button.grid(row=1, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # women
        women_results_button = tk.Button(
            overall_button_grid_frame, text="Women", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "WOMEN")
        )
        women_results_button.grid(row=1, column=2, padx=(30, 30), pady=(10, 10), sticky="nsew")

    # creating the 10 buttons for the category results on 5 rows and 2 columns (male and female)
        # create a frame for organizing the buttons in a grid
        category_button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        category_button_grid_frame.pack(pady=(10, 0), padx=(200, 200), fill="x")
        # Add grid column configurations to ensure buttons are centered
        category_button_grid_frame.grid_columnconfigure(0, weight=1)
        category_button_grid_frame.grid_columnconfigure(1, weight=1)
        category_results_label = tk.Label(
            category_button_grid_frame, text="Category Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        category_results_label.grid(row=3, column=0, columnspan=2, padx=(50, 50), pady=(20, 10), sticky="nsew")
        # junior men    
        junior_men_results_button = tk.Button(
            category_button_grid_frame, text="Junior Men (born 2006-2007)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "JUH")
        )
        junior_men_results_button.grid(row=4, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # junior women 
        junior_women_results_button = tk.Button(
            category_button_grid_frame, text="Junior Women (born 2006-2007)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "JUF")
        )
        junior_women_results_button.grid(row=4, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # espoir men 
        espoir_men_results_button = tk.Button(
            category_button_grid_frame, text="Espoir Men (born 2003-2005)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "ESH")
        )
        espoir_men_results_button.grid(row=5, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # espoir women 
        espoir_women_results_button = tk.Button(
            category_button_grid_frame, text="Espoir Women (born 2003-2005)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "ESF")
        )
        espoir_women_results_button.grid(row=5, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # senior men 
        senior_men_results_button = tk.Button(
            category_button_grid_frame, text="Senior Men (born 1991-2002)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "SEH")
        )
        senior_men_results_button.grid(row=6, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # senior women 
        senior_women_results_button = tk.Button(
            category_button_grid_frame, text="Senior Women (born 1991-2002)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "SEF")
        )
        senior_women_results_button.grid(row=6, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAH1 men 
        mah1_men_results_button = tk.Button(
            category_button_grid_frame, text="Men (born 1966-1990)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAH1")
        )
        mah1_men_results_button.grid(row=7, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAF1 women 
        maf1_women_results_button = tk.Button(
            category_button_grid_frame, text="Women (born 1966-1990)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAF1")
        )
        maf1_women_results_button.grid(row=7, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAH2 men
        mah2_men_results_button = tk.Button(
            category_button_grid_frame, text="Men (born before 1965)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAH2")
        )
        mah2_men_results_button.grid(row=8, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAF2 women 
        maf2_women_results_button = tk.Button(
            category_button_grid_frame, text="Women (born before 1965)", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAF2")
        )
        maf2_women_results_button.grid(row=8, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")

        # putting back the scrollable frame to the top
        self.scroll_canvas.yview_moveto(0)
    
    # function to show the overall results submenu in the scrollable frame
    def show_overall_results_sub_menu(self, event=None):
        # destroy the old scrollable frame (clear old widgets)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # destroy all the previous informations on screen
        if hasattr(self, "results_header_frame"):
            self.results_header_frame.destroy()
        self.scrollable_frame.destroy()
        self.scroll_canvas.destroy()
        self.scrollbar.destroy()

        # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.bind("<Enter>", lambda event: self.scroll_canvas.focus_set())  # Focus the canvas when mouse enters
        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # creating the 3 buttons for the overall results
        # create a frame for organizing the buttons in a grid
        overall_button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        overall_button_grid_frame.pack(pady=(10, 0), padx=(200, 200), fill="x")
        # Add grid column configurations to ensure buttons are centered
        overall_button_grid_frame.grid_columnconfigure(0, weight=1)
        overall_button_grid_frame.grid_columnconfigure(1, weight=1)
        overall_button_grid_frame.grid_columnconfigure(2, weight=1)
        overall_results_label = tk.Label(
            overall_button_grid_frame, text="Overall Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        overall_results_label.grid(row=0, column=0, columnspan=3, padx=(50, 50), pady=(0, 10), sticky="nsew")
        # overall scratch 
        overall_results_button = tk.Button(
            overall_button_grid_frame, text="Overall", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda: self.show_results("", "OVERALL")
        )
        overall_results_button.grid(row=1, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # men
        men_results_button = tk.Button(
            overall_button_grid_frame, text="Men", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda: self.show_results("", "MEN")
        )
        men_results_button.grid(row=1, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # women
        women_results_button = tk.Button(
            overall_button_grid_frame, text="Women", font=("Helvetica", 20), fg="#000000", anchor="center", width=15, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "WOMEN")
        )
        women_results_button.grid(row=1, column=2, padx=(30, 30), pady=(10, 10), sticky="nsew")
    
        # putting back the scrollable frame to the top
        self.scroll_canvas.yview_moveto(0)
    
    # function to show the category results submenu in the scrollable frame
    def show_category_results_sub_menu(self, event=None):
       # destroy the old scrollable frame (clear old widgets)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # destroy all the previous informations on screen
        if hasattr(self, "results_header_frame"):
            self.results_header_frame.destroy()
        self.scrollable_frame.destroy()
        self.scroll_canvas.destroy()
        self.scrollbar.destroy()

    # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.bind("<Enter>", lambda event: self.scroll_canvas.focus_set())  # Focus the canvas when mouse enters
        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # creating the 10 buttons for the category results on 5 rows and 2 columns (male and female)
        # create a frame for organizing the buttons in a grid
        category_button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        category_button_grid_frame.pack(pady=(10, 0), padx=(200, 200), fill="x")
        # Add grid column configurations to ensure buttons are centered
        category_button_grid_frame.grid_columnconfigure(0, weight=1)
        category_button_grid_frame.grid_columnconfigure(1, weight=1)
        category_results_label = tk.Label(
            category_button_grid_frame, text="Category Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        category_results_label.grid(row=3, column=0, columnspan=2, padx=(50, 50), pady=(0, 10), sticky="nsew")
        # junior men    
        junior_men_results_button = tk.Button(
            category_button_grid_frame, text="Junior Men (born 2006-2007)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "JUH")
        )
        junior_men_results_button.grid(row=4, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # junior women 
        junior_women_results_button = tk.Button(
            category_button_grid_frame, text="Junior Women (born 2006-2007)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "JUF")
        )
        junior_women_results_button.grid(row=4, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # espoir men 
        espoir_men_results_button = tk.Button(
            category_button_grid_frame, text="Espoir Men (born 2003-2005)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "ESH")
        )
        espoir_men_results_button.grid(row=5, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # espoir women 
        espoir_women_results_button = tk.Button(
            category_button_grid_frame, text="Espoir Women (born 2003-2005)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "ESF")
        )
        espoir_women_results_button.grid(row=5, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # senior men 
        senior_men_results_button = tk.Button(
            category_button_grid_frame, text="Senior Men (born 1991-2002)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "SEH")
        )
        senior_men_results_button.grid(row=6, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # senior women 
        senior_women_results_button = tk.Button(
            category_button_grid_frame, text="Senior Women (born 1991-2002)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "SEF")
        )
        senior_women_results_button.grid(row=6, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAH1 men 
        mah1_men_results_button = tk.Button(
            category_button_grid_frame, text="Men (born 1966-1990)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAH1")
        )
        mah1_men_results_button.grid(row=7, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAF1 women 
        maf1_women_results_button = tk.Button(
            category_button_grid_frame, text="Women (born 1966-1990)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAF1")
        )
        maf1_women_results_button.grid(row=7, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAH2 men
        mah2_men_results_button = tk.Button(
            category_button_grid_frame, text="Men (born before 1965)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAH2")
        )
        mah2_men_results_button.grid(row=8, column=0, padx=(30, 30), pady=(10, 10), sticky="nsew")
        # MAF2 women 
        maf2_women_results_button = tk.Button(
            category_button_grid_frame, text="Women (born before 1965)", font=("Helvetica", 20), fg="#000000", anchor="center", width=25, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda: self.show_results("", "MAF2")
        )
        maf2_women_results_button.grid(row=8, column=1, padx=(30, 30), pady=(10, 10), sticky="nsew")

        # putting back the scrollable frame to the top
        self.scroll_canvas.yview_moveto(0)

    # function to make the search and display the results in the scrollable frame
    def perform_search(self, event=None):
        self.show_results(self.search_var.get().strip(), "")

    # function to show the results in the scrollable frame with the associated graphics (use in the submenu button or the perfom search results)
    def show_results(self, name : str, category : str, event=None):
        # destroy the old scrollable frame (clear old widgets)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # destroy all the previous informations on screen
        if hasattr(self, "results_header_frame"):
            self.results_header_frame.destroy()
        self.scrollable_frame.destroy()
        self.scroll_canvas.destroy()
        self.scrollbar.destroy()

    # create the result header frame
        self.results_header_frame = tk.Frame(self, bg="#282c34", height=40)
        self.results_header_frame.pack(fill="x", side="top")
        # define header labels and their widths
        col_widths = [3, 14, 3, 5, 5, 5, 5, 5, 5]
        header_labels = ["Rank", "Name", "Category", "5k ", "10k", "12k", "15k", "Finish", "Avg Pace"]
        # format headers with fixed widths and centering
        formatted_headers = [
            f"{label:^{col_width}}"  # center-align text within fixed width
            for label, col_width in zip(header_labels, col_widths)
        ]
        # join headers with " | " separator for visual alignment
        header_text = " | ".join(formatted_headers)
        tk.Label(
            self.results_header_frame, text=header_text, font=("Courier", 20), fg="#ffffff", bg="#282c34", anchor="w"
        ).pack(side="top", fill="x", expand=True, padx=(25, 0))

    # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.bind("<Enter>", lambda event: self.scroll_canvas.focus_set())  # Focus the canvas when mouse enters
        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # getting the datas and displaying them in the scrollable frame
        datas = self.datas.get_specific_datas(name, category)

    # showing the datas in the scrollable frame
        if datas == 0:
            # adding a label to tell the user that there is no result
            no_result_label = tk.Label(
                self.scrollable_frame, text="No results found (either no runners or no single runners)", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
            )
            no_result_label.pack(pady=(20, 10))
            # putting back the scrollable frame to the top
            self.scroll_canvas.yview_moveto(0)

        # category results
        elif datas[0] == 1:
            picture_width, picture_height = 720, 300
        # displaying the category graph
            self.category_graph = None
            category_graph_paths = {
                "OVERALL": "overall.png", "MEN": "men.png", "WOMEN": "women.png",
                "JUH": "juh.png", "JUF": "juf.png", "ESH": "esh.png", "ESF": "esf.png",
                "SEH": "seh.png", "SEF": "sef.png", "MAH1": "mah_1.png", "MAF1": "maf_1.png",
                "MAH2": "mah_2.png", "MAF2": "maf_2.png"
            }
            if category in category_graph_paths:
                self.category_graph = Utility.load_resized_image(f"Data/Precomputed_graphs/{category_graph_paths[category]}", picture_width, picture_height)
            
            # place the graph at the top
            if self.category_graph:
                individual_graph_label = tk.Label(self.scrollable_frame, image=self.category_graph, bg="#282c34")
                individual_graph_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew")

        # displaying the search result graph
            col_widths = [10, 24, 15, 10, 10, 10, 10, 12, 10]
            all_rows_text = ""  # initialize an empty string for all data
            n = 0
            for index, (_, row) in enumerate(datas[1].iterrows()):
                category_string = row["Category"]
                if pd.isna(category_string):  # handle the "**** Dossard Inconnu" case
                    category_string = "None"
                runners_infos = [str(index + 1), row["Name"], category_string, str(row["5km"]), str(row["10km"]), str(row["12km"]), str(row["15km"]), str(row["Finish"]), self.datas.get_average_pace_str(str(row["Finish"]))]
                # format each field with fixed length (centered)
                formatted_infos = [f"{info:^{col_width}}" for info, col_width in zip(runners_infos, col_widths)]
                # create a single row text
                row_text = " | ".join(formatted_infos)
                n=len(row_text)
                # append it to the full text (with newline + separator)
                all_rows_text += row_text + "\n" + "-" * (n+20) + "\n"

            all_table = "-" * (n+20) + "\n" + all_rows_text
            # create a single label containing all rows
            table_label =tk.Label(
                self.scrollable_frame, text=all_table, font=("Courier", 12),  # monospaced font
                justify="left", anchor="w", bg="#f7f7f7",
            )
            table_label.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

            # configure single column width
            self.scrollable_frame.grid_columnconfigure(0, weight=1)

            # putting back the scrollable frame to the top
            self.scroll_canvas.yview_moveto(0)

        # non finisher result for a runner
        elif datas[0] == 2:
            """still to do """
            # putting back the scrollable frame to the top
            self.scroll_canvas.yview_moveto(0)

        # search for a specific runner and its category results 
        elif datas[0] == 3:
        # getting the graphs
            picture_width, picture_height = 600, 250
            self.left_graph = Utility.load_resized_image("Data/left_figure.png", picture_width, picture_height)
            self.right_graph = Utility.load_resized_image("Data/right_figure.png", picture_width, picture_height)
           
        # getting the runner infos 
            runner_info = datas[1]
            runner_name = runner_info["Name"].values[0]
        
        # we need to cut the first datas so there is only a maximun of 400 runners above the runner and 400 below
            runner_rank = int(runner_info["Category_Rank"].values[0])
            start_idx = max(0, runner_rank - 400)
            end_idx = min(len(datas[2]), runner_rank + 401) 
            # Truncate the dataset
            window_runners = datas[2].iloc[start_idx:end_idx]


        # displaying the search result table with the integrated graphs
            col_widths = [10, 24, 15, 10, 10, 10, 10, 12, 10]
            all_rows_text_before = ""  # text before the searched runner
            searched_runner_text = ""  # text for the searched runner
            all_rows_text_after = ""  # text after the searched runner
            n = 0
            found_searched_runner = False  # flag to indicate if the searched runner is found

            for index, (_, row) in enumerate(window_runners.iterrows()):
                category_string = row["Category"]
                if pd.isna(category_string):  # handle the "**** Dossard Inconnu" case
                    category_string = "None"

                name = row["Name"]
                runners_infos = [str(row["Category_Rank"]), name, category_string, str(row["5km"]), str(row["10km"]), str(row["12km"]), str(row["15km"]), str(row["Finish"]), self.datas.get_average_pace_str(str(row["Finish"]))]
                # format each field with fixed length (centered)
                formatted_infos = [f"{info:^{col_width}}" for info, col_width in zip(runners_infos, col_widths)]
                # create a single row text
                row_text = " | ".join(formatted_infos)
                n=len(row_text)

                # check if this is the searched runner
                if not found_searched_runner:
                    if name == runner_name:
                        # searched runner found
                        searched_runner_text = row_text
                        found_searched_runner = True
                        all_rows_text_after += "-" * (n + 20) + "\n"
                    else:
                        all_rows_text_before += row_text + "\n" + "-" * (n + 20) + "\n"
                else:
                    all_rows_text_after += row_text + "\n" + "-" * (n + 20) + "\n"

            # create a label for before the searched runner
            before_table_label = tk.Label(
                self.scrollable_frame, text=all_rows_text_before, font=("Courier", 12),  # monospaced font
                justify="left", anchor="w", bg="#f7f7f7"
            )
            before_table_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
            
            if self.left_graph and self.right_graph:
                # create a label for the left graph
                left_graph_label = tk.Label(self.scrollable_frame, image=self.left_graph, bg="#282c34")
                left_graph_label.grid(row=1, column=0, pady=(0, 10), sticky="w")
                # create a label for the right graph
                right_graph_label = tk.Label(self.scrollable_frame, image=self.right_graph, bg="#282c34")
                right_graph_label.grid(row=1, column=1, pady=(0, 10), sticky="w")

            # create a label for the searched runner
            searched_table_label = tk.Label(
                self.scrollable_frame, text=searched_runner_text, font=("Courier", 12),
                justify="left", anchor="w", bg="#FFDB58"
            )
            searched_table_label.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
            # create a label for after the searched runner
            after_table_label = tk.Label(
                self.scrollable_frame, text=all_rows_text_after, font=("Courier", 12),
                justify="left", anchor="w", bg="#f7f7f7"
            )
            after_table_label.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

            # configure row and column weights
            for i in range(4):
                self.scrollable_frame.grid_rowconfigure(i, weight=1)
            for i in range(2):
                self.scrollable_frame.grid_columnconfigure(i, weight=1)

            # finding the position of the searched search table label to move the scrollable frame on its position
            self.scroll_canvas.update_idletasks()  # ensure layout calculations are updated
            searched_runner_y = left_graph_label.winfo_y()-80  # get the Y-position of the figure (-40 to see the man on top)
            frame_height = self.scrollable_frame.winfo_height()  # get total height of the frame
            # compute the relative scroll position
            if frame_height > 0:  # avoid division by zero
                relative_y = max(0, min(1, searched_runner_y / frame_height))  # normalize between 0 and 1
                self.scroll_canvas.yview_moveto(relative_y)
            
    # reset the scollable frame to its initial state (the text and gpx preview)
    def reset_screen(self, event=None):
        # clear the search bar
        self.search_var.set("")

        # destroy the old scrollable frame (clear old widgets)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # destroy all the previous informations on screen
        if hasattr(self, "results_header_frame"):
            self.results_header_frame.destroy()
        self.scrollable_frame.destroy()
        self.scroll_canvas.destroy()
        self.scrollbar.destroy()

    # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # home page content
        # title text
        self.description_title_label = tk.Label(
            self.scrollable_frame, text=self.description_title_text, font=("Helvetica", 30), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_title_label.pack(padx=(50,50), pady=(10,10))
        # description text
        self.description_half_label = tk.Label(
            self.scrollable_frame, text=self.description_text,font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_half_label.pack(padx=(50,50), pady=(0,10))
    # two buttons to redirect to the overall and category results
        # frame for result link buttons
        self.button_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.button_frame.pack(pady=(0, 10),)
        # buttons for overall results in the home page
        home_page_overall_results_button = tk.Label(
            self.button_frame, text="View Overall Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_overall_results_button.pack(padx=(50, 50), pady=(0, 10), side = "left")
        home_page_overall_results_button.bind("<Enter>", lambda event, b=home_page_overall_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_overall_results_button.bind("<Leave>", lambda event, b=home_page_overall_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_overall_results_button.bind("<Button-1>", self.show_overall_results_sub_menu)
        # buttons for category results in the home page
        home_page_category_results_button = tk.Label(
            self.button_frame, text="View Category Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_category_results_button.pack(padx=(50, 50), pady=(0, 10), side = "right") 
        home_page_category_results_button.bind("<Enter>", lambda event, b=home_page_category_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_category_results_button.bind("<Leave>", lambda event, b=home_page_category_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_category_results_button.bind("<Button-1>", self.show_category_results_sub_menu)
    # race map 
        map_width, map_height = 850, 500
        self.parcours = Utility.load_resized_image("Data/Pictures/semi_parcours.png", map_width, map_height)
        self.race_map_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.race_map_frame.pack(pady=(0, 10), fill="x", side="bottom", anchor="s")
        map_label = tk.Label(self.race_map_frame, image=self.parcours, bg="#282c34")
        map_label.pack()
      
        # putting back the scrollable frame to the top
        self.scroll_canvas.yview_moveto(0)
       
    # handle mouse wheel scrolling
    def on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    # handle making a button bigger when hovering with the mouse over it
    def on_submenu_button_hover(self, event, button, is_entering):
        # change visuals when hovering over submenu buttons.
        if is_entering:
            button.config(font=("Helvetica", 30, "bold"))
        else:
            button.config(font=("Helvetica", 20))

    # function to use the dismissable messagebox to ask the user if he really wants to deconnect
    def deconnexion(self, event=None):
        Utility.show_dismissable_messagebox(self.master, "Deconnexion", "Are you sure you want to deconnect?", lambda: self.navigate_callback(1), duration=4000, is_deconnexion_avorted=True)
        self.reset_screen()
    
    # return the first name and last name of the user that is connected
    def get_own_person_results(event=None):
        # database file path
        db_folder = "Data/Databases/"
        # ensure the database folder exists
        if not os.path.exists(db_folder):
            os.makedirs(db_folder) 
        # create the database if it doesn't exist
        db_path = os.path.join(db_folder, "App_Database.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # creating the users table if it doesn't exist
        cursor.execute("SELECT first_name, last_name FROM users WHERE connection_status = 1")
        result = cursor.fetchone()
        conn.close()
        return f"{result[0]} {result[1]}"

