import tkinter
from tkinter.messagebox import showinfo
from pages.login import LoginFrame
from pages.client import ClientFrame


class MainFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        # login frame
        self.login_frame = LoginFrame(self, success_command=self.go_to_chat)
        self.login_frame.grid(row=0, column=0)

        # chat frame
        self.chat_frame= ClientFrame(self)
        

        # show the frame on the container
        self.pack(**options)

    def go_to_chat(self):
        self.login_frame.grid_remove()
        self.chat_frame.grid(row=0, column=0)
