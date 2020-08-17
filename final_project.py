#import all modules-
from tkinter import *
import tkinter
import pyttsx3
import sqlite3
import tkinter.messagebox as tm
from tkinter import messagebox
import tkinter as tk 
from tkinter import Message, Text 
import cv2 
import os 
import shutil 
import csv 
import numpy as np 
from PIL import Image, ImageTk 
import pandas as pd 
import datetime 
import time 
import tkinter.ttk as ttk 
import tkinter.font as font 
from pathlib import Path 
engine=pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
#mark the attendance
def verify(aaa,w):
    df = pd.read_csv("UserDetails\\UserDetails.csv")
    col_names =  ['Id','name','Date','Time','TimeStamp']
    attendance = pd.DataFrame(columns = col_names)
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    tcs=date+' '+timeStamp
    Id=1
    aa=df.loc[df['Id'] == Id]['name'].values
    tt=str(Id)+"-"+aaa
    attendance.loc[len(attendance)] = [w,aaa[0],date,timeStamp,tcs]      
    attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="attendance\\attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=True)
def mark(aa):
    time.sleep(3)
    speak("hello Have a nice day")
    speak(aa)
    root=Tk()
    root.title("Attendence System")
    Label(root,text="").grid(row=0,column=0)
    btn_log1=Label(root,text=" "+aa+" ",width=10,height=2,
                           font=("times new roman",30,"bold"),fg="black").grid(row=1,column=1,pady=10)
    btn_log=Label(root,text="Verified",width=10,height=2,
                           font=("times new roman",40,"bold"),fg="green").grid(row=0,column=1,pady=10)
    root.after(5000,root.destroy)
    root.mainloop()
#code for detection the student face-
def test():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  
    recognizer.read("TrainingImageLabel\Trainner.yml")  
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath) 
    count=0
    df = pd.read_csv("UserDetails\\UserDetails.csv")   
    cam = cv2.VideoCapture(0) 
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True: 
        ret, im = cam.read() 
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)     
        for(x, y, w, h) in faces:
            count+=1
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2) 
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])                                    
            if(conf < 50):
                aa = df.loc[df['Id'] == Id]['name'].values 
                tt = str(Id)+"-"+aa
                speak("thank you")
                mark(aa[0])
                verify(aa,Id)
            else: 
                Id ='Unknown'                
                tt = str(Id)   
            if(conf > 75): 
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+ str(noOfFile) + ".jpg", im[y:y + h, x:x + w])             
            cv2.putText(im, str(tt), (x, y + h),font, 1, (255, 255, 255), 2)
            #speak("Sorry")
        cv2.imshow('im', im)  
        if (cv2.waitKey(1)== ord('q')): 
            break
    cam.release()
    cv2.destroyAllWindows()
#to save the record of student 
def fun4():
    def fun():
        cam = cv2.VideoCapture(0)
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        name = n1.get()
        count = 0
        Id=u1.get()
        while(True):
            _, image_frame = cam.read()
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1
                #cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imwrite( "TrainingImage\ "+name +"."+str(Id) +'.'+ str(count) + ".jpg", gray[y:y + h, x:x + w]) 
                cv2.imshow('frame', image_frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif count>60:
                break
        cam.release()
        cv2.destroyAllWindows()
        row=[Id,name]
        with open('UserDetails\\UserDetails.csv', 'a+') as csvFile: 
            writer = csv.writer(csvFile) 
            writer.writerow(row)  
        csvFile.close()
    def save_data():
        con=sqlite3.connect('C:\\Users\\Priyanka\\Desktop\\Final_Year_project\\final_year_data.db')
        cursorObj=con.cursor()
        #cursorObj.execute('CREATE TABLE Final_Year_Data(Id primary KEY,Name)')
        cursorObj.execute('INSERT INTO Final_Year_Data(Id,Name) VALUES (?,?)',(u1.get(),n1.get()))
        con.commit()
    def TrainImages(): 
        recognizer = cv2.face.LBPHFaceRecognizer_create()   
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath) 
        faces, Id = getImagesAndLabels("TrainingImage")  
        recognizer.train(faces, np.array(Id))      
        recognizer.save("TrainingImageLabel\Trainner.yml")  
    def getImagesAndLabels(path): 
        imagePaths =[os.path.join(path, f) for f in os.listdir(path)]
        faces =[] 
        Ids =[] 
        for imagePath in imagePaths: 
            pilImage = Image.open(imagePath).convert('L') 
            imageNp = np.array(pilImage, 'uint8') 
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp) 
            Ids.append(Id)         
        return faces, Ids
    speak("details ")
    root=Tk()
    root.title("Student data ")
    root.geometry("1350x740")
    img=ImageTk.PhotoImage(Image.open ("C:\\Users\\Priyanka\\Desktop\\Final_Year_project\\face1.jpg"))
    lab=Label(image=img).pack()
    Login_Frame=Frame(root,bg="dark turquoise")
    Login_Frame.place(x=270,y=200)
    ro=Label(Login_Frame,text="DETAILS -",compound=LEFT,font=("times new roman",25,"bold"),fg="red",
                   bg="dark turquoise").grid(row=0,column=0,padx=20,pady=10)
    roll=Label(Login_Frame,text="Student Id :",compound=LEFT,font=("times new roman",25,"bold"),
                   bg="dark turquoise").grid(row=2,column=0,padx=20,pady=10)
    name=Label(Login_Frame,text="  Student Name : ",compound=LEFT,font=("times new roman",25,"bold"),
                   bg="dark turquoise").grid(row=3,column=0,padx=20,pady=10)
    u1=Entry(Login_Frame,bd=5,relief=GROOVE,font=("",15))
    u1.grid(row=2,column=1,padx=20)
    n1=Entry(Login_Frame,bd=5,relief=GROOVE,font=("",15))
    n1.grid(row=3,column=1,padx=20)
    add_student=Button(Login_Frame,text="Save Data",width=15,command=save_data,
                       font=("times new roman",14,"bold"),bg="cyan",fg="red",bd=10,relief=GROOVE).grid(row=10,column=0,pady=10)
    Quit=Button(Login_Frame,text="Quit",width=15,command=root.destroy,
                       font=("times new roman",14,"bold"),bg="cyan",fg="red",bd=10,relief=GROOVE).grid(row=10,column=2,pady=10)
    pic=Button(Login_Frame,text="Click Photo",width=10,command=fun,height=1,font=("times new roman",14,"bold"),bg="cyan",fg="red",
              bd=10,relief=GROOVE).grid(row=0,column=2,pady=10)
    pic2=Button(Login_Frame,text="  Sure  ",width=10,command=TrainImages,height=1,font=("times new roman",14,"bold"),bg="cyan",fg="red",
              bd=10,relief=GROOVE).grid(row=10,column=1,pady=10)
    root.mainloop()
def fun3():
    root=Tk()
    speak("Enter Student details")
    root.title("Attendence System")
    root.geometry("1350x740")
    img=ImageTk.PhotoImage(Image.open ("C:\\Users\\Priyanka\\Desktop\\Final_Year_project\\face1.jpg"))
    lab=Label(image=img).pack()
    Login_Frame=Frame(root,bg="dark turquoise")
    Login_Frame.place(x=455,y=265)
    user=Label(Login_Frame,text="Student Details ",compound=LEFT,
                   font=("times new roman",40,"bold"),bg="dark turquoise").grid(row=0,column=0,padx=20,pady=20)
    btn_log=Button(Login_Frame,text="Enter",width=15,command=root.destroy,
                       font=("times new roman",20,"bold"),bg="cyan",fg="blue").grid(row=1,column=0,pady=10)
    root.mainloop()
class Login_System1:
    def __init__(self,root):
        speak("welcome admin please enter your username and passward")
        self.root=root
        self.root.title("Admin")
        self.root.geometry("1350x740")
        self.bg_icon=ImageTk.PhotoImage(file="C:\\Users\\Priyanka\\Desktop\\Final_Year_project\\face1.jpg")
        self.username=StringVar()
        self.pass_=StringVar()
        bg_lbl=Label(self.root,image=self.bg_icon).pack()
        Login_Frame=Frame(self.root,bg="dark turquoise")
        Login_Frame.place(x=450,y=235)
        wel=Label(Login_Frame,text=" ",compound=LEFT,font=("times new roman",20,"bold")
                       ,bg="dark turquoise").grid(row=1,column=1,padx=20,pady=10)
        username=Label(Login_Frame,text="Username :",compound=LEFT,font=("times new roman",20,"bold")
                       ,bg="dark turquoise").grid(row=2,column=0,padx=20,pady=10)
        username1=Entry(Login_Frame,textvariable=self.username,bd=5
                        ,relief=GROOVE,font=("",15)).grid(row=2,column=1,padx=20)
        pass1=Label(Login_Frame,text="Password  :",compound=LEFT,font=("times new roman",20,"bold"),
                    bg="dark turquoise").grid(row=6,column=0,padx=20,pady=10)
        pass2=Entry(Login_Frame,textvariable=self.pass_,bd=5,relief=GROOVE
                    ,show="*",font=("",15)).grid(row=6,column=1,padx=20)
        btn_log=Button(Login_Frame,text="Login",width=15,command=self.login,font=("times new roman",15,"bold")
                      ,bg="cyan",fg="blue4").grid(row=8,column=1,pady=10)
    def login(self):
        if self.username.get()=="" or self.pass_.get()=="":
            messagebox.showerror("Error","All field are required!!")
        elif self.username.get()=="admin" and self.pass_.get()=="admin":
            messagebox.showinfo("Successfull")
            speak("Thanku so much")
            self.root.after(1000,self.root.destroy)
        else:
            messagebox.showerror("Error","Invalid Username or Password!")
def fun1():
    root=Tk()
    speak("welcome")
    root.title("Attendence System")
    speak("attendence system using face recognition")
    root.geometry("1350x740")
    img=ImageTk.PhotoImage(Image.open ("C:\\Users\\Priyanka\\Desktop\\Final_Year_project\\face1.jpg"))
    lab=Label(image=img).pack()
    Login_Frame=Frame(root,bg="dark turquoise")
    Login_Frame.place(x=435,y=300)
    user=Label(Login_Frame,text="ATTENDENCE SYSTEM ",compound=LEFT,
                   font=("times new roman",30,"bold"),bg="dark turquoise").grid(row=1,column=0,padx=10,pady=10)
    btn_log=Button(Login_Frame,text="Start",width=15,command=root.destroy,
                       font=("times new roman",20,"bold"),bg="cyan",fg="white").grid(row=2,column=0,pady=10)
    root.mainloop()

#start
fun1()
r=Tk()
obj=Login_System1(r)
r.mainloop()
fun3()
fun4()
test()


