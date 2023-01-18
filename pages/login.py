import tkinter
from tkinter import messagebox, Frame

def default_success_command():
        print("success")

class LoginFrame(tkinter.Frame): 

    

    def __init__(self,container, success_command= default_success_command):
        super().__init__(container)

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
            self, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=self.login)

        # Placing widgets on the screen
        self.login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)

        self.success_command= success_command

    def login(self):
        username = "motez"
        password = "baccouch"
        if self.username_entry.get()==username and self.password_entry.get()==password:
            messagebox.showinfo(title="Login Success", message="You successfully logged in.")
            self.success_command()

        else:
            messagebox.showerror(title="Error", message="Invalid login.")


    
    

    

    

