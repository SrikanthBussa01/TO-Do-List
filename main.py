import tkinter as tk

if __name__ == "__main__":
    from databaseconnection import DatabaseConnection
    from login import LoginPage
    dbc = DatabaseConnection('localhost', 'root', '123456789', 'TODO')
    root = tk.Tk()
    login_page = LoginPage(root, dbc)
    root.mainloop()