# Import Module
from tkinter import *

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

def home():
    clear_page()
    root.title("Home")
    global page
    tet = Button(page, text = "Class 1", command=lambda:(t_class("1")))
    tet.grid()
    reload_page()

def t_class(c_id):
    clear_page()
    root.title("Class" + c_id)
    studen = Button(page, text = "Studen 1", command=lambda:(stu("1")))
    studen.grid()
    project =Button(page, text = "Project 1", command=lambda:(pro("1")))
    project.grid()
    reload_page()

def stu(s_id):
    clear_page()
    root.title("Sudent" + s_id)
    classes = Button(page, text = "Class 1", command=lambda:(t_class("1")))
    classes.grid()
    project =Button(page, text = "Project 1", command=lambda:(pro("1")))
    project.grid()
    reload_page()

def pro(p_id):
    clear_page()
    root.title("Poject" + p_id)
    studen = Button(page, text = "Studen 1", command=lambda:(stu("1")))
    studen.grid()
    classes = Button(page, text = "Class 1", command=lambda:(t_class("1")))
    classes.grid()
    reload_page()  

# Bar Segmat
if 1==1:
    home_button = Button(bar,text="Home", command= lambda: (home()))
    home_button.grid(column=0,row=0)

# Open Window
home()
bar.grid(column=0,row=0)
page.grid(column=0, row=1)
root.mainloop()