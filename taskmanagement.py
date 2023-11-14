import tkinter as tk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk
import os
class TaskManagementPage:
    def __init__(self, root, user, databaseConnection):
        self.root = root
        self.databaseConnection = databaseConnection
        self.databaseConnection.connect()
        self.username = user
        
        query = "select * from user where UserName = \""+self.username+"\""
        exe = self.databaseConnection.execute_query(query)
        self.full_name = exe[0][1] + " " + exe[0][2]
        
        self.root.title("To Do Application")
        
        self.root.geometry("600x600")
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.add_img = ImageTk.PhotoImage(Image.open(os.path.join(r"C:\Srikanth Bussa\OC-GRAD\OOSE\Final-project-OG\Project\Project\\add.png")).resize((280, 150), Image.LANCZOS))
        self.edit_img = ImageTk.PhotoImage(Image.open("C:\Srikanth Bussa\OC-GRAD\OOSE\Final-project-OG\Project\Project\edit.png").resize((280, 150), Image.LANCZOS))
        self.delete_img = ImageTk.PhotoImage(Image.open("C:\Srikanth Bussa\OC-GRAD\OOSE\Final-project-OG\Project\Project\delete.png").resize((280, 150), Image.LANCZOS))
        self.view_img = ImageTk.PhotoImage(Image.open("C:\Srikanth Bussa\OC-GRAD\OOSE\Final-project-OG\Project\Project\\view.png").resize((280, 150), Image.LANCZOS))
        
        self.frame1 = tk.Frame(root, width=600, height=200)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        
        self.frame2 = tk.Frame(root, width=600, height=300)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        
        self.frame3 = tk.Frame(root, width=600, height=100)
        self.frame3.grid(row=2, column=0, sticky="nsew")


        self.t1 = tk.Canvas(self.frame2, width=300, height=150)
        self.t1.grid(row=0, column=0, padx=5, pady=5)

        self.t2 = tk.Canvas(self.frame2, width=300, height=150)
        self.t2.grid(row=0, column=1, padx=5, pady=5)

        self.t3 = tk.Canvas(self.frame2, width=300, height=150)
        self.t3.grid(row=1, column=0, padx=5, pady=5)
        
        self.t4 = tk.Canvas(self.frame2, width=300, height=150)
        self.t4.grid(row=1, column=1, padx=5, pady=5)

        
        self.name_label = tk.Label(self.frame1, text="Hi, "+self.full_name+". Welcome to Task Management", font = font.Font(size=16, weight="bold"))
        self.name_label.pack(pady=10)
        
        self.b1 = tk.Button(self.t1, text="Create Task", image=self.add_img, compound=tk.BOTTOM, command=self.add_task, font = font.Font(weight="bold"))
        self.b1.pack(expand=True)

        self.b2 = tk.Button(self.t2, text="Edit Task", image=self.edit_img, compound=tk.BOTTOM, command=self.edit_task, font = font.Font(weight="bold"))
        self.b2.pack(expand=True)

        self.b3 = tk.Button(self.t3, text="Delete Task", image=self.delete_img, compound=tk.BOTTOM, command=self.delete_task, font = font.Font(weight="bold"))
        self.b3.pack(expand=True)

        self.b4 = tk.Button(self.t4, text="View Task", image=self.view_img, compound=tk.BOTTOM, command=self.view_task, font = font.Font(weight="bold"))
        self.b4.pack(expand=True)
        
        self.blog = tk.Button(self.frame3, text="Logout", command=self.log_out, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(pady = 20)
        
    def add_task(self):
        from addtask import AddTaskPage
        self.root.destroy()
        addtask_page = tk.Tk()
        AddTaskPage(addtask_page, self.username, self.databaseConnection)
        addtask_page.mainloop()
        
    def edit_task(self):
        from edittask import EditTaskPage
        self.root.destroy()
        edittask_page = tk.Tk()
        EditTaskPage(edittask_page, self.username, self.databaseConnection)
        edittask_page.mainloop()
        
    def delete_task(self):
        from deletetask import DeleteTaskPage
        self.root.destroy()
        deltask_page = tk.Tk()
        DeleteTaskPage(deltask_page, self.username, self.databaseConnection)
        deltask_page.mainloop()
        
    def view_task(self):
        from viewtask import ViewTaskPage
        self.root.destroy()
        viewtask_page = tk.Tk()
        ViewTaskPage(viewtask_page, self.username, self.databaseConnection)
        viewtask_page.mainloop()
        
    def log_out(self):
        from login import LoginPage
        self.root.destroy()
        login_page = tk.Tk()
        LoginPage(login_page, self.databaseConnection)
        login_page.mainloop()
