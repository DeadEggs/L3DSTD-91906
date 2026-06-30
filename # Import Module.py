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
overlay= Frame(root)

def close_overlay():
    global overlay, page

    overlay.grid_remove()  

    #Reactive the rest of the page
    for widget in page.winfo_children():
        if widget.winfo_class() == "Frame":
            for widget_2 in widget.winfo_children():
                widget_2.config(state = "active")
        else:
            widget.config(state = "active")
      

# Sql Query Outlines
if 1 == 1:
    # Queries Student's Name & ID from selected Class/Project
    def Query(qrl):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            curser.execute(qrl)
            return(curser.fetchall())

    def sql_stu_in(id, to, ect):
        qrl = f"""SELECT User.User_ID, User.Name, Stu_in_{to}.Flagged
                FROM User
                JOIN Stu_in_{to} on Stu_in_{to}.User_ID = User.User_ID
                WHERE Stu_in_{to}.{to}_ID = {id} {ect}"""
        return(Query(qrl))

    # Queries Class/Project's Name & ID from selected Student
    def sql_join(id, to, ect1, ect2):
        qrl = f"""SELECT Stu_in_{to}.{to}_ID, {to}.Name, Stu_in_{to}.Flagged {ect1}
                FROM Stu_in_{to}
                join {to} on Stu_in_{to}.{to}_ID = {to}.{to}_ID
                Where Stu_in_{to}.User_ID = {id} {ect2} """
        return(Query(qrl))

    # Base qsl query
    def sql_base(From):
        return(f"SELECT {From}_ID, Name FROM {From}")

# Change Page
if 1 == 1:
    def clear_page():
        global page, overlay
        for widget in page.winfo_children():
            widget.destroy()
        
        overlay.grid_remove()

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
                     AND {place}_ID = {place_id} """
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

    # Queries who is flagging the kid
    qrl = f"""SELECT Email, Name FROM User
                WHERE User_ID = {current_user}"""
    sender = Query(qrl)

    # Queries for the kid
    qrl = f"""SELECT Name FROM User
                WHERE User_ID = {user_id}"""
    kid = Query(qrl)

    # Queries Where the flag is
    if place == "Project":
        qrl = f"""SELECT User.Name, User.Email, Class.Name, Project.Name
                FROM Project
                JOIN Class on Project.Class_ID = Class.Class_ID
                JOIN User on Class.User_ID = User.User_ID
                WHERE Project.Project_ID = {place_id}"""
        class_info = Query(qrl)[0]
        place_name = "Class: " + class_info[2] + ", Project: " + class_info[3]
    else:
        qrl = f"""SELECT User.Name, User.Email, Class.Name
                FROM Class
                JOIN User on Class.User_ID = User.User_ID
                WHERE Class.Class_ID = {place_id}"""
        class_info = Query(qrl)[0]
        place_name = "Class: " + class_info[2]

    # Sets how is getting the email
    if current_user_type == "c":
        receiver = class_info[0]
        msg["To"] = class_info[1]
    else: 
        qrl = f"""SELECT Name, Email FROM user
                WHERE family = (SELECT family FROM User WHERE User_ID = {user_id})
                And User_type = "c" """
        info = Query(qrl)
        receiver =  info[0][1]
        for x in range(len(info)):
            emails.append(info[x][1])
        msg["To"] = ", ".join(emails)

    msg["Subject"] = f"""{kid[0][0]} Flagged in {place_name}"""

    # Sets the message in the email
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
        qrl = f"""SELECT User_ID, User_type, family
            FROM User WHERE Name = "{x}" """
        info = Query(qrl)
        
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

        wrong_input = Label(page, text="")

        inputs = Frame(page)
        user_name_txt = Label(inputs, text="Username:")
        user_name_txt.grid(column=0, row=0)
        user_name_input = Entry(inputs, width=8)
        user_name_input.grid(column=1,row=0)
        
        password_txt = Label(inputs, text="Password:")
        password_txt.grid(column=0, row=1)
        password_input = Entry(inputs, width=8)
        password_input.grid(column=1,row=1)
        inputs.grid(column=0, row=2)

        # Enter
        enter_button = Button(page, text="Enter",
            command=lambda:(log_in_function(user_name_input.get(),password_input.get(), wrong_input)))
        enter_button.grid(column=0,row=3)

        reload_page()

    def log_in_function(user_name, password, frame):
        frame.grid_remove()
        frame.grid(column=0, row=1)
        check = 0

        for x in range(2):
            if (user_name, password)[x] == "":
                frame.config(text = f"No {("name", "password")[x]}")
            else:
                check = check + 1

        if check == 0:
            frame.config(text = f"Input both a username and password")

        elif check == 2:
            # Queries For User that matching inputted name & password
            qrl = f"""SELECT User_ID, User_type FROM User
                        WHERE Name = "{user_name}"
                        AND password = "{password}" """
            results = Query(qrl)

            # Informs user if no matches are found
            if len(results) == 0:
                frame.config(text="Username or password is incorrect")
            else:
                change_user(user_name)
                home_page()

    def signup():
        clear_page()
        
        back_button = Button(page, text = "back", command=lambda:(log_in_page()))
        back_button.grid(column=0, row=0)

        warnings = []
        entries = []

        for x in range(4):
            # Adds a place for the warnings to go
            warning = Label(page, text = "")
            warnings.append(warning)

            # Adds a block for the input
            input_frame = Frame(page)
            
            # Adds the text and input box 
            input_txt = Label(input_frame, 
                text=f"{("Username","Email","Password","Renter Password")[x]}: ")
            input_txt.grid(column=0,row=0)
            input_entry = Entry(input_frame, width=8)
            input_entry.grid(column=1,row=0)
            entries.append(input_entry)
            input_frame.grid(column=1,row=(2*x+2))

        # Adds a place for the warnings to go
        warning = Label(page, text= "")
        warnings.append(warning)

        # Adds a block for the input
        input_frame = Frame(page)

        # Adds the text and input box 
        type_txt = Label(input_frame, text="User Type:")
        type_txt.grid(column=0, row=0)
        type_input = ttk.Combobox(input_frame, values=["Student", "Teacher", "Caregiver"], width=8,state= "readonly")
        type_input.set("")
        type_input.grid(column=1,row=0)
        entries.append(type_input)
        input_frame.grid(column=1,row=(10))

        enter_button = Button(page, text="Enter",command=lambda:
            (sign_up_function(entries,warnings)))
        enter_button.grid(column=2,row=11)
        reload_page()

    def sign_up_function(entries,warnings):
        check = [0,0,0,0,0,0,0,0]

        # Checks and informs user if they forgot a input
        for x in range(5):
            if entries[x].get() == "":
                warnings[x].grid(column=1,row=(2*x+1))
                warnings[x].config(text = f"Input {("username","email","password","password","user type")[x]}")
            else:
                check[x] = 1
                warnings[x].grid_remove()

        # If user inputs both passwords, checks and informs user if they match
        if check[2] == 1 and check[3] == 1:    
            if entries[2].get() == entries[3].get():
                check[5] = 1
            else:
                warnings[2].grid(column=1,row=(2*x+1))
                warnings[2].config(text = "Passwords don't match")

        # If user inputted ever name or email, checks and informs if there free to use
        for x in range(2):
            qrl = f"""SELECT * FROM User
                    WHERE {("Name", "Email")[x]} =
                    "{entries[x].get()}"; """
            results = Query(qrl)
            if check[x] == 1:
                if len(results) == 0:
                    check[x+6] = 1
                else:
                    # Informs user if Not
                    warnings[x].grid(column=1,row=(2*x+1))
                    warnings[x].config(text=f"{("Name", "Email")[x]} is already in uses")
        
        # Add user and logs in if all checks are passed
        if sum(check) == 8:
            fam = ""

            # Set family code for caregivers
            if (entries[4].get())[0].lower() == "c":
                qrl = f""" SELECT Family FROM User
                            Where Family Like "{(entries[0].get())[0:3]}%" 
                            ORDER BY Family DESC"""
                results = Query(qrl)
                if len(results) ==0:
                    fam = (entries[0].get())[0:3] + "1"
                else:
                    fam = f"{(entries[0].get())[0:3]}{int((results[0][0])[3:])+1}"
            
            # Update database with the new user
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()    
                qrl = f"""INSERT INTO User (Email, Name, Password, User_type, User_pic, Family)
                    VALUES ("{(entries[1].get())}", "{(entries[0].get())}", "{(entries[2].get())[0]}", "{(entries[4].get())[0].lower()}", "basic.png", "{fam}");"""
                curser.execute(qrl)
            change_user((entries[0].get()))
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


        qrl = f"""SELECT User_ID, Family, User_type FROM User 
                    WHERE Name = "{name}"
                        AND Password = "{password}"
                        AND Email = "{email}" """
        person = Query(qrl)
        
        if len(person) == 0:
            frame[0].config(text = "No user founded")
        
        if person[0][1] == "" and person[0][2] == "s":
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
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

    incorrect_input = Label(page, text="")
    incorrect_input.grid(column=0, row=0)

    if current_user_type == "s":
        
        # Queries classes thats students are in
        links = sql_join(current_user, "Class", ", Class.User_ID","")
        destination = class_page
        destination_class = "Class"

        # Allows students to join class
        join_class_txt = Label(page, text="Class Code:")
        join_class_txt.grid(column=0, row=0)
        join_class_input = Entry(page, width=8)
        join_class_input.grid(column=1,row=1)
        enter_button = Button(page, text="Enter",command=lambda: 
            join_class(join_class_input.get(), incorrect_input))
        enter_button.grid(column=2,row=1)

    elif current_user_type == "t":
        
        incorrect_input2 = Label(page, text="")
        incorrect_input2.grid(column=2, row=0)

        # Queries classes that teachers are in 
        qrl = f""" {sql_base("Class")} WHERE User_ID = {current_user}"""
        links = Query(qrl)
        destination = class_page
        destination_class = "Class"

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
            add_class(add_class_name_input.get(),add_class_password_input.get(),(incorrect_input,incorrect_input2)))
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
        qrl = f"""{sql_base("User")} WHERE family = "{current_family}"
                    AND User_type = "s" """
        links = Query(qrl)
        destination = student_page
        destination_class = "Kid"

    # Lists and links class/student pages
    for x in range (len(links)):
        link = Frame (page,highlightbackground="blue", highlightthickness=2)
        destination_name = Label(link, text= f"{destination_class}: {links[x][1]}")
        destination_name.grid()

        if current_user_type == "s":
            teacher = Label(link, text= f"Teacher: {links[x][1]}")
            teacher.grid()
        for widget in link.winfo_children():
            widget.bind("<Button-1>",lambda event, c = x :(destination(links[c][0],links[c][1])))
        link.grid()
    reload_page()

# Classes
if 1 == 1:
    def add_class(name, join_code, frames):
        global current_user
        check = 0
        for x in range(len((name, join_code))):
            
            # checks if the user inputted a name & code
            if (name, join_code)[x] != "":
                check = check +1
                frames[x].config(text ="")
            
            else:
                frames[x].config(text = f"No {("name", "join code")[x]} inputted")

            # checks if the name & code are in uses
            qrl = f""" {sql_base("Class")} Where
                {("Name", "Join_code")[x]} = "{(name, join_code)[x]}"; """
            selected_class = Query(qrl)
            if len(selected_class) != 0:
                frames[x].config(text = f"{("Name", "Join code")[x]} already in uses")
            else:
                check = check +1
                frames[x].config(text ="")

        # Add to pasted all checks add class
        if check == 4:
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                qrl = f"""INSERT INTO Class (User_ID, Name, Join_code, Pic)
                            VALUES ({current_user}, "{name}", "{join_code}", "icon1")"""
                curser.execute(qrl)
            qrl = f""" {sql_base("Class")} Where
                Name = "{name}"; """
            c_id = Query(qrl)
            class_page(c_id[0][0],name)


    def join_class(x, frame):
        global current_user

        # Queries for the class that matches the code
        qrl = f""" {sql_base("Class")} Where join_code = "{x}"; """
        selected_class = Query(qrl)
        if len(selected_class) == 0:
            frame.config(text = "No class exists")

        # checks if user is already in a class
        else:
            qrl = f"""SELECT * From Stu_in_Class
                    WHERE User_ID = {current_user} AND User_ID = "{x}"; """
            results = Query(qrl)

                # Save user in class send the to it's page
            if len(results) == 0:
                with sqlite3.connect(DATABASE) as db:
                    curser = db.cursor()
                    qrl = f"""INSERT INTO Stu_in_Class 
                            VALUES ({current_user}, {selected_class[0][0]}, 0, 2)"""
                    curser.execute(qrl)
                join_project(selected_class[0][0])
                class_page(selected_class[0][0],selected_class[0][1])
                
            else:
                frame.config(text = "Already in class")

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
                add_project_name_txt = Label(selected_frame, text="Project Name:")
                add_project_name_input = Entry(selected_frame, width=8)
                add_project_name_txt.grid(column=0, row=1)
                add_project_name_input.grid(column=1,row=1)
                enter_button = Button(selected_frame, text="Enter",command=lambda:
                            add_project(add_project_name_input.get(), c_id, selected_frame))
                enter_button.grid(row=1, column=2)

            # Queries for projects in the class
            qrl = f"""{sql_base("Project")} WHERE Class_ID = {c_id}"""
            projects = Query(qrl)

            # List & link all project in class
            for x in range (len(projects)):
                project = Button(selected_frame, text= projects[x][1],
                    command=lambda c = x :(project_page(projects[c][0],projects[c][1])))
                project.grid(column=(0), row=(x+2))
                if current_user_type == "c":
                    flags = Button(selected_frame, text="flag", command= lambda x = x : flag_kids("project", projects[x][0]))
                    flags.grid(column=(1), row=(x+2))
            
            selected_frame.grid(column=0, row=1)
        reload_page()


def flag_kids(place, place_id):
    global page, overlay, current_user ,current_family
    for widget in overlay.winfo_children():
        widget.destroy()
    
    for widget in page.winfo_children():
        if widget.winfo_class() == "Frame":
            for widget_2 in widget.winfo_children():
                widget_2.config(state = "disabled")
        else:
            widget.config(state = "disabled")
    
    qrl = f"""Select User.User_ID, User.Name, Stu_in_{place}.Flagged From User
        JOIN Stu_in_{place} on Stu_in_{place}.User_ID = User.User_ID 
        WHERE Family = "{current_family}"
        AND Stu_in_{place}.{place}_id = {place_id} """
    kids = Query(qrl)
    
    close = Button(overlay, text="Close", command= lambda: close_overlay())
    close.grid(column= 0, row=0)

    flags = []
    for x in range(len(kids)):
        kid = Button(overlay, text=kids[x][1], bg = "blue",
            command=lambda c = x :flag(kids[c][2], kids[c][0], place_id, "Project", flags[c]))
        flags.append(kid)
        if kids[x][2] == 1:
            kid.config( bg = "red")
        kid.grid(column=1, row=(1+x))
    overlay.grid(column=0, row=1)

def student_page(s_id, s_name):
    clear_page()
    global current_user, current_user_type
    root.title("student" + s_name)
    flags = []

    # Queries Class that both you and the student can go to
    if current_user_type == "c":
        classes = sql_join(s_id, "Class","", "")
    elif current_user_type == "t":
        classes = sql_join(s_id, "Class", "",f"AND Class.User_ID = {current_user}")

    # List & Link classes
    for x in range (len(classes)):
        class_link = Button(page, text= classes[x][1],
            command=lambda c = x :(class_page(classes[c][0],classes[c][1])))
        class_link.grid(column=(2*x), row=0)

        # Queries project in the class
        qrl = f"""{sql_base("Project")} WHERE Class_ID = {classes[x][0]}"""
        projects = Query(qrl)
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
        qrl = f"""SELECT Project_ID FROM Project
                    WHERE Class_ID = "{new_class}"
                    AND Auto_join = 1 """
        projects =  Query(qrl)

            # Connect Students and project in the database
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            for project in projects:
                qrl = f"""INSERT INTO Stu_in_Project (User_ID, Project_ID, Joined)
                            VALUES ({current_user}, {project[0]}, 2)"""
                curser.execute(qrl)

    def add_project(name, c_ID, frame):
        qrl = f"""SELECT Project_ID FROM Project 
                    WHERE Class_ID = {c_ID} AND Name = "{name}" """
        used = Query(qrl)

        if len(used) != 0:
            txt = Label(frame, text = "Already Used in this class")
            txt.grid(row=0, column=1)
        
        else:
            with sqlite3.connect(DATABASE) as db:
                curser = db.cursor()
                qrl = f"""INSERT INTO Project (Name, Class_ID) 
                            VALUES ("{name}", {c_ID})"""
                curser.execute(qrl)

                qrl = f"""SELECT Project_ID FROM Project 
                        WHERE Class_ID = {c_ID} AND Name = "{name}" """
                project_id = Query(qrl)

                qrl = f"""SELECT User_ID FROM Stu_in_class
                        WHERE Class_ID = {c_ID}"""
                students = Query(qrl)

                for student in students:
                    qrl = f"""INSERT INTO Stu_in_Project 
                            VALUES ({student[0]}, {project_id[0][0]}, 0, 0)"""
                    curser.execute(qrl)

    def project_page(p_id, p_name):
        
        root.title("Project" + p_name)
        project_base(p_id)

    def project_base(p_id):
        clear_page()

        # Set up Frame select
        if 1 == 1:
            frame_select = Frame(page)

            if current_user_type == "t":
                observer_frame = Button(frame_select, text="Observe",command=lambda:project_observe(p_id))
                observer_frame.grid(column=0, row=0)
            
            project_frame = Label(frame_select, text="Project")
            project_frame.grid(column=1,row=0)

            frame_select.grid(column=0, row=0)

        reload_page()
    
    def edit_stu_in_project(p_id):
        global page, overlay, current_user ,current_family
        for widget in overlay.winfo_children():
            widget.destroy()

        close = Button(overlay, text="Close", command= lambda: close_overlay())
        close.grid(column= 0, row=0)

        for widget in page.winfo_children():
            if widget.winfo_class() == "Frame":
                for widget_2 in widget.winfo_children():
                    widget_2.config(state = "disabled")
            else:
                widget.config(state = "disabled")

        qrl = f"""SELECT User.User_ID, User.Name FROM User
                    Join Stu_in_class on Stu_in_class.User_ID = User.User_ID
                   WHERE Class_ID = (SELECT Class_ID FROM Project
                                      WHERE Project_ID = {p_id})"""
        kids = Query(qrl)
        for x in range(len(kids)):
            qrl = f"""SELECT * FROM Stu_in_project
                       WHERE User_ID = {kids[x][0]}"""
            student = Button(overlay, text=kids[x][1], command=lambda kid = kids[x]: edit_stu_in_project_2(p_id, kid[0], 1, student))
            if len(Query(qrl)) == 0:
                student.config(command=lambda kid = kids[x]: edit_stu_in_project_2(p_id, kid[0], 0, student))
            student.grid(column=0, row=x)

        overlay.grid(column=0, row=1)

    def edit_stu_in_project_2(p_id, s_id, join, button):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            if join == 0:
                qrl = f"""INSERT INTO Stu_in_project VALUES ({s_id}, {p_id}, 0 , 2)"""
                button.config(command=lambda: edit_stu_in_project_2(p_id, s_id, 1, button))
            else:
                qrl = f"""DELETE FROM Stu_in_project 
                           WHERE User_id = {s_id}
                             AND Project_ID = {p_id}"""
                button.config(command=lambda: edit_stu_in_project_2(p_id, s_id, 0, button))
            curser.execute(qrl)

    def project_observe(p_id):
        clear_page()
        global page, current_user, current_user_type, current_family
        # Set up Frame select
        if 1 == 1:
            frame_select = Frame(page)
            
            observer_frame = Label(frame_select, text="Observe")
            observer_frame.grid(column=0, row=0)
            
            project_frame = Button(frame_select, text="Project",command=lambda:project_base(p_id))
            project_frame.grid(column=1,row=0)

            frame_select.grid(column=0, row=0)
            
        # Set up the selected frame
        if 1 == 1:
            selected_frame = Frame(page)
            
            edit_project_roster = Button(selected_frame, text= "add student",
                command=lambda:edit_stu_in_project(p_id))
            
            edit_project_roster.grid(column=2, row=1)


            qrl = f"""SELECT Auto_join FROM Project
                    WHERE Project_ID = {p_id}"""
            auto_join = Query(qrl)[0][0]
            toggle_auto_join = Button(selected_frame, text = "Project auto join", bg = "green", 
                command=lambda: auto_join_toggle(toggle_auto_join, auto_join, p_id))
            if auto_join == 0:
                toggle_auto_join.config(bg="red")
            toggle_auto_join.grid(column=0, row=1)

            # List & link all students in the class
            students = sql_stu_in(p_id, "Project", "")
            flags = []
            for x in range (len(students)):
                student = Button(selected_frame, text= students[x][1],
                    command=lambda c = x :(student_page(students[c][0],students[c][1])))
                student.grid(column=(0), row=(x+2))

                # Display if student is flagged and changes it
                flagged = Button(selected_frame, text="Flag", bg = "red",
                    command=lambda c = x :flag(students[c][2], students[c][0], p_id, "Project", flags[c]))
                if students[x][2] == 0:
                    flagged.config(bg = "blue")
                    
                flagged.grid(column=(1), row=(x+2))
                flags.append(flagged)

            selected_frame.grid(column=0, row=1)

        reload_page()

    def auto_join_toggle(button, auto_join, p_id):
        with sqlite3.connect(DATABASE) as db:
            curser = db.cursor()
            qrl = f"""UPDATE Project SET Auto_join = {(auto_join+1)%2} 
                       WHERE Project_ID = {p_id}"""
            curser.execute(qrl)
        if auto_join == 1:
            button.config(bg = "red", command=lambda: auto_join_toggle(button, 0, p_id))
        else:
            button.config(bg = "green", command=lambda: auto_join_toggle(button, 1, p_id))

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