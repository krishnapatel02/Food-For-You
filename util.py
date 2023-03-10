import mysql.connector
from tkinter import ttk

font = "Helvetica"
searchInputSize = "9"
regFontSize = "12"

style = ttk.Style()
style.theme_create("Custom")
# style.wm_attributes('-transparentcolor', '#ab23ff')
style.configure("TLabel", font=f'{font} {regFontSize}', background="#fff")
style.configure("TButton", font=f'{font} {regFontSize}', background="#fff")
style.configure("TCheckbutton", font=f'{font} {regFontSize}', background="#fff")
style.configure("TEntry", font=f'{font} {regFontSize}')
#style.configure("Spinbox")

def fetchLocations(cursor):
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