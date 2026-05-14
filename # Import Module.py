# Import Module
from tkinter import *
import sqlite3

DATABASE = "\\g\My Drive\School\DTSD\L3\91906 Program\L3DSTD-91906\Databases"

# Create root window
root = Tk()

# Sets Up Page secsions
bar = Frame(root)
page = Frame(root)

def clear_page():
    global page
    for widget in page.winfo_children():
        widget.destroy()
def reload_page():
    page.grid_remove()
    page.grid(column=0, row=1)

def log_in_page():
    clear_page()
    root.title("Home")
    global page
    login_button = Button(page, text = "Log in", command=login)
    login_button.grid(column=0, row=0)
    signup_button = Button(page, text = "Sign up", command=signup)
    signup_button.grid(column=0, row=0)
    reload_page()

def login():
    clear_page()

def signup():
    clear_page()

def home_page():
    clear_page()
    root.title("Home")
    global page
    tet = Button(page, text = "Class 1", command=lambda:(class_page("1")))
    tet.grid()
    reload_page()

def class_page(c_id):
    clear_page()
    root.title("Class" + c_id)
    studen = Button(page, text = "Studen 1", command=lambda:(sudent_page("1")))
    studen.grid()
    projects =Button(page, text = "Project 1", command=lambda:(project_page("1")))
    projects.grid()
    reload_page()

def sudent_page(s_id):
    clear_page()
    root.title("Sudent" + s_id)
    classes = Button(page, text = "Class 1", command=lambda:(class_page("1")))
    classes.grid()
    projects =Button(page, text = "Project 1", command=lambda:(project_page("1")))
    projects.grid()
    reload_page()

def project_page(p_id):
    clear_page()
    root.title("Poject" + p_id)
    studen = Button(page, text = "Studen 1", command=lambda:(sudent_page("1")))
    studen.grid()
    classes = Button(page, text = "Class 1", command=lambda:(class_page("1")))
    classes.grid()
    reload_page()  

# Bar Segmat
if 1==1:
    home_button = Button(bar,text="Home", command= lambda: (home_page()))
    home_button.grid(column=0,row=0)

# Open Window
home_page()
bar.grid(column=0,row=0)
page.grid(column=0, row=1)
root.mainloop()