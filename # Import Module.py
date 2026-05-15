# Import Module
from tkinter import *
import sqlite3

DATABASE = "Databases"

user_id = -1
user_type = "n"

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

#Login page
if 1 == 1:
    def log_in_page():
        clear_page()
        root.title("Home")
        global page
        login_button = Button(page, text = "Log in", command=login)
        login_button.grid(column=0, row=0)
        signup_button = Button(page, text = "Sign up", command=signup)
        signup_button.grid(column=1, row=0)
        reload_page()

    def login():
        clear_page()
        #Back Button
        back_button = Button(page, text = "back", command=lambda:(log_in_page()))
        back_button.grid(column=0, row=0)
        

        

        #Input user name
        user_name_txt = Label(page, text="Username:")
        user_name_txt.grid(column=1, row=2)
        user_name_input = Entry(page, width=8)
        user_name_input.grid(column=2,row=2)
        
        #Input password
        password_txt = Label(page, text="Password:")
        password_txt.grid(column=1, row=4)
        password_input = Entry(page, width=8)
        password_input.grid(column=2,row=4)

        #Enter
        enter_button = Button(page, text="Enter",
            command=lambda:(log_in_funcion(user_name_input.get(),password_input.get())))
        enter_button.grid(column=2,row=5)
        reload_page()

    def log_in_funcion(user_name, password):
            with sqlite3.connect(DATABASE) as db:
                currser = db.cursor()
                qrl = f"""SELECT User_ID, User_type FROM User
                            WHERE Name = "{user_name}"
                            AND password = "{password}" """
                currser.execute(qrl)
                resailts = currser.fetchall()
                print(resailts)
            if len(resailts) == 0:
                incorred = Label(page, text="Username or pasword is incorred")
                incorred.grid(column=1,row=1)
            else:
                global user_id
                user_id = resailts[0][0]
                global user_type
                user_type = resailts[0][1]
                home_page()

    def signup():
        clear_page()
        #Back Button
        back_button = Button(page, text = "back", command=lambda:(log_in_page()))
        back_button.grid(column=0, row=0)

        #Input user name
        user_name_txt = Label(page, text="Username:")
        user_name_txt.grid(column=1, row=2)
        user_name_input = Entry(page, width=8)
        user_name_input.grid(column=2,row=2)

        #Input user name
        email_txt = Label(page, text="Email:")
        email_txt.grid(column=1, row=4)
        email_input = Entry(page, width=8)
        email_input.grid(column=2,row=4)

        #Input password
        password_txt = Label(page, text="Password:")
        password_txt.grid(column=1, row=6)
        password_input = Entry(page, width=8)
        password_input.grid(column=2,row=6)

        #Cheek password
        password_cheek_txt = Label(page, text="Renter Password:")
        password_cheek_txt.grid(column=1, row=8)
        password_cheek_input = Entry(page, width=8)
        password_cheek_input.grid(column=2,row=8)
        reload_page()

def home_page():
    clear_page()
    bar.grid(column=0,row=0)
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
log_in_page()
page.grid(column=0, row=1)
root.mainloop()