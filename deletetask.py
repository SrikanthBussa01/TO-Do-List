import tkinter as tk
from tkinter import messagebox
from tkinter import font
from functools import partial

class DeleteTaskPage:
    def __init__(self, root, user, databaseConnection):
        self.root = root
        self.databaseConnection = databaseConnection
        self.databaseConnection.connect()
        self.username = user
        
        query = "select UserID from user where UserName = \""+self.username+"\""
        exe = self.databaseConnection.execute_query(query)
        self.userid = exe[0][0]
        
        query = "select TaskID, Title,Description,Status,Priority,Date from task where UserID = "+str(self.userid)+" order by Date asc"
        exe = self.databaseConnection.execute_query(query)
        self.data = exe
        
        self.root.title("To Do Application")
        
        self.root.geometry("600x600")
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.frame1 = tk.Frame(root, width=600, height=200)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        
        self.frame2 = tk.Frame(root, width=600, height=300)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        
        self.frame3 = tk.Frame(root, width=600, height=100)
        self.frame3.grid(row=2, column=0, sticky="nsew")
        
        self.wel_label = tk.Label(self.frame1, text="Delete Task",font = font.Font(size=16, weight="bold"))
        self.wel_label.pack(pady=15)
        self.wel_label = tk.Label(self.frame1, text="Select Task to Delete", font = font.Font(size = 10,weight="bold"))
        self.wel_label.pack(pady=10)
        
        self.select_task = tk.IntVar(value = 0)
        if(len(self.data)>0):
            self.canvas = tk.Canvas(self.frame2)
            self.canvas.pack(side="left", fill="both", expand=True)
        
            self.scrollbar_y = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
            self.scrollbar_y.pack(side="right", fill="y")
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
            self.scrollbar_x = tk.Scrollbar(self.frame2, orient="horizontal", command=self.canvas.xview)
            self.scrollbar_x.pack(side="bottom", fill="x")
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        
            self.gp = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.gp, anchor="nw")
        
            self.columns = ["Select Task", "Title", "Description", "Status", "Priority", "Date", "View"]
            for i in range(len(self.columns)):
                label = tk.Label(self.gp, text=self.columns[i],width = 20, height= 3, font = font.Font(size = 10,weight="bold"), borderwidth=1, relief="solid",  wraplength = 100)
                label.grid(row=0, column=i)
        
            for i in range(len(exe)):
                for j in range(len(self.columns)):
                    if(j==0):
                        radio_button = tk.Radiobutton(self.gp, variable = self.select_task,font = font.Font(size=10),width = 17, height= 3, value=self.data[i][j], borderwidth=1, relief="solid")
                        radio_button.grid(row=i+1, column=j)
                    elif(j==6):
                        button = tk.Button(self.gp, text="View Full Details",width = 19,font = font.Font(size=10), height= 3, command=partial(self.view, self.data[i][0]), borderwidth=1, relief="solid")
                        button.grid(row=i+1, column=j)
                    else:
                        label = tk.Label(self.gp, text=str(self.data[i][j]),width = 20,font = font.Font(size=10), height= 3, borderwidth=1, relief="solid", wraplength = 140)
                        label.grid(row=i+1, column=j)
            
            self.gp.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        else:
            self.wel_label = tk.Label(self.frame2, text="No Tasks Found",font = font.Font(size=20, weight="bold"))
            self.wel_label.pack(pady=15)
        
        self.f = tk.Frame(self.frame3)
        self.f.pack(side=tk.TOP, pady=7)
        
        self.blog = tk.Button(self.f, text="<< Back", command=self.back, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT,padx = 15) 
        
        self.blog = tk.Button(self.f, text="Delete Task", command=self.delete, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT, padx = 15) 
        
        self.blog = tk.Button(self.f, text="Logout", command=self.log_out, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT, padx = 15) 
    
    def view(self, tid):
        query = "select Title,Description,Status,Priority,Date from task where TaskID = "+str(tid)
        exe = self.databaseConnection.execute_query(query)
        messagebox.showinfo("Task Details", "Title : "+exe[0][0]+"\nDescription : "+exe[0][1]+"\nStatus : "+exe[0][2]+"\nPriority : "+exe[0][3]+"\nDate : "+str(exe[0][4]))
    
    def delete(self):
        from taskmanagement import TaskManagementPage
        tid = self.select_task.get()
        if(tid>0):
            response = messagebox.askyesno("Delete Task", "Are you sure you want to delete the task?")
            if response:
                query = "delete from task where TaskID = %s"
                data = (tid,)
                self.databaseConnection.execute_query(query,data)
                messagebox.showinfo("Delete Task Status", "Task Deleted successfully. Redirecting to Task Management Page to create or manage tasks...")
                self.root.destroy()
                taskmgmt_page = tk.Tk()
                TaskManagementPage(taskmgmt_page, self.username, self.databaseConnection)
                taskmgmt_page.mainloop()
            else:
                messagebox.showinfo("Delete Task Status", "Task was not deleted. Redirecting to Delete task page to select correct task to delete")
                self.root.destroy()
                deltask_page = tk.Tk()
                DeleteTaskPage(deltask_page, self.username, self.databaseConnection)
                deltask_page.mainloop()
        else:
            messagebox.showerror("Delete Task Error", "You've not selected any task to delete. Select task to delete")

    def back(self):
        from taskmanagement import TaskManagementPage
        self.root.destroy()
        taskmgmt_page = tk.Tk()
        TaskManagementPage(taskmgmt_page, self.username, self.databaseConnection)
        taskmgmt_page.mainloop()
    
    def log_out(self):
        from login import LoginPage
        self.root.destroy()
        login_page = tk.Tk()
        LoginPage(login_page, self.databaseConnection)
        login_page.mainloop()