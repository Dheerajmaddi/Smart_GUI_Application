import cv2
import datetime
import time
import tkinter as tk
from tkinter import *
import os
import numpy as np
from PIL import Image
from register_csv import save_to_csv
from send_email import registration_succesful


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    # sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='#FAF1E4')
    Label(sc1, text='Enrollment & Name required!!!', fg='red',
          bg='yellow', font=('times', 16, ' bold ')).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="#435334",
           width=9, height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)


def del_sc1():
    sc1.destroy()

# Capture image of student


def take_img(studentId, studentName, studentEmail, Notification):
    idNumber = studentId.get()
    name = studentName.get()
    email = studentEmail.get()
    if idNumber == '':
        err_screen()
    elif name == '':
        err_screen()
    elif email == '':
        err_screen()
    else:
        try:
            Enrollment = studentId.get()
            Name = studentName.get()
            Email = studentEmail.get()

            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')

            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Email, Date, Time]
            save_to_csv(row)
            registration_succesful(Email)
            # with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            #     writer = csv.writer(csvFile, delimiter=',')
            #     writer.writerow(row)

        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="goldenrod", width=21)
            Notification.place(x=450, y=650)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


# Train the model
def trainimg(Notification):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces, Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l = 'Create a folder named "TrainingImage" to include Images'
        Notification.configure(text=l, bg="goldenrod", fg="black",
                               width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=650)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainer.yml")
    except Exception as e:
        q = 'Create a folder named "TrainingImageLabel"'
        Notification.configure(text=q, bg="goldenrod", fg="black",
                               width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=650)
