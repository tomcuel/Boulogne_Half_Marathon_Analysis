# import the necessary libraries
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


# import the class created in other files
from utility import Utility


# screen 1: classe to manage the sign up screen
class Login_Screen(tk.Frame):

    # initialize the login screen
    def __init__(self, master, navigate_callback):
        super().__init__(master, bg="#282c34", highlightthickness=0, borderwidth=0, border=0)
        self.navigate_callback = navigate_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # ensure this frame expands within its parent
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    # header Label
        label = tk.Label(
            self, text="Boulogne Half Marathon App", font=("Helvetica", 75, "bold"), fg="#ffffff", bg="#282c34"
        )
        label.pack(pady=(90, 50))

    # username Field
        username_label = tk.Label(
            self, text="Username:", font=("Helvetica", 40), fg="#ffffff", bg="#282c34"
        )
        username_label.pack()
        self.username_entry = tk.Entry(
            self, font=("Helvetica", 20), bg="#f7f7f7"
        )
        self.username_entry.pack(pady=(30, 20))
        self.username_entry.bind("<Return>", Utility.focus_next_widget)

    # password Field
        password_label = tk.Label(
            self, text="Password:", font=("Helvetica", 40), fg="#ffffff", bg="#282c34"
        )
        password_label.pack()
        self.password_entry = tk.Entry(
            self, show="*", font=("Helvetica", 20), bg="#f7f7f7"
        )
        self.password_entry.pack(pady=(30, 20))
        self.password_entry.bind("<Return>", Utility.focus_next_widget)

    # login button 
        self.login_button = tk.Button(
            self, text="Login", font=("Helvetica", 40), fg="#000000", relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, command=self.login,
        )
        self.login_button.pack(pady=(20, 20))
        self.login_button.bind("<Return>", lambda e: self.login_button.invoke())

    # sign up button
        self.signup_button = tk.Button(
            self, text="Sign Up", font=("Helvetica", 40), fg="#000000", relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, command=lambda: [self.navigate_callback(2), self.clear_user_info()] 
        )
        self.signup_button.pack(pady=(20, 20))
        self.signup_button.bind("<Return>", lambda e: self.signup_button.invoke())
        self.signup_button.bind("<Tab>", lambda e: self.refocus_to_username())

    # function to check if the login credentials are valid (in the Excel file)
    def login(self):
        username = self.username_entry.get()
        if not username : 
            Utility.show_dismissable_messagebox(self, "Error", "Please enter a username", lambda: None)
            return
        password = self.password_entry.get()
        if not password :
            Utility.show_dismissable_messagebox(self, "Error", "Please enter a password", lambda: None)
            return

        # open the database and check if the username and password match
        # database file path
        db_folder = "Data/Databases/"
        # ensure the database folder exists
        if not os.path.exists(db_folder):
            os.makedirs(db_folder) 
        # create the database if it doesn't exist
        db_path = os.path.join(db_folder, "App_Database.db")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, first_name TEXT, last_name TEXT, age INTEGER, nationality TEXT, username TEXT UNIQUE, password TEXT UNIQUE)")
            conn.commit()
            conn.close()

            conn = sqlite3.connect(db_path)
            result = conn.execute("SELECT password FROM users WHERE username = ?", (username, )).fetchone()
            if Utility.check_password(password, result[0]):
                Utility.show_dismissable_messagebox(self, "Success", "Login successful!", lambda: self.navigate_callback(3))
                self.clear_user_info()
                conn.close()
                return
            # if no match is found, show an error and reset the password fields
            Utility.show_dismissable_messagebox(self, "Error", "Invalid login", lambda: None)
            self.clear_user_info()
            conn.close()
        
        except Exception as e:
            messagebox.showerror(title="Error", message=f"An error occurred: {e}")

    # function to refocus on the username entry field when the Tab key is pressed on the Sign Up button
    def refocus_to_username(self):
        self.username_entry.focus()
        return "break"
    
    # function to clear both username and password fields from the login screen
    def clear_user_info(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

