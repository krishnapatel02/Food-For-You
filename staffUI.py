"""
Name: staffUI.py
Created: 3/5/2023
Authors: Katherine Smirnov, Krishna Patel

Provides a table view of food items in the databases, allows user to modify food items by updating quantity,
moving or deletion, and allows insertion of new food items. The table may be sorted by quanity, and filtered by food item,
food item ID, and location.

Modifications:
    3/5/2023: Rough sketch of GUI -KS
              Added SQL queries, and connected to table widget -KP
              Added update screen - KS
    3/7/2023: Modified update screen to allow for "move", "update", "deletion" options -KS
              Rough implementation of moving items -KP
    3/8/2023: Added ID search, cleaned up GUI -KS
    3/9/2023: Fully implementation of insert of deletion -KP
    3/10/2023: Integrated with util.py -KS

References:
    EasyA, admin.py from Jerry Pi
        -Recycled code to display database into table and update items from data to database
"""

from utilffy import *

connection = None
cursor = None

connection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3079, "foodforyou")
#connection = connectToDatabase("kp", "pass", "127.0.0.1", 3306, "foodforyou")
cursor = connection.cursor()


class StaffGUI:
    def __init__(self):
        #----------------------setting up screen for "New item"---------
        self.root = Tk()
        root = self.root
        self.root.title("Staff")
        self.screenWidth = 900
        self.root.geometry(f'{self.screenWidth}x540')
        self.foodItemSearchText = StringVar()
        self.ascSort = BooleanVar()
        self.locations = fetchLocations(cursor)
        use_theme(root)
        #-----------------------------setting up background---------------------------------------
        global fetchData
        #structured to catch errors if user does not have background images,
            # allows the user to run the program without bg images
        try:
            self.bg = PhotoImage(file="img/backgroundimg.png")
            Label(master=root, image=self.bg, borderwidth=0, highlightthickness=0).place(x=0, y=0)

            self.trailing_img = PhotoImage(file="img/trailingIMG.png")
            for i in range(0, self.screenWidth, self.trailing_img.width()):
                Label(master=root, image=self.trailing_img, bg='white').place(x=i, y=480)
        except Exception as e:
            print(e)

        root.configure(background='white')

        #-------------------------- item modification functions ---------------------------------------------
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

        def addItem():
            NewItem(root)


        #--------------------------------------- search widgets -------------------------------------
        # widgets to search by item
        ttk.Label(root, text="Search by item").place(x=675, y=110)
        ItemSearch = ttk.Entry(root, width=25)
        ItemSearch.place(x=675, y=130)

        # widgets to search by item ID
        ttk.Label(root, text="Search by item ID").place(x=675, y=170)
        IDSearch = ttk.Entry(root, width=25)
        IDSearch.place(x=675, y=190)

        # widgets to filter by location
        ttk.Label(root, text="Sort by location").place(x=675, y=230)
        LocationFilter = ttk.Combobox(root, values=self.locations)
        LocationFilter.place(x=675, y=250)

        # widgets to sort by quantity
        QuantitySortButton = ttk.Checkbutton(root, text="Sort ascending quantity", command=fetchData, onvalue=True,
                                             offvalue=False, variable=self.ascSort)
        QuantitySortButton.place(x=675, y=300)

        # widgets to do the search action
        SearchButton = ttk.Button(root, text="Search", width=15, command=fetchData)
        SearchButton.place(x=675, y=350)

        # widgets to do the "add item" action
        addButton = ttk.Button(text="New Item +", command=addItem, width=15)
        addButton.place(x=675, y=410)


        #------------------------------------ table ---------------------------------------------------
        viewFrame = Frame(root, bd=5, relief='ridge', bg='wheat')
        viewFrame.place(x=30, y=110, width=600, height=350)
        xScroll = Scrollbar(viewFrame, orient=HORIZONTAL)   #allows the user to scroll
        yScroll = Scrollbar(viewFrame, orient=VERTICAL)
        table = ttk.Treeview(viewFrame, columns=(
            'item_to_filter', 'quantity_to_filter', 'units', 'fid_to_filter', 'location_to_filter'),
                             xscrollcommand=xScroll.set,
                             yscrollcommand=yScroll.set)

        table.heading("item_to_filter", text="item")
        table.heading("quantity_to_filter", text="quantity")
        table.heading("units", text="units")
        table.heading("fid_to_filter", text="food id")
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
        root.mainloop()


class NewItem:
    def __init__(self, parent):
        #----------------------setting up screen for "New item"---------
        self.screen = Toplevel(parent)      #creates a child window of main screen
        self.screen.title("New Item")
        self.swidth = 300
        self.screen.geometry(f'{self.swidth}x300')
        self.screen.configure(background='white')
        self.locations = fetchLocations(cursor)     #holds list of locations in database
        self.categories = fetchCategory(cursor)     #holds list of categories in databse
        #--------------------------------------------------------------

        #============== holds user input of the new item ==========
        self.quantity_to_update = IntVar()
        self.units_to_update = StringVar()
        #===========================================================

        global font
        global searchInputSize

        #================== user widgets =============================================================
        ttk.Label(self.screen, text="New Item", font=(font, 13)).place(x=(self.swidth)/2 - 30, y=10)

        ttk.Label(self.screen, text="item").place(x=50, y=50)
        iteminput = ttk.Entry(self.screen, width=20, font=(font, searchInputSize)) # user input for food item
        iteminput.place(x=(self.swidth) / 2 - 30, y=50)

        ttk.Label(self.screen, text="category:").place(x=50, y=80)
        categoryinput = ttk.Combobox(self.screen, values=self.categories, font=(font, 8)) #user dropdown for category
        categoryinput.place(x=(self.swidth) / 2 - 30, y=80)

        ttk.Label(self.screen, text="quantity:").place(x=50, y=110)
        quantityinput = ttk.Entry(self.screen, width=10,                        #user input for quantity
                                  textvariable=self.quantity_to_update, font=(font, searchInputSize))
        quantityinput.place(x=(self.swidth) / 2 - 30, y=110)

        ttk.Label(self.screen, text="units: ").place(x=50, y=140)
        unitsInput = ttk.Entry(self.screen, width=10,                           #user input for units
                               textvariable=self.units_to_update, font=(font, searchInputSize))
        unitsInput.place(x=(self.swidth) / 2 - 30, y=140)

        ttk.Label(self.screen, text="location:").place(x=50, y=170)
        locationinput = ttk.Combobox(self.screen, values=self.locations, font=(font, 8))    #user dropdown for location
        locationinput.place(x=(self.swidth) / 2 - 30, y=170)
        #======================================================================

        def saveChanges():
            item_name = iteminput.get()
            quantity = (quantityinput.get())
            location = locationinput.get()
            units = unitsInput.get()
            category = categoryinput.get()
            cursor.execute(f"select fb.fb_ID from food_bank fb where fb.Location='{location}'")
            temp = cursor.fetchall()
            if (category != "" and item_name != "" and units != "" and quantity != "" and location != ""):
                quantity = int(quantity)
                if (quantity >= 0):
                    if (temp != []):
                        print(temp)
                        fb_id = int(temp[0][0])
                        print(location)
                        cursor.execute(
                            f"select * from food_item fi where fi.Item_name = '{item_name}' and fi.units = '{units}' and fi.location = '{location}' and fi.fb_ID = {fb_id}")
                        result = cursor.fetchall()
                        if (result == []):
                            cursor.execute(f"select MAX(fi.fd_ID) from food_item fi")
                            temp = cursor.fetchall()
                            key = 1
                            if (temp != []):
                                key = int(temp[0][0]) + 1
                            cursor.execute(
                                f"insert into foodforyou.food_item values ('{item_name}', '{category}', {quantity}, '{units}', '{location}', {int(fb_id)}, {key})")
                            connection.commit()
                            messagebox.showinfo("Success", "Item added")

                        else:
                            messagebox.showerror("ERROR",
                                                 "This item appears to exist in the database, please find entry and modify.")
                    else:
                        messagebox.showerror("ERROR", "Location is not valid, please pick valid location.")
                else:
                    messagebox.showerror("ERROR", "Enter a non-negative quantity.")
            else:
                messagebox.showerror("ERROR", "Please enter all fields to insert an item.")
            self.screen.destroy()

        submitButton = ttk.Button(self.screen, text="Save changes", width=15, command=saveChanges)
        submitButton.place(x=(self.swidth) / 2 - 60, y=250)


class UpdateItem:
    def __init__(self, parent, item, quantity, units, location, food_id):
        #----------------------setting up screen for "Update item"---------
        self.screen = Toplevel(parent) #creates a child window of main screen
        screen = self.screen
        self.screen.title("Updating")
        screen.configure(background='white')
        self.swidth = 300
        self.screen.geometry(f'{self.swidth}x300')
        self.locations = fetchLocations(cursor)

        #============== holds what the user inputs =================
        self.quantity_to_update = IntVar()
        self.units_to_update = StringVar()
        self.screenopt = StringVar() #holds if the user is updating, moving or deleting
        #============== holds what the user inputs =================


        global font
        global searchInputSize

        #-------------------------------------------------- input widgets -----------------------------------------
        # user input for food item
        ttk.Label(screen, text="item").place(x=50, y=50)
        iteminput = ttk.Entry(screen, width=20, font=(font, searchInputSize))
        iteminput.insert(0, item)   #inserts the existing food item
        iteminput.configure(state=DISABLED)     #makes the text field read-only
        iteminput.place(x=(self.swidth) / 2 - 30, y=50)

        # user input for quantity
        ttk.Label(screen, text="quantity:").place(x=50, y=80)
        quantityinput = ttk.Entry(screen, width=10, textvariable=self.quantity_to_update, font=(font, searchInputSize))
        self.quantity_to_update.set(quantity)   # inserts the existing quantity
        quantityinput.place(x=(self.swidth) / 2 - 30, y=80)

        # user input for units
        ttk.Label(screen, text="units: ").place(x=50, y=110)
        unitsInput = ttk.Entry(screen, width=10, textvariable=self.units_to_update, font=(font, searchInputSize))
        self.units_to_update.set(units)     # inserts the existing units
        unitsInput.place(x=(self.swidth) / 2 - 30, y=110)

        # user input for location
        ttk.Label(screen, text="location:").place(x=50, y=140)
        locationinput = ttk.Entry(screen, width=20, font=(font, searchInputSize))
        locationinput.insert(0, location)   # inserts the existing location
        locationinput.place(x=(self.swidth) / 2 - 30, y=140)
        locationinput.configure(state="disabled")       #makes the text field read-only

        # location input (only for moving item, so placement will be later)
        locationDD = ttk.Combobox(screen, values=self.locations, font=(font, 8))

        #allow users to save their changes
        submitButton = ttk.Button(screen, text="Save changes", width=15)
        submitButton.place(x=(self.swidth) / 2 - 60, y=250)

        fillerlbl = ttk.Label(screen)
        movelbl = ttk.Label(screen, text="location to move items to")


        # ------------------------------ modification functions -----------------------------------------------
        def compareItems(item1, item2):
            name = (item1[0] == item2[0])
            category = (item1[1] == item2[1])
            units = (item1[3] == item2[3])
            return (name and category and units)

        def saveChanges():

            # If one or more required field is empty, show error
            operation = self.screenopt.get()
            cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{location}'")
            fb_id = [int(i[0]) for i in cursor.fetchall()][0]
            if (operation == 'update'):
                if (int(quantityinput.get()) < 0):
                    messagebox.showerror("ERROR", "Quantity must be non-negative")
                else:
                    # cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{location}'")
                    currentfb_id = fb_id
                    cursor.execute(
                        f"select * from food_item fi where fi.Item_name='{item}' and fi.fb_id={currentfb_id} and fi.units = '{units}'")
                    origEntry = cursor.fetchall()[0]
                    origQuantity = origEntry[2]

                    cursor.execute(
                        f"update foodforyou.food_item set Item_name='{iteminput.get()}', Quantity='{quantityinput.get()}', Units='{unitsInput.get()}', Location='{location}', fb_id='{currentfb_id}' where fd_ID='{int(food_id)}'")
                    if (int(quantityinput.get()) < origQuantity):
                        cursor.execute(
                            f"select * from outgoing o where o.Item_name='{item}' and o.fb_ID={fb_id} and o.fd_ID={food_id}")
                        outgoingEntry = cursor.fetchall()
                        if (outgoingEntry != []):
                            cursor.execute(
                                f"update foodforyou.outgoing set Quantity={int(outgoingEntry[0][2]) + origQuantity - int(quantityinput.get())} where fd_ID='{int(food_id)}'")
                        else:
                            cursor.execute(
                                f"insert into foodforyou.outgoing (Item_name, Category, Quantity, Units, Location, fb_ID, fd_ID) values ('{item}', '{origEntry[1]}', {origQuantity - int(quantityinput.get())}, '{origEntry[3]}', '{origEntry[4]}', {int(origEntry[5])}, {int(origEntry[6])})")
                    connection.commit()
                    messagebox.showinfo("Success", "Quantity successfully updated.")

            elif (operation == 'move'):
                cursor.execute(f"select fi.Quantity from food_item fi where fi.fd_id = '{food_id}'")
                origQuantity = [int(i[0]) for i in cursor.fetchall()][0]
                moveQuantity = int(quantityinput.get())

                if (moveQuantity > origQuantity):
                    messagebox.showerror("ERROR", "The move quantity cannot be greater than the current quantity")
                elif (moveQuantity < 0):
                    messagebox.showerror("ERROR", "The move quantity cannot be negative")
                elif (locationDD.get() == "None" or locationDD.get() == ""):
                    messagebox.showerror("Operation Cancelled", "Move location was none.")
                else:
                    cursor.execute(f"select fb.fb_id from food_bank fb where fb.Location = '{locationDD.get()}'")
                    movefb_id = [int(i[0]) for i in cursor.fetchall()][0]
                    cursor.execute(
                        f"select * from food_item fi where fi.Item_name='{item}' and fi.units = '{units}' and fi.fb_id={movefb_id}")
                    a = cursor.fetchall()
                    # print(a)
                    item2 = a[0]
                    if (item2 != []):
                        cursor.execute(f"select * from food_item fi where fi.Item_name='{item}' and fi.fb_id={fb_id}")
                        item1 = cursor.fetchall()[0]
                        if (compareItems(item1, item2)):
                            cursor.execute(
                                f"select fi.fd_id from food_item fi join food_bank fb using (fb_id) where fb_id = '{movefb_id}' and fi.Item_name = '{iteminput.get()}'")
                            newFoodID = [int(i[0]) for i in cursor.fetchall()][0]
                            cursor.execute(f"select fi.Quantity from food_item fi where fi.fd_id = '{newFoodID}'")
                            existingNewQuantity = [int(i[0]) for i in cursor.fetchall()][0]
                            updateQuantity = moveQuantity + existingNewQuantity
                            currentItemUpdateQuantity = origQuantity - moveQuantity
                            print(currentItemUpdateQuantity)
                            print(updateQuantity)

                            cursor.execute(
                                f"update foodforyou.food_item set Quantity='{currentItemUpdateQuantity}' where fd_ID='{int(food_id)}'")
                            cursor.execute(
                                f"update foodforyou.food_item set Quantity='{updateQuantity}' where fd_ID='{int(newFoodID)}'")

                            connection.commit()
                            messagebox.showinfo("Success", "Quantity successfully moved.")



                        else:
                            messagebox.showerror("ERROR", "The items are not the same. Check quantity and category.")
                    else:
                        messagebox.showerror("ERROR", "Item to move to does not exist, please add the item.")
            elif (operation == 'delete'):
                cursor.execute(f"delete from food_item where fd_id = {food_id}")
                connection.commit()
                messagebox.showinfo("Success", "Item successfully removed.")
            fetchData()
            screen.destroy()

        def showScreen(a, b, c):
            s = self.screenopt.get()
            #reset to normal state for "update" screen
            quantityinput.configure(state="active")     #reset from "delete"
            unitsInput.configure(state="active")
            submitButton.configure(text="Save changes")
            unitsInput.configure(state="active")
            movelbl.pack_forget()       #clears the widgets from the "move" screen
            locationDD.pack_forget()
            fillerlbl.pack_forget()
            if s == "update":
                pass
            elif s == "delete":
                # disable users from editing the items to be deletion
                quantityinput.configure(state="disabled")
                unitsInput.configure(state="disabled")
                #change the action button text
                submitButton.configure(text="Confirm deletion")
            else:
                # only want to "edit" quantity -> disable everything but quantity
                unitsInput.configure(state="disabled")
                #show moving location dropdown
                fillerlbl.pack(side=BOTTOM, pady=25)
                locationDD.pack(side=BOTTOM, pady=5)
                movelbl.pack(side=BOTTOM)

        #set default screen option as update
        self.screenopt.set("update")
        options = ["update", "move", "delete"]
        # when screenopt is changed, calls showscreen to change the screen
        self.screenopt.trace('w', showScreen)
        #holds the screen options
        tabControl = ttk.Combobox(screen, textvariable=self.screenopt, values=options, font=(font, 12), width=7)
        tabControl.pack(pady=10)
        #add action/function to submit button
        submitButton.configure(command=saveChanges)

StaffGUI()

