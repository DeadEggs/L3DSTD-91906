# Import Module
from tkinter import *
from tkinter import ttk
import sqlite3
import smtplib
from email.message import EmailMessage

EMAIL = "email25sender@gmail.com"
APP_PASSWORD = "oozf iyzr ljsd hfmf"

DATABASE = "Databases"

current_user = -1
current_user_type = "n"
current_family = ""

# Create root window
root = Tk()

# Sets Up Page sections
bar = Frame(root)
page = Frame(root)

# Sql Query Outlines
if 1 == 1:
    # Queries Student's Name & ID from selected Class/Project
    def sql_stu_in(id, to, ect):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT User.User_ID, User.Name, Stu_in_{to}.Flagged
                    FROM User
                    JOIN Stu_in_{to} on Stu_in_{to}.User_ID = User.User_ID
                    WHERE Stu_in_{to}.{to}_ID = {id} {ect}"""
            curser.execute(qrl)
            return(curser.fetchall())

    # Queries Class/Project's Name & ID from selected Student
    def sql_join(id, to, ect):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT Stu_in_{to}.{to}_ID, {to}.Name, Stu_in_{to}.Flagged
                    FROM Stu_in_{to}
                    join {to} on Stu_in_{to}.{to}_ID = {to}.{to}_ID
                    Where Stu_in_{to}.User_ID = {id} {ect} """
            curser.execute(qrl)
            return(curser.fetchall())

    # Base qsl query
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

def flag(flagged, user_id, place_id, place, button):
    global current_user, current_user_type

    # Update Database
    with sqlite3.connect(DATABASE) as db:
        curser = db.cursor()
        qrl = f"""UPDATE Stu_in_{place} SET Flagged = {(flagged+1)%2}
                   WHERE User_ID = {user_id}
                     AND Class_ID = {place_id} """
        curser.execute(qrl)
    
    # Update Flag button 
    if flagged == 0 :
        button.config(bg = "red", command=lambda :flag(1, user_id, place_id, place, button))
        send_flag(user_id, place_id, place)
    else:
        button.config(bg = "blue", command=lambda :flag(0, user_id, place_id, place, button))

def send_flag(user_id, place_id, place):
    global current_user, current_user_type
    msg = EmailMessage()
    emails = []
    
    with sqlite3.connect(DATABASE) as db:
        curser = db.cursor()

        # Queries who is flagging the kid
        qrl = f"""SELECT Email, Name FROM User
                   WHERE User_ID = {current_user}"""
        curser.execute(qrl)
        sender = curser.fetchall()

        # Queries for the kid
        qrl = f"""SELECT Name FROM User
                   WHERE User_ID = {user_id}"""
        curser.execute(qrl)
        kid = curser.fetchall()

        # Queries Where the flag is
        if place == "Project":
            qrl = f"""SELECT User.Name, User.Email, Class.Name, Project.Name
                    FROM Project
                    JOIN Class on Project.Class_ID = Class.Class_ID
                    JOIN User on Class.User_ID = User.User_ID
                    WHERE Project.Project_ID = {place_id}"""
            curser.execute(qrl)
            class_info = (curser.fetchall())[0]
            place_name = "Class: " + class_info[2] + ", Project: " + class_info[3]
        else:
            qrl = f"""SELECT User.Name, User.Email, Class.Name
                    FROM Class
                    JOIN User on Class.User_ID = User.User_ID
                    WHERE Project.Project_ID = {place_id}"""
            curser.execute(qrl)
            class_info = (curser.fetchall())[0]
            place_name = "Class: " + class_info[2]

        # Queries who is getting the email
        if current_user_type == "c":
            receiver = class_info[1]
            msg["To"] = class_info[0]
        else: 
            qrl = f"""SELECT Name, Email FROM user
                    WHERE family = (SELECT family FROM User WHERE User_ID = {user_id})
                    And User_type = "c" """
            curser.execute(qrl)
            info = curser.fetchall()
            receiver =  info[0][1]

            # Sends the email to all caregivers
            for x in range(len(info)):
                emails.append(info[x][0])
            msg["To"] = ", ".join(emails)
    msg["Subject"] = f"""{kid[0][0]} Flagged in {place_name}"""

    if len(emails) <= 1:
        msg.set_content(f"""Dare {receiver}, Has be flagged in {place_name} by {sender[0][1]} at {sender[0][0]}""")
    else:
        msg.set_content(f"""Dare caregivers, has be flagged in {place_name} by {sender[0][1]} at {sender[0][0]}""")
    
    # Send Email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, APP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

# Login/out
if 1 == 1:
    def change_user(x):
        global current_user, current_user_type, current_family

        # Queries Necessary user info
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT User_ID, User_type, family
                FROM User WHERE Name = "{x}" """
            curser.execute(qrl)
            info = curser.fetchall()
        
        # save necessary user info on the program 
        current_family = info[0][2]
        current_user = info[0][0]
        current_user_type = info[0][1]

        bar.grid(column=0,row=0)

    def log_in_page():
        clear_page()
        global page
        root.title("Login/Sing up")

        login_button = Button(page, text = "Log in", command=login)
        login_button.grid(column=0, row=0)

        signup_button = Button(page, text = "Sign up", command=signup)
        signup_button.grid(column=1, row=0)
        reload_page()

    def login():
        clear_page()
        
        back_button = Button(page, text = "back", command=lambda:(log_in_page()))
        back_button.grid(column=0, row=0)

        user_name_txt = Label(page, text="Username:")
        user_name_txt.grid(column=1, row=2)
        user_name_input = Entry(page, width=8)
        user_name_input.grid(column=2,row=2)
        
        password_txt = Label(page, text="Password:")
        password_txt.grid(column=1, row=4)
        password_input = Entry(page, width=8)
        password_input.grid(column=2,row=4)

        # Enter
        enter_button = Button(page, text="Enter",
            command=lambda:(log_in_function(user_name_input.get(),password_input.get())))
        enter_button.grid(column=2,row=5)

        reload_page()

    def log_in_function(user_name, password):

        # Queries For User that matching inputted name & password
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT User_ID, User_type FROM User
                        WHERE Name = "{user_name}"
                        AND password = "{password}" """
            curser.execute(qrl)
            results = curser.fetchall()

        # Informs user if no matches are found
        if len(results) == 0:
            incorrect = Label(page, text="Username or password is incorrect")
            incorrect.grid(column=1,row=1)

        else:
            change_user(user_name)
            home_page()

    def signup():
        clear_page()
        
        back_button = Button(page, text = "back", command=lambda:(log_in_page()))
        back_button.grid(column=0, row=0)

        user_name_txt = Label(page, text="Username:")
        user_name_txt.grid(column=1, row=2)
        user_name_input = Entry(page, width=8)
        user_name_input.grid(column=2,row=2)

        email_txt = Label(page, text="Email:")
        email_txt.grid(column=1, row=4)
        email_input = Entry(page, width=8)
        email_input.grid(column=2,row=4)

        type_txt = Label(page, text="User Type:")
        type_txt.grid(column=1, row=6)
        type_input = ttk.Combobox(page, values=["Student", "Teacher", "Caregiver"], width=8,state= "readonly")
        type_input.set("")
        type_input.grid(column=2, row=6)

        password_txt = Label(page, text="Password:")
        password_txt.grid(column=1, row=8)
        password_input = Entry(page, width=8)
        password_input.grid(column=2,row=8)

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

        # Cheek that passwords match
        if password[0] == password[1]:
            cheek = cheek + 1
        else:
            # Informs user if Not
            wrong_password = Label(page, text="Passwords don't match")
            wrong_password.grid(column=1,row=7)
        
        # Cheeks if a user type was selected
        if user_type[0] in ("T","S","C"):
            cheek = cheek + 1
        else:
            # Informs user if Not
            no_type = Label(page, text="No User type selected")
            no_type.grid(column=1,row=5)

        # Queries if name and email are free to use
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            for x in range(2):
                qrl = f"""SELECT * FROM User
                        WHERE {("Name", "Email")[x]} =
                        "{(user_name, user_email)[x]}"; """
                curser.execute(qrl)
                results = curser.fetchall()
                if len(results) == 0:
                    cheek = cheek + 1
                else:
                    # Informs user if Not
                    e_n_used = Label(page, text=f"{("Name", "Email")[x]} is already in uses")
                    e_n_used.grid(column=1, row=(2*x +1))
        
        # Add user and logs in if all Cheeks are passed
        if cheek == 4:
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                fam = ""

                # Set family code for caregivers
                if user_type[0].lower() == "c":
                    qrl = f""" SELECT Family FROM User
                                Where Family Like "{user_name[0:3]}%" 
                                ORDER BY Family DESC"""
                    curser.execute(qrl)
                    results = curser.fetchall()
                    if len(results) ==0:
                        fam = user_name[0:3] + "1"
                    else:
                        fam = f"{user_name[0:3]}{int((results[0][0])[3:])+1}"
                
                # Update database with the new user
                qrl = f"""INSERT INTO User (Email, Name, Password, User_type, User_pic, Family)
                    VALUES ("{user_email}", "{user_name}", "{password[0]}", "{user_type[0].lower()}", "basic.png", "{fam}");"""
                curser.execute(qrl)
            change_user(user_name)
            home_page()

    def log_out():
        global current_user, current_user_type, current_family
        current_family = ""
        current_user = -1
        current_user_type = "n"
        bar.grid_forget()
        log_in_page()

# Add Family
if 1 == 1:
    def add_family(name, email, password, frame):
        global current_family

        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()

            qrl = f"""SELECT User_ID, Family, User_type FROM User 
                       WHERE Name = "{name}"
                         AND Password = "{password}"
                         AND Email = "{email}" """
            curser.execute(qrl)
            person = curser.fetchall()
            if len(person) == 0:
                frame[0].config(text = "No user founded")
            if person[0][1] == "" and person[0][2]:
                qrl = f"""UPDATE User SET Family = "{current_family}"
                           WHERE User_ID = "{person[0][0]}" """
                curser.execute(qrl)
                frame[0].config(text = "")
                student_page(person[0][0],name)

def home_page():
    clear_page()
    destination = home_page
    root.title("Home")
    links = []
    global page, current_user, current_user_type, current_family

    if current_user_type == "s":
        
        # Queries classes thats students are in
        links = sql_join(current_user, "Class", "")
        destination = class_page

        # Allows students to join class
        join_class_txt = Label(page, text="Class Code:")
        join_class_txt.grid(column=0, row=0)
        join_class_input = Entry(page, width=8)
        join_class_input.grid(column=1,row=0)
        enter_button = Button(page, text="Enter",command=lambda: join_class(join_class_input.get()))
        enter_button.grid(column=2,row=0)

    elif current_user_type == "t":

        # Queries classes that teachers are in 
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f""" {sql_base("Class")} WHERE User_ID = {current_user}"""
            curser.execute(qrl)  
            links = curser.fetchall()
            destination = class_page

        # Allows teachers to mack a new class 
        add_class_name_txt = Label(page, text="Class Name:")
        add_class_name_input = Entry(page, width=8)
        add_class_name_txt.grid(column=0, row=1)
        add_class_name_input.grid(column=1,row=1)

        add_class_password_txt = Label(page, text="Class Join Code")
        add_class_password_input = Entry(page, width=8)
        add_class_password_txt.grid(column=0, row=3)
        add_class_password_input.grid(column=1, row=3)
        enter_button = Button(page, text="Enter",command=lambda:
                                add_class(add_class_name_input.get(),add_class_password_input.get()))
        enter_button.grid(column=2,row=3)

    elif current_user_type == "c":

        incorrect_input = Label(page, text="")
        incorrect_input.grid(column=0, row=0)

        add_kid_name_txt = Label(page, text="Child Name:")
        add_kid_name_input = Entry(page, width=8)
        add_kid_name_txt.grid(column=0, row=1)
        add_kid_name_input.grid(column=1,row=1)

        add_kid_email_txt = Label(page, text="Child Email:")
        add_kid_email_input = Entry(page, width=8)
        add_kid_email_txt.grid(column=2, row=1)
        add_kid_email_input.grid(column=3, row=1)

        add_kid_password_txt = Label(page, text="Child Password:")
        add_kid_password_input = Entry(page, width=8)
        add_kid_password_txt.grid(column=4, row=1)
        add_kid_password_input.grid(column=5,row=1)

        enter_button = Button(page, text="Enter",command=lambda:add_family(add_kid_name_input.get(),
            add_kid_email_input.get(),add_kid_password_input.get(),(incorrect_input)))
        enter_button.grid(column=6,row=3)

        # Queries kids of user's
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""{sql_base("User")} WHERE family = "{current_family}"
                       AND User_type = "s" """
            curser.execute(qrl)
            links = curser.fetchall()
            destination = student_page

    # Lists and links class/student pages
    for x in range (len(links)):
        link = Button(page, text= links[x][1],
                    command=lambda c = x :(destination(links[c][0],links[c][1])))
        link.grid()
    reload_page()

# Classes
if 1 == 1:
    def add_class(name, join_code):
        global current_user
        cheek = 0
        for x in range(len((name, join_code))):
            
            # Cheeks if the user inputted a name & code
            if (name, join_code)[x] != "":
                print((name, join_code)[x])
                cheek = cheek +1

            # Cheeks if the name & code are in uses
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                qrl = f""" {sql_base("Class")} Where
                    {("Name", "Join_code")[x]} = "{(name, join_code)[x]}"; """
                curser.execute(qrl)
                selected_class = curser.fetchall()
                if len(selected_class) != 0:
                    print(len(selected_class))
                else:
                    cheek = cheek +1

        # Add to pasted all Cheeks add class
        if cheek == 4:
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                qrl = f"""INSERT INTO Class (User_ID, Name, Join_code, Pic)
                            VALUES ({current_user}, "{name}", "{join_code}", "icon1")"""
                curser.execute(qrl)
                qrl = f""" {sql_base("Class")} Where
                    Name = "{name}"; """
                curser.execute(qrl)
                c_id = curser.fetchall()
            class_page(c_id[0][0],name)


    def join_class(x):
        global current_user
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()

            # Queries for the class that matches the code
            qrl = f""" {sql_base("Class")} Where join_code = "{x}"; """
            curser.execute(qrl)
            selected_class = curser.fetchall()
            if len(selected_class) == 0:
                print(len(selected_class))

            # Cheeks if user is already in a class
            else:
                qrl = f"""SELECT * From Stu_in_Class
                        WHERE User_ID = {current_user} AND User_ID = "{x}"; """
                curser.execute(qrl)
                results = curser.fetchall()

                # Save user in class send the to it's page
                if len(results) == 0:
                    qrl = f"""INSERT INTO Stu_in_Class 
                            VALUES ({current_user}, {selected_class[0][0]}, 0, 2)"""
                    curser.execute(qrl)
                    join_project(selected_class[0][0])
                    class_page(selected_class[0][0],selected_class[0][1])

    def class_page(c_id, c_name):
        root.title("Class" + c_name)
        
        # Load the project frame
        class_project(c_id)
    
    def class_observe(c_id):
        clear_page()
        global page, current_user, current_user_type, current_family

        # Set up Frame select
        if 1 == 1:
            frame_select = Frame(page)
            
            observer_frame = Label(frame_select, text="Observe")
            observer_frame.grid(column=0, row=0)
            
            project_frame = Button(frame_select, text="Projects",command=lambda:class_project(c_id))
            project_frame.grid(column=1,row=0)

            frame_select.grid(column=0, row=0)
            
        # Set up the selected frame
        if 1 == 1:
            selected_frame = Frame(page)

            # List & link all students in the class
            students = sql_stu_in(c_id, "Class", "")
            flags = []
            for x in range (len(students)):
                student = Button(selected_frame, text= students[x][1],
                    command=lambda c = x :(student_page(students[c][0],students[c][1])))
                student.grid(column=(0), row=(x+2))

                # Display if student is flagged and changes it
                if students[x][2] == 0:
                    flagged = Button(selected_frame, text="Flag", bg = "blue",
                    command=lambda c = x :flag(students[c][2], students[c][0], c_id, "Class", flags[c]))
                else:
                    flagged = Button(selected_frame, text="Flag", bg = "red",
                    command=lambda c = x :flag(students[c][2], students[c][0], c_id, "Class", flags[c]))
                flagged.grid(column=(1), row=(x+2))
                flags.append(flagged)

            selected_frame.grid(column=0, row=1)

        reload_page()
    
    def class_project(c_id):
        clear_page()
        global page, current_user, current_user_type, current_family

        # Set up Frame select
        if 1 == 1:
            frame_select = Frame(page)

            if current_user_type == "t":
                observer_frame = Button(frame_select, text="Observe",command=lambda:class_observe(c_id))
                observer_frame.grid(column=0, row=0)
            
            project_frame = Label(frame_select, text="Projects")
            project_frame.grid(column=1,row=0)

            frame_select.grid(column=0, row=0)

        # Set up the selected frame
        if 1 == 1:
            selected_frame = Frame(page)

            # Allows teachers to mack a new class 
            if current_user_type == "t":
                add_class_name_txt = Label(selected_frame, text="Class Name:")
                add_class_name_input = Entry(selected_frame, width=8)
                add_class_name_txt.grid(column=0, row=1)
                add_class_name_input.grid(column=1,row=1)
                enter_button = Button(selected_frame, text="Enter",command=lambda:
                            add_project(add_class_name_input.get(), c_id, selected_frame))
                enter_button.grid(row=1, column=2)

            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()

                # Queries for projects in the class
                qrl = f"""{sql_base("Project")} WHERE Class_ID = {c_id}"""
                curser.execute(qrl)
                projects = curser.fetchall()

                # List & link all project in class
                for x in range (len(projects)):
                    project = Button(selected_frame, text= projects[x][1],
                        command=lambda c = x :(project_page(projects[c][0],projects[c][1])))
                    project.grid(column=(0), row=(x+2))
            
            selected_frame.grid(column=0, row=1)
        reload_page()


def student_page(s_id, s_name):
    clear_page()
    global current_user, current_user_type
    root.title("student" + s_name)
    flags = []

    # Queries Class that both you and the student can go to
    if current_user_type == "c":
        classes = sql_join(s_id, "Class", "")
    elif current_user_type == "t":
        classes = sql_join(s_id, "Class", f"AND Class.User_ID = {current_user}")

    # List & Link classes
    for x in range (len(classes)):
        class_link = Button(page, text= classes[x][1],
            command=lambda c = x :(class_page(classes[c][0],classes[c][1])))
        class_link.grid(column=(2*x), row=0)

        # Queries project in the class
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""{sql_base("Project")} WHERE Class_ID = {classes[x][0]}"""
            curser.execute(qrl)
            projects = curser.fetchall()

            # Display if class is flagged and changes it
            if classes[x][2] == 0:
                flagged = Button(page, text="Flag", bg = "blue",
                command=lambda c = x :flag(classes[c][2], s_id, classes[c][0], "Class", flags[c]))
            else:
                flagged = Button(page, text="Flag", bg = "red",
                command=lambda c = x :flag(classes[c][2], s_id, classes[c][0], "Class", flags[c]))
            flagged.grid(column=((2*x)+1), row=0)
            flags.append(flagged)

            # List & Link project
            for y in range (len(projects)):
                projects = Button(page, text= projects[y][1],
                    command=lambda c = y :(project_page(projects[c][0],projects[c][1])))
                projects.grid(column=(2*x), row=(y+1))

                # Display if class is flagged and changes it
                if classes[x][2] == 0:
                    flagged = Button(page, text="Flag", bg = "blue",
                    command=lambda c = y :flag(projects[c][2], s_id, projects[c][0], "Project", flags[c]))
                else:
                    flagged = Button(page, text="Flag", bg = "red",
                    command=lambda c = y :flag(projects[c][2], s_id, projects[c][0], "Project", flags[c]))
                flagged.grid(column=((2*x)+1), row=(y+1))
                flags.append(flagged)
    reload_page()

# Projects
if 1 == 1:
    def join_project(new_class):
        global current_user

        # Queries projects in the class
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT Project_ID FROM Project
                     WHERE Class_ID = "{new_class}" """
            curser.execute(qrl)
            projects =  curser.fetchall()

            # Connect Students and project in the database
            for project in projects:
                qrl = f"""INSERT INTO Stu_in_Project 
                            VALUES ({current_user}, {project[0]}, 0, 2)"""
                curser.execute(qrl)

    def add_project(name, c_ID, frame):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""SELECT Project_ID FROM Project 
                        WHERE Class_ID = {c_ID} AND Name = "{name}" """
            curser.execute(qrl)
            used = curser.fetchall()

            if len(used) != 0:
                txt = Label(frame, text = "Already Used in this class")
                txt.grid(row=0, column=1)
            
            else:
                qrl = f"""INSERT INTO Project (Name, Class_ID) 
                            VALUES ("{name}", {c_ID})"""
                curser.execute(qrl)

                qrl = f"""SELECT Project_ID FROM Project 
                        WHERE Class_ID = {c_ID} AND Name = "{name}" """
                curser.execute(qrl)
                project_id = curser.fetchall()

                qrl = f"""SELECT User_ID FROM Stu_in_class
                        WHERE Class_ID = {c_ID}"""
                curser.execute(qrl)
                students = curser.fetchall()

                for student in students:
                    qrl = f"""INSERT INTO Stu_in_Project 
                            VALUES ({student[0]}, {project_id[0][0]}, 0)"""
                    curser.execute(qrl)


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