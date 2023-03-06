import tkinter as t
from tkinter import ttk
import mysql.connector
#https://www.google.com/search?q=create+theme+tkinter+python&rlz=1C1VDKB_enUS1034US1034&sxsrf=AJOqlzVyUBHWRfGeC6eRK0zbFZLyOMlJmw%3A1678037292298&ei=LNEEZN7tEY660PEPkbOW6AE&ved=0ahUKEwjes-iFqMX9AhUOHTQIHZGZBR0Q4dUDCBA&uact=5&oq=create+theme+tkinter+python&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIICCEQoAEQwwQyCAghEKABEMMEOgoIABBHENYEELADOgcIIxCwAhAnOggIABAIEAcQHjoICAAQCBAeEA06BQgAEIYDOgoIIRCgARDDBBAKSgQIQRgAUNoDWMMJYO0KaAFwAXgAgAF3iAH5BJIBAzUuMpgBAKABAcgBCMABAQ&sclient=gws-wiz-serp#fpstate=ive&vld=cid:55497400,vid:fOVmMiyezMU

def connectToDatabase(user, password, host, port, database):
    dbconnect = None
    counter = 0
    while dbconnect is None:
        if(counter >= 10):
            print("Check connection to internet")
            exit()
        try:
            dbconnect = mysql.connector.connect(
                host = host,
                user = user,
                passwd=password,
                port = port,
                database = database)
            print("Connected")
        except:
            print("Connection failed")
            dbconnect = None
            counter+=1
    return dbconnect


connection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3624, "foodforyou")
cursor = connection.cursor()
cursor.execute("SELECT fb.Location from food_bank fb")
locations = []
for row in cursor:
    for col in row:
        locations.append(col)
locations.append(None)
print(locations)

def updateItem():
    def saveChanges():
        item = iteminput.get(1.0, "end-1c")
        print("item: ", item)
        quantity = quantityinput.get(1.0, "end-1c")
        print("quantity: ", quantity)
        location = locationDD.get()

        #database stuff

        updateItemScreen.destroy()


    updateItemScreen = t.Tk()
    updateItemScreen.geometry("500x200")

    iteminput = t.Text(updateItemScreen,
        height=2,
        width=10
    )
    itemLabel = t.Label(updateItemScreen,
        text="item"
    )

    quantityinput = t.Text(updateItemScreen,
        height=2,
        width=10
    )
    quantityLabel = t.Label(updateItemScreen,
            text="quantity"
    )

    locationLabel = t.Label(updateItemScreen,
        text="location"
    )

    locationDD = ttk.Combobox(updateItemScreen,
        values=["abc"]
    )

    submitButton = t.Button(updateItemScreen,
        text = "Save changes",
        height =2,
        width =10,
        command=saveChanges
        )

    iteminput.place(x=25, y=50)
    itemLabel.place(x=25, y=25)
    quantityinput.place(x=150, y=50)
    quantityLabel.place(x=150, y=25)
    locationDD.place(x=275, y=50)
    locationLabel.place(x=265, y=25)
    submitButton.place(x=400, y=150)

    ## TODO: insert item, quanity and location from selection
    ##       autofill item


    updateItemScreen.mainloop()


"""
Function name: focus()
Usage: Auto fill the values when a table item is selected
"""

foodItemSearchText = None


# def focus(e):
#     cursor = table.focus()
#     content = table.item(cursor)
#     row = content['values']
#     self.title.set(row[0])
#     self.term.set(row[1])
#     self.name.set(row[2])
#     self.A.set(row[3])
#     self.B.set(row[4])
#     self.C.set(row[5])
#     self.D.set(row[6])
#     self.F.set(row[7])
#     self.crn.set(row[8])
#     self.facultyType.set(row[9])

def searchQuery():
    item = ItemSearch.get(1.0, "end-1c")
    locationBool = True
    itemBool = True
    location = LocationFilter.get()
    ascending = ascSort.get()
    if(location == "None" or location == ""):
        locationBool = False
    if(item.strip() == ""):
        itemBool = False
    if(locationBool and itemBool and ascending):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}' order by fi.Quantity ASC")
    elif(locationBool and ascending):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}' order by fi.Quantity ASC")
    elif(itemBool and ascending):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' order by fi.Quantity ASC")
    elif(itemBool and locationBool):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}' and fb.location = '{location}'")
    elif(itemBool):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fi.Item_name='{item}'")
    elif(locationBool):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) where fb.location = '{location}'")
    elif(ascending):
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id) order by fi.quantity ASC")
    else:
        cursor.execute(f"SELECT fi.Item_name, fi.Quantity, fi.Units, fi.fd_id, fb.Location from food_item fi join food_bank fb using(fb_id)")
    result = cursor.fetchall()
    for line in result:
        print(line)
        

    ##database stuff




mainScreen = t.Tk()
mainScreen.geometry("1000x500")
ascSort = t.BooleanVar()
# UpdateItemButton = t.Button(mainScreen,
#     text="Update Item",
#     width = 20,
#     height = 3,
#     command=updateItem
#     )

ItemSearch = t.Text(mainScreen,
        height=2,
        width=15,
        
)

SearchButton = t.Button(mainScreen,
    text="Search",
    width = 15,
    height = 1,
    command=searchQuery
)

SearchLabel = t.Label(mainScreen,
    text= "item to search"
)


QuantitySortLabel = t.Label(mainScreen,
    text= "Sort quantity"
)

QuantitySortButton = t.Checkbutton(mainScreen,
    text="Sort Ascending",
    width = 15,
    height = 1,
    variable = ascSort,
    onvalue=True,
    offvalue=False,
)

LocationLabel = t.Label(mainScreen,
    text= "Sort by location"
)

LocationFilter = ttk.Combobox(mainScreen,
    values=locations
)


QuantitySortLabel.place(x=700, y=50)
QuantitySortButton.place(x=700, y=100)
LocationLabel.place(x=700, y=200)
LocationFilter.place(x=700, y=250)

#UpdateItemButton.place(x=300, y=400)
SearchLabel.place(x=700, y=325)
ItemSearch.place(x=700, y=350)
SearchButton.place(x=725, y=400)


mainScreen.mainloop()
connection.close()