import os
from PIL import ImageTk, Image
import numpy as np
import csv

basedir = os.path.dirname(__file__)
attendanceDir = os.path.join(basedir, 'Attendance')
imageDir = os.path.join(basedir, 'Images')
studentDetailsDir = os.path.join(basedir, 'StudentDetails')
trainingImgDir = os.path.join(basedir, 'TrainingImage')
trainingImgLabelDir = os.path.join(basedir, 'TrainingImageLabel')

date = "14-07-2022"
attendanceFileName = 'Attendance-'+date+'.csv'
if not os.path.exists(os.path.join(attendanceDir, attendanceFileName)):
    print("file not found")
    with open(os.path.join(attendanceDir, attendanceFileName), 'a+') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([date])
