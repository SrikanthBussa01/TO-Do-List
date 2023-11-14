import tkinter as tk
from tkinter import messagebox
from tkinter import font

class SignUpPage:
    def __init__(self, root, databaseConnection):
        self.root = root
        self.databaseConnection = databaseConnection
        self.databaseConnection.connect()
        
        self.root.title("To Do Application")
        
        self.root.geometry("600x600")
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.frame1 = tk.Frame(root, width=600, height=200)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        
        self.wel_label = tk.Label(self.frame1, text="Welcome To Task Management",font = font.Font(size=20, weight="bold"))
        self.wel_label.pack(pady=10)
        self.wel_label = tk.Label(self.frame1, text="Signup to Create/Manage Tasks",font = font.Font(size=16))
        self.wel_label.pack(pady=10)
        
        self.frame2 = tk.Frame(root, width=600, height=300)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        
        self.firstname_label = tk.Label(self.frame2, text="First Name",font = font.Font(size=10))
        self.firstname_label.pack(pady=10)
        self.firstname_entry = tk.Entry(self.frame2)
        self.firstname_entry.pack(pady=10)
        
        self.lastname_label = tk.Label(self.frame2, text="Last Name",font = font.Font(size=10))
        self.lastname_label.pack(pady=10)
        self.lastname_entry = tk.Entry(self.frame2)
        self.lastname_entry.pack(pady=10)
        
        self.username_label = tk.Label(self.frame2, text="User Name",font = font.Font(size=10))
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.frame2)
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self.frame2, text="Password",font = font.Font(size=10))
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.frame2, show="*")
        self.password_entry.pack(pady=10)
        
        self.frame3 = tk.Frame(root, width=600, height=100)
        self.frame3.grid(row=2, column=0, sticky="nsew")
        
        self.signup_button = tk.Button(self.frame3, text="Sign Up", command=self.validate_username, font = font.Font(size = 10,weight="bold"))
        self.signup_button.pack(pady=10)
        
        self.login_button = tk.Button(self.frame3, text="Back To Login Page", command=self.log_in, font = font.Font(size = 10,weight="bold"))
        self.login_button.pack(pady=10)

    def validate_username(self):
        from login import LoginPage
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if(len(firstname) == 0 or len(lastname) == 0 or len(username) == 0 or len(password) == 0):
            messagebox.showerror("Sign Up Failed", "All the Fields in Sign Up form should not be empty. Please fill up all fields.")
            
        elif(len(firstname) < 4 or len(lastname) < 4 or len(username) < 4 or len(password) < 4):
            messagebox.showerror("Sign Up Failed", "All the Fields in Sign Up form should be atleast 4 characters")
        else:
            query = "select * from user where UserName = \""+username+"\""
            exe = self.databaseConnection.execute_query(query)
            if(len(exe) == 1):
                messagebox.showerror("Sign Up Failed", "User Name already taken. Please try with different UserName.")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            else:
                query = "insert into user(FirstName,LastName,UserName,Password) values (%s, %s, %s, %s)"
                data = (firstname, lastname, username, password)
                self.databaseConnection.execute_query(query,data)
                messagebox.showinfo("Sign Up Successful", "Hello "+firstname+" "+lastname+". You've sign up successfully. Redirecting to Login Page to login to create or manage tasks...")
                self.root.destroy()
                login_page = tk.Tk()
                LoginPage(login_page, self.databaseConnection)
                login_page.mainloop()

    def log_in(self):
        from login import LoginPage
        self.root.destroy()
        login_page = tk.Tk()
        LoginPage(login_page, self.databaseConnection)
        login_page.mainloop()