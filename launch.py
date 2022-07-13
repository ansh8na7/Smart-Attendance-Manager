
# Import module
from tkinter import *
import tkinter as tk
from tkinter import Message, Text
import cv2
# import os
# import shutil
# import csv
# import numpy as np
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


def readFinger():
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


def resize_image(e):
    global image, resized, image2
    # open image to resize it
    image = Image.open("./Images/bg4.png")
    # resize the image with width and height of root
    resized = image.resize((e.width, e.height), Image.Resampling.LANCZOS)

    image2 = ImageTk.PhotoImage(resized)
    canvas.create_image(0, 0, image=image2, anchor='nw')


# Bind the function to configure the parent window
window.bind("<Configure>", resize_image)

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

updateMessage = tk.Label(window, text="", bg="White", fg="Black", width=36,
                         height=3, activebackground="Green", font=('Arial', 15, ' bold '))
updateMessage.place(x=570, y=300)

attendance = tk.Label(window, text=" Attendance: ", width=18, fg="Black",
                      bg="orange", height=3, font=('Arial', 15, ' bold '))
attendance.place(x=350, y=550)


attMessage = tk.Label(window, text="", bg="White", fg="Black", width=36,
                      height=3, activebackground="Green", font=('Arial', 15, ' bold '))
attMessage.place(x=550, y=550)

# buttons placement

takeImgBtn = tk.Button(window, text="Take Images", command=temp, fg="Black", highlightbackground='#3E4149',
                       width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
takeImgBtn.place(x=300, y=420)
registerImgBtn = tk.Button(window, text="Register", command=temp, fg="Black", bg="orange",
                           width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
registerImgBtn.place(x=500, y=420)
takeAttBtn = tk.Button(window, text="Take Attendance", command=temp, fg="Black",
                       bg="orange", width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
takeAttBtn.place(x=700, y=420)
sensSMSbtn = tk.Button(window, text="Send Absent SMS", command=temp, fg="Black", bg="orange",
                       width=15, height=2, activebackground="blue", font=('times', 15, ' bold '))
sensSMSbtn.place(x=900, y=420)

exitBtn = tk.Button(window, text="Exit", command=temp, fg="Black", bg="orange",
                    width=15, height=3, activebackground="blue", font=('times', 15, ' bold '))
exitBtn.place(x=1150, y=22)

window.mainloop()
