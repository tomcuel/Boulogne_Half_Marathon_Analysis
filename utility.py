# import the necessary libraries
import tkinter as tk
from PIL import Image, ImageTk
import bcrypt
import sqlite3


# class to gather some useful functions that are common to multiple screens
class Utility:

    @staticmethod
    # function to show a dismissable messagebox with a custom duration, that can navigate to a new screen also, depending on the callback
    def show_dismissable_messagebox(parent, title, message, navigate_callback, duration = 3000, is_deconnexion_avorted = False):
        current_focus = parent.focus_get()
        
        popup = tk.Toplevel(parent)
        popup.title(title)
        window_width = 500
        window_height = 250
        if "Password must" in message:
            window_width = 1000
            window_height = 500

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        popup.transient(parent) 
        popup.resizable(False, False)  
        popup.grab_set()

        # add text to the popup
        canvas = tk.Canvas(popup, width=window_width, height=window_height / 2, bg="#282c34", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_text(
            window_width // 2, window_height // 4, text=message, font=("Helvetica", 40), fill="#ffffff", width=window_width - 40, anchor="center"
        )

        # deconnexion case : put all users to 0 as connection status
        def perform_deconnexion(is_deconnexion_avorted):
            if is_deconnexion_avorted: # case of a deconnexion, so we reset the connection status to 0
                conn = sqlite3.connect("Data/Databases/App_database.db")
                cursor = conn.cursor()

                # set connection_status to 0 for all users
                cursor.execute("UPDATE users SET connection_status = 0")
                conn.commit()
                conn.close()

        # add dismiss button
        dismiss_button = tk.Button(
            popup, text="Ok", font=("Helvetica", 30), fg="#000000", relief="flat",  activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda: (popup.destroy(), navigate_callback(), perform_deconnexion(is_deconnexion_avorted))  # close the popup and navigate to the next screen
        )
        dismiss_button.place(relx=0.5, rely=0.75, anchor="center", width=200, height=50)

        # automatically close the popup after a certain duration
        def auto_close():
            if popup.winfo_exists():
                popup.destroy()
                if not is_deconnexion_avorted : # if the deconnexion is not aborted, we can navigate to the next screen, otherwise we stay on the same screen (the 3rd one)
                    navigate_callback()
        
        # close the popup after "duration" milliseconds
        popup.after(duration, auto_close)
            
    @staticmethod
    # function to focus the next widget in the tab order when the Enter key is pressed
    def focus_next_widget(event):
        # focus the next widget in tab order
        event.widget.tk_focusNext().focus()
        return "break"

    @staticmethod
    # load and resize images with high quality using PIL
    def load_resized_image(image_path, new_width, new_height):
        image = Image.open(image_path)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)
    
    # generate a hashed password
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()  # generate a salt
        hashed = bcrypt.hashpw(password.encode(), salt)  # hash the password
        return hashed
    
    # verify a password
    def check_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)

