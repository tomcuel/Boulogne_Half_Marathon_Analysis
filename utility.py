# import the necessary libraries
import tkinter as tk
from PIL import Image, ImageTk


# class to gather some useful functions that are common to multiple screens
class Utility:

    @staticmethod
    # Function to show a dismissable messagebox with a custom duration, that can navigate to a new screen also, depending on the callback
    def show_dismissable_messagebox(parent, title, message, navigate_callback, duration = 3000, is_deconnexion_avorted = False):
        current_focus = parent.focus_get()
        
        popup = tk.Toplevel(parent)
        popup.title(title)
        window_width = 500
        window_height = 250
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        popup.transient(parent) 
        popup.resizable(False, False)  
        popup.grab_set()

        # Add text to the popup
        canvas = tk.Canvas(popup, width=window_width, height=window_height / 2, bg="#282c34", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_text(
            window_width // 2, window_height // 4, text=message, font=("Helvetica", 40), fill="#ffffff", width=window_width - 40, anchor="center"
        )

        # Add dismiss button
        dismiss_button = tk.Button(
            popup, text="Ok", font=("Helvetica", 30), fg="#000000", relief="flat",  activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda: (popup.destroy(), navigate_callback())
        )
        dismiss_button.place(
            relx=0.5, rely=0.75, anchor="center", width=200, height=50
        )

        # Automatically close the popup after `duration` milliseconds (optional)
        def auto_close():
            if popup.winfo_exists():
                popup.destroy()
                if not is_deconnexion_avorted : # if the deconnexion is not aborted, we can navigate to the next screen, otherwise we stay on the same screen (the 3rd one)
                    navigate_callback()
        
        # Close the popup after `duration` milliseconds
        popup.after(duration, auto_close)
            
        # Return focus to the previously focused widget when the popup closes
        def on_close():
            if current_focus:
                current_focus.focus_set()
    
        # Handle the close button
        popup.protocol("WM_DELETE_WINDOW", lambda: (on_close(), popup.destroy()))  # Handle the close button (X)
        popup.bind("<Destroy>", lambda event: on_close())
    
    @staticmethod
    # Function to focus the next widget in the tab order when the Enter key is pressed
    def focus_next_widget(event):
        # Focus the next widget in tab order
        event.widget.tk_focusNext().focus()
        return "break"

    @staticmethod
    # Load and resize images with high quality using PIL
    def load_resized_image(image_path, new_width, new_height):
        image = Image.open(image_path)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)