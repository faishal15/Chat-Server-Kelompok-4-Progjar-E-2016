import Tkinter
from Tkinter import *
import tkMessageBox

import socket
import sys
from thread import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('10.151.36.250', 10050)

sock.connect(server_address)
mains = 1

#KEVIN
def terima_pesan_personal(text1):       
    while True:
        status=sock.recv(1024)
        temp = status.split()
        i = 2
        message = []
        message.append(temp[1] + ":")
        while i != len(temp):
            message.append(temp[i])
            i += 1
        message.append("\n")
        strings = " ".join(message)
        print strings
        text1.insert(END, strings)
#WILDAN
def terima_pesan_grup(text1):
    while True:
        status = sock.recv(1024)
        print status
        temp = status.split()
        i = 3
        message = []
        message.append(temp[1] + ": " + temp[2] + ": ")
        while i != len(temp):
            message.append(temp[i])
            i += 1
        strings = " ".join(message)
        print strings
        text1.insert(END, strings)
#RISMA
def terima_list_grup(text1):
    sock.sendall("LISTGROUP")
    while True:
        status=sock.recv(1024)
        temp = status.split()
        i = 0
        while i != len(temp) - 1:
            text1.insert(END, temp[i] + "\n")
            i += 1
#KEVIN
def terima_pesan():
    while True:
        status = sock.recv(1024)
        if status == "+REG_SUCCESS":
            tkMessageBox.showinfo("Success!","Registration success!")
        elif status == "-USR_REGISTERED":
            tkMessageBox.showinfo("Failed!", "Username already used!")
        elif status == "+LOGIN_SUCCESS":
            response = tkMessageBox.showinfo("Success!", "Login success")
            if response == "ok":
                mainWindow()
        elif status == "-USER_NOT_FOUND":
            tkMessageBox.showinfo("Failed!", "Username not found!")
        elif status == "-WRONG_PASS":
            tkMessageBox.showinfo("Failed!", "Wrong password")
        elif status == "+ALREADY_LOGGED_IN":
            tkMessageBox.showinfo("Failed!", "Already logged in")
        elif status == "+GROUP_CREATED":
            tkMessageBox.showinfo("Success!", "Group successfully created!")
        elif status == "-GROUP_EXISTED" or status == "-GROUP_EXISTS":
            tkMessageBox.showinfo("Failed!", "Group already exists!")
        elif status == "+JOINED_SUCCESS":
            tkMessageBox.showinfo("Success!", "Successfully joined group!")
        elif status == "-GROUP_FULL":
            tkMessageBox.showinfo("Failed!", "Group already full!")
        elif status == "-GROUP_NOT_FOUND":
            tkMessageBox.showinfo("Failed!", "Group not found!")
        elif status == "-WRONG_PASS":
            tkMessageBox.showinfo("Failed!", "Wrong group password!")
#FARHAN
def terima_list_grup_member(text1):
    while True:
        status = sock.recv(1024)
        temp = status.split()
        i = 0
        while i != len(temp) - 1:
            text1.insert(END, temp[i] + "\n")
            i += 1
#FARHAN
def membersListWindowShow():
    top1 = Tkinter.Tk()
    frame0 = Frame(top1)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    start_new_thread(terima_list_grup_member, (W1,))
    top1.mainloop()
#FARHAN
def membersListWindowHandler(entry1):
    grup = entry1.get()
    sock.sendall("LISTUSER " + grup)
    membersListWindowShow()
#FARHAN
def membersListWindow():
    top1 = Tkinter.Tk()
    top1.title("Group Members")
    L0 = Label(top1, text="Group Members\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Group Name")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    Z = Button(frame3, text="View Members", command=lambda: membersListWindowHandler(E1))
    Z.pack()
    top1.mainloop()
#ICAL
def personalWindowHandler(entry1, entry2,text1):
    recipient = entry1.get()
    message = entry2.get()
    text1.insert(END,"You -> "+recipient+" : "+message+"\n")
    sock.sendall("PM " + recipient + " " + message)
#ICAL
def groupListWindow():
    top = Tkinter.Tk()
    top.title("Group List")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    start_new_thread(terima_list_grup, (W1,))
    top.mainloop()
#KEVIN
def groupMessageWindowHandler(entry1,entry2,text1):
    grup = entry1.get()
    message = entry2.get()
    text1.insert(END, "You -> " + grup + " : " + message + "\n")
    sock.sendall("GM " + grup + " " + message)
#KEVIN
def groupMessageWindow():
    top = Tkinter.Tk()
    top.title("Group Chat")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    frame3 = Frame(top)
    frame3.pack()
    L1 = Label(frame1, text="Group")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Message")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5)
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Send", command=lambda: groupMessageWindowHandler(E1, E2,W1))
    Z.pack()
    start_new_thread(terima_pesan_grup,(W1,))
    top.mainloop()
#RISMA
def personalWindow():
    top = Tkinter.Tk()
    top.title("Personal Chat")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    frame3 = Frame(top)
    frame3.pack()
    L1 = Label(frame1, text="Recipient")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Message")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5)
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Send", command=lambda: personalWindowHandler(E1, E2,W1))
    Z.pack()
    start_new_thread(terima_pesan_personal,(W1,))
    top.mainloop()
#KEVIN
def createWindowHandler(entry1,entry2):
    groupname = entry1.get()
    password = entry2.get()
    sock.sendall("CREATEGROUP " + groupname + " " + password)
#ICAL
def joinWindowHandler(entry1,entry2):
    groupname = entry1.get()
    password = entry2.get()
    sock.sendall("JOIN " + groupname + " " + password)
#KEVIN
def createWindow():
    top1 = Tkinter.Tk()
    top1.title("Sign Up")
    L0 = Label(top1, text="Create New Group\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Group Name (alphanumeric)")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password (alphanumeric)")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5, show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Create Group!", command=lambda: createWindowHandler(E1, E2))
    Z.pack()
    top1.mainloop()
#RISMA
def joinWindow():
    top1 = Tkinter.Tk()
    top1.title("Join Group")
    L0 = Label(top1, text="Join A Group\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Group Name")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5, show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Join Group!", command=lambda: joinWindowHandler(E1, E2))
    Z.pack()
    top1.mainloop()
#WILDAN
def groupWindowHandler(entry1):
    choice = entry1.get()
    if choice == "1":
        createWindow()
    elif choice == "2":
        joinWindow()
    elif choice == "3":
        groupListWindow()
    elif choice == "4":
        membersListWindow()
    elif choice == "5":
        groupMessageWindow()
    else:
        tkMessageBox.showinfo("Failed!", "Wrong number!")
#FARHAN
def logoutHandler(top):
    sock.sendall("LOGOUT")
    response = tkMessageBox.showinfo("Success!", "Logout success")
    if response == "ok":
        global mains
        mains.destroy()
#KEVIN
def groupWindow():
    top = Tkinter.Tk()
    top.title("Groups")
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    L1 = Label(frame1, text="Choose a number")
    L1.pack()
    L2 = Label(frame1, text="1: Create group")
    L2.pack()
    L3 = Label(frame1, text="2: Join group")
    L3.pack()
    L3 = Label(frame1, text="3: Group List")
    L3.pack()
    L4 = Label(frame1, text="4: Group's Members List")
    L4.pack()
    L5 = Label(frame1, text="5: Send Group Message")
    L5.pack()
    E1 = Entry(frame2, bd=5)
    E1.pack(side=RIGHT)
    Z = Button(frame2, text="Submit", command=lambda: groupWindowHandler(E1))
    Z.pack(side=LEFT)
    start_new_thread(terima_pesan, ())
    top.mainloop()
#ICAL
def mainWindow():
    top = Tkinter.Tk()
    top.title("Home")
    A = Button(top,text="Personals", command=personalWindow)
    A.pack()
    B = Button(top, text="Groups", command=groupWindow)
    B.pack()
    C = Button(top, text="Logout", command=lambda: logoutHandler(top))
    C.pack()
    top.mainloop()
#WILDAN
def signupWindowHandler(entry1,entry2):
    username =  entry1.get()
    password = entry2.get()
    sock.sendall("REGISTER " + username + " " + password)
#FARHAN
def firstWindowHandler(entry1,entry2):
    username = entry1.get()
    password = entry2.get()
    sock.sendall("LOGIN " + username + " " + password)
#WILDAN
def signupWindow():
    top1 = Tkinter.Tk()
    top1.title("Sign Up")
    L0 = Label(top1, text="Sign Up\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="User Name (alphanumeric)")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password (alphanumeric)")
    L2.pack(side=LEFT)
    E2 = Entry(frame2,  bd=5,show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Sign Up!", command= lambda: signupWindowHandler(E1,E2))
    Z.pack()
    top1.mainloop()
#RISMA
def firstWindow():
    top = Tkinter.Tk()
    global mains
    mains = top
    top.title("Welcome!")
    L0 = Label(top, text="Welcome to Wumbo Chat!\n")
    L0.pack()
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    frame3 = Frame(top)
    frame3.pack()
    L1 = Label(frame1, text="User Name")
    L1.pack( side = LEFT)
    E1 = Entry(frame1, bd =5)
    E1.pack(side = RIGHT)
    L2 = Label(frame2, text="Password")
    L2.pack(side = LEFT)
    E2 = Entry(frame2, bd =5,show="*")
    E2.pack(side = RIGHT, )
    A = Button(frame3, text ="Log In!", command = lambda: firstWindowHandler(E1,E2) )
    A.pack()
    L3 = Label(frame3, text="\nDon't have an account?\n")
    L3.pack()
    B = Button(frame3, text ="Sign Up", command = signupWindow)
    B.pack()
    top.mainloop()


start_new_thread(terima_pesan,())

try:
    firstWindow()
finally:
    sock.close()
