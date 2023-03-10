from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import timepicker as time
import csv
import os
from utilffy import *

"""
README!!!!!!!!!
for db: write saveChanges()
        view data on main screen

for KS:
allow times to be none (store is closed)
verify that all times are times are inputted before submit
"""

FBconnection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3079, "foodforyou")
# connection = connectToDatabase("kp", "pass", "127.0.0.1", 3306, "foodforyou")
FBcursor = FBconnection.cursor()

Dconnection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3079, "foodforyou")
# connection = connectToDatabase("kp", "pass", "127.0.0.1", 3306, "foodforyou")
Dcursor = Dconnection.cursor()

class FBView:
    def __init__(self, parent):
        self.root = ttk.Frame(parent)
        root = self.root
        self.foodItemSearchText = StringVar()
        self.ascSort = BooleanVar()
        self.loc_to_update = StringVar()
        self.locations = fetchLocations(FBcursor)

        global font

        def fetchData():
            search()
            rows = FBcursor.fetchall()

            # Delete the old table and insert each row in the current database to accomplish refresh
            if rows != 0:
                table.delete(*table.get_children())

                for row in rows:
                    table.insert('', END, values=row)

        def search():
            pass
            # item = ItemSearch.get()
            # locationBool = True
            # itemBool = True
            # location = LocationFilter.get()
            # ascending = self.ascSort.get()
            # if (location == "None" or location == ""):
            #     locationBool = False
            # if (item.strip() == ""):
            #     itemBool = False
            # if (locationBool and itemBool and ascending):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}' order by fi.Quantity ASC")
            # elif (locationBool and ascending):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}' order by fi.Quantity ASC")
            # elif (itemBool and ascending):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' order by fi.Quantity ASC")
            # elif (itemBool and locationBool):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}'")
            # elif (itemBool):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}'")
            # elif (locationBool):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}'")
            # elif (ascending):
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) order by fi.quantity ASC")
            # else:
            #     cursor.execute(
            #         f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id)")

        def update(e):
            # taken from focus(e) by jerry
            cursor = table.focus()
            content = table.item(cursor)
            row = content['values']
            item = row[0]
            quantity = row[1]
            units = row[2]
            food_id = row[3]
            location = row[4]

            #UpdateItem(self.root, item, quantity, units, location, food_id)

        AddFBButton = ttk.Button(root, text="New Food Bank +", width=20, command=self.addFB)
        AddFBButton.place(x=700, y=200)

        viewFrame = Frame(root, bd=5, relief='ridge', bg='wheat')
        viewFrame.place(x=30, y=110, width=600, height=350)
        # 800
        xScroll = Scrollbar(viewFrame, orient=HORIZONTAL)
        yScroll = Scrollbar(viewFrame, orient=VERTICAL)
        table = ttk.Treeview(viewFrame, columns=(
            'item_to_filter', 'quantity_to_filter', 'units', 'fid_to_filter', 'location_to_filter'),
                             xscrollcommand=xScroll.set,
                             yscrollcommand=yScroll.set)

        table.heading("item_to_filter", text="item")
        table.heading("quantity_to_filter", text="quantity")
        table.heading("units", text="units")
        table.heading("fid_to_filter", text="food_id")
        table.heading("location_to_filter", text="locations")

        table.column("item_to_filter", width=100)
        table.column("quantity_to_filter", width=25)
        table.column("units", width=25)
        table.column("fid_to_filter", width=10);
        table.column("location_to_filter", width=100)
        table['show'] = 'headings'

        # get all values and pack the table on to the screen

        table.bind('<ButtonRelease-1>', update)
        fetchData()

    def addFB(self):
        # if succesfull return a dictionary of the csv
        def validateFile(filepath):
            # checking headers
            try:
                file = open(filepath, 'r')
                expected = ["item", "quantity"]

                dict_from_csv = list(csv.DictReader(file))

                if expected != [x.strip() for x in dict_from_csv[0].keys()]:
                    messagebox.showerror("File error", "Incorrect headers")
                    return -1

                for i, item in enumerate(dict_from_csv):
                    quant = item['quantity']

                    # checks if integer and non-negative
                    # isdigit() also returns false if digit is negative
                    if not (quant.isdigit()):
                        messagebox.showerror("File error", "Invalid quantity (" + quant + ") on row " + str(i + 2))
                        return -1

                returnval = []
                for x in dict_from_csv:
                    i, q = x.values()
                    returnval.append((i, q))
                return returnval

            except Exception as e:
                print("Error:", e)
                messagebox.showerror("File error",
                                     "Having trouble uploading file. Please ensure the file uploaded is a CSV with two columns of 'item' and 'quantity'")

        def fileUpload():
            filepath = filedialog.askopenfilename()
            filename, fextension = os.path.splitext(filepath)

            if fextension != '.csv':
                messagebox.showerror("Incorrect File Type. Must be CSV")
                return

            # check headers
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

            # when finished up
            newFBScreen.destroy()

        newFBScreen = Tk()
        newFBScreen.geometry("800x300")

        locationInput = ttk.Entry(newFBScreen, width=20)
        locationInput.place(x=75, y=200)

        FBNameInput = ttk.Entry(newFBScreen, width=20)
        FBNameInput.place(x=225, y=200)

        fileUploadButton = ttk.Button(newFBScreen, text="Upload Data", width=15, command=fileUpload)
        fileUploadButton.place(x=400, y=200)

        submitButton = ttk.Button(newFBScreen, text="Save changes", width=15, command=saveChanges)
        submitButton.place(x=600, y=200)

        ttk.Label(newFBScreen, text="Insert times").place(x=75, y=25)
        ttk.Label(newFBScreen, text="Open").place(x=25, y=75)
        ttk.Label(newFBScreen, text="Close").place(x=25, y=100)
        ttk.Label(newFBScreen, text="Insert Location").place(x=75, y=175)
        ttk.Label(newFBScreen, text="Insert Food Bank Name").place(x=225, y=175)

        ttk.Label(newFBScreen, text="Monday").place(x=75, y=50)
        MtimeOpen = time.App(newFBScreen)
        MtimeOpen.place(x=75, y=75)
        MtimeClose = time.App(newFBScreen)
        MtimeClose.place(x=75, y=100)

        ttk.Label(newFBScreen, text="Tuesday").place(x=175, y=50)
        TtimeOpen = time.App(newFBScreen)
        TtimeOpen.place(x=175, y=75)
        TtimeClose = time.App(newFBScreen)
        TtimeClose.place(x=175, y=100)

        ttk.Label(newFBScreen, text="Wednesday").place(x=275, y=50)
        WtimeOpen = time.App(newFBScreen)
        WtimeOpen.place(x=275, y=75)
        WtimeClose = time.App(newFBScreen)
        WtimeClose.place(x=275, y=100)

        ttk.Label(newFBScreen, text="Thursday").place(x=375, y=50)
        RtimeOpen = time.App(newFBScreen)
        RtimeOpen.place(x=375, y=75)
        RtimeClose = time.App(newFBScreen)
        RtimeClose.place(x=375, y=100)

        ttk.Label(newFBScreen, text="Friday").place(x=475, y=50)
        FtimeOpen = time.App(newFBScreen)
        FtimeOpen.place(x=475, y=75)
        FtimeClose = time.App(newFBScreen)
        FtimeClose.place(x=475, y=100)

        ttk.Label(newFBScreen, text="Saturday").place(x=575, y=50)
        StimeOpen = time.App(newFBScreen)
        StimeOpen.place(x=575, y=75)
        StimeClose = time.App(newFBScreen)
        StimeClose.place(x=575, y=100)

        ttk.Label(newFBScreen, text="Sunday").place(x=675, y=50)
        UtimeOpen = time.App(newFBScreen)
        UtimeOpen.place(x=675, y=75)
        UtimeClose = time.App(newFBScreen)
        UtimeClose.place(x=675, y=100)

        # TODO show fb hours database

        newFBScreen.mainloop()

class DataView:
    def __init__(self, parent):
        self.root = ttk.Frame(parent)
        root = self.root
        self.foodItemSearchText = StringVar()
        self.ascSort = BooleanVar()
        self.loc_to_update = StringVar()
        self.locations = fetchLocations(Dcursor)

        global font

        def fetchData():
            search()
            rows = Dcursor.fetchall()

            # Delete the old table and insert each row in the current database to accomplish refresh
            if rows != 0:
                table.delete(*table.get_children())

                for row in rows:
                    table.insert('', END, values=row)

        def search():
            item = ItemSearch.get()
            locationBool = True
            itemBool = True
            location = LocationFilter.get()
            ascending = self.ascSort.get()
            if (location == "None" or location == ""):
                locationBool = False
            if (item.strip() == ""):
                itemBool = False
            if (locationBool and itemBool and ascending):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}' order by fi.Quantity ASC")
            elif (locationBool and ascending):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}' order by fi.Quantity ASC")
            elif (itemBool and ascending):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' order by fi.Quantity ASC")
            elif (itemBool and locationBool):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}'")
            elif (itemBool):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}'")
            elif (locationBool):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}'")
            elif (ascending):
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) order by fi.quantity ASC")
            else:
                Dcursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id)")

        def update(e):
            # taken from focus(e) by jerry
            cursor = table.focus()
            content = table.item(cursor)
            row = content['values']
            item = row[0]
            quantity = row[1]
            units = row[2]
            food_id = row[3]
            location = row[4]

            #UpdateItem(self.root, item, quantity, units, location, food_id)
        def export():
            pass

        ttk.Label(root, text="Search by item").place(x=700, y=110)

        #searchframe = Frame(root, x=700, y=140)
        ItemSearch = ttk.Entry(root, width=25)
        ItemSearch.place(x=700, y=135)

        ttk.Label(root, text="Search by item ID").place(x=700, y=185)
        IDSearch = ttk.Entry(root, width=25)
        IDSearch.place(x=700, y=210)

        #ItemSearch.grid(searchframe, row=0, column=0)
        # ttk.Label(root, text="Sort quantity").place(x=700, y=50)

        ttk.Label(root, text="Sort by location").place(x=700, y=260)
        LocationFilter = ttk.Combobox(root, values=self.locations)
        LocationFilter.place(x=700, y=285)

        QuantitySortButton = ttk.Checkbutton(root, text="Sort Ascending", width=15, command=fetchData, onvalue=True,
                                             offvalue=False, variable=self.ascSort)
        QuantitySortButton.place(x=700, y=335)

        SearchButton = ttk.Button(root, text="Search", width=15, command=fetchData)
        SearchButton.place(x=700, y=400)

        exportButton = ttk.Button(root, text="Export data", width=15, command=export)
        exportButton.place(x=700, y=50)

        viewFrame = Frame(root, bd=5, relief='ridge', bg='wheat')
        viewFrame.place(x=30, y=110, width=600, height=350)
        # 800
        xScroll = Scrollbar(viewFrame, orient=HORIZONTAL)
        yScroll = Scrollbar(viewFrame, orient=VERTICAL)
        table = ttk.Treeview(viewFrame, columns=(
            'item_to_filter', 'quantity_to_filter', 'units', 'fid_to_filter', 'location_to_filter'),
                             xscrollcommand=xScroll.set,
                             yscrollcommand=yScroll.set)

        table.heading("item_to_filter", text="item")
        table.heading("quantity_to_filter", text="quantity")
        table.heading("units", text="units")
        table.heading("fid_to_filter", text="food_id")
        table.heading("location_to_filter", text="locations")

        table.column("item_to_filter", width=100)
        table.column("quantity_to_filter", width=25)
        table.column("units", width=25)
        table.column("fid_to_filter", width=10);
        table.column("location_to_filter", width=100)
        table['show'] = 'headings'

        # get all values and pack the table on to the screen

        table.bind('<ButtonRelease-1>', update)
        fetchData()

# form = Tk()
# tab_parent = ttk.Notebook(form)
# tab1 = ttk.Frame(tab_parent)
# tab2 = ttk.Frame(tab_parent)
# tab_parent.add(tab1, text="All Records")
# tab_parent.add(tab2, text="Add New Record")
# tab_parent.pack(expand=1, fill='both')

root = Tk()
root.geometry('900x540')
tabControl = ttk.Notebook(root)

tab1 = FBView(root).root
#tab1.place(x=0, y=0, width=900, height = 540)
tabControl.add(tab1, text= "foodbanks")

tab2 = DataView(root).root
tabControl.add(tab2, text= "data")
#tab2.place(x=0, y=0, width=900, height = 540)

tabControl.pack(expand=1, fill="both")
root.mainloop()

#
# try:
#     bg = PhotoImage(master=tab1, file="img/backgroundimg.png")
#
#     Label(root, image=bg, borderwidth=0, highlightthickness=0).place(x=0, y=0)
#
#     trailing_img = PhotoImage(master=root, file="img/trailingIMG.png")
#     for i in range(0, 900, trailing_img.width()):
#         Label(master=root, image=trailing_img, bg='white').place(x=i, y=480)
# except Exception as e:
#     print(e)
