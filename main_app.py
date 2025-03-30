# import the necessary libraries
import tkinter as tk
from tkinter import PhotoImage


# import the class created in other files
from login_screen import Login_Screen
from signup_screen import Signup_Screen
from app_screen import App_Screen
from Data import Race_Datas


# classe to manage the multi-screen app
class Main_App:

    # initialize the app
    def __init__(self, window):

        # getting all the Half-Marathon datas
        data = Race_Datas("Data/Databases/App_Database.db")

        self.window = window
        self.window.title("Multi-Screen Scrollable App")
        self.window.attributes("-fullscreen", True)
        window.configure(height=window.winfo_height(), width=window.winfo_width())
        Icone_app = PhotoImage(file="Data/Pictures/App_Icon.png")
        self.window.iconphoto(True, Icone_app)

        # create a container frame to hold all screens
        self.container = tk.Frame(window)
        self.container.pack(fill="both", expand=True)

        # create and store screens in the container
        self.screens = {
            1: Login_Screen(self.container, self.show_screen),
            2: Signup_Screen(self.container, self.show_screen),
            3: App_Screen(self.container, self.show_screen, window.winfo_width(), data)
        }

        # place all screens in the same location within the container
        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

        # start with the first screen
        self.current_screen = 3
        self.show_screen(self.current_screen)

        # bind keyboard inputs
        self.window.bind("<Escape>", self.quit_game)

    # function to show the selected screen
    def show_screen(self, screen_number):
        # raise the selected screen to the front and update the current screen tracker
        self.screens[screen_number].tkraise()
        self.current_screen = screen_number
        # direct focus to the first field for the login and sign up screens
        if self.current_screen == 1:
            self.screens[screen_number].after(500, lambda: self.screens[screen_number].username_entry.focus())
        elif self.current_screen == 2:
            self.screens[screen_number].after(500, lambda: self.screens[screen_number].first_name_entry.focus())

    # function to navigate to the next screen
    def next_screen(self, event=None):
        if self.current_screen < len(self.screens):
            self.show_screen(self.current_screen + 1)

    # function to navigate to the previous screen
    def previous_screen(self, event=None):
        if self.current_screen > 1:
            self.show_screen(self.current_screen - 1)

    # function to quit the app
    def quit_game(self, event=None):
        self.window.quit()

