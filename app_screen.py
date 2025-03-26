# import the necessary libraries
import tkinter as tk


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
        logo_button.place(x=100, y=header_frame.winfo_reqheight() // 2, anchor="center")  
        logo_button.bind("<Button-1>", self.reset_screen)

    # home label/button
        home_button = tk.Label(
            header_frame, text="Home", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        home_button.place(x=300, y=header_frame.winfo_reqheight() // 2, anchor="center") 
        home_button.bind("<Enter>", lambda event: home_button.config(font=("Helvetica", 50, "bold"), fg="#000000", bg="#FFDB58"))
        home_button.bind("<Leave>", lambda event: home_button.config(font=("Helvetica", 40), fg="#000000", bg="#FFDB58"))
        home_button.bind("<Button-1>", self.reset_screen)
        
    # results label/button
        results_button = tk.Label(
            header_frame, text="Results", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        results_button.place(x=600, y=header_frame.winfo_reqheight() // 2, anchor="center")
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
        submenu = tk.Frame(master, bg="#FFDB58", relief="raised", border=0, highlightthickness=0, width=300, height=100)
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

    # deconnexion button
        # function to use the dismissable messagebox to ask the user if he really wants to deconnect
        def deconnexion(event=None):
            Utility.show_dismissable_messagebox(master, "Deconnexion", "Are you sure you want to deconnect?", lambda: self.navigate_callback(1), duration=4000, is_deconnexion_avorted=True)
        self.logout_image = Utility.load_resized_image("Data/Pictures/Log_Out.png", 40, 40)
        logout_button = tk.Button(
            header_frame, image=self.logout_image, border=0, highlightthickness=0, compound="center"
        )
        logout_button.place(x=self.window_width - 100, y=header_frame.winfo_reqheight() // 2, anchor="center")
        logout_button.bind("<Button-1>", deconnexion)

    # search bar
        self.search_var = tk.StringVar()
        search_bar = tk.Entry(
            header_frame, textvariable=self.search_var, font=("Helvetica", 20), background="#f7f7f7", highlightbackground="#282c34"
        )
        search_bar.place(x=self.window_width // 2 + 275, y=header_frame.winfo_reqheight() // 2, anchor="center")
        search_bar.bind("<Return>", self.perform_search)

    # create the scrollable frame for results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=scrollbar.set)
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    # frame for fixed header content (hidden initially)
        self.results_header_frame = tk.Frame(self.scroll_canvas, bg="#282c34", height=40)
        self.results_header_window = self.scroll_canvas.create_window(
            (0, 0), window=self.results_header_frame, anchor="nw", width=self.scroll_canvas.winfo_width()
        )
        self.results_header_frame.pack_forget()
        header_labels = ["Rank", "Name", "Category", "Time", "Pace"]
        for index, header_text in enumerate(header_labels):
            tk.Label(
                self.results_header_frame, text=header_text, font=("Helvetica", 20), fg="#ffffff", bg="#282c34", anchor="w", padx=5
            ).grid(row=0, column=index, sticky="nsew")
        for col in range(len(header_labels)):
            self.results_header_frame.grid_columnconfigure(col, weight=1)

    # frame for scrollable results
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
        )
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # home page content
        # title text
        description_title_text = (
            "Welcome to the Boulogne Half Marathon App!"
        )
        self.description_title_label = tk.Label(
            self.scrollable_frame, text=description_title_text, font=("Helvetica", 30), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_title_label.pack(padx=(50,50), pady=(0,10))
        # description text
        description_text = (
            "The Boulogne Half Marathon is a long-distance running event covering a distance of 21.0975 kilometers.\n"
            "The app is designed give access to essential race information, rankings and performance analysis.\n"
            "You can click on one of the results buttons or search for a specific runner or team in the search bar to access the results, both overall and by category"
        )
        self.description_half_label = tk.Label(
            self.scrollable_frame, text=description_text,font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
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
        # load the images with the specified dimensions
        map_width, map_height = 850, 500
        self.parcours = Utility.load_resized_image("Data/Pictures/semi_parcours.png", map_width, map_height)
        self.race_map_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.race_map_frame.pack(pady=(0, 10), fill="x", side="bottom", anchor="s")
        race_map_title = tk.Label(
            self.race_map_frame, text="Half Marathon Course", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center"
        )
        race_map_title.pack(pady=(0, 10))
        map_label = tk.Label(self.race_map_frame, image=self.parcours, bg="#282c34")
        map_label.pack()

    # function to show the results menu in the scrollable frame
    def show_results_menu(self, event=None):   
        test = 0

    # function to show the overall results submenu in the scrollable frame
    def show_overall_results_sub_menu(self, event=None):
        test = 0

    # function to show the category results submenu in the scrollable frame
    def show_category_results_sub_menu(self, event=None):
       test = 0
        
    # function to show the overall results in the scrollable frame with the associated graphics (use in the submenu button or the perfom search results)
    def show_overall_results(self, sex, is_by_name : bool, name : str):
        test = 0

    # function to show the category results in the scrollable frame with the associated graphics (use in the submenu button or the perfom search results)
    def show_category_results(self, distance, sex, is_by_name, name):
        test = 0

    # function to make the search and display the results in the scrollable frame
    def perform_search(self, event=None):
        test = 0
        
    # reset the scollable frame to its initial state (the text and gpx preview)
    def reset_screen(self, event=None):
        # clear the search bar
        self.search_var.set("")

        # clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # hide the results header
        self.results_header_frame.pack_forget()

        # main text, shown at the start --> recreate here 
        # title text
        description_title_text = (
            "Welcome to the Boulogne Half Marathon App!"
        )
        self.description_title_label = tk.Label(
            self.scrollable_frame, text=description_title_text, font=("Helvetica", 30), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_title_label.pack(padx=(50,50), pady=(0,10))
        # description text
        description_text = (
            "The Boulogne Half Marathon is a long-distance running event covering a distance of 21.0975 kilometers.\n"
            "The app is designed give access to essential race information, rankings and performance analysis.\n"
            "You can click on one of the results buttons or search for a specific runner or team in the search bar to access the results, both overall and by category"
        )
        self.description_half_label = tk.Label(
            self.scrollable_frame, text=description_text,font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
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
        # load the images with the specified dimensions
        map_width, map_height = 850, 500
        self.parcours = Utility.load_resized_image("Data/Pictures/semi_parcours.png", map_width, map_height)
        self.race_map_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.race_map_frame.pack(pady=(0, 10), fill="x", side="bottom", anchor="s")
        race_map_title = tk.Label(
            self.race_map_frame, text="Half Marathon Course", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center"
        )
        race_map_title.pack(pady=(0, 10))
        map_label = tk.Label(self.race_map_frame, image=self.parcours, bg="#282c34")
        map_label.pack()
      
        # putting back the scrollable frame to the top
        self.scroll_canvas.yview_moveto(0)
       
    # handle mouse wheel scrolling
    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    # handle making a button bigger when hovering with the mouse over it
    def on_submenu_button_hover(self, event, button, is_entering):
        # change visuals when hovering over submenu buttons.
        if is_entering:
            button.config(font=("Helvetica", 30, "bold"))
        else:
            button.config(font=("Helvetica", 20))

