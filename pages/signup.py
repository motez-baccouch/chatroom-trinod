import tkinter
from tkinter import messagebox, Frame

def default_success_command():
    print("success")

class SignupFrame(tkinter.Frame): 
    def __init__(self,container, success_command= default_success_command, login_command=default_success_command):
        super().__init__(container)

        # Creating widgets
        self.login_label = tkinter.Label(
            self, text="Signup", bg='#333333', fg="#FF3399", font=("Arial", 30))
        self.username_label = tkinter.Label(
            self, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.username_entry = tkinter.Entry(self, font=("Arial", 16))
        self.password_entry = tkinter.Entry(self, show="*", font=("Arial", 16))
        self.password_label = tkinter.Label(
            self, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.signup_button = tkinter.Button(
            self, text="Signup", command=self.signup)
        self.login_button = tkinter.Button(
            self, text="Login", command=login_command
        )

        # Placing widgets on the screen
        self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=30)
        self.login_button.grid(row=4, column=0, columnspan=2)

        self.success_command= success_command

    def sigup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        



    