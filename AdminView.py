import tkinter as t
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import os
import csv
import timepicker as time

"""
README!!!!!!!!!
for db: write saveChanges()
        view data on main screen

for KS:
allow times to be none (store is closed)
verify that all times are times are inputted before submit
s
"""
data = []
def addFB():
    #if succesfull return a dictionary of the csv
    def validateFile(filepath):
        #checking headers
        try:
            file = open(filepath, 'r')
            expected = ["item", "quantity"]

            dict_from_csv = list(csv.DictReader(file))

            if expected != [x.strip() for x in dict_from_csv[0].keys()]:
                messagebox.showerror("File error", "Incorrect headers")
                return -1

            for i, item in enumerate(dict_from_csv):
                quant = item['quantity']

                #checks if integer and non-negative
                #isdigit() also returns false if digit is negative
                if not (quant.isdigit()):
                    messagebox.showerror("File error", "Invalid quantity (" + quant + ") on row " + str(i+2))
                    return -1

            returnval = []
            for x in dict_from_csv:
                i, q = x.values()
                returnval.append((i, q))
            return returnval

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("File error", "Having trouble uploading file. Please ensure the file uploaded is a CSV with two columns of 'item' and 'quantity'")

    def fileUpload():
        filepath = t.filedialog.askopenfilename()
        filename, fextension = os.path.splitext(filepath)

        if fextension != '.csv':
            messagebox.showerror("Incorrect File Type. Must be CSV")
            return

        #check headers
        global data
        data = validateFile(filepath)
        if data == -1:
            return
        print("Succesfully imported file")



    def saveChanges():
        # happens when user pushes "save changes"
        #   (user can input times, location and upload files in any order
        #   so "save changes" does the commit)

        global data
        newloc = locationInput.get(1.0, "end-1c")
        times = {"Monday": (MtimeOpen.getTime(), MtimeClose.getTime()),
                 "Tuesday": (TtimeOpen.getTime(), TtimeClose.getTime()),
                 "Wednesday": (WtimeOpen.getTime(), WtimeClose.getTime()),
                 "Thursday": (RtimeOpen.getTime(), RtimeClose.getTime()),
                 "Friday": (FtimeOpen.getTime(), FtimeClose.getTime()),
                "Saturday": (StimeOpen.getTime(), StimeClose.getTime()),
                "Sunday": (UtimeOpen.getTime(), UtimeClose.getTime())
                 }


        print("data from csv: ", data)
        print("newloc: ", newloc)
        print("times: ", times)

        # TODO ---------------- db stuff (upload the dictionary to food items and location database) ------------------------
        #   use the variables that are printed above

        #when finished up
        newFBScreen.destroy()


    newFBScreen = t.Tk()
    newFBScreen.geometry("800x400")

    locationInput = t.Text(newFBScreen, height=2, width=10)
    locationInput.place(x=75, y=200)

    fileUploadButton = t.Button(newFBScreen, text="Upload Data", height=2, width=10, command=fileUpload)
    fileUploadButton.place(x=400, y=150)

    submitButton = t.Button(newFBScreen, text="Save changes", height=2, width=10, command=saveChanges)
    submitButton.place(x=675, y=200)

    t.Label(newFBScreen, text="Insert times").place(x=75, y=25)
    t.Label(newFBScreen, text="Open").place(x=25, y=75)
    t.Label(newFBScreen, text="Close").place(x=25, y=100)
    t.Label(newFBScreen, text="Insert Location").place(x=75, y=150)

    t.Label(newFBScreen,text="Monday").place(x=75, y=50)
    MtimeOpen = time.App(newFBScreen)
    MtimeOpen.place(x=75, y=75)
    MtimeClose = time.App(newFBScreen)
    MtimeClose.place(x=75, y=100)

    t.Label(newFBScreen,text="Tuesday").place(x=175, y=50)
    TtimeOpen = time.App(newFBScreen)
    TtimeOpen.place(x=175, y=75)
    TtimeClose = time.App(newFBScreen)
    TtimeClose.place(x=175, y=100)

    t.Label(newFBScreen,text="Wednesday").place(x=275, y=50)
    WtimeOpen = time.App(newFBScreen)
    WtimeOpen.place(x=275, y=75)
    WtimeClose = time.App(newFBScreen)
    WtimeClose.place(x=275, y=100)

    t.Label(newFBScreen,text="Thursday").place(x=375, y=50)
    RtimeOpen = time.App(newFBScreen)
    RtimeOpen.place(x=375, y=75)
    RtimeClose = time.App(newFBScreen)
    RtimeClose.place(x=375, y=100)

    t.Label(newFBScreen,text="Friday").place(x=475, y=50)
    FtimeOpen = time.App(newFBScreen)
    FtimeOpen.place(x=475, y=75)
    FtimeClose = time.App(newFBScreen)
    FtimeClose.place(x=475, y=100)

    t.Label(newFBScreen,text="Saturday").place(x=575, y=50)
    StimeOpen = time.App(newFBScreen)
    StimeOpen.place(x=575, y=75)
    StimeClose = time.App(newFBScreen)
    StimeClose.place(x=575, y=100)

    t.Label(newFBScreen,text="Sunday").place(x=675, y=50)
    UtimeOpen = time.App(newFBScreen)
    UtimeOpen.place(x=675, y=75)
    UtimeClose = time.App(newFBScreen)
    UtimeClose.place(x=675, y=100)

    #TODO show fb hours database

    newFBScreen.mainloop()



mainScreen = t.Tk()
mainScreen.geometry("1000x500")

AddFBButton = t.Button(mainScreen, text="New Food Bank +", width=20, height=3, command=addFB)
AddFBButton.place(x=700, y=200)

mainScreen.mainloop()