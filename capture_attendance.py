import time
import tkinter as tk
from tkinter import *
import cv2
import pandas as pd
import datetime
import csv
import pymysql.connections
import subprocess
import os
from send_email import attendance_confirmation


def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    # sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='#FAF1E4')
    Label(sc2, text='Please enter your subject name!!!', fg='red',
          bg='yellow', font=('times', 16, ' bold ')).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="#435334", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)


# for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub = subject.get()
        now = time.time()  # For calculate seconds of video
        future = now + 20
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("TrainingImageLabel/Trainer.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notification.configure(
                        text=e, bg="goldenrod", fg="black", width=33, font=('times', 15, 'bold'))
                    Notification.place(x=20, y=250)
                    windo.after(3000, lambda: Notification.place_forget())

                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Email', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf < 70):
                            # print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = subject.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%m-%d-%Y')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            # print(aa)
                            e = df.loc[df['Enrollment'] == Id]['Email'].values

                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [
                                Id, aa, e, date, timeStamp]
                            cv2.rectangle(
                                im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y),
                                        font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(
                                im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y),
                                        font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")

                fileName1 = "Attendance/" + Subject + ".csv"
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                # print(attendance)

                attendance['Name'] = attendance['Name'].apply(
                    lambda x: ', '.join(x))
                attendance['Email'] = attendance['Email'].apply(
                    lambda x: ', '.join(x))
                student_data = attendance.iloc[0].to_list()

                # print(student_data)

                header = ["Enrollment", "Name", "Email", "Date", "Time"]

                if not os.path.isfile(fileName1):
                    # File doesn't exist, write the header
                    with open(fileName1, 'w', newline='') as csvFile:
                        writer = csv.writer(csvFile, delimiter=',')
                        writer.writerow(header)

                with open(fileName1, 'a+') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(student_data)

                try:
                    # Establish a connection to the MySQL server
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='Xxxxxxxxxx', db='Smart_GUI_Attendance')
                    cursor = connection.cursor()

                    # Define the table name and check if it exists
                    DB_Table_name = Subject
                    table_exists_query = f"SHOW TABLES LIKE '{DB_Table_name}'"
                    cursor.execute(table_exists_query)
                    table_exists = cursor.fetchone()

                    if not table_exists:
                        # If the table doesn't exist, create it
                        create_table_query = f"""
                            CREATE TABLE {DB_Table_name} (
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
                        connection.commit()

                    student_name = str(aa)[1:-1]
                    # print(e)
                    student_email = str(e)[1:-1]
                    date = datetime.datetime.fromtimestamp(
                        ts).strftime('%m-%d-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(
                        ts).strftime('%H:%M:%S')

                    # SQL query to insert data into the table
                    insert_data_query = f"""
                        INSERT INTO {DB_Table_name} (ENROLLMENT, NAME, EMAIL, DATE, TIME)
                        VALUES ({str(Id)}, {student_name}, {student_email}, '{date}', '{timeStamp}')
                    """

                    # Execute the INSERT query
                    cursor.execute(insert_data_query)
                    connection.commit()

                    attendance_confirmation(student_data[2])

                except Exception as e:
                    print(e)

                finally:
                    # Close the cursor and connection
                    cursor.close()
                    connection.close()
                    print("Insertion Successfull!!!!!!")

                M = 'Attendance filled Successfully'
                Notification.configure(
                    text=M, bg="goldenrod", fg="black", width=33, font=('times', 15, 'bold'))
                Notification.place(x=20, y=250)
                windo.after(3000, lambda: Notification.place_forget())

                cam.release()
                cv2.destroyAllWindows()

                root = tk.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='#FAF1E4')
                cs = fileName1
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = Label(root, width=30, height=1, fg="black", font=('times', 15, ' bold '),
                                          bg="gray62", text=row, relief=RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                # print(attendance)

    # windo is frame for subject chooser
    windo = tk.Tk()
    # windo.iconbitmap('AMS.ico')
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='#FAF1E4')
    Notification = tk.Label(windo, text="Attendance filled Successfully", bg="goldenrod", fg="black", width=33,
                            height=2, font=('times', 15, 'bold'))

    def Attf():
        try:
            # Specify the path to the "Attendance" folder
            attendance_folder = 'Attendance'

            # Open Windows Explorer to the specified directory
            subprocess.Popen(
                f'explorer /select,"{attendance_folder}"')

        except Exception as e:
            print(f"Error: {e}")

    attf = tk.Button(windo,  text="Check Sheets", command=Attf, fg="black", bg="#435334",
                     width=12, height=1, activebackground="Red", font=('times', 14, ' bold '))
    attf.place(x=430, y=255)

    sub = tk.Label(windo, text="Enter Subject", width=15, height=2,
                   fg="black", bg="#9EB384", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    subject = tk.Entry(windo, width=20, bg="#F4EEEE",
                       fg="black", font=('times', 23, ' bold '))
    subject.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="black", command=Fillattendances, bg="#435334", width=20, height=2,
                       activebackground="dark sea green", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()
