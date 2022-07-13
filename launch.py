
# Import module
from tkinter import *
import tkinter as tk
from tkinter import Message, Text
import cv2
import os
# import shutil
import csv
import numpy as np
# from PIL import Image, ImageTk
# import pandas as pd
import datetime
import time
# import tkinter.ttk as ttk
# import tkinter.font as font
# import time
# import re
# from tensorflow.keras.utils import img_to_array
# import imutils
# import cv2
# from keras.models import load_model
# import numpy as np
import serial
# from PIL.ImageTk import PhotoImage
from PIL import ImageTk, Image

try:
    fingerData = serial.Serial(
        '/dev/tty.usbserial-1410',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # must use when using data.readline()
    )
except serial.serialutil.SerialException:
    print("Connect the Fingerprint setups")
    # exit(1)

# read fingerprint


# def readFinger():
#     return 2

def readFinger():
    updateMessage("Place finger on sensor")
    while True:
        fId = fingerData.read(1)
        fId = fId.decode('UTF-8', 'ignore')
        if fId.isdigit():
            print('FIngerprint Confirmation Recived', fId)
            return fId


# parameters for loading data and images
detection_model_path = './haarcascade_frontalface_default.xml'
# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')


basedir = os.path.dirname(__file__)
attendanceDir = os.path.join(basedir, 'Attendance')
imageDir = os.path.join(basedir, 'Images')
studentDetailsDir = os.path.join(basedir, 'StudentDetails')
trainingImgDir = os.path.join(basedir, 'TrainingImage')
trainingImgLabelDir = os.path.join(basedir, 'TrainingImageLabel')

if not os.path.exists(attendanceDir):
    os.mkdir(attendanceDir)
if not os.path.exists(studentDetailsDir):
    os.mkdir(studentDetailsDir)
if not os.path.exists(trainingImgDir):
    os.mkdir(trainingImgDir)
if not os.path.exists(trainingImgLabelDir):
    os.mkdir(trainingImgLabelDir)


if not os.path.exists(os.path.join(studentDetailsDir, 'StudentDetails.csv')):
    with open(os.path.join(studentDetailsDir, 'StudentDetails.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Id", "Name", "Phone"])

attendanceFileName = 'Attendance-'+date+'.csv'
if not os.path.exists(os.path.join(attendanceDir, attendanceFileName)):
    with open(os.path.join(attendanceDir, attendanceFileName), 'a+') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Id", "Name", "Phone"])

if not os.path.exists(os.path.join(attendanceDir, attendanceFileName)):
    print("file not found")
    with open(os.path.join(attendanceDir, attendanceFileName), 'a+') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([date])


def TakeImages():
    Id = idEntry.get()
    name = nameEntry.get()
    phone = phEntry.get()

    if not Id.isdigit():
        updateMessage("Enter a numeric Id")
        return
    if name == '':
        updateMessage("Enter a valid name")
        return
    if not (phone.isdigit() and len(phone) == 10):
        updateMessage("Enter a valid phone number of 10 digits")
        return
    # Id = 5
    # name = 'ansh'
    # phone = '1234567890'
    cam = cv2.VideoCapture(0)
    harcascadePath = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0

    while True:
        _, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
            cv2.imwrite(os.path.join(trainingImgDir, str(Id) + "-" +
                                     str(sampleNum)+".jpg"), gray[y:y+h, x:x+w])
        cv2.imshow('Register Face', img)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        if sampleNum > 10:
            break

    cam.release()
    cv2.destroyAllWindows()
    row = [Id, name, phone]
    with open(os.path.join(studentDetailsDir, 'StudentDetails.csv'), 'a+') as studentcsv:
        writer = csv.writer(studentcsv)
        writer.writerow(row)
    studentcsv.close()
    updateMessage("Images taken for Id: "+str(Id)+" Name:"+name)


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[0].split('-')[0])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrainImages():
    #recognizer =cv2.face_LBPHFaceRecognizer.create()
    # cv2.face.LBPHFaceRecognizer_create()#$  cv2.face_LBPHFaceRecognizer.create()
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save(os.path.join(trainingImgLabelDir, "trainingData.yml"))
    message.configure(text="Image Trained")


def RegisterFace():
    TakeImages()
    TrainImages()


def TakeAttendance():
    fingerId = readFinger()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(os.path.join(trainingImgLabelDir, 'trainingData.yml'))
    harcascadePath = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    c = 0
    attendanceGiven = ""
    proxyAttempt = ""
    while True:
        _, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        c += 1
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            ids, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50 and ids == int(fingerId):
                cv2.putText(img, str(ids), (x, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 255, 0), 2)
                attendanceGiven = str(ids)
            else:
                cv2.putText(img, "proxy attempt by "+str(ids), (x, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 255, 0), 2)
                proxyAttempt = str(ids)
            # print(ids, conf)
        cv2.imshow("Attendance", img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        if c > 50:
            break
    cam.release()
    cv2.destroyAllWindows()
    if attendanceGiven != "":
        updateMessage("attendance given to "+attendanceGiven)
    elif proxyAttempt != "":
        updateMessage("proxy attempt by "+proxyAttempt)


# GUI
window = tk.Tk()
window.title("Smart Attendance System")
window.geometry('1280x720')

# Add image file
bg = PhotoImage(file="./Images/bg4.png")

# Create Canvas
canvas = Canvas(window, width=700, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")


def resize_bg(e):
    global image, resized, image2
    # open image to resize it
    image = Image.open("./Images/bg4.png")
    # resize the image with width and height of root
    resized = image.resize((e.width, e.height), Image.Resampling.LANCZOS)

    image2 = ImageTk.PhotoImage(resized)
    canvas.create_image(0, 0, image=image2, anchor='nw')


# Bind the function to configure the parent window
window.bind("<Configure>", resize_bg)

title = Label(window, text="Smart Attendance System", width=70, height=3,
              fg="Black", bg="orange", font=('Arial', 18, ' bold '))
title.place(x=250, y=25)

logoImg = PhotoImage(file='./Images/logo.png')
logoLabel = Label(window, image=logoImg, width=70, height=70)
logoLabel.place(x=25, y=25)


idLabel = tk.Label(window, text="Enter ID", width=18, height=2,
                   fg="Black", bg="orange", font=('Arial', 15, ' bold '))
idLabel.place(x=350, y=120)

idEntry = tk.Entry(window, width=24, bg="White",
                   fg="Black", font=('Arial', 22))
idEntry.place(x=570, y=120)

nameLabel = tk.Label(window, text="Enter Name", width=18,
                     fg="Black", bg="orange", height=2, font=('Arial', 15, ' bold '))
nameLabel.place(x=350, y=180)

nameEntry = tk.Entry(window, width=24, bg="White",
                     fg="Black", font=('Arial', 22))
nameEntry.place(x=570, y=180)

phLabel = tk.Label(window, text="Enter Phone NO", width=18, fg="Black",
                   bg="orange", height=2, font=('Arial', 15, ' bold '))
phLabel.place(x=350, y=240)

phEntry = tk.Entry(window, width=24, bg="White",
                   fg="Black", font=('Arial', 22, ' bold '))
phEntry.place(x=570, y=240)

updateLabel = tk.Label(window, text=" Updates: ", width=18, fg="Black",
                       bg="orange", height=3, font=('Arial', 15, ' bold '))
updateLabel.place(x=350, y=300)

message = tk.Label(window, text="", bg="White", fg="Black", width=36,
                   height=3, activebackground="Green", font=('Arial', 15, ' bold '))
message.place(x=570, y=300)

attendance = tk.Label(window, text=" Attendance: ", width=18, fg="Black",
                      bg="orange", height=3, font=('Arial', 15, ' bold '))
attendance.place(x=350, y=550)


attMessage = tk.Label(window, text="", bg="White", fg="Black", width=36,
                      height=3, activebackground="Green", font=('Arial', 15, ' bold '))
attMessage.place(x=550, y=550)

# buttons placement


def temp():
    message.configure(text="button not in use")
    return


def updateMessage(msg):
    message.configure(text=msg)


takeImgBtn = tk.Button(window, text="Take Images", command=temp, fg="Black", highlightbackground='#3E4149',
                       width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
takeImgBtn.place(x=300, y=420)
registerImgBtn = tk.Button(window, text="Register", command=RegisterFace, fg="Black", bg="orange",
                           width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
registerImgBtn.place(x=500, y=420)
takeAttBtn = tk.Button(window, text="Take Attendance", command=TakeAttendance, fg="Black",
                       bg="orange", width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
takeAttBtn.place(x=700, y=420)
sensSMSbtn = tk.Button(window, text="Send Absent SMS", command=temp, fg="Black", bg="orange",
                       width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
sensSMSbtn.place(x=900, y=420)


def exitWindow():

    updateMessage('exiting software...')
    window.after(500, window.destroy)


exitBtn = tk.Button(window, text="Exit", command=exitWindow, fg="Black", bg="orange",
                    width=15, height=3, activebackground="blue", font=('times', 15, ' bold '))
exitBtn.place(x=1150, y=22)

window.mainloop()
