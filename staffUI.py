from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# https://www.google.com/search?q=create+theme+tkinter+python&rlz=1C1VDKB_enUS1034US1034&sxsrf=AJOqlzVyUBHWRfGeC6eRK0zbFZLyOMlJmw%3A1678037292298&ei=LNEEZN7tEY660PEPkbOW6AE&ved=0ahUKEwjes-iFqMX9AhUOHTQIHZGZBR0Q4dUDCBA&uact=5&oq=create+theme+tkinter+python&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIICCEQoAEQwwQyCAghEKABEMMEOgoIABBHENYEELADOgcIIxCwAhAnOggIABAIEAcQHjoICAAQCBAeEA06BQgAEIYDOgoIIRCgARDDBBAKSgQIQRgAUNoDWMMJYO0KaAFwAXgAgAF3iAH5BJIBAzUuMpgBAKABAcgBCMABAQ&sclient=gws-wiz-serp#fpstate=ive&vld=cid:55497400,vid:fOVmMiyezMU

connection = None
cursor = None
font = "Helvetica"
searchInputSize =9

def fetchLocations():
    cursor.execute("SELECT fb.Location from food_bank fb order by fb.Location ASC")
    locations = []
    locations.append(None)
    for row in cursor:
        for col in row:
            locations.append(col)
    return locations

def fetchCategory():
    #TODO
    return []

class NewItem:
    def __init__(self, parent):
        self.screen = Toplevel(parent)
        self.screen.title("New Item")
        self.swidth = 300
        self.screen.geometry(f'{self.swidth}x300')
        self.locations = fetchLocations()
        self.categories = fetchCategory()

        self.item_to_update = StringVar()
        self.quantity_to_update = IntVar()
        self.loc_to_update = StringVar()
        self.units_to_update = StringVar()
        self.screenopt = StringVar()

        global font
        global searchInputSize

        self.screen.configure(background='white')


        #ttk.Label(screen, text="item").grid(row=1,  column=0,  padx=10,  pady=5)
        ttk.Label(self.screen, text="item").place(x=50, y=50)
        iteminput = ttk.Entry(self.screen, width=20, font=(font, searchInputSize))
        iteminput.place(x=(self.swidth)/2-30, y=50)
        #iteminput.grid(row=2,  column=0,  padx=10,  pady=5)

        #ttk.Label(screen, text="quantity").grid(row=3,  column=0,  padx=10,  pady=5)
        ttk.Label(self.screen, text="quantity:").place(x=50, y=80)
        quantityinput = ttk.Entry(self.screen, width=10, textvariable=self.quantity_to_update, font=(font, searchInputSize))
        quantityinput.place(x=(self.swidth)/2-30, y=80)
        #quantityinput.grid(row=4,  column=0,  padx=10,  pady=5)

        #ttk.Label(screen, text="units").grid(row=3, column=1, padx=10, pady=5)
        ttk.Label(self.screen, text="units: ").place(x=50, y=110)
        unitsInput = ttk.Entry(self.screen, width=10, textvariable=self.units_to_update, font=(font, searchInputSize))
        #unitsInput.grid(row=4,  column=1,  padx=10,  pady=5)
        unitsInput.place(x=(self.swidth)/2-30, y=110)

        ttk.Label(self.screen, text="location:").place(x=50, y=140)
        locationinput = ttk.Entry(self.screen, width=20, font=(font, searchInputSize))
        locationinput.place(x=(self.swidth) / 2 - 30, y=140)

        ttk.Label(self.screen, text="category:").place(x=50, y=170)
        categoryinput = ttk.Entry(self.screen, width=20, font=(font, searchInputSize))
        categoryinput = ttk.Combobox(self.screen, values=self.categories, textvariable=self.loc_to_update,
                                  font=(font, 8))
        categoryinput.place(x=(self.swidth) / 2 - 30, y=170)
        # ttk.Label(screen, text=location, font=(font, 9)).place(x=(self.swidth)/2, y=300)

        fillerlbl = ttk.Label(self.screen)
        movelbl = ttk.Label(self.screen, text="location to move items to")


        def saveChanges():
            # TODO
            pass
            # # If one or more required field is empty, show error
            # if (iteminput.get() == "" or quantityinput.get() == "" or locationDD.get() == "" or unitsInput.get() == ""):
            #     messagebox.showerror("ERROR", "Please enter the correct data in each catagory")
            # # otherwise update all categories
            # else:
            #
            #     """
            #     con = mysql.connect(host="ix.cs.uoregon.edu", port=3673, user="prodrig2", password="irodmario@2001", database="422json")
            #     custer.execute('UPDATE 422json.naturalsciences SET COURSE_NAME=%s, TERM=%s, INSTRUCTOR=%s, APREC=%s, BPREC=%s, CPREC=%s, DPREC=%s, FPREC=%s, faculty=%s where crn=%s',
            #     (self.title.get(),self.term.get(), self.name.get(), self.A.get(), self.B.get(), self.C.get(), self.D.get(), self.F.get(), self.facultyType.get(), self.crn.get()))
            #     con.commit()
            #     con.close()
            #     fetchData()
            #     clear()
            #     messagebox.showinfo('Success', f'Course CRN: {crn} is updated in the database')
            # """
            #     cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{location}'")
            #     currentfb_id = fb_id = [int(i[0]) for i in cursor.fetchall()][0]
            #     cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{locationDD.get()}'")
            #     fb_id = [int(i[0]) for i in cursor.fetchall()][0]
            #     if (location == locationDD.get()):
            #         cursor.execute(
            #             f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{quantityinput.get()}', Units='{unitsInput.get()}', Location='{locationDD.get()}', fb_id='{currentfb_id}' where fd_ID='{int(food_id)}'")
            #     else:
            #         cursor.execute(f"select fi.Quantity from food_item fi where fi.fd_id = '{food_id}'")
            #         origQuantity = [int(i[0]) for i in cursor.fetchall()][0]
            #         cursor.execute(
            #             f"select fi.fd_id from food_item fi join food_bank fb using (fb_id) where fb_id = '{fb_id}' and fi.Item_name = '{iteminput.get()}'")
            #         newFoodID = [int(i[0]) for i in cursor.fetchall()][0]
            #         cursor.execute(f"select fi.Quantity from food_item fi where fi.fd_id = '{newFoodID}'")
            #         existingNewQuantity = [int(i[0]) for i in cursor.fetchall()][0]
            #         newOrigQuantity = origQuantity - int(quantityinput.get())
            #
            #         cursor.execute(
            #             f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{newOrigQuantity}', Units='{unitsInput.get()}', Location='{location}', fb_id='{currentfb_id}' where fd_ID='{int(food_id)}'")
            #         cursor.execute(
            #             f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{existingNewQuantity + int(quantityinput.get())}', Units='{unitsInput.get()}', Location='{locationDD.get()}', fb_id='{fb_id}' where fd_ID='{int(newFoodID)}'")
            #     connection.commit()

        submitButton = ttk.Button(self.screen, text="Save changes", width=15, command=saveChanges)
        submitButton.place(x=(self.swidth) / 2 - 60, y=250)




class UpdateItem:
    def __init__(self, parent, item, quantity, units, location, food_id):
        self.screen = Toplevel(parent)
        screen = self.screen
        self.screen.title("Updating")
        self.swidth = 300
        self.screen.geometry(f'{self.swidth}x300')
        self.locations = fetchLocations()

        self.item_to_update = StringVar()
        self.quantity_to_update = IntVar()
        self.loc_to_update = StringVar()
        self.units_to_update = StringVar()
        self.screenopt = StringVar()

        global font
        global searchInputSize

        screen.configure(background='white')

        #ttk.Label(screen, text="item").grid(row=1,  column=0,  padx=10,  pady=5)
        ttk.Label(screen, text="item").place(x=50, y=50)
        iteminput = ttk.Entry(screen, width=20, font=(font, searchInputSize))
        iteminput.insert(0, item)
        iteminput.configure(state=DISABLED)
        iteminput.place(x=(self.swidth)/2-30, y=50)
        #iteminput.grid(row=2,  column=0,  padx=10,  pady=5)

        #ttk.Label(screen, text="quantity").grid(row=3,  column=0,  padx=10,  pady=5)
        ttk.Label(screen, text="quantity:").place(x=50, y=80)
        quantityinput = ttk.Entry(screen, width=10, textvariable=self.quantity_to_update, font=(font, searchInputSize))
        #replace w this statement
        self.quantity_to_update.set(quantity)
        #quantityinput.insert(0, quantity)
        quantityinput.place(x=(self.swidth)/2-30, y=80)
        #quantityinput.grid(row=4,  column=0,  padx=10,  pady=5)

        #ttk.Label(screen, text="units").grid(row=3, column=1, padx=10, pady=5)
        ttk.Label(screen, text="units: ").place(x=50, y=110)
        unitsInput = ttk.Entry(screen, width=10, textvariable=self.units_to_update, font=(font, searchInputSize))
        unitsInput.insert(0, units)
        #unitsInput.grid(row=4,  column=1,  padx=10,  pady=5)
        unitsInput.place(x=(self.swidth)/2-30, y=110)

        ttk.Label(screen, text="location:").place(x=50, y=140)
        locationinput = ttk.Entry(screen, width=20, font=(font, searchInputSize))
        locationinput.insert(0, location)
        locationinput.place(x=(self.swidth) / 2 - 30, y=140)
        locationinput.configure(state="disabled")
        # ttk.Label(screen, text=location, font=(font, 9)).place(x=(self.swidth)/2, y=300)

        fillerlbl = ttk.Label(screen)
        movelbl = ttk.Label(screen, text="location to move items to")

        locationDD = ttk.Combobox(screen, values=self.locations, textvariable=self.loc_to_update,
                                  font=(font, 8))

        def saveChanges():

            # If one or more required field is empty, show error
            operation = self.screenopt.get()

            #if (iteminput.get() == "" or quantityinput.get() == "" or locationDD.get() == "" or unitsInput.get() == ""):
            #    messagebox.showerror("ERROR", "Please enter the correct data in each catagory")
            # otherwise update all categories
            #else:
            if(operation == 'update'):
                if(int(quantityinput.get())<0):
                    messagebox.showerror("ERROR", "Quantity must be non-negative")
                else:
                    cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{location}'")
                    currentfb_id = fb_id = [int(i[0]) for i in cursor.fetchall()][0]
                    #cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{locationDD.get()}'")
                    #fb_id = [int(i[0]) for i in cursor.fetchall()][0]
                    cursor.execute(
                        f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{quantityinput.get()}', Units='{unitsInput.get()}', Location='{location}', fb_id='{currentfb_id}' where fd_ID='{int(food_id)}'")
                    connection.commit()

            elif(operation == 'move'):
                pass
            elif(operation == 'delete'):
                cursor.execute(f"delete from food_item where fd_id = {food_id}")
                connection.commit()
            

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
           # cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{location}'")
           # currentfb_id = fb_id = [int(i[0]) for i in cursor.fetchall()][0]
           # cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{locationDD.get()}'")
           # fb_id = [int(i[0]) for i in cursor.fetchall()][0]
            
            """
            if (location == locationDD.get()):
                cursor.execute(
                    f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{quantityinput.get()}', Units='{unitsInput.get()}', Location='{locationDD.get()}', fb_id='{currentfb_id}' where fd_ID='{int(food_id)}'")
            else:
                cursor.execute(f"select fi.Quantity from food_item fi where fi.fd_id = '{food_id}'")
                origQuantity = [int(i[0]) for i in cursor.fetchall()][0]
                cursor.execute(
                    f"select fi.fd_id from food_item fi join food_bank fb using (fb_id) where fb_id = '{fb_id}' and fi.Item_name = '{iteminput.get()}'")
                newFoodID = [int(i[0]) for i in cursor.fetchall()][0]
                cursor.execute(f"select fi.Quantity from food_item fi where fi.fd_id = '{newFoodID}'")
                existingNewQuantity = [int(i[0]) for i in cursor.fetchall()][0]
                newOrigQuantity = origQuantity - int(quantityinput.get())

                cursor.execute(
                    f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{newOrigQuantity}', Units='{unitsInput.get()}', Location='{location}', fb_id='{currentfb_id}' where fd_ID='{int(food_id)}'")
                cursor.execute(
                    f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{existingNewQuantity + int(quantityinput.get())}', Units='{unitsInput.get()}', Location='{locationDD.get()}', fb_id='{fb_id}' where fd_ID='{int(newFoodID)}'")
            """
        submitButton = ttk.Button(screen, text="Save changes", width=15, command=saveChanges)
        submitButton.place(x=(self.swidth) / 2 - 60, y=250)


        def showScreen(a, b, c):
            #FOR DB
            s = self.screenopt.get()
            quantityinput.configure(state="active")
            unitsInput.configure(state="active")
            submitButton.configure(text="Save changes")
            unitsInput.configure(state="active")
            if s == "update":
                movelbl.pack_forget()
                locationDD.pack_forget()
            elif s == "delete":
                movelbl.pack_forget()
                locationDD.pack_forget()
                quantityinput.configure(state="disabled")
                unitsInput.configure(state="disabled")
                submitButton.configure(text="Confirm deletion")
            else:
                unitsInput.configure(state="disabled")
                fillerlbl.pack(side=BOTTOM, pady=25)
                #movelbl.place(x=325, y=75)
                locationDD.pack(side = BOTTOM, pady=5)
                movelbl.pack(side=BOTTOM)
                #locationDD.place(x=325, y=100)

        self.screenopt.set("update")
        options = ["update", "move", "delete"]
        self.screenopt.trace('w', showScreen)
        tabControl = ttk.Combobox(screen, textvariable=self.screenopt, values=options, font=(font, 12), width =7)

        #tabControl.grid(row=0,  column=0,  padx=10,  pady=5)
        #tabControl.place(x=200, y=10)
        tabControl.pack(pady=10)


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
            # print("Connected")
        except:
            print("Connection failed")
            dbconnect = None
            counter += 1
    return dbconnect


#connection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3624, "foodforyou")
connection = connectToDatabase("krishna", "pass", "127.0.0.1", 3306, "foodforyou")
cursor = connection.cursor()


class StaffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff")
        self.screenWidth = 900
        self.root.geometry(f'{self.screenWidth}x540')
        self.foodItemSearchText = StringVar()
        self.ascSort = BooleanVar()
        self.loc_to_update = StringVar()
        self.locations = fetchLocations()

        try:
            self.bg = PhotoImage(file="img/backgroundimg.png")
            Label(root, image=self.bg, borderwidth=0, highlightthickness=0).place(x=0, y=0)

            self.trailing_img = PhotoImage(file="img/trailingIMG.png")
            for i in range(0, self.screenWidth, self.trailing_img.width()):
                Label(root, image=self.trailing_img, bg='white').place(x=i, y=480)
        except Exception as e:
            print(e)

        root.configure(background='white')

        global font

        style = ttk.Style(root)
        style.theme_create("Custom")
        # style.wm_attributes('-transparentcolor', '#ab23ff')
        style.configure("TLabel", font=f'{font} 11', background="#fff")
        style.configure("TButton", font=f'{font} 11', background="#fff")
        style.configure("TCheckbutton", font=f'{font} 11', background="#fff")
        style.configure("TEntry", font=f'{font} 11')

        def fetchData():
            search()
            rows = cursor.fetchall()

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

            UpdateItem(root, item, quantity, units, location, food_id)

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

        def addItem():
            NewItem(root)

        addButton = ttk.Button(text="Add Item +", command=addItem)
        addButton.place(x=700, y=450)



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
        table.pack(fill=BOTH, expand=1)


root = Tk()
ob = StaffGUI(root)
root.mainloop()

# child = Tk()
# UpdateItem(child, "apples", 1, "oz", "123 ferry street", 2)
# child.mainloop()
#

