# coding=utf-8
import base64
import ctypes
import json
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
import sys
import os.path

import msvcrt

import keyring
from imapclient import IMAPClient


import imaplib
imaplib._MAXLINE = 40000
__author__ = 'Quoc Lap'
import winsound
import os
import threading
import logging
import ftplib
import socket
import ctypes
import platform
import sys
import time
import subprocess
import time
import shutil
import datetime
import tkinter
from tkinter import *
import threading
import pygame as pg
import pyscreenshot as ImageGrab
import getpass

LocalDirectVideo = r"E:/Foscam/record/"
LocalDirectImage = r"E:/Foscam/snap/"


TIME_OUT = 1000 # seconds
TIME_WAIT = 10 # seconds
NumFile = 150
LIMIT_STORAGE_VIDEO = 13*1024
LIMIT_STORAGE_IMAGE = 2*1024
FROM = "cameraposcam@gmail.com"
TO = "cameraposcam@yahoo.com"
SYSTEM = "system"
PASSMAIL = ""
PASSFTP = ""
USERMAIL =""
IPFOSCAM = ""
PORTFOSCAM = ""
USERLOGIN = ""

from easygui import passwordbox



def SaveData():

    dataObject = {IPFOSCAM,PORTFOSCAM, USERLOGIN, USERMAIL, PASSFTP, PASSMAIL, FROM, TO}
    print(json.dumps(dataObject,default=jdefault))
    # file = open("data.txt","w")
    # file.write(IPFOSCAM + os.linesep)
    # file.write(PORTFOSCAM + os.linesep)
    # file.write(USERLOGIN + os.linesep)
    # file.write(FROM + os.linesep)
    # file.write(TO + os.linesep)
    # keyring.set_password(SYSTEM,USERLOGIN,PASSFTP)
    # keyring.set_password(SYSTEM,USERMAIL,PASSMAIL)


def jdefault(o):
    return list(o)


def FirstSetup():
     global IPFOSCAM, PORTFOSCAM, USERLOGIN, USERMAIL, PASSFTP, PASSMAIL, FROM, TO
     print("**** Set up information ****")
     IPFOSCAM = input('Enter your Foscam IP: ')
     PORTFOSCAM = input('Enter your Foscam Port: ')
     USERLOGIN = input('Enter your Username: ')
     PASSFTP = passwordbox("Enter your password: ")
     FROM = input("Enter email to send: ")
     PASSMAIL = passwordbox("Enter email password: ")
     TO = input("Enter email to be sent: ")


def GetData():
    global IPFOSCAM, PORTFOSCAM, USERLOGIN, USERMAIL, PASSFTP, PASSMAIL, FROM, TO
    file = open("data.txt","r")
    temp = file.read().splitlines()
    while '' in temp : temp.remove('')
    IPFOSCAM = temp
    PORTFOSCAM = file.readline().strip()
    USERLOGIN = file.readline().strip()
    FROM  = file.readline().strip()
    TO = file.readline().strip()
    PASSFTP = keyring.get_password(SYSTEM,USERLOGIN)
    PASSMAIL = keyring.get_password(SYSTEM,USERMAIL)


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def Shutdown(*root):
    root[0].quit()
    CheckTasks[4] = 1
    ImageGrab.grab_to_file("Hibernate_"+str(datetime.datetime.now()).replace(".","").replace(":","") +".png")
    os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')


def ShutdownTask():
    root = tkinter.Tk()
    root.wm_title("FOSCAMRETRIEVING")
    root.focus_force()
    def Yes():
        shuttimer.cancel()
        Shutdown(root)
    def No():
        shuttimer.cancel()
        root.quit()

    b = Button(root, text="Yes", width=10, height=2, command=Yes)
    c = Button(root, text="No", width=10, height=2, command=No)
    b.grid(row=2,column=0, sticky=W,padx = 20)
    c.grid(row=2,column=1, sticky=W, padx = 20)

    textframe = Frame(root)
    textframe.grid(in_=root, row=1, column=0, columnspan=4, sticky=NSEW)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    label = Label(textframe,text ="Computer will SHUTDOWN in 60s", width = 50, height = 6)
    label.pack()

    #
    # # text = Text(root, width=35, height=15)
    # # scrollbar = Scrollbar(root)
    # # scrollbar.config(command=text.yview)
    # # text.config(yscrollcommand=scrollbar.set)
    # # scrollbar.pack(in_=textframe, side=RIGHT, fill=Y)
    # # text.pack(in_=textframe, side=LEFT, fill=BOTH, expand=True)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pg_play_music("alarm.wav",0.2)

    shuttimer =  threading.Timer(60, Shutdown,[root])
    shuttimer.start()

    root.mainloop()




def pg_play_music(music_file, volume=0.8):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment for good sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Playing file %s" % music_file)
    except pg.error:
        print("File %s not found! (%s)" % \
            (music_file, pg.get_error()))
        return
    pg.mixer.music.play()

    # check if playback has finished
    while pg.mixer.music.get_busy():
        clock.tick(30)


def Decode(val):
    val = base64.b64decode(val)
    val = val.decode('ascii')
    return val

def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024



class Callback(object):
    def __init__(self, totalsize, fp):
        self.totalsize = totalsize
        self.fp = fp
        self.received = 0

    def __call__(self, data):
        self.fp.write(data)
        self.received += len(data)
        print('\r%.3f%%' % (100.0*self.received/self.totalsize),"\r")
        if timerthread[0] is not None:
          timerthread[0].cancel()
        timerthread[0] = threading.Timer(TIME_OUT, timeout)
        timerthread[0].start()




def Retrieve_Video():
    global Name, Read_only
    os.chdir(LocalDirectVideo)
    print()
    print()
    print("Moving videos to " + LocalDirectVideo)
    VideoDir = "/IPCamera/FI9826P_00626E5485D1/record/"

    ftp.cwd(VideoDir)
    dates = ftp.nlst()

    for date in dates:
        if get_free_space_mb(LocalDirectVideo) < LIMIT_STORAGE_VIDEO:
            continue;
        ftp.cwd(VideoDir + date)
        if not os.path.exists(LocalDirectVideo + date + "/") :
           os.makedirs(LocalDirectVideo + date + "/")

        os.chdir(date)
        times = ftp.nlst()

        if len(times) > 0:
            for time in times:
                print()
                print("Current Folder: " + time)
                print("Checking...")
                if not os.path.exists(LocalDirectVideo + date + "/" + time + "/"):
                    os.makedirs(LocalDirectVideo + date + "/" + time + "/")
                os.chdir(time)
                ftp.cwd(time)
                files = ftp.nlst("*.*")
                count =0
                for file in files:
                    if file in ListIgnoreVideos:
                        count = count+1
                        continue
                    CurFile = file
                    count = count + 1
                    print (count.__str__() + "/" + len(files).__str__() +" -- " + " Getting => " + file)
                    size = ftp.size(file)
                    dest = file
                    f = open(dest, 'wb')
                    w = Callback(size, f)
                    try:
                        # if Name == file and Read_only:
                        #     print("Try deleting first!")
                        #     ftp.delete(file)
                        ftp.retrbinary('RETR %s' % file, w, 32127)
                    except ftplib.all_errors as e:
                        if "451-Error" in str(e):
                            print("451-Error occurs!")
                            print("Trying delete the file " + file +" and reprocess...")
                            try:
                                ftp.delete(file)
                                print("     Deleted on SDCard!")
                            except ftplib.all_errors as f:
                                if "Read-only" in str(f):
                                    print("Save file and value")
                                    ListIgnoreVideos.append(file)
                                    Name = file
                                    Read_only = True
                                    raise f
                        raise e
                    try:

                        ftp.delete(file)
                        print("     Deleted on SDCard!")
                    except ftplib.all_errors as d:
                         if "Read-only" in str(d):
                                    print("Save file and value")
                                    Name = file
                                    ListIgnoreVideos.append(file)
                                    Read_only = True
                                    raise d
                    f.close()

                ftp.cwd(VideoDir + date)
                if not ListIgnoreVideos:
                    ftp.rmd(time)
                os.chdir(LocalDirectVideo + date + "/")

            ftp.cwd(VideoDir)
            if not ListIgnoreVideos:
                ftp.rmd(date)
                print(" Deleted folder " + date)
          #  ListIgnoreVideos.clear()       Avoid loop
        ftp.cwd(VideoDir)
        os.chdir(LocalDirectVideo)
    CheckTasks[1] = 1

def Retrieve_Image():
    global Name, Read_only
    os.chdir(LocalDirectImage)
    print()
    print()
    print("Moving photos to " + LocalDirectImage)
    ImageDir = "/IPCamera/FI9826P_00626E5485D1/snap/"

    ftp.cwd(ImageDir)
    dates = ftp.nlst()
    if get_free_space_mb(LocalDirectImage) < LIMIT_STORAGE_IMAGE:
        return
    if len(dates) > 0:
        ftp.cwd(dates[0])
        if not os.path.exists(LocalDirectImage + dates[0] + "/") :
           os.makedirs(LocalDirectImage + dates[0] + "/")
        os.chdir(dates[0] + "/")
        times = ftp.nlst()

        if len(times) > 0:
            for time in times:
                print()
                print("Current Folder: " + time)
                print("Checking...")
                if not os.path.exists(LocalDirectImage + dates[0] + "/" + time + "/"):
                    os.makedirs(LocalDirectImage + dates[0] + "/" + time + "/")
                os.chdir(time)
                ftp.cwd(time)
                files = ftp.nlst("*.*")
                count =0
                for file in files:
                    if file in ListIgnoreImages:
                        count = count+1
                        continue
                    count = count + 1
                    print (count.__str__() + "/" + len(files).__str__() +" -- " + " Getting => " + file)
                    size = ftp.size(file)
                    dest = file
                    f = open(dest, 'wb')
                    w = Callback(size, f)
                    try:
                        # if Name == file and Read_only:
                        #     print("Try deleting first!")
                        #     ftp.delete(file)
                        ftp.retrbinary('RETR %s' % file, w, 32127)
                    except ftplib.all_errors as e:
                        if "451-Error" in str(e):
                            print("451-Error occurs!")
                            print("Trying delete the file " + file +" and reprocess...")

                            try:
                                ftp.delete(file)
                                print("     Deleted on SDCard!")
                            except ftplib.all_errors as f:
                                if "Read-only" in str(f):
                                    print("Save file and value")
                                    ListIgnoreImages.append(file)
                                    Name = file
                                    Read_only = True
                                    raise f
                        raise e

                    try:

                        ftp.delete(file)
                        print("     Deleted on SDCard!")
                    except ftplib.all_errors as d:
                         if "Read-only" in str(d):
                                    print("Save file and value")
                                    Name = file
                                    ListIgnoreImages.append(file)
                                    Read_only = True
                                    raise d
                    f.close()
                ftp.cwd(ImageDir + dates[0])
                if not ListIgnoreImages:
                    ftp.rmd(time)
                os.chdir(LocalDirectImage + dates[0] + "/")
         #       ListIgnoreImages.clear()       Avoid loop
        ftp.cwd(ImageDir + dates[0])
        times = ftp.nlst()
        ftp.cwd(ImageDir)
        if not times:
               ftp.rmd(dates[0])
               print(" Deleted folder " + dates[0])
    CheckTasks[0] = 1


def Delete_Video():         #Delete on local computer to release storage
    os.chdir(LocalDirectVideo)
    dates = os.listdir(LocalDirectVideo)
    for date in dates:
        if get_free_space_mb(LocalDirectVideo) < LIMIT_STORAGE_VIDEO:
            shutil.rmtree(date)
            print()
            print(date)
            print("Deleted " +  date + " on " + LocalDirectVideo)
        else: break
    CheckTasks[3] = 1


def Delete_Image():         #Delete on local computer to release storage
    os.chdir(LocalDirectImage)
    dates = os.listdir(LocalDirectImage)
    year = dates[0][:4]
    month = dates[0][4:6]
    day = dates[0][6:]
    date = datetime.datetime(int(year),int(month),int(day))
    inter = datetime.datetime.now() - date
    DeleteMail()
    if inter.days > 10:
            sendImage(FROM,TO,"Send images foscam",dates[0])
            DeleteMail()
            os.chdir(LocalDirectImage)
            shutil.rmtree(LocalDirectImage + dates[0])
            print()
            print(dates)
            print("Deleted " +  dates[0] + " on " + LocalDirectImage)
    CheckTasks[2] = 1


def timeout():  # may not work according to docs
  print("Timeout!  Reprocress...")
  StartProgram()





def sendImage(FROM,TO,TEXT,date):
    os.chdir(LocalDirectImage+date)
    times = os.listdir(LocalDirectImage+date)
    for timepart in times:
        time = os.listdir(LocalDirectImage+date + "/" +timepart)
        i=1;
        print("Folder: " + timepart + " - " + str(time.__len__()))
        if time.__len__() is 0 : continue
        while NumFile*i < time.__len__():
            files = time[(i-1)*NumFile:i*NumFile]
            sendImagePart(FROM,TO,TEXT,files,LocalDirectImage+date + "/"+timepart)
            i +=1
            for file in files:
                 os.remove(LocalDirectImage+date+"/"+timepart+"/"+file)
        files = time[(i-1)*NumFile:time.__len__()]
        sendImagePart(FROM,TO,TEXT,files,LocalDirectImage+date + "/"+timepart)
        shutil.rmtree(LocalDirectImage+date+"/"+timepart)


def IsDetected(file):
        try:
            img_data = open(file, 'rb').read()
            #print(file)
            image = MIMEImage(img_data, name=os.path.basename(file))
            return image
        except:
            #print("Fail to detect!")
            return None

def sendImagePart(FROM,TO,TEXT,files,DIRECT):
    SERVER = "smtp.gmail.com"
    server = smtplib.SMTP(SERVER,25)
    server.starttls()
    server.login(FROM, Decode(PASSMAIL))
    msg = MIMEMultipart()
    Subject = "From " + files[0] + " To " + files[files.__len__()-1]
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] =  Subject

    body = TEXT
    msg.attach(MIMEText(body, 'plain'))

    print("Sending " + Subject + "...")

    for file in files:
        if ".jpg" not in file or os.path.getsize(DIRECT +"/"+ file) <= 0: continue
        ImgFileName = DIRECT +"/"+ file
        image = IsDetected(ImgFileName)
        #print(file)
        if image is not None:
            msg.attach(image)

    text = msg.as_string()
    server.sendmail(FROM, TO, text)

    print("An email data was sent to " + TO + " !")
    print()
    server.quit()






def sendMail(FROM,TO,SUBJECT,TEXT):
    """this is some test documentation in the function"""

    # Send the mail
    SERVER = "smtp.gmail.com"
    server = smtplib.SMTP(SERVER,25)
    server.starttls()
    server.login(Decode(USERMAIL), Decode(PASSMAIL))

    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = SUBJECT

    body = TEXT
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail(FROM, TO, text)

    print("An email was sent to " + TO + " !")
    print()
    server.quit()




def DeleteMail():
    client = IMAPClient('imap.googlemail.com', use_uid=True, ssl=True)
    client.login(FROM, Decode(PASSMAIL))
    folders = [
        'INBOX',
        '[Gmail]/Drafts',
        '[Gmail]/Important',
        '[Gmail]/Sent Mail',
        '[Gmail]/Spam',
        '[Gmail]/Starred',
        '[Gmail]/Trash'
    ]

    #for f in folders:
    fold = client.select_folder(folders[3])
    print(client.search())
    res = client.delete_messages(client.search())
    res = client.expunge()
    client.close_folder()

    fold = client.select_folder(folders[6])
    print(client.search())
    res = client.delete_messages(client.search())
    res = client.expunge()
    client.close_folder()

    #Google automatically will move deleted messages to "All Mail" folder.
    #Now we can remove all messages from "All Mail"

    client.select_folder("[Gmail]/All Mail")
    client.set_gmail_labels(client.search(), '\\Trash')
    client.delete_messages(client.search())
    client.expunge()
    client.logout()
    print("Sent mails are deleted!")




def StartProgram():
    global Read_only
    global ftp
    try:
        ftp = ftplib.FTP()
        ftp.connect('192.168.1.25',50021)
        ftp.login('Trieuthai089',Decode(PASSFTP))
        ftp.set_pasv(False)
        Read_only = False
        print("RunTask ...")
        RunTasks()
        ftp.quit()

    except ftplib.all_errors as e:
        ftp.close()
        timerthread[0].cancel()

        if Read_only is not True:
            print("Something went wrong! " + str(e))
            print(" Reprocessing in " + str(TIME_WAIT) + " seconds..." )
            time.sleep(TIME_WAIT)
        else:
            print("Ignore! Next...")
        StartProgram()
    finally:
        ftp.close()



def RunTasks():

    if CheckTasks[0] is 0:   Retrieve_Image()
    if CheckTasks[1] is 0:   Retrieve_Video()
    timerthread[0].cancel()
    if CheckTasks[2] is 0:   Delete_Image()
    if CheckTasks[3] is 0:   Delete_Video()
    sendMail(FROM,TO,"Done!","The Process ends at " + str(datetime.datetime.now()))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ImageGrab.grab_to_file("ScreenShot_"+str(datetime.datetime.now()).replace(".","").replace(":","") +".png")
    if CheckTasks[4] is 0: ShutdownTask()



if __name__ == '__main__':

        global CheckTasks
        global ListIgnoreVideos
        global ListIgnoreImages
        global Name
        global Read_only
        global timerthread
        Read_only = False
        Name = ""
        ListIgnoreImages = []
        ListIgnoreVideos = []
        CheckTasks = [0,0,0,0,0]
        timerthread = [threading.Timer(TIME_OUT, timeout)]
        sendMail(FROM,TO,"Retrieving...","The Process starts at " + str(datetime.datetime.now()))
        ftp = ftplib.FTP()
        ftp.connect(IPFOSCAM,PORTFOSCAM)
        ftp.login(USERLOGIN,Decode(PASSFTP))
        ftp.set_pasv(False)
        StartProgram()


        #FirstSetup()
        SaveData()
       # GetData()
        print(IPFOSCAM ," - ",PORTFOSCAM," - ",USERLOGIN, " - ",USERMAIL," -  ",PASSFTP,"  - ",PASSMAIL)
        print("Process done!")



