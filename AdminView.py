import tkinter as t
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import os
import csv

"""
README!!!!!!!!!
left to do: finish up the insertion of the times 
for db: write saveChanges()
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
                    messagebox.showerror("File error", "Invalid quantity {" + quant + "} on row " + str(i+2))
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

        # TODO ---------------- db stuff (upload the dictionary to food items and location database) ------------------------
        # use the following variables:

        global data
        # list of tuples: [(item, quantity), ....]
        #       i.e.  [('apple', '0'), ('grapes', '20')]
        newloc = locationInput.get(1.0, "end-1c")
        times = {"Monday": MInput.get(1.0, "end-1c")}

        print("data from csv: ", data)
        print("newloc: ", newloc)
        print("times: ", times)

        newFBScreen.destroy()


    newFBScreen = t.Tk()
    newFBScreen.geometry("500x500")


    T = t.Label(newFBScreen,
        text="Insert times"
    )
    MLabel = t.Label(newFBScreen,
        text="Monday"
    )
    TLabel = t.Label(newFBScreen,
        text="Tuesday"
    )
    WLabel = t.Label(newFBScreen,
        text="Wednesday"
    )
    RLabel = t.Label(newFBScreen,
        text="Thursday"
    )
    FLabel = t.Label(newFBScreen,
        text="Sunday"
    )
    SLabel = t.Label(newFBScreen,
        text="Saturday"
    )
    ULabel = t.Label(newFBScreen,
        text="Sunday"
    )

    ## will the hours be text input or dropdown?
    MInput = t.Text(newFBScreen,
                           height=2,
                           width=10
                           )

    locationInput = t.Text(newFBScreen,
                           height=2,
                           width=10,
                              )

    locationlabel = t.Label(newFBScreen, text= "Insert Location")

    fileUploadButton = t.Button(newFBScreen,
                            text="Upload File",
                            height=2,
                            width=10,
                            command=fileUpload
                            )

    submitButton = t.Button(newFBScreen,
                            text="Save changes",
                            height=2,
                            width=10,
                            command=saveChanges
                            )
    T.place(x=75, y=25)
    MLabel.place(x=75, y=50)
    MInput.place(x=75, y=75)
    TLabel.place(x=75, y=150)
    WLabel.place(x=75, y=200)
    RLabel.place(x=75, y=300)
    FLabel.place(x=75, y=400)
    SLabel.place(x=75, y=500)
    ULabel.place(x=75, y=600)
    locationlabel.place(x=250,y=25)
    locationInput.place(x=250,y=100)
    fileUploadButton.place(x=250,y=200)
    submitButton.place(x=250, y=300)



    ## TODO: insert item, quanity and location from selection
    ##       autofill item

    newFBScreen.mainloop()



mainScreen = t.Tk()
mainScreen.geometry("1000x500")

AddFBButton = t.Button(mainScreen,
                            text="New Food Bank +",
                            width=20,
                            height=3,
                            command=addFB
                            )


AddFBButton.place(x=700, y=200)

mainScreen.mainloop()