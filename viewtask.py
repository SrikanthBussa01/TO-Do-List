import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkcalendar import Calendar
from datetime import date
from datetime import datetime, timedelta
from functools import partial

class ViewTaskPage:
    def __init__(self, root, user, databaseConnection):
        self.root = root
        self.databaseConnection = databaseConnection
        self.databaseConnection.connect()
        self.username = user
        
        self.data = []
        
        query = "select UserID from user where UserName = \""+self.username+"\""
        exe = self.databaseConnection.execute_query(query)
        self.userid = exe[0][0]
        
        query = "select TaskID, Title,Description,Status,Priority,Date from task where Date = \""+str(datetime.now().date().strftime("%Y-%m-%d"))+"\" and UserID = "+str(self.userid)
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
        
        self.wel_label = tk.Label(self.frame1, text="View Task",font = font.Font(size=16, weight="bold"))
        self.wel_label.pack(pady=15)
        
        self.f = tk.Frame(self.frame1)
        self.f.pack(side=tk.TOP, pady=7)
        
        self.date_label = tk.Label(self.f, text="Select Date",font = font.Font(size=10))
        self.date_label.pack(side=tk.LEFT)
        
        self.date_entry = tk.Entry(self.f, width=12)
        self.date_entry.pack(side=tk.LEFT)
        
        self.selected_date = tk.StringVar()
        
        self.cal_button = tk.Button(self.f, text="Calendar", command  = self.calendar,font = font.Font(size=10))
        self.cal_button.pack(side=tk.LEFT)
        
        self.select_view = tk.IntVar(value = 0)
        
        self.f1 = tk.Frame(self.frame1)
        self.f1.pack(side=tk.TOP, pady=7)
        
        self.view_label = tk.Label(self.f1, text="Select View",font = font.Font(size=10))
        self.view_label.pack(side=tk.LEFT)
        
        self.v1 = tk.Radiobutton(self.f1, text="Date", variable = self.select_view, value=1,font = font.Font(size=10))
        self.v1.pack(side=tk.LEFT) 

        self.v2 = tk.Radiobutton(self.f1, text="Weekly", variable=self.select_view, value=2,font = font.Font(size=10))
        self.v2.pack(side=tk.LEFT)

        self.v3 = tk.Radiobutton(self.f1, text="Monthly", variable=self.select_view, value=3,font = font.Font(size=10))
        self.v3.pack(side=tk.LEFT)
        
        self.v4 = tk.Radiobutton(self.f1, text="Yearly", variable=self.select_view, value=4,font = font.Font(size=10))
        self.v4.pack(side=tk.LEFT)
        
        self.view_button = tk.Button(self.frame1, text="View", command  = self.view,font = font.Font(size=10))
        self.view_button.pack(pady=10)
        
        if(len(exe)>0):
            self.wel_label = tk.Label(self.frame2, text="Today Tasks",font = font.Font(size=18, weight="bold"))
            self.wel_label.pack(pady=15)
            
            self.canvas = tk.Canvas(self.frame2)
            self.canvas.pack(side="left", fill="both", expand=True)
        
            self.scrollbar_y = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
            self.scrollbar_y.pack(side="right", fill="y")
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
            self.scrollbar_x = tk.Scrollbar(self.frame2, orient="horizontal", command=self.canvas.xview)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        
            self.gp = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.gp, anchor="nw")
        
            self.columns = ["Title", "Description", "Status", "Priority", "Date", "View"]
            
            for i in range(len(self.columns)):
                label = tk.Label(self.gp, text=self.columns[i],width = 20, height= 3, font = font.Font(size = 10,weight="bold"), borderwidth=1, relief="solid",  wraplength = 100)
                label.grid(row=0, column=i)
        
            for i in range(len(exe)):
                for j in range(len(self.columns)):
                    k=j
                    if(j==5):
                        button = tk.Button(self.gp, text="View Full Details",width = 19,font = font.Font(size=10), height= 3, command=partial(self.viewtask, self.data[i][0]), borderwidth=1, relief="solid")
                        button.grid(row=i+1, column=j)
                    else:
                        label = tk.Label(self.gp, text=str(self.data[i][k+1]),width = 20,font = font.Font(size=10), height= 3, borderwidth=1, relief="solid", wraplength = 140)
                        label.grid(row=i+1, column=j)
            
            self.gp.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        else:
            self.wel_label = tk.Label(self.frame2, text="No Pending Tasks for Today",font = font.Font(size=20, weight="bold"))
            self.wel_label.pack(pady=15)
        
        
        self.f2 = tk.Frame(self.frame3)
        self.f2.pack(side=tk.TOP, pady=7)
        
        self.blog = tk.Button(self.f2, text="<< Back", command=self.back, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT,padx = 15)  
        
        self.blog = tk.Button(self.f2, text="Logout", command=self.log_out, font = font.Font(size = 10,weight="bold"))
        self.blog.pack(side=tk.LEFT, padx = 15) 
    
    def view(self):
        userid = self.userid
        dat = self.date_entry.get()
        sel_view = self.select_view.get()
        if(len(dat)==0 and sel_view == 0):
            messagebox.showerror("View Task Error", "Date and Select View Option cannot be empty. Please Select Date and View Option")
        elif(len(dat)==0):
            messagebox.showerror("View Task Error", "Date cannot be empty. Please Select Date")
        elif(sel_view == 0):
            messagebox.showerror("View Task Error", "Select View Option cannot be empty. Please Select View Option")
        else:
            try:
                dat_valid = datetime.strptime(dat,'%Y-%m-%d' )
                week = int(dat_valid.strftime('%U'))
                year = int(dat_valid.strftime('%Y'))
                month = int(dat_valid.strftime('%m'))
                day = int(dat_valid.strftime('%d'))
                start_date = dat_valid - timedelta(days=dat_valid.weekday())
                end_date = start_date + timedelta(days=6)
                if(sel_view == 1):
                    query = "select TaskID, Title,Description,Status,Priority,Date from task where Date = \""+str(dat)+"\" and UserID = "+str(self.userid)+" order by Date asc"
                    exe = self.databaseConnection.execute_query(query)
                    self.data = exe
                elif(sel_view == 2):
                    query = "select TaskID, Title,Description,Status,Priority,Date from task where Date between  \""+str(start_date.strftime("%Y-%m-%d"))+"\" and  \""+str(end_date.strftime("%Y-%m-%d"))+"\" and UserID = "+str(self.userid)+" order by Date asc"
                    exe = self.databaseConnection.execute_query(query)
                    self.data = exe
                elif(sel_view == 3):
                    query = "select TaskID, Title,Description,Status,Priority,Date from task where MONTH(Date) = "+str(month)+" and YEAR(Date) ="+str(year)+" and UserID = "+str(self.userid)+" order by Date asc"
                    exe = self.databaseConnection.execute_query(query)
                    self.data = exe
                else:
                    query = "select TaskID, Title,Description,Status,Priority,Date from task where YEAR(Date) ="+str(year)+" and UserID = "+str(self.userid)+" order by Date asc"
                    exe = self.databaseConnection.execute_query(query)
                    self.data = exe
                for widget in self.frame2.winfo_children():
                    widget.destroy()
                if(len(exe)>0):
                    self.wel_label = tk.Label(self.frame2, text="Tasks",font = font.Font(size=18, weight="bold"))
                    self.wel_label.pack(pady=15)
            
                    self.canvas = tk.Canvas(self.frame2)
                    self.canvas.pack(side="left", fill="both", expand=True)
        
                    self.scrollbar_y = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
                    self.scrollbar_y.pack(side="right", fill="y")
                    self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
                    self.scrollbar_x = tk.Scrollbar(self.frame2, orient="horizontal", command=self.canvas.xview)
                    self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
                    self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        
                    self.gp = tk.Frame(self.canvas)
                    self.canvas.create_window((0, 0), window=self.gp, anchor="nw")
        
                    self.columns = ["Title", "Description", "Status", "Priority", "Date", "View"]
            
                    for i in range(len(self.columns)):
                        label = tk.Label(self.gp, text=self.columns[i],width = 20, height= 3, font = font.Font(size = 10,weight="bold"), borderwidth=1, relief="solid",  wraplength = 100)
                        label.grid(row=0, column=i)
        
                        for i in range(len(exe)):
                            for j in range(len(self.columns)):
                                k=j
                                if(j==5):
                                    button = tk.Button(self.gp, text="View Full Details",width = 19,font = font.Font(size=10), height= 3, command=partial(self.viewtask, self.data[i][0]), borderwidth=1, relief="solid")
                                    button.grid(row=i+1, column=j)
                                else:
                                    label = tk.Label(self.gp, text=str(self.data[i][k+1]),width = 20,font = font.Font(size=10), height= 3, borderwidth=1, relief="solid", wraplength = 140)
                                    label.grid(row=i+1, column=j)
            
                    self.gp.update_idletasks()
                    self.canvas.config(scrollregion=self.canvas.bbox("all"))
                else:
                    self.wel_label = tk.Label(self.frame2, text="No Tasks Found",font = font.Font(size=20, weight="bold"))
                    self.wel_label.pack(pady=15)
            except ValueError:
                messagebox.showerror("View Task Error", "Date should be of yyyy/mm/dd format. Please input correct date")
        
    def viewtask(self, tid):
        query = "select Title,Description,Status,Priority,Date from task where TaskID = "+str(tid)
        exe = self.databaseConnection.execute_query(query)
        messagebox.showinfo("Task Details", "Title : "+exe[0][0]+"\nDescription : "+exe[0][1]+"\nStatus : "+exe[0][2]+"\nPriority : "+exe[0][3]+"\nDate : "+str(exe[0][4]))
    
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