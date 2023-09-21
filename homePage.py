import sqlite3
from datetime import datetime
import random

loggedIn = False
activeUser = None
userType = None
cursor = None
connection = None

def view_my_art(artist_id):
    global cursor, connection
    query = """SELECT * FROM ArtPiece WHERE artist = ?;"""
    tup = (artist_id, )
    cursor.execute(query, tup)
    connection.commit()
    data = cursor.fetchall()
    if len(data) == 0:
        print("There were no artworks found")
        input("Press any key to return: ")
        return
    should_return = ""
    for art in data:
        for item in art:
            if item == None:
                item = "Information Not Found"
        print(f"Description: {art[9]}")
        print(f"Year: {art[6]}")
        print(f"Style: {art[7]}")
        print(f"Medium: {art[8]}")
        print(f"List Price: {art[10]}")
        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
            cursor.execute(cus_query, (art[13],))
            connection.commit()
            customer = cursor.fetchall()[0]
            print(f"Purchase Date: {art[1]}")
            print(f"Purchased By: {customer[0]} {customer[1]}")
        print(f"Height and Width: {art[3]} {art[4]}")
        print(f"Condition: {art[5]}")
        print(f"Stored in Gallery ID: {art[11]}")
        should_return = input("Press any key to continue to the next piece, or press (R) to return: ").lower()
        if should_return == "r":
            break


def length_check(length, input_type):
    returnable = input(f"Please enter your {input_type} (up to {length} characters): ")
    while len(returnable) > length:
        print("Too Long!")
        returnable = input(f"Please enter your {input_type} (up to {length} characters): ")
    return returnable

def signup():
    random.seed()
    total = 1
    global loggedIn, activeUser, userType, cursor, connection
    artist_status = input("Would you like to sign up as an artist (y/n): ")
    username = input("Please enter your username (up to 20 characters): ")
    if artist_status.lower() == "y":
        unamecheck = "SELECT * FROM Artist WHERE username = ?;"
    else:
        unamecheck = "SELECT * FROM Customer WHERE username = ?;"
    cursor.execute(unamecheck, (username,))
    data = cursor.fetchall()
    while len(username) > 20 or len(data) > 0:
        if len(data) > 0:
            print("Username is taken")
        else:
            print("Invalid Username")
        username = input("Please enter your username (up to 20 characters): ")
        if artist_status.lower() == "y":
            unamecheck = "SELECT * FROM Artist WHERE username = ?;"
        else:
            unamecheck = "SELECT * FROM Customer WHERE username = ?;"
        cursor.execute(unamecheck, (username,))
        data = cursor.fetchall()
    password = length_check(50, "password")
    fn = length_check(20, "first name")
    ln = length_check(20, "last name")
    if artist_status.lower() == "n":
        email = length_check(254, "email")
        while "@" not in email or "." not in email or email[-1] == ".":
            print("Invalid Email.")
            email = length_check(254, "email")

    if artist_status.lower() == "y":
        while total != 0:
            random_id = random.randint(0, 8000000000000)
            verification_check = """SELECT COUNT(*) FROM Artist WHERE artistID = ?;"""
            cursor.execute(verification_check, (random_id,))
            total = cursor.fetchone()
            total = total[0]
        query = """INSERT INTO Artist (artistID, username, password, firstName, lastName) VALUES (?,?,?,?,?); """
        userType = "artist"
        tup = (random_id, username, password, fn, ln)
    else:
        while total != 0:
            random_id = random.randint(0, 8000000000000)
            verification_check = """SELECT COUNT(*) FROM Customer WHERE customerID = ?;"""
            cursor.execute(verification_check, (random_id,))
            total = cursor.fetchone()
            total = total[0]
        query = """INSERT INTO Customer (customerID, username, password, firstName, lastName, email) VALUES (?,?,?,?,?,?); """
        userType = "customer"
        tup = (random_id, username, password, fn, ln, email)
    cursor.execute(query, tup)
    loggedIn = True
    activeUser = username

    connection.commit()
    return

def artist_login():
    global loggedIn, activeUser, userType
    login_attempts = 0
    username = ""
    password = ""
    while not loggedIn and username.lower() != "r" and login_attempts < 5:
        username = input("\nPlease enter your username: ")
        password = input("Please enter your password: ")
        query = """SELECT * FROM Artist WHERE username = ? AND password = ?; """
        cursor.execute(query, (username, password))
        data = cursor.fetchall()
        if len(data) == 0:
            login_attempts += 1
            continue
        else:
            loggedIn = True
            activeUser = username
            userType = "artist"
    return

def login():
    global loggedIn, activeUser, userType
    login_attempts = 0
    username = ""
    password = ""
    while not loggedIn and username.lower() != "r" and login_attempts < 5:
        username = input("\nPlease enter your username: ")
        password = input("Please enter your password: ")
        query = """SELECT * FROM Customer WHERE username = ? AND password = ?; """
        cursor.execute(query, (username, password))
        data = cursor.fetchall()
        if len(data) == 0:
            login_attempts += 1
            continue
        else:
            loggedIn = True
            activeUser = username
            userType = "customer"
    return

def logout():
    global loggedIn, activeUser, userType
    loggedIn = False
    activeUser = None
    userType = None

def artist_profile(row):
    global cursor, connection
    print("\nThank you for contributing to the Gallery. Please update any information, so customers may better find your work.")
    print("You can also view your artworks in the gallery!")
    print(f"Your First Name: {row[1]}")
    print(f"Your Last Name: {row[2]}")
    print(f"Your DOB: {row[3]}")
    print(f"Your Primary Medium: {row[4]}")
    print(f"Your Biography: {row[5]}")
    print(f"Your Country of Origin: {row[6]}")
    selection = ""
    while(selection != "r"):
        selection = input("Update your"
        "\n(D)OB"
        "\n(P)rimary Medium"
        "\n(B)iography"
        "\n(C)ountry"
        "\n(V)iew your art"
        "\n(R)eturn: "
        ).lower()
        if selection == 'd':
            new_dob = input("Please enter your DOB in the format YYYY-MM-DD: ")
            try:
                date = datetime(int(new_dob[0:4]), int(new_dob[5:7]), int(new_dob[8:]))
            except:
                print("Invalid Date")
            query = """UPDATE Artist set DOB = ? where artistID = ?"""
            tup = (date, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'p':
            new_medium = length_check(50, "primary medium")
            query = """UPDATE Artist set primaryMedium = ? where artistID = ?"""
            tup = (new_medium, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'b':
            new_bio = length_check(400, "biography")
            query = """UPDATE Artist set biography = ? where artistID = ?"""
            tup = (new_bio, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'c':
            new_country = length_check(50, "country of origin")
            query = """UPDATE Artist set originCountry = ? where artistID = ?"""
            tup = (new_country, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'v':
            view_my_art(row[0])
        elif selection == 'r':
            break
        else:
            print("invalid input")
    


def customer_profile(row):
    global cursor, connection
    #   TESTING - print(row)
    print("\nThank you for being a loyal customer! Your information is as follows: ")
    print(f"Your Gender: {row[1]}")
    print(f"Your Phone Number: {row[2]}")
    print(f"Your First Name: {row[4]}")
    print(f"Your Last Name: {row[5]}")
    print(f"Your Card Number: Hidden for your security")
    print(f"Your Address: {row[7]}")
    print(f"Your Primary Store: {row[8]}")
    selection = ""
    while(selection != "r"):
        selection = input("\nUpdate your:"
        "\n(G)ender"
        "\n(P)hone Number"
        "\n(F)irst Name"
        "\n(L)ast Name"
        "\n(C)ard Number"
        "\n(A)ddress"
        "\n(R)eturn: "
        ).lower()
        if selection == 'g':
            new_gender = length_check(9, "gender")
            query = """UPDATE Customer set gender = ? where customerID = ?"""
            tup = (new_gender, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'p':
            phone_num = ""
            while len(phone_num) != 12:
                phone_num = input("Please enter your phone number of the format xxx-xxx-xxxx: ")
            query = """UPDATE Customer set phoneNumber = ? where customerID = ?"""
            tup = (phone_num, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'f':
            new_fn = length_check(20, "first name")
            query = """UPDATE Customer set firstName = ? where customerID = ?"""
            tup = (new_fn, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'l':
            new_ln = length_check(50, "last name")
            query = """UPDATE Customer set lastName = ? where customerID = ?"""
            tup = (new_ln, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'c':
            card_num = ""
            while len(card_num) != 16:
                card_num = input("Please enter your 16 digit card number")
            query = """UPDATE Customer set cardNumber = ? where customerID = ?"""
            tup = (card_num, row[0])
            cursor.execute(query, tup)
            connection.commit()
        elif selection == 'a':
            new_ln = length_check(40, "address")
            query = """UPDATE Customer set address = ? where customerID = ?"""
            tup = (new_ln, row[0])
            cursor.execute(query, tup)
            connection.commit()
        else:
            print("\ninvalid input")

def user_page():
    global cursor, userType, activeUser
    if userType == "artist":
        query = "SELECT * FROM Artist WHERE username = ?;"
    else:
        query = "SELECT * FROM Customer WHERE username = ?"
    cursor.execute(query, (activeUser,))
    data = cursor.fetchall()[0]
    if len(data) == 0:
        print("Profile Read Error. Returning to the main menu.")
        return
    if userType == "artist":
        artist_profile(data)
    else:
        customer_profile(data)
    return

def search():
    global loggedIn, activeUser, userType, cursor, connection
    selection = ""
    while selection != "r":
        selection = input(
        "\nSearch: "
        "\n(A)rtist"
        "\n(P) for Art Piece "
        "\n(R) to return: "
        ).lower()

        #   ARTIST
        if selection == 'a':
            selection_a = ""
            while selection_a != 'r':
                selection_a = input(
                "\nSearch Artist by:"
                "\n(A)ll artists" 
                "\n(F)irst name"
                "\n(L)ast name"
                "\n(M)edium"
                "\n(R) to return: "
                ).lower()
                
                #   ALL Artists
                if selection_a == 'a':
                    tup = ""
                    while tup != "firstName" and tup != "lastName" and tup != "primaryMedium":
                        tup = input(
                        "\nPlease type one of the options to order all artists by:"
                        "\nfirstName"
                        "\nlastName"
                        "\nprimaryMedium: "
                        )
                    cursor.execute("SELECT * FROM Artist ORDER BY {} ;".format(tup))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("Nothing found")
                        continue
                    for artist in data:
                        for item in artist:
                            if item == None:
                                item = "None Listed"
                        print("\n")
                        print(f"Name: {artist[1]} {artist[2]}")
                        print(f"Primary Medium: {artist[4]}")
                        print(f"Biography: {artist[5]}")
                        print(f"Nationality: {artist[6]}")
                        if loggedIn and userType == 'customer':
                            shouldFavorite = input("(S)ave this artist, or press (C) to stop the search, or any other key to continue: ").lower()
                            if shouldFavorite == 's':
                                cursor.execute("""SELECT customerID FROM Customer WHERE username = ?;""", (activeUser,))
                                cID = cursor.fetchall()[0][0]
                                cursor.execute("""SELECT COUNT(*) FROM FavoriteArtist WHERE customerID = ? AND artistID = ?""", (cID, artist[0]))
                                exists = cursor.fetchall()[0][0]
                                if exists > 0:
                                    print("Already saved!")
                                    continue
                                query = """INSERT INTO FavoriteArtist (customerID, artistID) VALUES (?,?);"""
                                tup = (cID, artist[0])
                                cursor.execute(query, tup)
                                connection.commit()
                            elif shouldFavorite == 'c':
                                break

                #   First Name
                elif selection_a == 'f':
                    tup = input("\nPlease enter artist's first name: ")
                    query = """SELECT * FROM Artist WHERE firstName LIKE ? ORDER BY lastName; """
                    cursor.execute(query, ("%"+tup+"%",))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("Nothing found")
                        continue
                    for artist in data:
                        for item in artist:
                            if item == None:
                                item = "None Listed"
                        print(f"Name: {artist[1]} {artist[2]}")
                        print(f"Primary Medium: {artist[4]}")
                        print(f"Biography: {artist[5]}")
                        print(f"Nationality: {artist[6]}")
                        if loggedIn and userType == 'customer':
                            shouldFavorite = input("(S)ave this artist, or press (C) to stop the search, or any other key to continue: ").lower()
                            if shouldFavorite == 's':
                                cursor.execute("""SELECT customerID FROM Customer WHERE username = ?;""", (activeUser,))
                                cID = cursor.fetchall()[0][0]
                                cursor.execute("""SELECT COUNT(*) FROM FavoriteArtist WHERE customerID = ? AND artistID = ?""", (cID, artist[0]))
                                exists = cursor.fetchall()[0][0]
                                if exists > 0:
                                    print("Already saved!")
                                    continue
                                query = """INSERT INTO FavoriteArtist (customerID, artistID) VALUES (?,?);"""
                                tup = (cID, artist[0])
                                cursor.execute(query, tup)
                                connection.commit()
                            elif shouldFavorite == 'c':
                                break

                #   Last name
                elif selection_a == 'l':
                    tup = input("\nPlease enter artist's last name: ")
                    query = """SELECT * FROM Artist WHERE lastName LIKE ? ORDER BY firstName; """
                    cursor.execute(query, ("%"+tup+"%",))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("Nothing found")
                        continue
                    for artist in data:
                        for item in artist:
                            if item == None:
                                item = "None Listed"
                        print(f"Name: {artist[1]} {artist[2]}")
                        print(f"Primary Medium: {artist[4]}")
                        print(f"Biography: {artist[5]}")
                        print(f"Nationality: {artist[6]}")
                        if loggedIn and userType == 'customer':
                            shouldFavorite = input("(S)ave this artist, or press (C) to stop the search, or any other key to continue: ").lower()
                            if shouldFavorite == 's':
                                cursor.execute("""SELECT customerID FROM Customer WHERE username = ?;""", (activeUser,))
                                cID = cursor.fetchall()[0][0]
                                cursor.execute("""SELECT COUNT(*) FROM FavoriteArtist WHERE customerID = ? AND artistID = ?""", (cID, artist[0]))
                                exists = cursor.fetchall()[0][0]
                                if exists > 0:
                                    print("Already saved!")
                                    continue
                                query = """INSERT INTO FavoriteArtist (customerID, artistID) VALUES (?,?);"""
                                tup = (cID, artist[0])
                                cursor.execute(query, tup)
                                connection.commit()
                            elif shouldFavorite == 'c':
                                break
                
                #   Medium
                elif selection_a == 'm':
                    tup = input("\nPlease enter artist's primary medium: ")
                    query = """SELECT * FROM Artist WHERE primaryMedium LIKE ? ORDER BY lastName, firstName; """
                    cursor.execute(query, ("%"+tup+"%",))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("Nothing found")
                        continue
                    for artist in data:
                        for item in artist:
                            if item == None:
                                item = "None Listed"
                        print(f"Name: {artist[1]} {artist[2]}")
                        print(f"Primary Medium: {artist[4]}")
                        print(f"Biography: {artist[5]}")
                        print(f"Nationality: {artist[6]}")
                        if loggedIn and userType == 'customer':
                            shouldFavorite = input("(S)ave this artist, or press (C) to stop the search, or any other key to continue: ").lower()
                            if shouldFavorite == 's':
                                cursor.execute("""SELECT customerID FROM Customer WHERE username = ?;""", (activeUser,))
                                cID = cursor.fetchall()[0][0]
                                cursor.execute("""SELECT COUNT(*) FROM FavoriteArtist WHERE customerID = ? AND artistID = ?""", (cID, artist[0]))
                                exists = cursor.fetchall()[0][0]
                                if exists > 0:
                                    print("Already saved!")
                                    continue
                                query = """INSERT INTO FavoriteArtist (customerID, artistID) VALUES (?,?);"""
                                tup = (cID, artist[0])
                                cursor.execute(query, tup)
                                connection.commit()
                            elif shouldFavorite == 'c':
                                break

                #   Return
                elif selection_a == 'r':
                    return
                
                #   Invalid
                else:
                    print("Invalid Input")

        #   ART PIECE
        elif selection == 'p':
            selection_p = ""
            while selection_p != 'r':
                also_add = ""
                if userType == "customer":
                    also_add = "\n(F)avorite Artist"
                selection_p = input(
                "\nSearch Art Piece by:"
                "\n(E) for all artpieces"
                "\n(A)rtist"
                "\n(G)allery"
                "\n(C)ondition"
                "\n(S)tyle"
                "\n(M)edium"
                "\n(W)eight"
                "\n(D)imensions"
                f"\n(P)rice{also_add}"
                "\n(R) to return: "
                ).lower()

                #   ALL Artists
                if selection_p == 'e':
                    tup = ""
                    while tup not in ["purchaseDate","weight", "width", "height", "condition", "style", "medium", "listPrice", "style"]: 
                        tup = input(
                        "\nPlease type one of the options to order all art pieces by:"
                        "\npurchaseDate"
                        "\nweight"
                        "\nwidth"
                        "\nheight"
                        "\ncondition"
                        "\nstyle"
                        "\nmedium"
                        "\nlistPrice"
                        "\nstyle: "
                        )
                    cursor.execute("SELECT * FROM ArtPiece ORDER BY {}".format(tup))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == None or item == '':
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}\n")
                
                #   Artist
                elif selection_p == 'a':
                    tup = input("\nPlease enter the name of the first name or the last name of the artist: ")
                    query = """SELECT * FROM ArtPiece JOIN Artist ON ArtPiece.artist = Artist.artistID WHERE firstName LIKE ? OR lastName LIKE ? ORDER BY pieceID; """
                    cursor.execute(query, ("%"+tup+"%","%"+tup+"%"))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")
                
                #   Gallery
                elif selection_p =='g':
                    search_term = input("\nPlease enter the address of the gallery of the art piece: ")
                    query = """SELECT * FROM ArtPiece INNER JOIN gallery ON ArtPiece.gallery = Gallery.storeID WHERE address LIKE ? ORDER BY pieceID; """
                    tup = ("%"+search_term+"%",)
                    cursor.execute(query, tup)
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")
                
                #   Condition
                elif selection_p =='c':
                    print(
                    "\nCommon art conditions:"
                    "\nexcellent"
                    "\ngood"
                    "\nfair"
                    )
                    tup = input("\nPlease enter the condition of the art piece: ")
                    query = """SELECT * FROM ArtPiece WHERE condition LIKE ? ORDER BY pieceID; """
                    cursor.execute(query, ("%"+tup+"%",))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")

                #   Style
                elif selection_p =='s':
                    print(
                    "\nCommon art styles:"
                    "\nminimalism"
                    "\npop"
                    "\nimpressionism"
                    "\nconceptual"
                    "\nabstract"
                    "\nmodern"
                    "\nrealism"
                    )
                    tup = input("\nPlease enter the style of the art piece: ").lower()
                    query = """SELECT * FROM ArtPiece WHERE style LIKE ? ORDER BY pieceID; """
                    cursor.execute(query, ("%"+tup+"%",))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")

                #   Medium
                elif selection_p =='m':
                    print(
                    "\nCommon art mediums:"
                    "\noil" 
                    "\nacrylic"
                    "\nwatercolor"
                    "\ncharcoal"
                    "\npasatel"
                    "\nchalk"
                    "\nink"
                    "\npencil"
                    "\nclay"
                    "\nmetal"
                    "\nstone"
                    "\nmixed media")
                    tup = input("\nPlease enter the medium of the art piece: ").lower()
                    query = """SELECT * FROM ArtPiece WHERE medium LIKE ? ORDER BY pieceID; """
                    cursor.execute(query, ("%"+tup+"%",))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")

                #   Weight
                elif selection_p =='w':
                    tup = input("\nPlease enter the maximum weight of the art piece: ")
                    query = """SELECT * FROM ArtPiece WHERE weight <= ? ORDER BY pieceID; """
                    cursor.execute(query, (tup,))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")

                #   dimensions
                #   select artpiece of both width and height
                elif selection_p =='d':
                    selection_p_d = ""
                    while selection_p_d != 'r':
                        print(
                        "\nCommon art dimensions(width x height): "
                        "\n8 x 8"
                        "\n8 x 10"
                        "\n9 x 12"
                        "\n10 x 10"
                        "\n12 x 36"
                        "\n18 x 24"
                        "\n36 x 48"
                        )

                        selection_p_d = input(
                        "\nSearch for Art Piece by dimensions by:"
                        "\n(S)et Dimensions listed above"
                        "\n(C)ustom Dimensions"
                        "\n(R)eturn: "
                        ).lower()

                        #   Set dimensions.. based on common dimensions
                        if selection_p_d == 's':
                            width = input("Please enter width of art piece: ")
                            height = input("Please enter height of art piece: ")
                            tup = (width, height)
                            query = """SELECT * FROM  ArtPiece WHERE width = ? AND height = ? ORDER BY pieceID;"""
                            cursor.execute(query, tup)
                            data = cursor.fetchall()
                            if len(data) == 0:
                                print("None Found")
                                continue
                            for art in data:
                                for item in art:
                                    if item == '' or item == None:
                                        item = "Information Not Found"
                                print(f"Description: {art[9]}")
                                print(f"Year: {art[6]}")
                                print(f"Style: {art[7]}")
                                print(f"Medium: {art[8]}")
                                print(f"List Price: {art[10]}")
                                if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                                    cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                                    cursor.execute(cus_query, (art[13],))
                                    connection.commit()
                                    customer = cursor.fetchall()[0]
                                    print(f"Purchase Date: {art[1]}")
                                    print(f"Purchased By: {customer[0]} {customer[1]}")
                                print(f"Height and Width: {art[3]} {art[4]}")
                                print(f"Condition: {art[5]}")
                                print(f"Stored in Gallery ID: {art[11]}")

                        #   Custom dimensions.. range
                        elif selection_p_d == 'c':
                            widthMax = input("Please enter max width of art piece: ")
                            widthMin = input("Please enter min width of art piece: ")
                            heightMax = input("Please enter max height of art piece: ")
                            heightMin = input("Please enter min height of art piece: ")
                            tup = (widthMin, widthMax, heightMin, heightMax)
                            query = """SELECT * FROM ArtPiece WHERE (width BETWEEN ? AND ?) AND (height BETWEEN ? AND ?) ORDER BY pieceID;"""
                            cursor.execute(query, tup)
                            connection.commit()
                            data = cursor.fetchall()
                            if len(data) == 0:
                                print("None Found")
                                continue
                            for art in data:
                                for item in art:
                                    if item == '' or item == None:
                                        item = "Information Not Found"
                                print(f"Description: {art[9]}")
                                print(f"Year: {art[6]}")
                                print(f"Style: {art[7]}")
                                print(f"Medium: {art[8]}")
                                print(f"List Price: {art[10]}")
                                if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                                    cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                                    cursor.execute(cus_query, (art[13],))
                                    connection.commit()
                                    customer = cursor.fetchall()[0]
                                    print(f"Purchase Date: {art[1]}")
                                    print(f"Purchased By: {customer[0]} {customer[1]}")
                                print(f"Height and Width: {art[3]} {art[4]}")
                                print(f"Condition: {art[5]}")
                                print(f"Stored in Gallery ID: {art[11]}")


                        #   Return
                        elif selection_p_d == 'r':
                            continue
                
                #   Price
                elif selection_p =='p':
                    print("\nChoose an art piece between selected prices")
                    maxPrice = input("Please enter the max price of the art piece: ")
                    minPrice = input("Please enter the min price of the art piece: ")
                    tup = (minPrice, maxPrice)
                    query = """SELECT * FROM ArtPiece WHERE listPrice BETWEEN ? AND ? ORDER BY listPrice; """
                    cursor.execute(query, tup)
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")
                elif selection_p == 'f' and userType == "customer" and activeUser != None:
                    input("Press enter to see the art pieces by your favorite artists: ")
                    cursor.execute("""SELECT customerID FROM Customer WHERE username = ?;""", (activeUser,))
                    cID = cursor.fetchall()[0][0]                    
                    query = """SELECT * FROM ArtPiece JOIN (SELECT artistID FROM FavoriteArtist WHERE customerID = ?) ON artistID = artist ORDER BY artistID;"""
                    cursor.execute(query, (cID,))
                    connection.commit()
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("None Found")
                        continue
                    for art in data:
                        for item in art:
                            if item == '' or item == None:
                                item = "Information Not Found"
                        print(f"Description: {art[9]}")
                        print(f"Year: {art[6]}")
                        print(f"Style: {art[7]}")
                        print(f"Medium: {art[8]}")
                        print(f"List Price: {art[10]}")
                        if art[1] != "Information Not Found" and art[1] != '' and art[13] != "Information Not Found" and art[13] != '':
                            cus_query = """SELECT firstName, lastName FROM Customer WHERE customerID = ?;"""
                            cursor.execute(cus_query, (art[13],))
                            connection.commit()
                            customer = cursor.fetchall()[0]
                            print(f"Purchase Date: {art[1]}")
                            print(f"Purchased By: {customer[0]} {customer[1]}")
                        print(f"Height and Width: {art[3]} {art[4]}")
                        print(f"Condition: {art[5]}")
                        print(f"Stored in Gallery ID: {art[11]}")

                
                #   Return
                elif selection_p =='r':
                    return

                #   Invalid
                else:
                    print("Invalid Input")

        #   Return
        elif selection == 'r':
            return

        #   Invalid
        else:
            print("Invalid Input")
    





def view_gallery():
    global activeUser, cursor, connection
    selection = "f"
    while selection == "f" or selection == "s":
        selection = input("\nView (F)avorite gallery, (S)earch for a gallery, or press any key to return: ").lower()
        if selection == "f":
            #TODO: print info of favorite gallery
            if not loggedIn or userType != "customer":
                print("You need to be logged in as a customer to view your favorite gallery: ")
                continue
            query = """SELECT * FROM Gallery WHERE storeID = (SELECT primaryLocation FROM Customer WHERE username = ?);"""
            tup = (activeUser,)
            cursor.execute(query, tup)
            connection.commit()
            data = cursor.fetchall()
            if data[0][0] == None:
                print("No preferred location found. Please search and favorite!")
                continue
            print(f"Email: {data[0][1]}")
            print(f"Address: {data[0][2]}")
            print(f"Phone Number: {data[0][3]}")
            
        elif selection == "s":
            search_term = input("\nPlease enter part of the address to search for: ")
            shouldFavorite = False
            query = """SELECT * FROM Gallery WHERE address LIKE ?"""
            tup = ("%"+search_term+"%",)
            cursor.execute(query, tup)
            connection.commit()
            data = cursor.fetchall()
            if len(data) <= 0:
                print("No gallery found")
                continue
            print(f"\nThere are {len(data)} gallery/galleries matching your search: ")
            for store in data:
                print(f"Email: {store[1]}")
                print(f"Address: {store[2]}")
                print(f"Phone Number: {store[3]}")
                if loggedIn or userType == "customer":
                    shouldFavorite = input("\n(F)avorite store, or press any key to see the next gallery: ").lower()
                    if shouldFavorite == 'f':
                        shouldFavorite = True
                        newQuery = """UPDATE Customer SET primaryLocation = ? WHERE username = ?;"""
                        newTup = (store[0], activeUser)
                        cursor.execute(newQuery, newTup)
                        connection.commit()
                        break
    return

def main_menu():
    global activeUser, loggedIn
    selection = ""
    print("Main Page")
    while selection.lower() != "r":
        print("\nPlease make one of the following selections:")
        if loggedIn:
            while selection.lower() != "l":
                selection = input(
                "\n(Y)our Profile"
                "\n(S)earch"
                "\n(V)iew Galleries"
                "\n(L)og out: "
                )
                selection = selection.lower()
                if selection == "y":
                    user_page()
                elif selection == "s":
                    search()
                elif selection == "v":
                    view_gallery()
                elif selection == "l":
                    logout()
                    return
                else:
                    print("Invalid Input")
            return
                
        else:
            while selection.lower() != "q":
                selection = input(
                "\n(S)earch"
                "\n(V)iew Galleries"
                "\n(Q)uit to login screen: "
                )
                selection = selection.lower()
                if selection == "s":
                    search()
                elif selection == "v":
                    view_gallery()
                elif selection == "q":
                    return
                else:
                    print("Invalid Input")

def initial_screen():
    global cursor, connection
    connection = sqlite3.connect('dbdesignproj.db')
    cursor = connection.cursor()
    print("\nWelcome to the Gallery's online application!")
    selec = ""
    while selec != "q":
        selec = input("Press 'L' to login as a customer, 'A' to login as an artist, 'S' to sign up, 'Q' to quit, or press any other key to enter the application without logging in: ")
        if selec.lower() == 'l':
            login()
        elif selec.lower() == 'a':
            artist_login()
        elif selec.lower() == 's':
            signup()
        elif selec.lower() == 'q':
            return
        main_menu()
    connection.close()


if __name__ == "__main__":
    initial_screen()
