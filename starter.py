"""
Exercise: lab 5 / cash_register version 3  (DD1321)
Usage: GUI for cash_register_v3.py
Author: Nils Olivier
Date: 12-12-2023
"""

# Imports
from main_code import *


class App(ctk.CTk):
    """
    Initializes the App object.

    Args
     - title (str): The title of the application.
     - size (tuple): A tuple representing the size of the application window (width, height).
    """

    def __init__(self, title="APP", size=(600, 600)):
        super().__init__()

        # Main setup
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        # Widgets
        self.menu = Menu(self, corner_radius=10, fg_color="#1B1E23")
        self.main = Main(self, corner_radius=10, bg_color="#2D313C")

        # Run
        self.mainloop()

    def switch_frame(self, frame_name):
        """
        Switches the current frame in the application to the specified frame.

        Args
        - frame_name (str): The name of the frame to switch to.
        """
        self.main.switch_frame(frame_name)


if __name__ == "__main__":
    app = App("Cash Register", (800, 600))
