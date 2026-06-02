# Import Module
from tkinter import *
from tkinter import ttk
import sqlite3

DATABASE = "Databases"

current_user = -1
current_user_type = "n"
current_family = ""

# Create root window
root = Tk()

# Sets Up Page sections
bar = Frame(root)
page = Frame(root)

def sql_join(id, to, ect):
    with sqlite3.connect(DATABASE) as db:
        curser = db.cursor()
        qrl = f"""SELECT Stu_in_{to}.{to}_ID, {to}.Name
                FROM Stu_in_{to}
                join {to} on Stu_in_{to}.{to}_ID = {to}.{to}_ID
                Where Stu_in_{to}.User_ID = {id} {ect} """
        curser.execute(qrl)
        return(curser.fetchall())

def sql_base(From):
    return(f"SELECT {From}_ID, Name FROM {From}")

# Change Page
if 1 == 1:
    def clear_page():
        global page
        for widget in page.winfo_children():
            widget.destroy()
    def reload_page():
        page.grid_remove()
        page.grid(column=0, row=1)

# Login/out
if 1 == 1:
    def change_user(x):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT User_ID, User_type, family 
                FROM User WHERE Name = "{x}" """
            curser.execute(qrl)
            info = curser.fetchall()
            global current_user, current_user_type, current_family
            current_family = info[0][2]
            current_user = info[0][0]            
            current_user_type = info[0][1]
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
            command=lambda:(log_in_function(user_name_input.get(),password_input.get())))
        enter_button.grid(column=2,row=5)
        reload_page()

    def log_in_function(user_name, password):
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                qrl = f"""SELECT User_ID, User_type FROM User
                            WHERE Name = "{user_name}"
                            AND password = "{password}" """
                curser.execute(qrl)
                results = curser.fetchall()
            if len(results) == 0:
                incorrect = Label(page, text="Username or password is incorrect")
                incorrect.grid(column=1,row=1)
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
            command=lambda:(sign_up_function(user_name_input.get(), email_input.get(),
                                            type_input.get(), 
                                            (password_input.get(), password_cheek_input.get()))))
        enter_button.grid(column=2,row=11)
        reload_page()

    def sign_up_function(user_name, user_email, user_type, password):
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
            no_type.grid(column=1,row=5)
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            for x in range(2):
                qrl = f"""SELECT * FROM User
                        WHERE "{("Name", "Email")[x]}" = 
                        "{(user_name, user_email)[x]}"; """
                curser.execute(qrl)
                results = curser.fetchall()
                if len(results) == 0:
                    cheek = cheek + 1
                else:
                    e_n_used = Label(page, text=f"{("Name", "Email")[x]} is already in uses")
                    e_n_used.grid(column=1, row=(2*x +1))
        if cheek == 4:
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                qrl = f"""INSERT INTO User (Email, Name, Password, User_type, User_pic, family) VALUES ("{user_email}", "{user_name}", "{password[0]}", "{user_type[0].lower()}", "basic.png", "");"""
                curser.execute(qrl)
                results = curser.fetchall()
            change_user(user_name)
            home_page()

    def log_out():
        global current_user, current_user_type, current_family
        current_family = ""
        current_user = -1
        current_user_type = "n"
        bar.grid_forget()
        log_in_page()


def home_page():
    clear_page()
    destination = home_page
    root.title("Home")
    links = []
    global page, current_user, current_user_type, current_family
    if current_user_type == "s":
        links = sql_join(current_user, "Class", "")
        destination = class_page

        #join class
        join_class_txt = Label(page, text="Class Code")
        join_class_txt.grid(column=0, row=0)
        join_class_input = Entry(page, width=8)
        join_class_input.grid(column=1,row=0)
        enter_button = Button(page, text="Enter",command=lambda: join_class(join_class_input.get()))
        enter_button.grid(column=2,row=0)
    elif current_user_type == "t":
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f""" {sql_base("Class")} WHERE User_ID = {current_user}"""
            curser.execute(qrl)  
            links = curser.fetchall()  
            destination = class_page

            #Add class
            add_class_name_txt = Label(page, text="")
    elif current_user_type == "c":
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""{sql_base("User")} WHERE family = "{current_family}"
                       AND User_type = "s" """
            curser.execute(qrl)  
            links = curser.fetchall()  
            destination = student_page
    for x in range (len(links)):
        link = Button(page, text= links[x][1], 
                    command=lambda c = x :(destination(links[c][0],links[c][1])))
        link.grid()
    reload_page()

# Classes
if 1 == 1:
    def join_class(x):
        global current_user
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f""" {sql_base("Class")} Where join_code = "{x}"; """
            curser.execute(qrl)
            selected_class = curser.fetchall()
            if len(selected_class) == 0:
                print(len(selected_class))
            else:
                qrl = f"""SELECT * From Stu_in_Class 
                        WHERE User_ID = {current_user} AND User_ID = "{x}"; """
                curser.execute(qrl)
                results = curser.fetchall()
                if len(results) == 0:
                    qrl = f"""INSERT INTO Stu_in_Class 
                            VALUES ({current_user}, {selected_class[0][0]}, 0, 2)"""
                    curser.execute(qrl)
                    class_page(selected_class[0][0],selected_class[0][1])

    def class_page(c_id, c_name):
        clear_page()
        root.title("Class" + c_name)
        student = Button(page, text = "Student 1", command=lambda:(student_page("1")))
        student.grid()
        projects =Button(page, text = "Project 1", command=lambda:(project_page("1")))
        projects.grid()
        reload_page()

def student_page(s_id, s_name):
    clear_page()
    global current_user, current_user_type
    root.title("student" + s_name)
    if current_user_type == "c":
        classes = sql_join(s_id, "Class", "")
    elif current_user_type == "t":
        classes = sql_join(s_id, "Class", f"AND Class.User_ID = {current_user}")
    for x in range (len(classes)):
        class_link = Button(page, text= classes[x][1], 
            command=lambda c = x :(class_page(classes[c][0],classes[c][1])))
        class_link.grid(column=(x), row=0)
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""{sql_base("Project")} WHERE Class_ID = {classes[x][0]}"""
            curser.execute(qrl)  
            projects = curser.fetchall()
            for y in range (len(projects)):
                projects = Button(page, text= projects[y][1], 
                    command=lambda c = y :(class_page(projects[c][0],projects[c][1])))
                projects.grid(column=(x), row=(y+1))
    reload_page()

def project_page(p_id, p_name):
    clear_page()
    root.title("Project" + p_name)
    reload_page()  

# Bar Segment
if 1==1:
    home_button = Button(bar,text="Home", command = lambda: (home_page()))
    home_button.grid(column=0,row=0)
    log_out_button = Button(bar, text="Log Out",command = lambda: (log_out()))
    log_out_button.grid(column=1,row=0)

# Open Window
log_in_page()
page.grid(column=0, row=1)
root.mainloop()