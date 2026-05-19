# Import Module
from tkinter import *
from tkinter import ttk
import sqlite3

DATABASE = "Databases"

crueent_user = -1
creent_user_type = "n"

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

def log_out():
    global crueent_user
    global creent_user_type
    crueent_user = -1
    creent_user_type = "n"
    bar.grid_forget()
    log_in_page()

#Login page
if 1 == 1:
    def change_user(x):
        with sqlite3.connect(DATABASE) as db:
            currser = db.cursor()
            qrl = f"""SELECT User_ID, User_type FROM User
                WHERE Name = "{x}" """
            currser.execute(qrl)
            info = currser.fetchall()
            global crueent_user
            global creent_user_type
            crueent_user = info[0][0]
            creent_user_type = info[0][1]
            bar.grid(column=0,row=0)

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
            if len(resailts) == 0:
                incorred = Label(page, text="Username or pasword is incorred")
                incorred.grid(column=1,row=1)
            else:
                change_user(user_name)
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

        #Input user email
        email_txt = Label(page, text="Email:")
        email_txt.grid(column=1, row=4)
        email_input = Entry(page, width=8)
        email_input.grid(column=2,row=4)

        #Input user type
        type_txt = Label(page, text="User Type:")
        type_txt.grid(column=1, row=6)
        type_input = ttk.Combobox(page, values=["Student", "Teacher", "Caregiver"], width=8,state= "readonly")
        type_input.set("")
        type_input.grid(column=2, row=6)

        #Input password
        password_txt = Label(page, text="Password:")
        password_txt.grid(column=1, row=8)
        password_input = Entry(page, width=8)
        password_input.grid(column=2,row=8)

        #Cheek password
        password_cheek_txt = Label(page, text="Renter Password:")
        password_cheek_txt.grid(column=1, row=10)
        password_cheek_input = Entry(page, width=8)
        password_cheek_input.grid(column=2,row=10)

        enter_button = Button(page, text="Enter",
            command=lambda:(sign_up_funcion(user_name_input.get(), email_input.get(),
                                            type_input.get(), 
                                            (password_input.get(), password_cheek_input.get()))))
        enter_button.grid(column=2,row=11)
        reload_page()

        def sign_up_funcion(user_name, user_email, user_type, password):
            cheek = 0
            if password[0] == password[1]:
                cheek = cheek + 1
            else:
                wrong_password = Label(page, text="Passwords don't match")
                wrong_password.grid(column=1,row=7)
            if user_type[0] in ("T","S","C"):
                cheek = cheek + 1
            else: 
                no_type = Label(page, text="No User type selected")
                wrong_password.grid(column=1,row=5)
            with sqlite3.connect(DATABASE) as db:
                currser = db.cursor()
                for x in range(2):
                    qrl = f"""SELECT * FROM User
                            WHERE "{("Name", "Email")[x]}" = 
                            "{(user_name, user_email)[x]}" """
                    currser.execute(qrl)
                    resailts = currser.fetchall()
                    if len(resailts) == 0:
                        cheek = cheek + 1
                    else:
                        e_n_used = Label(page, text=f"{("Name", "Email")[x]} is alreddy in uses")
                        e_n_used.grid(column=1, row=(2*x +1))
                if cheek == 4:
                    qrl = f"""INSERT INTO User (Email, Name, Password, User_type, User_pic)
                             VALUES ("{user_email}", "{user_name}", "{password[0]}", "{user_type[0].lower()}", "bace.png")"""
                    currser.execute(qrl)
                    change_user(user_name)
                    home_page()

#Home Page
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
    home_button = Button(bar,text="Home", command = lambda: (home_page()))
    home_button.grid(column=0,row=0)
    log_out_button = Button(bar, text="Log Out",command = lambda: (log_out()))
    log_out_button.grid(column=1,row=0)

# Open Window
log_in_page()
page.grid(column=0, row=1)
root.mainloop()