import customtkinter
import win32gui
from time import sleep
from multiprocessing import Process

root = None
debug = False


# function to display tkinter notification window
class DisplayNotification:
    def __init__(
        self,
        message="",
        title_text=None,
        icon_path=None,
        window_size="250x150",
        debug=False,
        window_timeout=5,
        wait_until_closed=False,
    ):
        """
        displays a custom tkinter notification window
        :param message: message to display in notification window
        :param title_text: title of the notification window
        :param icon_path: path to .ico file
        :param window_size: size of the window default is 250x150
        :param debug: weather to show debug messages or not
        :return:
        """
        self.message = message
        self.size = window_size
        self.title_text = title_text
        self.icon_path = icon_path
        self.debug = debug
        self.window_timeout = window_timeout
        self.wait_until_closed = wait_until_closed

        # make main process
        self.main_process = Process(
            target=util_start,
            args=(
                self.message,
                self.size,
                self.title_text,
                self.icon_path,
                self.debug,
                self.window_timeout,
            ),
        )
        self.main_process.start()

        if self.wait_until_closed:
            self.main_process.join()


def util_start(message, size, title_text, icon_path, debug_param, window_timeout):
    global root, debug
    debug = debug_param

    # create the main window
    root = customtkinter.CTk()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"{size}+{screen_width - 250}+0")
    root.overrideredirect(1)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    frame = customtkinter.CTkFrame(root)
    frame.pack(padx=10, pady=10, expand=True, fill="both")

    if title_text is not None:
        title_label = customtkinter.CTkButton(
            frame,
            text=title_text,
        )
        title_label.pack(pady=(20, 10))

        # add message label
        message_label = customtkinter.CTkLabel(frame, text=message)
        message_label.pack()
    else:
        message_label = customtkinter.CTkLabel(frame, text=message, anchor="center")
        message_label.pack(padx=10, pady=10)

    root.after(0, update_focus)
    root.after(window_timeout * 1000, on_closing)
    root.mainloop()


def on_closing():
    global root, debug
    if debug:
        print("Closing window...")
    for i in range(50):
        root.attributes("-alpha", 1 - i / 50)
        root.update()
        sleep(0.01)
    root.quit()


def update_focus():
    global root, debug
    if debug:
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

    if debug:
        print(f"focus set to: {window_names[0]}...")

    # Find the handle of the window with the specified title
    hwnd = win32gui.FindWindow(None, window_names[0])
    # Give focus to the window
    win32gui.SetForegroundWindow(hwnd)
