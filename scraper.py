# https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions
import mechanicalsoup
import pandas as pd
import sqlite3

browser = mechanicalsoup.StatefulBrowser()

browser.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")

# extract table headers
th = browser.page.find_all("th", attrs={"class": "table-rh"})
distribution = [value.text.replace("\n", "") for value in th]
distribution = distribution[:distribution.index("Zorin OS")+1]

# extract table data
td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]
# print(columns.index("AlmaLinux Foundation"))
# print(columns.index("Zorin OS Lite & Core are free, while Business and Ultimate are paid")+2)
columns = columns[6:1062]

column_names = ["Founder",
                "Maintainer",
                "Initial_Release_Year",
                "Current_Stable_Version",
                "Security_Updates",
                "Release_Date",
                "System_Distribution_Commitment",
                "Forked_From",
                "Target_Audience",
                "Cost",
                "Status"]

dictionary = {"Distribution": distribution}

# insert column names and their data into a dictionary
for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::11]

# convert dictionary to data frame
df = pd.DataFrame(data=dictionary)
# print(df)

# create new database and cursor
connection = sqlite3.connect("linux_distro.db")
cursor = connection.cursor()

# create database table and insert all data frame rows
cursor.execute("create table linux (Distribution, " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

# PERMANENTLY save inserted data in "linux_distro.db"
connection.commit()

connection.close()












