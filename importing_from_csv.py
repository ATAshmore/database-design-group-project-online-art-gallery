import sqlite3, csv

connection = sqlite3.connect("dbdesignproj.db")
cursor = connection.cursor()

with open('favoriteartists.csv' , 'r') as file:
    #artistID,firstName,lastName,dob,primaryMedium,biography,originCountry,username,password
    no_records = 0
    for row in file:
        to_send = row.split(",")
        to_send[-1] = to_send[-1][:-1]
        print(to_send)

        cursor.execute("INSERT INTO FavoriteArtist VALUES (?,?)", to_send)
        connection.commit()
        no_records += 1

connection.close()
print('\n{} Records Transffered'.format(no_records))