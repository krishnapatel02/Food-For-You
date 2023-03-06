from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

#https://www.google.com/search?q=create+theme+tkinter+python&rlz=1C1VDKB_enUS1034US1034&sxsrf=AJOqlzVyUBHWRfGeC6eRK0zbFZLyOMlJmw%3A1678037292298&ei=LNEEZN7tEY660PEPkbOW6AE&ved=0ahUKEwjes-iFqMX9AhUOHTQIHZGZBR0Q4dUDCBA&uact=5&oq=create+theme+tkinter+python&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIICCEQoAEQwwQyCAghEKABEMMEOgoIABBHENYEELADOgcIIxCwAhAnOggIABAIEAcQHjoICAAQCBAeEA06BQgAEIYDOgoIIRCgARDDBBAKSgQIQRgAUNoDWMMJYO0KaAFwAXgAgAF3iAH5BJIBAzUuMpgBAKABAcgBCMABAQ&sclient=gws-wiz-serp#fpstate=ive&vld=cid:55497400,vid:fOVmMiyezMU

class UpdateItem:
    def __init__(self, parent, window, item, quantity, units, location):
        self.root = root
        self.root.title("Updating")
        self.root.geometry("500x200")
        self.locations = parent.locations

        style = ttk.Style(root)
        style.theme_use("clam")

        frame = Frame(root)
        frame.place(x=20, y=50, width=500, height=745)

        ttk.Label(frame, text="item").place(x=25, y=25)
        iteminput = ttk.Entry(frame, width=10, textvariable=self.item_to_update)
        #iteminput.grid(row=1, column=0, sticky='w', padx=10, pady=11)
        iteminput.place(x=25, y=50)

        ttk.Label(frame, text="quantity").place(x=150, y=25)
        quantityinput = ttk.Entry(frame, width=10, textvariable=self.quantity_to_update)
        #quantityinput.grid(row=1, column=0, sticky='w', padx=10, pady=11)
        quantityinput.place(x=150, y=50)

        Label(frame, text="location").place(x=265, y=25)
        locationDD = ttk.Combobox(frame, values=self.locations, textvariable=self.loc_to_update)
        locationDD.place(x=275, y=50)

        def saveChanges():

                        #If one or more required field is empty, show error
            if (iteminput.get() == "" or quantityinput.get() == "" or locationDD.get()):
                    messagebox.showerror("ERROR", "Please enter the correct data in each catagory")
            #otherwise update all categories
            else:
                #TODO
                """
                con = mysql.connect(host="ix.cs.uoregon.edu", port=3673, user="prodrig2", password="irodmario@2001", database="422json")
                custer.execute('UPDATE 422json.naturalsciences SET COURSE_NAME=%s, TERM=%s, INSTRUCTOR=%s, APREC=%s, BPREC=%s, CPREC=%s, DPREC=%s, FPREC=%s, faculty=%s where crn=%s',
                (self.title.get(),self.term.get(), self.name.get(), self.A.get(), self.B.get(), self.C.get(), self.D.get(), self.F.get(), self.facultyType.get(), self.crn.get()))
                con.commit()
                con.close()
                fetchData()
                clear()
                messagebox.showinfo('Success', f'Course CRN: {crn} is updated in the database')
            """

        submitButton = Button(root, text="Save changes", height=2, width=10, command=saveChanges)
        submitButton.place(x=400, y=150)

def connectToDatabase(user, password, host, port, database):
            dbconnect = None
            counter = 0
            while dbconnect is None:
                if (counter >= 10):
                    print("Check connection to internet")
                    exit()
                try:
                    dbconnect = mysql.connector.connect(
                        host=host,
                        user=user,
                        passwd=password,
                        port=port,
                        database=database)
                    print("Connected")
                except:
                    print("Connection failed")
                    dbconnect = None
                    counter += 1
            return dbconnect

connection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3624, "foodforyou")
cursor = connection.cursor()

class StaffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff")
        self.root.geometry("877x500")
        self.foodItemSearchText = StringVar()
        self.ascSort = BooleanVar()
        self.loc_to_update = StringVar()
        self.locations = []
        self.bg = PhotoImage(file="backgroundimg1.png")
        Label(root, image=self.bg).place(x=0, y=0)

        style = ttk.Style(root)
        style.theme_create("Custom")
        #style.wm_attributes('-transparentcolor', '#ab23ff')
        style.configure("TLabel", font=("arial", 11), background ="#fff")
        style.configure("TButton", font=("arial", 11), background="#fff")
        style.configure("TCheckbutton", font=("arial", 11), background ="#fff")
        style.configure("TEntry", font=("arial"), background ="#fff")

        #
        # style.theme_settings("Custom", {
        #     "TButton":{
        #         "fieldbackground": [("!disabled", "#5C5C5C")]
        #
        #     },
        #     "TLabel":{
        #         "fieldbackground": [("active", "#90fc03")]
        #     }
        #
        # })



        def fetchLocations():
            cursor.execute("SELECT fb.Location from food_bank fb order by fb.Location asc")
            self.locations.append(None)
            for row in cursor:
                for col in row:
                    self.locations.append(col)
        fetchLocations()

        def fetchData():
            search()
            rows = cursor.fetchall()
            
            #Delete the old table and insert each row in the current database to accomplish refresh
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
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}' order by fi.Quantity ASC")
            elif (locationBool and ascending):
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}' order by fi.Quantity ASC")
            elif (itemBool and ascending):
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' order by fi.Quantity ASC")
            elif (itemBool and locationBool):
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}'")
            elif (itemBool):
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}'")
            elif (locationBool):
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}'")
            elif (ascending):
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) order by fi.quantity ASC")
            else:
                cursor.execute(
                    f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id)")
            #result = cursor.fetchall()


        def update(e):
            #taken from focus(e) by jerry
            cursor = table.focus()
            content = table.item(cursor)
            row = content['values']
            item = row[0]
            quantity = row[1]
            units = row[2]
            location = row[3]

            window = Tk()
            ob = UpdateItem(window, root, item, quantity, units, location)
            window.mainloop()

        ttk.Label(root, text="Search item").place(x=700, y=110)

        ItemSearch = ttk.Entry(root, width=25)
        ItemSearch.place(x=700, y=140)
        SearchButton = ttk.Button(root, text="Search", width=15, command=fetchData)
        SearchButton.place(x=700, y=400)

        #ttk.Label(root, text="Sort quantity").place(x=700, y=50)
        QuantitySortButton = ttk.Checkbutton(root, text="Sort Ascending", width=15, command=search, onvalue=True,
                                         offvalue=False)
        QuantitySortButton.place(x=700, y=300)

        ttk.Label(root, text="Sort by location").place(x=700, y=200)
        LocationFilter = ttk.Combobox(root, values=self.locations)
        LocationFilter.place(x=700, y=240)

        # UpdateItemButton = Button(text="Update Item", command=update)
        # UpdateItemButton.place(x=300, y=400)

        viewFrame = Frame(root, bd=5, relief='ridge', bg='wheat')
        viewFrame.place(x=30, y=110, width=650, height=350)
                                            #800
        xScroll = Scrollbar(viewFrame, orient=HORIZONTAL)
        yScroll = Scrollbar(viewFrame, orient=VERTICAL)
        table = ttk.Treeview(viewFrame, columns=('item_to_filter', 'quantity_to_filter', 'units', 'fid_to_filter', 'location_to_filter'), xscrollcommand=xScroll.set,
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

        table.bind('<ButtonRelease-1>', update)

        # get all values and pack the table on to the screen
        fetchData()
        table.pack(fill=BOTH, expand=1)




root = Tk()
ob = StaffGUI(root)
root.mainloop()
