import tkinter as t
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import os
import csv

locations = ['FB1', 'FB20', 'aFB3']

def addFB():
    global locations
    def validateFile(filepath):
        #checking headers
        file = open(filepath, 'r')
        expected = ["item", "quantity"]
        csv_reader = csv.reader(file, delimiter=',')

        dict_from_csv = dict(list(csv_reader))
        print(dict_from_csv)

        if expected != list(dict_from_csv.keys()):
            print(list(dict_from_csv.keys()))
            messagebox.showerror("Incorrect headers")

        #check quantities

    def fileUpload():
        filepath = t.filedialog.askopenfilename()
        filename, fextension = os.path.splitext(filepath)

        if fextension != '.csv':
            messagebox.showerror("Incorrect File Type. Must be CSV")

        #check headers
        validateFile(filepath)


    def saveChanges():
        #db stuff
        newFBScreen.destroy()

    def check_input(event):
        value = event.widget.get()
        if value == '':
            locationInput['values'] = locations
        else:
            data = []
            for item in locations:
                if value.lower() in item.lower():
                    data.append(item)

            locationInput['values'] = locationInput



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

    locationInput = ttk.Combobox(newFBScreen,
                           height=2,
                           width=10,
                              )
    locationInput['values'] = locations
    locationInput.bind('<KeyRelease>', check_input)

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