import tkinter as tk
from tkinter import *
from admin import admin_panel
from register_csv import is_student_registered
from image_processing import take_img, trainimg, err_screen
from capture_attendance import subjectchoose
from manual_attendance import manually_fill

# Connect to the database
# MySQL pwd: Xxxxxxxxxx
# User: Me ------- pwd: Xxxxxxxxxx

window = tk.Tk()
window.title("SGAP-Smart GUI Attendance Platform")


window.geometry('1320x720')
window.configure(background='#FAF1E4')


def clear():
    txt.delete(first=0, last=22)


def clear1():
    txt2.delete(first=0, last=30)


def clear2():
    txt3.delete(first=0, last=30)


def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


message = tk.Label(window, text="Smart GUI Attendance Platform", bg="#CEDEBD", fg="black", width=50,
                   height=2, font=('times', 30, 'bold '))

message.place(x=60, y=20)

Notification = tk.Label(window, text="Registration Successful!", bg="goldenrod", fg="black", width=20,
                        height=3, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2,
               fg="black", bg="#9EB384", font=('times', 15, ' bold '))
lbl.place(x=200, y=150)


txt = tk.Entry(window, validate="key", width=20, bg="#F4EEEE",
               fg="black", font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=550, y=160)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black",
                bg="#9EB384", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=250)

txt2 = tk.Entry(window, width=20, bg="#F4EEEE",
                fg="black", font=('times', 25, ' bold '))
txt2.place(x=550, y=260)

lbl3 = tk.Label(window, text="Enter Email", width=20, fg="black",
                bg="#9EB384", height=2, font=('times', 15, ' bold '))
lbl3.place(x=200, y=350)

txt3 = tk.Entry(window, width=20, bg="#F4EEEE",
                fg="black", font=('times', 25, ' bold '))
txt3.place(x=550, y=360)

clearButton = tk.Button(window, text="Clear", command=clear, fg="black", bg="#435334",
                        width=10, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
clearButton.place(x=950, y=160)

clearButton1 = tk.Button(window, text="Clear", command=clear1, fg="black", bg="#435334",
                         width=10, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
clearButton1.place(x=950, y=260)

clearButton3 = tk.Button(window, text="Clear", command=clear2, fg="black", bg="#435334",
                         width=10, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
clearButton3.place(x=950, y=360)


def register_student():
    if txt.get() == '' or txt2.get() == '' or txt3.get() == '':
        err_screen()
        Notification.configure(
            text="Enter Details for Registration!", width=25)
        Notification.place(x=580, y=650)
    else:

        if is_student_registered(txt.get(), txt2.get()):
            msg = 'Student Data already exists'
            Notification.configure(text=msg, width=21)
            Notification.place(x=550, y=650)

        else:

            take_img(txt, txt2, txt3, Notification)

            trainimg(Notification)

            Notification.configure(
                text="Images Saved for Enrollment: " + txt.get() + "   Name: " + txt2.get() + "\n" +
                "Model Trained" + "\n" +
                "Registration Successful!",
                width=50)
            Notification.place(x=350, y=620)

        clear()
        clear1()
        clear2()

    # Show the message (response) accordingly
    # Schedule remove_notification to be called after 3000 milliseconds (3 seconds)
    window.after(5000, remove_notification)


def remove_notification():
    Notification.place_forget()


submit_button = tk.Button(window, text="Register", command=register_student, fg="black",
                          bg="#435334", width=10, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
submit_button.place(x=250, y=450)


admin_button = tk.Button(window, text="Admin", command=admin_panel, fg="black",
                         bg="#435334", width=10, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
admin_button.place(x=450, y=450)

attendance = tk.Button(window, text="Automatic Attendance", fg="black", command=subjectchoose,
                       bg="#435334", width=15, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
attendance.place(x=650, y=450)

manual_attendance = tk.Button(window, text="Manual Attendance", fg="black", command=manually_fill,
                              bg="#435334", width=15, height=1, activebackground="dark sea green", font=('times', 15, ' bold '))
manual_attendance.place(x=900, y=450)


window.mainloop()
