import tkinter
from tkinter import messagebox, Frame
from utils.Authentification import Authentification

def default_success_command():
    print("success")

def default_signup_command():
    print("signup")

class LoginFrame(tkinter.Frame): 
    def __init__(self,container, success_command= default_success_command, signup_command=default_signup_command):
        super().__init__(container)

        self.success_command= success_command

        # Creating widgets
        self.login_label = tkinter.Label(
            self, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
        self.username_label = tkinter.Label(
            self, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.username_entry = tkinter.Entry(self, font=("Arial", 16))
        self.password_entry = tkinter.Entry(self, show="*", font=("Arial", 16))
        self.password_label = tkinter.Label(
            self, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.login_button = tkinter.Button(
            self, text="Login", command=self.login)

        self.signup_button = tkinter.Button(
            self,text="Signup", command=signup_command
        )

        # Placing widgets on the screen
        self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.signup_button.grid(row=4, column=0, columnspan=2)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        authentification = Authentification()

        (ok, message) = authentification.authentifier(username, password)
        
        if(ok):
            self.success_command()
        else: 
            messagebox.showerror(title="Error", message=message)


    
    

    

    

