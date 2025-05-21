import tkinter as tk
from tkinter import *
import time
import datetime
import subprocess
import pymysql
import csv
import os
from send_email import attendance_confirmation


def manually_fill():
    global sb
    sb = tk.Tk()
    # sb.iconbitmap('AMS.ico')
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='#FAF1E4')

    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        # ec.iconbitmap('AMS.ico')
        ec.title('Warning!!')
        ec.configure(background='#FAF1E4')
        Label(ec, text='Please enter your subject name!!!', fg='red',
              bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        # Creatting csv of attendance

        # Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y')
        global subb
        subb = SUB_ENTRY.get()

        # Connect to the database
        # MySQL pwd: Xxxxxxxxxx
        # User: Me ------- pwd: Xxxxxxxxxx
        try:
            # Establish a connection to the MySQL server
            global cursor
            connection = pymysql.connect(
                host='localhost', user='root', password='Xxxxxxxxxx', db='Smart_GUI_Attendance')
            cursor = connection.cursor()

            # Define the table name and check if it exists
            DB_Table_name = subb
            table_exists_query = f"SHOW TABLES LIKE '{DB_Table_name}'"
            cursor.execute(table_exists_query)
            table_exists = cursor.fetchone()

            if not table_exists:
                # If the table doesn't exist, create it
                create_table_query = f"""
                    CREATE TABLE `{DB_Table_name}` (
                        ID INT NOT NULL AUTO_INCREMENT,
                        ENROLLMENT varchar(100) NOT NULL,
                        NAME VARCHAR(50) NOT NULL,
                        EMAIL VARCHAR(50) NOT NULL,
                        DATE VARCHAR(50) NOT NULL,
                        TIME VARCHAR(50) NOT NULL,
                        PRIMARY KEY (ID)
                    )
                """
                cursor.execute(create_table_query)
                # connection.commit()
                # for create a table
                # print('createddd')
        except Exception as ex:
            print(ex)  #

        if subb == '':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            # MFW.iconbitmap('AMS.ico')
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x700')
            MFW.configure(background='#FAF1E4')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                # errsc2.iconbitmap('AMS.ico')
                errsc2.title('Warning!!')
                errsc2.configure(background='#FAF1E4')
                Label(errsc2, text='Please enter Student Details!!!', fg='red', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="#9EB384",
                           font=('times', 15, ' bold '))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student Name", width=15, height=2, fg="black", bg="#9EB384",
                                font=('times', 15, ' bold '))
            STU_NAME.place(x=30, y=200)

            STU_EMAIL = tk.Label(MFW, text="Enter Student Email", width=15, height=2, fg="black", bg="#9EB384",
                                 font=('times', 15, ' bold '))
            STU_EMAIL.place(x=30, y=300)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key',
                                 bg="#F4EEEE", fg="black", font=('times', 23, ' bold '))
            ENR_ENTRY['validatecommand'] = (
                ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="#F4EEEE", fg="black", font=('times', 23, ' bold '))
            STUDENT_ENTRY.place(x=290, y=205)

            STUDENT_EMAIL = tk.Entry(
                MFW, width=20, bg="#F4EEEE", fg="black", font=('times', 23, ' bold '))
            STUDENT_EMAIL.place(x=290, y=305)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=30)

            def remove_email():
                STUDENT_EMAIL.delete(first=0, last=30)

            # get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                EMAIL = STUDENT_EMAIL.get()
                DB_Table_name = subb
                if ENROLLMENT == '':
                    err_screen1()
                elif STUDENT == '':
                    err_screen1()
                elif EMAIL == '':
                    err_screen1()
                else:
                    # SQL query to insert data into the table
                    insert_data_query = f"""
                        INSERT INTO `{DB_Table_name}` (ENROLLMENT, NAME, EMAIL, DATE, TIME)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    # Specify the values to be inserted
                    values = (ENROLLMENT, STUDENT, EMAIL, Date, timeStamp)

                    try:
                        print('inserting.....')
                        cursor.execute(insert_data_query, values)
                        connection.commit()
                        attendance_confirmation(EMAIL)
                        print('insertedddd successfully')
                    except Exception as e:
                        print(e)
                    remove_enr()
                    remove_student()
                    remove_email()

            def create_csv():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                EMAIL = STUDENT_EMAIL.get()

                student_data = [ENROLLMENT, STUDENT, EMAIL, Date, timeStamp]
                header = ["Enrollment", "Name", "Email", "Date", "Time"]
                csv_name = 'Attendance/Manual_Attendance/' + subb + '.csv'
                if not os.path.isfile(csv_name):
                    # File doesn't exist, write the header
                    with open(csv_name, 'w', newline='') as csvFile:
                        writer = csv.writer(csvFile, delimiter=',')
                        writer.writerow(header)

                with open(csv_name, 'a+') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(student_data)
                    msg = "CSV created Successfully"
                    Notifi.configure(text=msg, bg="goldenrod", fg="black",
                                     width=33, font=('times', 19, 'bold'))
                    Notifi.place(x=180, y=600)
                attendance_confirmation(EMAIL)

                root = tk.Tk()
                root.title("Attendance of " + subb)
                root.configure(background='#FAF1E4')
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = Label(root, width=30, height=1, fg="black", font=('times', 13, ' bold '),
                                          bg="gray62", text=row, relief=RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="goldenrod", fg="black", width=33,
                              height=2, font=('times', 19, 'bold'))

            clear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="black", bg="#435334", width=10,
                                     height=1,
                                     activebackground="dark sea green", font=('times', 15, ' bold '))
            clear_enroll.place(x=690, y=100)

            clear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="black", bg="#435334", width=10,
                                      height=1,
                                      activebackground="dark sea green", font=('times', 15, ' bold '))
            clear_student.place(x=690, y=200)

            clear_email = tk.Button(MFW, text="Clear", command=remove_email, fg="black", bg="#435334", width=10,
                                    height=1,
                                    activebackground="dark sea green", font=('times', 15, ' bold '))
            clear_email.place(x=690, y=300)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="#435334", width=20,
                                 height=2,
                                 activebackground="dark sea green", font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=400)

            MAKE_CSV = tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="black", bg="#435334", width=20,
                                 height=2,
                                 activebackground="dark sea green", font=('times', 15, ' bold '))
            MAKE_CSV.place(x=570, y=400)

            def attf():
                try:
                    # Specify the path to the "Attendance" folder
                    attendance_folder = 'Attendance'

                    # Open Windows Explorer to the specified directory
                    subprocess.Popen(
                        f'explorer /select,"{attendance_folder}"')

                except Exception as e:
                    print(f"Error: {e}")

            attf = tk.Button(MFW,  text="Check Sheets", command=attf, fg="black", bg="#435334",
                             width=12, height=1, activebackground="dark sea green", font=('times', 14, ' bold '))
            attf.place(x=730, y=510)

            MFW.mainloop()

    SUB = tk.Label(sb, text="Enter Subject", width=15, height=2,
                   fg="black", bg="#9EB384", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)

    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(sb, width=20, bg="#F4EEEE",
                         fg="black", font=('times', 23, ' bold '))
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="black", bg="#435334", width=20, height=2,
                                       activebackground="dark sea green", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()
