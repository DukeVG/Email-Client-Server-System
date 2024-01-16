from tkinter import *
from tkinter import filedialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re

def login():
    if validate_login():
        global username, password, server

        username = str(emailEntry.get())
        password = str(passEntry.get())

        server = smtplib.SMTP("smtp.gmail.com:587")

        server.ehlo()

        server.starttls()

        server.login(username, password)
        f2.pack()
        logoutBtn.grid()

        loginSuccessful["text"] = "Logged In!"
        root.after(10, root.grid)
        f1.pack_forget()
        root.after(10, root.grid)
        f3.pack()

        sendSuccessful.grid_remove()
        root.after(10, root.grid)

def hide_login_label():
    f2.pack_forget()
    f3.pack_forget()
    root.after(10, root.grid)

def attach_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        attached_files.insert(END, file_path)

def validate_message():
    email_text = str(toEntry.get())
    sub_text = str(subjectEntry.get())
    msg_text = str(messageEntry.get())

    if (email_text == "") or (sub_text == "") or (msg_text == ""):
        sendSuccessful.grid()
        sendSuccessful["text"] = "Fill in all the Fields"
        root.after(10, root.grid)
        return False
    else:
        EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")
        if not EMAIL_REGEX.match(email_text):
            f2.pack()
            sendSuccessful.grid()
            sendSuccessful["text"] = "Enter a valid Email Address"
            root.after(10, root.grid)
            return False
        else:
            return True

def validate_login():
    email_text = str(emailEntry.get())
    pass_text = str(passEntry.get())

    if (email_text == "") or (pass_text == ""):
        f2.pack()
        loginSuccessful.grid()
        loginSuccessful["text"] = "Fill all the Fields"
        logoutBtn.grid_remove()
        root.after(10, root.grid)
        return False
    else:
        email_regex = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")
        if not email_regex.match(email_text):
            f2.pack()
            loginSuccessful.grid()
            loginSuccessful["text"] = "Enter a valid Email Address"
            logoutBtn.grid_remove()
            root.after(10, root.grid)
            return False
        else:
            return True

def send_email():
    if validate_message():
        sendSuccessful.grid_remove()
        root.after(10, root.grid)

        receiver = str(toEntry.get())
        subject = str(subjectEntry.get())
        msgbody = str(messageEntry.get())

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.attach(MIMEText(msgbody, "plain", "utf-8"))

        for file_path in attached_files.get(0, END):
            with open(file_path, "rb") as file:
                part = MIMEApplication(file.read(), Name=file.name)
                part['Content-Disposition'] = f'attachment; filename="{file.name}"'
                msg.attach(part)

        try:
            server.sendmail(username, receiver, msg.as_string())
            sendSuccessful.grid()
            sendSuccessful["text"] = "Mail Sent!"
            root.after(10, sendSuccessful.grid)
        except Exception as e:
            sendSuccessful.grid()
            sendSuccessful["text"] = "Error in Sending Your Email"
            root.after(10, root.grid)

def logout():
    try:
        server.quit()
        f3.pack_forget()
        f2.pack()
        loginSuccessful.grid()
        loginSuccessful["text"] = "Logged Out Successfully"
        logoutBtn.grid_remove()
        f1.pack()
        passEntry.delete(0, END)
        root.after(10, root.grid)
    except Exception as e:
        loginSuccessful["text"] = "Error in Logout"

def show_inbox():
    
    inbox_messages = [
        {"from": "blissgris@example.com", "subject": "Hello vg", "body": "Message from bliss gris"},
        {"from": "blissgris@example.com", "subject": "hi", "body": ""},
        {"from": "blissgris@example.com", "subject": "yess", "body": "Message 3"}
    ]

    inbox_frame = Frame(root)
    inbox_frame.pack(side=TOP, expand=NO, fill=NONE)

    inbox_label = Label(inbox_frame, text="Inbox", font="Arial")
    inbox_label.grid(row=0, columnspan=3, pady=10)

    header_label = Label(inbox_frame, text="To", font="Arial")
    header_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

    header_label = Label(inbox_frame, text="Subject", font="Arial")
    header_label.grid(row=1, column=1, pady=5, padx=5, sticky=W)

    header_label = Label(inbox_frame, text="Body", font="Arial")
    header_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

    for idx, message in enumerate(inbox_messages, start=2):
        to_label = Label(inbox_frame, text=message["to"])
        to_label.grid(row=idx, column=0, pady=5, padx=5, sticky=W)

        subject_label = Label(inbox_frame, text=message["subject"])
        subject_label.grid(row=idx, column=1, pady=5, padx=5, sticky=W)

        body_label = Label(inbox_frame, text=message["body"])
        body_label.grid(row=idx, column=2, pady=5, padx=5, sticky=W)

    back_to_compose_btn = Button(inbox_frame, text="Back to Compose", width=15, bg="black", fg="white", command=lambda: switch_to_compose(inbox_frame))
    back_to_compose_btn.grid(row=len(inbox_messages) + 2, column=1, pady=10)


def switch_to_compose(inbox_frame):
    inbox_frame.pack_forget()
    f3.pack()

root = Tk()
root.title("Email Application")

f1 = Frame(root, width=10000, height=8000)
f1.pack(side=TOP)

credential = Label(f1, text="Enter Your Credentials", font="Arial")
credential.grid(row=0, columnspan=3, pady=80, padx=150)

email = Label(f1, text="Email").grid(row=1, sticky=E, pady=5, padx=10)
password = Label(f1, text="Password").grid(row=2, sticky=E, pady=5, padx=10)

emailEntry = Entry(f1)
passEntry = Entry(f1, show="*")

emailEntry.grid(row=1, column=1, pady=5)
passEntry.grid(row=2, column=1)

loginBtn = Button(f1, text="Login", width=10, bg="black", fg="white", command=lambda: login())
loginBtn.grid(row=3, columnspan=3, pady=10)

f2 = Frame(root)
f2.pack(side=TOP, expand=NO, fill=NONE)

loginSuccessful = Label(f2, width=20, bg="cyan", fg="red", text="Log in Success", font="Arial")
loginSuccessful.grid(row=0, column=0, columnspan=2, pady=5)

logoutBtn = Button(f2, text="Logout", bg="black", fg="white", command=lambda: logout())
logoutBtn.grid(row=0, column=4, sticky=E, pady=10, padx=(5, 0))

f3 = Frame(root)
f3.pack(side=TOP, expand=NO, fill=NONE)

composeEmail = Label(f3, width=20, text="Compose Email", font="Arial")
composeEmail.grid(row=0, columnspan=3, pady=10)

to = Label(f3, text="To").grid(row=1, sticky=E, pady=5)
subject = Label(f3, text="Subject").grid(row=2, sticky=E, pady=5)
message = Label(f3, text="Message").grid(row=3, sticky=E,pady=5)

toEntry = Entry(f3, width=30)
subjectEntry = Entry(f3, width=30)
messageEntry = Entry(f3, width=30)

toEntry.grid(row=1, column=1, pady=5)
subjectEntry.grid(row=2, column=1, pady=5)
messageEntry.grid(row=3, column=1, pady=5, rowspan=3, ipady=10)

attached_files = Listbox(f3, selectmode=MULTIPLE, width=30, height=5)
attached_files.grid(row=6, column=1, pady=5)

attachFileBtn = Button(f3, text="Attach File", width=10, bg="black", fg="white", command=lambda: attach_file())
attachFileBtn.grid(row=6, column=2, sticky=E, pady=10)

sendEmailBtn = Button(f3, text="Send Email", width=10, bg="black", fg="white", command=lambda: send_email())
sendEmailBtn.grid(row=7, columnspan=3, pady=10)

inboxBtn = Button(f3, text="Inbox", width=10, bg="black", fg="white", command=lambda: show_inbox())
inboxBtn.grid(row=7, column=2, pady=10)

sendSuccessful = Label(f3, width=20, fg="white", bg="black", font="Arial")
sendSuccessful.grid(row=8, columnspan=3, pady=5)

hide_login_label()

mainloop()