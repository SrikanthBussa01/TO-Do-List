import tkinter as tk
from tkinter import messagebox
from tkinter import font

class LoginPage:
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
        self.wel_label = tk.Label(self.frame1, text="Login to Create/Manage Tasks",font = font.Font(size=16))
        self.wel_label.pack(pady=10)
        
        
        self.frame2 = tk.Frame(root, width=600, height=300)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        
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
        
        self.login_button = tk.Button(self.frame3, text="Login", command=self.validate_login, font = font.Font(size = 10,weight="bold"))
        self.login_button.pack(pady=10)
        
        self.signup_button = tk.Button(self.frame3, text="New User? Sign Up", command=self.sign_up, font = font.Font(size = 10,weight="bold"))
        self.signup_button.pack(pady=10)

    def validate_login(self):
        from taskmanagement import TaskManagementPage
        username = self.username_entry.get()
        password = self.password_entry.get()
        query = "select * from user where UserName = \""+username+"\" and Password = \""+ password+"\""
        exe = self.databaseConnection.execute_query(query)
        if(len(exe) == 1):
            messagebox.showinfo("Login Successful", "Welcome! " + exe[0][1] + " " + exe[0][2])
            self.root.destroy()
            taskmgmt_page = tk.Tk()
            TaskManagementPage(taskmgmt_page, username, self.databaseConnection)
            taskmgmt_page.mainloop()
        else:
            messagebox.showerror("Login Error", "Invalid username or password. Please try again.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
    
    def sign_up(self):
        from signup import SignUpPage
        self.root.destroy()
        signup_page = tk.Tk()
        SignUpPage(signup_page, self.databaseConnection)
        signup_page.mainloop()