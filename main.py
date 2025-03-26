# import the necessary libraries
import tkinter as tk


# import the class created in other files
from main_app import Main_App


# launch the app
if __name__ == "__main__":
    window = tk.Tk()
    app = Main_App(window)
    window.mainloop()
