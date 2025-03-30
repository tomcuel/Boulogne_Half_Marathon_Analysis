# import the necessary libraries
import tkinter as tk
from tkinter import ttk
import os
import sqlite3
import re


# import the class created in other files
from utility import Utility


# screen 2: classe to manage the sign up screen
class Signup_Screen(tk.Frame):

    # initialize the sign up screen
    def __init__(self, master, navigate_callback):
        super().__init__(master, bg="#282c34", highlightthickness=0, borderwidth=0, border=0)
        self.navigate_callback = navigate_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # ensure this frame expands within its parent
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    # title Label
        label = tk.Label(
            self, text="Sign Up", font=("Helvetica", 70, "bold"), fg="#ffffff", bg="#282c34"
            )
        label.pack(pady=(20, 20))   

    # user info section
        user_info_frame = tk.LabelFrame(
            self, text="User Information", font=("Helvetica", 30), fg="#ffffff", bg="#282c34", border=0, labelanchor="n"
        )
        user_info_frame.pack(pady=(10,30), fill="y")

        first_name_label = tk.Label(
            user_info_frame, text="First Name (required)", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        first_name_label.grid(row=0, column=0)
        self.first_name_entry = tk.Entry(user_info_frame)
        self.first_name_entry.grid(row=1, column=0)
        self.first_name_entry.bind("<Return>", Utility.focus_next_widget)
        
        last_name_label = tk.Label(
            user_info_frame, text="Last Name (required)", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        last_name_label.grid(row=0, column=1)
        self.last_name_entry = tk.Entry(user_info_frame)
        self.last_name_entry.grid(row=1, column=1)
        self.last_name_entry.bind("<Return>", Utility.focus_next_widget)

        title_label = tk.Label(
            user_info_frame, text="Title", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        title_label.grid(row=0, column=2)
        self.title_combobox = ttk.Combobox(
            user_info_frame, values=["Mr.", "Ms.", "Dr."], state="readonly"
        )
        self.title_combobox.set('')
        self.title_combobox.grid(row=1, column=2)
        self.title_combobox.bind("<Return>", Utility.focus_next_widget)

        age_label = tk.Label(
            user_info_frame, text="Age", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        age_label.grid(row=2, column=0)
        self.age_combobox = ttk.Combobox(
            user_info_frame, values=[str(age) for age in range(15, 101)], state="readonly"
        )
        self.age_combobox.grid(row=3, column=0)
        self.age_combobox.bind("<Return>", Utility.focus_next_widget)

        nationality_label = tk.Label(
            user_info_frame, text="Nationality", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
            )
        nationality_label.grid(row=2, column=1)
        self.nationality_combobox = ttk.Combobox(
            user_info_frame, values=["French", "Tunisian", "Brazilian", "Ukrainian", "Polish", "Swiss", "Lebanese", "Other"], state="readonly"
            )
        self.nationality_combobox.set('')
        self.nationality_combobox.grid(row=3, column=1)
        self.nationality_combobox.bind("<Return>", Utility.focus_next_widget)

        for widget in user_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    # username and password info
        login_info_frame = tk.LabelFrame(
            self, text="Login Information (required)", font=("Helvetica", 30), fg="#ffffff", bg="#282c34", border=0, labelanchor="n"
        )
        login_info_frame.pack(pady=(10,30), fill="y")

        username_label = tk.Label(
            login_info_frame, text="Username", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(login_info_frame)
        self.username_entry.grid(row=1, column=0)
        self.username_entry.bind("<Return>", Utility.focus_next_widget)

        password_label = tk.Label(
            login_info_frame, text="Password", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        password_label.grid(row=0, column=1)
        self.password_entry = tk.Entry(login_info_frame, show="*")
        self.password_entry.grid(row=1, column=1)
        self.password_entry.bind("<Return>", Utility.focus_next_widget)

        password_confirm_label = tk.Label(
            login_info_frame, text="Confirm Password", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        password_confirm_label.grid(row=0, column=2)
        self.password_confirm_entry = tk.Entry(login_info_frame, show="*")
        self.password_confirm_entry.grid(row=1, column=2)
        self.password_confirm_entry.bind("<Return>", Utility.focus_next_widget)

        for widget in login_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    # accept terms and conditions
        terms_frame = tk.LabelFrame(
            self, text="Terms & Conditions (required)", font=("Helvetica", 20), fg="#ffffff", bg="#282c34"
        )
        terms_frame.pack(padx=20, pady=10, fill="x")
        self.accept_var = tk.StringVar(value="Not Accepted")
        terms_check = tk.Checkbutton(
            terms_frame, text="I accept the terms and conditions", font=("Helvetica", 10), fg="#ffffff", bg="#282c34",
            variable=self.accept_var, onvalue="Accepted", offvalue="Not Accepted"
        )
        terms_check.grid(row=0, column=0)
        terms_check.bind("<Return>", Utility.focus_next_widget)

    # buttons
        self.submit_button = tk.Button(
            self, text="Submit", font=("Helvetica", 30), fg="#000000", relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, command=self.sign_up
        )
        self.submit_button.pack(pady=(20, 20))
        self.submit_button.bind("<Return>", lambda e: self.submit_button.invoke())

        self.back_button = tk.Button(
            self, text="Back to Login", font=("Helvetica", 30), fg="#000000", relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, command=lambda: self.navigate_callback(1),
        )
        self.back_button.pack(pady=(20, 20))
        self.back_button.bind("<Return>", lambda e: self.back_button.invoke())
        self.back_button.bind("<Tab>", lambda e: self.refocus_to_firstname())

    # function to sign up a new user and save the data in the Excel file
    def sign_up(self):
        # check acceptance of terms and conditions
        accepted = self.accept_var.get()
        if accepted == "Accepted":

            # user info
            firstname = self.first_name_entry.get()
            lastname = self.last_name_entry.get()
            # raising error if first name or last name is empty
            if not firstname:
                Utility.show_dismissable_messagebox(self, "Error", "First name is required", lambda: None)
                return
            if not lastname:
                Utility.show_dismissable_messagebox(self, "Error", "Last name is required", lambda: None)
                return
            
            # runner info (title, age, nationality)
            title = self.title_combobox.get()
            age = self.age_combobox.get()
            nationality = self.nationality_combobox.get()

            # username and password
            username = self.username_entry.get()
            password = self.password_entry.get()
            password_confirm = self.password_confirm_entry.get()
            # raising error if self.username or password is empty
            if not username or not password or not password_confirm:
                Utility.show_dismissable_messagebox(self, "Error", "Username and passwords are required", lambda: None)
                return
            # raising error if password and confirm password do not match
            if password != password_confirm:
                Utility.show_dismissable_messagebox(self, "Error", "Passwords do not match", lambda: None)
                return
            # the password should be at least 6 characters long, contain 2 numbers, and include at least one special character from *_+=?&@#-
            if not self.validate_password(password):
                Utility.show_dismissable_messagebox(self, "Error", "Password must be at least 6 characters long, contain 2 numbers, and include at least one special character from *_+=?&@#-", lambda: None)
                return

            # database file path
            db_folder = "Data/Databases/"
            # ensure the database folder exists
            if not os.path.exists(db_folder):
                os.makedirs(db_folder) 
            # create the database if it doesn't exist
            db_path = os.path.join(db_folder, "App_Database.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, first_name TEXT, last_name TEXT, age INTEGER, nationality TEXT, username TEXT UNIQUE, password TEXT UNIQUE)")
            conn.commit()
            conn.close()

            # open the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # check for duplicate users (same name or same username)
            cursor.execute("SELECT * FROM users WHERE (first_name = ? AND last_name = ?) OR username = ?", (firstname, lastname, username))
            existing_user = cursor.fetchone()
            if existing_user:
                Utility.show_dismissable_messagebox(self, "Error", "This user already exists", lambda: None)
                conn.close()
                return
            # check for duplicate password
            hashed_password = Utility.hash_password(password)
            cursor.execute("SELECT * FROM users WHERE password = ?", (hashed_password, ))
            existing_password = cursor.fetchone()
            if existing_password:
                Utility.show_dismissable_messagebox(self, "Error", "This password is already used", lambda: None)
                conn.close()
                return

            # if no duplicates found, add new user into the database
            cursor.execute("INSERT INTO users (title, first_name, last_name, age, nationality, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)",(title, firstname, lastname, age, nationality, username, hashed_password))
            conn.commit()
            conn.close()
            # reset the fields after submission
            self.first_name_entry.delete(0, 'end')
            self.last_name_entry.delete(0, 'end')
            self.title_combobox.set("")
            self.age_combobox.set('')
            self.nationality_combobox.set("")
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.password_confirm_entry.delete(0, 'end')
            self.accept_var.set("Not Accepted")

            Utility.show_dismissable_messagebox(self, "Success", "Sign-up successful", lambda: self.navigate_callback(1))
            self.navigate_callback(1)
        
        # if the terms are not accepted, show a warning
        else:
            Utility.show_dismissable_messagebox(self, "Error", "You have not accepted the terms", lambda: None)
    
    # function to validate the password
    def validate_password(self, password):
        return len(password) >= 8 and len(re.findall(r'[0-9]', password)) >= 2 and len(re.findall(r'[a-z]', password))+len(re.findall(r'[A-Z]', password)) >= 6 and any(char in "*_+=?&@#-" for char in password)

    # function to refocus on the first name entry field when the Tab key is pressed on the Sign Up button
    def refocus_to_firstname(self):
        self.first_name_entry.focus()
        return "break"  

