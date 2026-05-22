# Import Module
from tkinter import *
from tkinter import ttk
import sqlite3

DATABASE = "Databases"

crueent_user = -1
creent_user_type = "n"
creent_famly = ""

# Create root window
root = Tk()

# Sets Up Page secsions
bar = Frame(root)
page = Frame(root)

def sql_base(From):
    return(f"SELECT {From}_ID, Name FROM {From}")

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
    global creent_famly
    creent_famly = ""
    crueent_user = -1
    creent_user_type = "n"
    bar.grid_forget()
    log_in_page()

#Login page
if 1 == 1:
    def change_user(x):
        with sqlite3.connect(DATABASE) as db:
            currser = db.cursor()
            qrl = f"""SELECT User_ID, User_type, Famly 
                FROM User WHERE Name = "{x}" """
            currser.execute(qrl)
            info = currser.fetchall()
            global crueent_user
            global creent_user_type
            global creent_famly
            creent_famly = info[0][2]
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

def sql_join(id, to, ect):
    with sqlite3.connect(DATABASE) as db:
        currser = db.cursor()
        qrl = f"""SELECT Stu_in_{to}.{to}_ID, {to}.Name
                FROM Stu_in_{to}
                join {to} on Stu_in_{to}.{to}_ID = {to}.{to}_ID
                Where Stu_in_{to}.User_ID = {id} {ect} """
        currser.execute(qrl)
        return(currser.fetchall())

#Home Page
def home_page():
    clear_page()
    desternaion = home_page
    root.title("Home")
    links = []
    global page
    global crueent_user
    global creent_user_type
    global creent_famly
    if creent_user_type == "s":
        links = sql_join(crueent_user, "Class", "")
        desternaion = class_page
    elif creent_user_type == "t":
        with sqlite3.connect(DATABASE) as db:
            currser = db.cursor()
            qrl = f""" {sql_base("Class")} WHERE User_ID = {crueent_user}"""
            currser.execute(qrl)  
            links = currser.fetchall()  
            desternaion = class_page
    elif creent_user_type == "c":
        with sqlite3.connect(DATABASE) as db:
            currser = db.cursor()
            qrl = f"""{sql_base("User")} WHERE Famly = "{creent_famly}"
                       AND User_type = "s" """
            currser.execute(qrl)  
            links = currser.fetchall()  
            desternaion = sudent_page
    for x in range (len(links)):
        link = Button(page, text= links[x][1], 
                    command=lambda c = x :(desternaion(links[c][0],links[c][1])))
        link.grid()
    reload_page()

def class_page(c_id, c_name):
    clear_page()
    root.title("Class" + c_name)
    studen = Button(page, text = "Studen 1", command=lambda:(sudent_page("1")))
    studen.grid()
    projects =Button(page, text = "Project 1", command=lambda:(project_page("1")))
    projects.grid()
    reload_page()

def sudent_page(s_id, s_name):
    clear_page()
    global crueent_user
    global creent_user_type
    root.title("Sudent" + s_name)
    if creent_user_type == "c":
        classes = sql_join(s_id, "Class", "")
    elif creent_user_type == "t":
        classes = sql_join(s_id, "Class", f"AND Class.User_ID = {crueent_user}")
    for x in range (len(classes)):
        class_link = Button(page, text= classes[x][1], 
            command=lambda c = x :(class_page(classes[c][0],classes[c][1])))
        class_link.grid(column=x, row=0)
        with sqlite3.connect(DATABASE) as db:
            currser = db.cursor()
            qrl = f"""{sql_base("Project")} WHERE Class_ID = {classes[x][0]}"""
            print(qrl)
            currser.execute(qrl)  
            projects = currser.fetchall()
            for y in range (len(projects)):
                projects = Button(page, text= projects[y][1], 
                    command=lambda c = y :(class_page(projects[c][0],projects[c][1])))
                projects.grid(column=x, row=(y+1))
    reload_page()

def project_page(p_id, p_name):
    clear_page()
    root.title("Poject" + p_name)
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