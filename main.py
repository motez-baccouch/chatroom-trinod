import tkinter
from tkinter.messagebox import showinfo
from pages.login import LoginFrame
from pages.client import ClientFrame
from pages.signup import SignupFrame


class MainFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        # login frame
        self.login_frame = LoginFrame(self, success_command=self.go_to_chat, signup_command=self.go_to_signup)
        self.login_frame.grid(row=0, column=0)
        
        # signup frame
        self.signup_frame= SignupFrame(self, login_command=self.go_to_login)

        # chat frame
        self.chat_frame= ClientFrame(self)
        

        # show the frame on the container
        self.pack(**options)

    def go_to_chat(self):
        self.login_frame.grid_remove()
        self.chat_frame.grid(row=0, column=0)

    def go_to_signup(self): 
        self.login_frame.grid_remove()
        self.signup_frame.grid(column=0, row=0)

    def go_to_login(self):
        self.signup_frame.grid_remove()
        self.login_frame.grid(column=0, row=0)