from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

font = "Helvetica"
searchInputSize = "9"
regFontSize = "11"

port = 3079     #holds the database port number

def use_theme(window:Tk):
    """ use_theme(window)
    Applies the theme to the inputted 'window'
    Note: can change the font (font) and size (regFontSize) from the global variables
    """
    style = ttk.Style(window)
    style.theme_create("Custom")    #creates a blank theme
    # creates a theme for such widgets
    style.configure("TLabel", font=(f'{font}, {regFontSize}'), background="#fff")
    style.configure("TButton", font=(f'{font}, {regFontSize}'), background="#fff")
    style.configure("TCheckbutton", font=(f'{font}, {regFontSize}'), background="#fff")
    style.configure("TEntry", font=(f'{font}, {regFontSize}'))
    style.configure("TSpinbox", font=(f'{font} {regFontSize}'))

def fetchLocations(cursor):
    """ fetchLocations(cursor)
    Pulls the existing locations from the database from the cursor.
    """
    cursor.execute("SELECT fb.Location from food_bank fb order by fb.Location ASC") #selects all foodbank locations from food bank database
    locations = []
    locations.append(None)
    #for each row in the databsae
    for row in cursor:
        #grab the location and appends to return value
        for col in row:
            locations.append(col)
    return locations

def fetchCategory(cursor):
    """ fetchLocations(cursor)
        Pulls the existing categories from the database from the cursor.
    """
    cursor.execute("SELECT DISTINCT fi.Category from food_item fi order by fi.Category ASC") #selects all distinct categories from food bank database
    categories = []
    #for each row in the databsae
    for row in cursor:
        #grab the category and appends to return value
        for col in row:
            categories.append(col)
    return categories

def connectToDatabase(user, password, host, port, database):
    """ connectToDatabase(user, password, host, port, database)
    user: username
    password: user's password
    host: server name
    port: port number
    database: database name
    """
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