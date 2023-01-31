import customtkinter
import win32gui
from time import sleep
from threading import Thread


# function to display tkinter notification window
class DisplayNotification:

    def __init__(self, message="", show_button=False, button_text="", icon_path=None, window_size="250x150",
                 debug=False):
        """
        displays a custom tkinter notification window
        :param message: message to display in notification window
        :param show_button: weather to show button or not
        :param button_text: button text
        :param icon_path: path to .ico file
        :param window_size: size of the window default is 250x150
        :param debug: weather to show debug messages or not
        :return:
        """
        self.root = None
        self.message = message
        self.size = window_size
        self.show_button = show_button
        self.button_text = button_text
        self.icon_path = icon_path
        self.button_function = False
        self.debug = debug
        self.running = True

        # make main thread
        self.main_thread = Thread(target=self.util_start)
        self.main_thread.start()

    def util_start(self):
        # create the main window
        self.root = customtkinter.CTk()
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"{self.size}+{screen_width - 250}+0")
        self.root.overrideredirect(1)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = customtkinter.CTkFrame(self.root)
        frame.pack(padx=10, pady=10, expand=True, fill="both")

        if self.show_button:
            title_label = customtkinter.CTkButton(
                frame,
                text=self.button_text,
                command=self.set_button_function
            )
            title_label.pack(pady=(20, 10))

            # add message label
            message_label = customtkinter.CTkLabel(frame, text=self.message)
            message_label.pack()
        else:
            message_label = customtkinter.CTkLabel(frame, text=self.message, anchor="center")
            message_label.pack(padx=10, pady=10)

        self.root.after(0, self.update_focus)
        self.root.after(5000, self.on_closing)
        self.root.mainloop()
        self.running = False

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

        if self.debug:
            print(f"focus set to: {window_names[1]}...")
        # Find the handle of the window with the specified title
        hwnd = win32gui.FindWindow(None, window_names[1])
        # Give focus to the window
        win32gui.SetForegroundWindow(hwnd)

    def set_button_function(self):
        self.button_function = True


def wait_until_closed(notification):
    """
    waits until the notification window is closed
    :param notification: the notification object
    :return:
    """
    while notification.running:
        sleep(0.01)
        pass
