import tkinter as tk
import mysql.connector as mysql
import datetime

def connectToDatabase(user, password, host, port, database):
    dbconnect = None
    counter = 0
    while dbconnect is None:
        if (counter >= 10):
            print("Check connection to internet")
            exit()
        try:
            dbconnect = mysql.connect(
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

connection = connectToDatabase("jerryp", "111", "ix-dev.cs.uoregon.edu", 3624, "foodforyou")
c = connection.cursor()

# get the food options from the database
c.execute("SELECT DISTINCT Item_name FROM food_item")
food_options = [row[0] for row in c.fetchall()]

c.execute("SELECT DISTINCT Neighborhood FROM food_bank")
neighborhood_options = [row[0] for row in c.fetchall()]

# create the GUI window
root = tk.Tk()
root.title("Food Finder")
# window size
root.geometry("430x340")
root.resizable(False, False)

try:
    root.bg = tk.PhotoImage(file="img/backgroundimg.png")
    tk.Label(image=root.bg, borderwidth=0, highlightthickness=0).place(relx=-.15, rely=0)

    root.trailing_img = tk.PhotoImage(file="img/trailingIMG.png")
    for i in range(0, 480, root.trailing_img.width()):
        tk.Label(root, image=root.trailing_img, bg='white').place(x=i, y=280)
except Exception as e:
    print(e)

# create the food category dropdown
food_label = tk.Label(root, text="Select a food category:")
food_label.pack()
food_label.place(relx=0.5, rely=0.36, anchor=tk.CENTER)
# add a blank option to the list of food options
food_options.insert(0, "All Food")
# create the variable for the food dropdown and set it to the first option
food_var = tk.StringVar(root)
food_var.set(food_options[0])
# create the food dropdown with the blank option
food_dropdown = tk.OptionMenu(root, food_var, *food_options)
food_dropdown.pack()
food_dropdown.place(relx=0.5, rely=0.43, anchor=tk.CENTER)

# create the neighborhood dropdown
neighborhood_label = tk.Label(root, text="Select a neighborhood:")
neighborhood_label.pack()
neighborhood_label.place(relx=0.5, rely=0.53, anchor=tk.CENTER)
# add a blank option to the list of neighborhoods
neighborhood_options.insert(0, "All Neighborhoods")
# create the variable for the neighborhood dropdown and set it to the first option
neighborhood_var = tk.StringVar(root)
neighborhood_var.set(neighborhood_options[0])
# create the neighborhood dropdown with the blank option
neighborhood_dropdown = tk.OptionMenu(root, neighborhood_var, *neighborhood_options)
neighborhood_dropdown.pack()
neighborhood_dropdown.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def opennow(neighborhood):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    dayofweek = datetime.datetime.now().weekday()
    day = days[dayofweek]
    open_stat = []
    dayclose = f"{day}_close"
    if neighborhood != "All Neighborhoods":
        c.execute(f"SELECT h.{day}, h.{dayclose}, fb.Location "
                  f"FROM hours h "
                  f"JOIN food_bank fb USING(fb_id) "
                  f"WHERE fb.Neighborhood = '{neighborhood}' "
                  f"AND h.{day} <> '' "
                  f"AND h.{dayclose} <> '' ")
    else:
        c.execute(f"SELECT h.{day}, h.{dayclose}, fb.Location "
                  f"FROM hours h "
                  f"JOIN food_bank fb USING(fb_id) "
                  f"WHERE h.{day} <> '' AND h.{dayclose} <> '' ")

    hours = c.fetchall()
    if len(hours) == 0:
        return open_stat
    for entry in hours:
        open_time = entry[0]
        close_time = entry[1]
        if open_time <= time_str <= close_time:
            if entry[2] not in open_stat:
                open_stat.append(entry[2])
    return open_stat

def writetofile(filename, results, open_stat):
    with open(filename, 'w') as f:
        maxitem = 0
        maxlocation = 0
        maxstatus = 0
        for entry in results:
            lenentry = len(entry[0])
            lenlocation = len(entry[1])
            lenstatus = len(entry[2])
            if lenentry > maxitem:
                maxitem = len(entry[0])
            if lenlocation > maxlocation:
                maxlocation = lenlocation
            if lenstatus > maxstatus:
                maxstatus = lenstatus
        ispace = (maxitem + 5 - 4) * " "
        lspace = (maxlocation + 5 - 8) * " "
        sspace = (maxstatus + 5 - 6) * " "
        f.write(f"Item{ispace}Location{lspace}Status{sspace}Hours\n")
        f.write('-' * (maxitem + maxlocation +33) + '\n')
        print(f"Item{ispace}Location{lspace}Status{sspace}Hours")
        print("-"*(maxitem + maxlocation + 34))
        for entry in results:
            fname = entry[0]
            fspace = (maxitem + 5 - len(fname)) * " "
            lname = entry[1]
            lspace = (maxlocation + 5 - len(lname)) * " "
            stat = entry[2]
            sspace = (maxstatus + 5 - len(stat)) * " "
            if open_stat != []:
                if lname in open_stat:
                    hours = "Open Now"
                else:
                    hours = "Closed"
            else:
                hours = "Closed"
            f.write(f"{fname}{fspace}{lname}{lspace}{stat}{sspace}{hours}\n")
            print(f"{fname}{fspace}{lname}{lspace}{stat}{sspace}{hours}")
        print("\n")

# create a function to get the data from the database and display it
def search_database():
    food = food_var.get()
    neighborhood = neighborhood_var.get()

    if neighborhood == "All Neighborhoods" and food == "All Food":
        c.execute(f"SELECT fi.Item_name, fi.Location, "
                  f"CASE WHEN Quantity = 0 THEN 'Unavailable' "
                  f"WHEN Quantity < 21 THEN 'Low Stock' ELSE 'Available' END AS stock_status "
                  f"FROM food_item fi "
                  f"LEFT JOIN food_bank fb USING(Location) "
                  f"ORDER BY Quantity DESC")
    elif neighborhood == "All Neighborhoods":
        c.execute(f"SELECT fi.Item_name, fi.Location, "
                  f"CASE WHEN Quantity = 0 THEN 'Unavailable' "
                  f"WHEN Quantity < 21 THEN 'Low Stock' ELSE 'Available' END AS stock_status "
                  f"FROM food_item fi "
                  f"LEFT JOIN food_bank fb USING(Location) "
                  f"WHERE fi.Item_name = '{food}' "
                  f"ORDER BY fi.Quantity DESC")
    elif food == "All Food":
        c.execute(f"SELECT fi.Item_name, fi.Location, "
                  f"CASE WHEN Quantity = 0 THEN 'Unavailable' "
                  f"WHEN Quantity < 21 THEN 'Low Stock' ELSE 'Available' END AS stock_status "
                  f"FROM food_item fi "
                  f"LEFT JOIN food_bank fb USING(Location) "
                  f"WHERE fb.Neighborhood = '{neighborhood}' "
                  f"ORDER BY Quantity DESC")
    else:
        c.execute(f"SELECT fi.Item_name, fi.Location, "
                  f"CASE WHEN Quantity = 0 THEN 'Unavailable' "
                  f"WHEN Quantity < 21 THEN 'Low Stock' ELSE 'Available' END AS stock_status "
                  f"FROM food_item fi "
                  f"LEFT JOIN food_bank fb USING(Location) "
                  f"WHERE fi.Item_name = '{food}' AND fb.Neighborhood = '{neighborhood}' "
                  f"ORDER BY Quantity DESC")

    results = c.fetchall()

    if results == []:
        print(f"{food} is not available at the food banks located in {neighborhood}. "
              f"Please either select a different food item or neighborhood. Thank you!")
        return

    filename = f"{food}AvailabilityAt{neighborhood}.txt"
    open_stat = opennow(neighborhood)
    writetofile(filename, results, open_stat)


# create the search button
search_button = tk.Button(root, text="Search", command=search_database)
search_button.pack()
search_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# create the label to display the results
result_label = tk.Label(root, text="")
result_label.pack()

# start the main loop
root.mainloop()

# close the database connection when finished
connection.close()