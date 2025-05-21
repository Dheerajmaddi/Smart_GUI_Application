import tkinter as tk
from tkinter import *
import csv


def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='#FAF1E4')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'Dheeraj':
            if password == 'Admin@321':
                win.destroy()
                root = tk.Tk()
                root.title("Registered Students")
                root.configure(background='#FAF1E4')

                cs = 'StudentDetails/StudentDetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 1

                    for col in reader:
                        c = 0

                        for row in col:
                            # Styling
                            label = tk.Label(root, width=25, height=1, fg="black", font=('times', 15, ' bold '),
                                             bg="gray62", text=row, relief=tk.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
        else:
            valid = 'Invalid Credentials'
            Nt = tk.Label(win, text=valid, bg="goldenrod", fg="black",
                          width=25, height=2, font=('times', 19, 'bold'))
            Nt.place(x=240, y=350)
            win.after(3000, lambda: Nt.place_forget())

    un = tk.Label(win, text="Enter username", width=15, height=2, fg="black", bg="#9EB384",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password", width=15, height=2, fg="black", bg="#9EB384",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="#F4EEEE", fg="black",
                       font=('times', 23, ' bold '))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="#F4EEEE",
                       fg="black", font=('times', 23, ' bold '))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="#435334", width=10, height=1,
                   activebackground="dark sea green", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="#435334", width=10, height=1,
                   activebackground="dark sea green", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="Login", fg="black", bg="dark olive green", width=20,
                      height=2,
                      activebackground="dark sea green", command=log_in, font=('times', 15, ' bold '))
    Login.place(x=310, y=250)
    win.mainloop()
