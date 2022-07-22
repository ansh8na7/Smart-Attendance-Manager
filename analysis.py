import os
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import datetime
import time
import pickle

isAnalyser = True

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

basedir = os.path.dirname(__file__)
attendanceDir = os.path.join(basedir, 'AttendanceCSV')
attendancePkl = os.path.join(basedir, 'AttendancePKL')
imageDir = os.path.join(basedir, 'Images')
studentDetailsDir = os.path.join(basedir, 'StudentDetails')
trainingImgDir = os.path.join(basedir, 'TrainingImage')
trainingImgLabelDir = os.path.join(basedir, 'TrainingImageLabel')

window = tk.Tk()
window.title("Smart Attendance System - Analysis")
window.geometry('1280x720')

bg = PhotoImage(file="./Images/bg4.png")

canvas = Canvas(window, width=700, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")


def resize_bg(e):
    global image, resized, image2
    image = Image.open("./Images/bg4.png")
    resized = image.resize((e.width, e.height), Image.Resampling.LANCZOS)

    image2 = ImageTk.PhotoImage(resized)
    canvas.create_image(0, 0, image=image2, anchor='nw')


window.bind("<Configure>", resize_bg)

title = Label(window, text="Smart Attendance System - Analysis", width=70, height=3,
              fg="Black", bg="orange", font=('Arial', 18, ' bold '))
title.place(x=250, y=25)

logoImg = PhotoImage(file='./Images/logo.png')
logoLabel = Label(window, image=logoImg, width=70, height=70)
logoLabel.place(x=25, y=25)


updateWindow = tk.Label(window, text="", bg="#E4DCCF", fg="Black", width=86, justify=LEFT,
                        height=20, font=('Arial', 15, ' bold '))

updateWindow.place(x=257, y=280)


def updateMessage(s):
    updateWindow.configure(text=s)


dateLabel = tk.Label(window, text="Date:", bg="orange", fg="Black", width=14,
                     height=2, font=('Arial', 15, ' bold '))
dateLabel.place(x=280, y=120)
dateEntry = tk.Entry(window, width=24, bg="#E4DCCF",
                     fg="Black", font=('Arial', 22))
dateEntry.insert(0, date)
dateEntry.place(x=460, y=120)


def clearDateEntry():
    dateEntry.delete(0, END)


def getAllDates():
    if not os.path.exists(os.path.join(attendancePkl, 'attendanceDB')):
        updateMessage("Record not found")
        return
    with open(os.path.join(attendancePkl, 'attendanceDB'), 'rb') as attendanceDbFile:
        attendanceDB = pickle.load(attendanceDbFile)
        msgString = "Dates available:\n"
        for date in attendanceDB.keys():
            msgString += date+'\n'
        updateMessage(msgString)


def getAllStudentData():
    if not os.path.exists(os.path.join(studentDetailsDir, "StudentDetailsDB")):
        updateMessage("Record not found")
    with open(os.path.join(studentDetailsDir, "StudentDetailsDB"), 'rb') as studentDbFile:
        studentDb = pickle.load(studentDbFile)
        msgString = "Id\tname\tphone\n"
        Ids = sorted(studentDb.keys())
        for Id in Ids:
            msgString += str(Id)+"\t" + \
                studentDb[Id][0]+"\t"+studentDb[Id][1]+"\n"
        updateMessage(msgString)


def studentsPresent():
    date = dateEntry.get()
    if not os.path.exists(os.path.join(attendancePkl, 'attendanceDB')):
        updateMessage("Record not found")
        return
    studentDb = dict()
    with open(os.path.join(studentDetailsDir, "StudentDetailsDB"), 'rb') as studentDbFile:
        studentDb = pickle.load(studentDbFile)
    with open(os.path.join(attendancePkl, "attendanceDB"), 'rb') as attendanceDbFile:
        attendanceDb = pickle.load(attendanceDbFile)
        msgString = "Students Present on "+date+":\nId\tName\n"
        if date not in attendanceDb.keys():
            updateMessage("Record not found")
            return
        Ids = sorted(list(attendanceDb[date]))
        for Id in Ids:
            msgString += str(Id)+"\t"+studentDb[Id][0]+"\n"
        updateMessage(msgString)


def studentsAbsent():
    date = dateEntry.get()
    if not os.path.exists(os.path.join(attendancePkl, 'absentDB')):
        updateMessage("Record not found")
        return
    studentDb = dict()
    with open(os.path.join(studentDetailsDir, "StudentDetailsDB"), 'rb') as studentDbFile:
        studentDb = pickle.load(studentDbFile)
    with open(os.path.join(attendancePkl, "absentDB"), 'rb') as attendanceDbFile:
        absentDb = pickle.load(attendanceDbFile)
        msgString = "Students Absent on "+date+":\nId\tName\n"
        if date not in absentDb.keys():
            updateMessage("Record not found")
            return
        Ids = sorted(list(absentDb[date]))
        for Id in Ids:
            msgString += str(Id)+"\t"+studentDb[Id][0]+"\n"
        updateMessage(msgString)


dateClearBtn = tk.Button(window, text="Clear", command=clearDateEntry, fg="Black", bg="orange",
                         width=15, height=2, activebackground="blue", font=('times', 14))
dateClearBtn.place(x=850, y=120)

allDatesBtn = tk.Button(window, text="Working days", command=getAllDates, fg="Black", bg="orange",
                        width=15, height=2, activebackground="blue", font=('times', 14))
allDatesBtn.place(x=250, y=220)

allStudentDetailsBtn = tk.Button(window, text="All Students' Data", command=getAllStudentData, fg="Black", bg="orange",
                                 width=15, height=2, activebackground="blue", font=('times', 14))
allStudentDetailsBtn.place(x=470, y=220)

studentsPresentListBtn = tk.Button(window, text="Students Present", command=studentsPresent, fg="Black", bg="orange",
                                   width=15, height=2, activebackground="blue", font=('times', 14))
studentsPresentListBtn.place(x=680, y=220)

studentsAbsentListBtn = tk.Button(window, text="Students Absent", command=studentsAbsent, fg="Black", bg="orange",
                                  width=15, height=2, activebackground="blue", font=('times', 14))
studentsAbsentListBtn.place(x=885, y=220)


def exitWindow():
    window.after(500, window.destroy)


exitBtn = tk.Button(window, text="Exit", command=exitWindow, fg="Black", bg="orange",
                    width=15, height=3, activebackground="blue", font=('times', 15, ' bold '))
exitBtn.place(x=1150, y=22)


window.mainloop()
