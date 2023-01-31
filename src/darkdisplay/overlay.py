import customtkinter
import win32gui
from time import sleep
import threading
import os


class Overlay:

    # init function that takes , message, window size, debug
    def __init__(self, message="", window_size="250x150", debug=False, start_hidden=False):
        """
        makes an overlay object
        :param message: message to display
        :param window_size: size of the window
        :param debug: whether to print debug messages
        :param start_hidden: whether to start the window hidden
        """
        self.main_thread = None
        self.message_label = None
        self.is_hidden = False
        self.root = None
        self.message = message
        self.size = window_size
        self.debug = debug
        self.start_hidden = start_hidden

    # function to start the overlay
    def start(self):
        """
        starts the overlay
        :return:
        """
        # create the main window
        self.main_thread = threading.Thread(target=self.util_start)
        self.main_thread.start()

    def util_start(self):
        self.root = customtkinter.CTk()
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"{self.size}+{screen_width - 250}+0")
        self.root.overrideredirect(1)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # hide the window if start_hidden is true
        if self.start_hidden:
            self.root.withdraw()
            self.is_hidden = True

        frame = customtkinter.CTkFrame(self.root)
        frame.pack(padx=10, pady=10, expand=True, fill="both")

        # add message label
        self.message_label = customtkinter.CTkLabel(frame, text=self.message)
        self.message_label.pack(pady=10)

        self.root.after(0, self.update_focus)
        self.root.mainloop()

        if self.debug:
            print("Window closed")

    def on_closing(self):
        if self.debug:
            print("Closing window...")
        for i in range(50):
            self.root.attributes("-alpha", 1 - i / 50)
            self.root.update()
            sleep(0.01)
        self.root.quit()

    def update_focus(self):
        if self.debug:
            print("Updating focus...")
        # Initialize an empty list to store the window names
        window_names = []
        # Get the handle of the topmost window
        hwnd = win32gui.GetTopWindow(None)
        # Loop through the windows to get their handles and names
        while hwnd:
            # Check if the window is visible and non-minimized
            if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
                # Get the title of the current window
                title = win32gui.GetWindowText(hwnd)
                # Add the title to the list
                if title != "":
                    window_names.append(title)
            # Get the handle of the next window
            hwnd = win32gui.GetWindow(hwnd, 2)

        if self.is_hidden:
            window_name = window_names[0]
        else:
            window_name = window_names[1]

        if self.debug:
            print(f"focus set to: {window_name}...")
        # Find the handle of the window with the specified title
        hwnd = win32gui.FindWindow(None, window_name)
        # Give focus to the window
        win32gui.SetForegroundWindow(hwnd)

    def update_message(self, message):
        """
        updates the message
        :param message: what to update the message to
        :return:
        """
        self.message = message
        self.message_label.configure(text=self.message)

    def hide(self):
        """
        hides the window
        :return:
        """
        self.root.withdraw()
        self.is_hidden = True

    def show(self):
        """
        shows the window
        :return:
        """
        self.root.deiconify()
        self.is_hidden = False

    def close(self):
        """
        closes the window
        :return:
        """
        self.on_closing()
