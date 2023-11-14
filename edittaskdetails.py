import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkcalendar import Calendar
from datetime import date
from datetime import datetime

class EditPage:
    def __init__(self, root, user, task, databaseConnection):
        self.root = root
        self.databaseConnection = databaseConnection
        self.databaseConnection.connect()
        self.taskid = task
        self.username = user
        
        query = "select Title,Description,Status,Priority,Date from task where TaskID = "+str(self.taskid)
        exe = self.databaseConnection.execute_query(query)
        
        self.root.title("To Do Application")
        
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
        
        self.wel_label = tk.Label(self.frame1, text="Edit Task Details",font = font.Font(size=16, weight="bold"))
        self.wel_label.pack(pady=10)
        
        self.date_label = tk.Label(self.frame2, text="Select Date",font = font.Font(size=10))
        self.date_label.pack(pady=7)
        
        self.f = tk.Frame(self.frame2)
        self.f.pack(side=tk.TOP, pady=7)
        
        self.date_entry = tk.Entry(self.f, width=12)
        self.date_entry.pack(side=tk.LEFT)
        self.date_entry.insert(0,exe[0][4])
        
        self.cal_button = tk.Button(self.f, text="Calendar", command  =self.calendar,font = font.Font(size=10))
        self.cal_button.pack(side=tk.LEFT)
        
        self.selected_date = tk.StringVar()
        
        self.title_label = tk.Label(self.frame2, text="Title",font = font.Font(size=10))
        self.title_label.pack(pady=7)
        self.title_entry = tk.Entry(self.frame2, width = 40)
        self.title_entry.pack(pady=7)
        self.title_entry.insert(0,exe[0][0])

        self.desc_label = tk.Label(self.frame2, text="Description",font = font.Font(size=10))
        self.desc_label.pack(pady=7)
        self.desc_entry = tk.Entry(self.frame2, width = 40)
        self.desc_entry.pack(pady=7)
        self.desc_entry.insert(0,exe[0][1])
        
        self.status_label = tk.Label(self.frame2, text="Status",font = font.Font(size=10))
        self.status_label.pack(pady=7)
        
        self.f1 = tk.Frame(self.frame2)
        self.f1.pack(side=tk.TOP, pady=7)
        
        self.select_status = tk.StringVar(value = exe[0][2])

        self.s1 = tk.Radiobutton(self.f1, text="To Do", variable = self.select_status, value="To Do",font = font.Font(size=10))
        self.s1.pack(side=tk.LEFT) 

        self.s2 = tk.Radiobutton(self.f1, text="Ongoing", variable=self.select_status, value="Ongoing",font = font.Font(size=10))
        self.s2.pack(side=tk.LEFT)

        self.s3 = tk.Radiobutton(self.f1, text="Completed", variable=self.select_status, value="Completed",font = font.Font(size=10))
        self.s3.pack(side=tk.LEFT)
        
        self.priority_label = tk.Label(self.frame2, text="Priority",font = font.Font(size=10))
        self.priority_label.pack(pady=7)
        
        self.f2 = tk.Frame(self.frame2)
        self.f2.pack(side=tk.TOP, pady=7)
        
        self.select_priority = tk.StringVar(value = exe[0][3])

        self.p1 = tk.Radiobutton(self.f2, text="Low", variable = self.select_priority, value="Low",font = font.Font(size=10))
        self.p1.pack(side=tk.LEFT) 

        self.p2 = tk.Radiobutton(self.f2, text="Medium", variable = self.select_priority, value="Medium",font = font.Font(size=10))
        self.p2.pack(side=tk.LEFT) 

        self.p3 = tk.Radiobutton(self.f2, text="High", variable = self.select_priority, value="High",font = font.Font(size=10))
        self.p3.pack(side=tk.LEFT) 
        
        self.f3 = tk.Frame(self.frame3)
        self.f3.pack(side=tk.TOP, pady=7)
        
        self.blog = tk.Button(self.f3, text="<< Back", command=self.back, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT,padx = 15) 
        
        self.blog = tk.Button(self.f3, text="Edit Task", command=self.edit, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT, padx = 15) 
        
        self.blog = tk.Button(self.f3, text="Logout", command=self.log_out, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT, padx = 15) 
        
    
    def calendar(self):
        top = tk.Toplevel(self.root)
        today = date.today()
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', date=today)
        cal.pack(padx=10, pady=10)
        cal.bind("<<CalendarSelected>>", lambda event: self.update_date(cal, top))

    def update_date(self, cal, top):
        selected_date = cal.get_date()
        self.selected_date.set(selected_date)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date)
        top.destroy()
    
    def edit(self):
        from taskmanagement import TaskManagementPage
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        status = self.select_status.get()
        priority = self.select_priority.get()
        dat = self.date_entry.get()
        if(len(title) == 0 or len(desc) == 0 or len(dat)==0 or status=="None" or priority == "None"):
            messagebox.showerror("Edit Task Error", "All the Fields in Edit Task Page should not be empty. Please fill up all fields.")
        elif(len(title)>50):
            messagebox.showerror("Edit Task Error", "Title cannot be more than 50 characters.")
        elif(len(desc)>200):
            messagebox.showerror("Edit Task Error", "Description cannot be more than 200 characters.")
        else:
            try:
                dat_valid = datetime.strptime(dat,'%Y-%m-%d' )
                query = "update task set Title = %s, Description = %s, Status = %s, Priority = %s, Date = %s where TaskID = "+str(self.taskid)
                data = (title,desc,status,priority,dat)
                self.databaseConnection.execute_query(query,data)
                messagebox.showinfo("Edit Task Status", "Task Edited successfully. Redirecting to Task Management Page to create or manage tasks...")
                self.root.destroy()
                taskmgmt_page = tk.Tk()
                TaskManagementPage(taskmgmt_page, self.username, self.databaseConnection)
                taskmgmt_page.mainloop()
            except ValueError:
                messagebox.showerror("Edit Task Error", "Date should be of yyyy/mm/dd format. Please input correct date")

    def back(self):
        from edittask import EditTaskPage
        self.root.destroy()
        edittask_page = tk.Tk()
        EditTaskPage(edittask_page, self.username, self.databaseConnection)
        edittask_page.mainloop()
    
    def log_out(self):
        from login import LoginPage
        self.root.destroy()
        login_page = tk.Tk()
        LoginPage(login_page, self.databaseConnection)
        login_page.mainloop()