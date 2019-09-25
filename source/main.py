import sys
import os
from source.file import *
#from source.db import Database


# system setting
arg_list = sys.argv
os.system('clear')

# string stuff
menu_option_list = ["List of people", "List of drinks", "Show preferences", "Create Round", "Help", "Exit"]
barrier = "+ = = = = = = = = = = = ="
yes = ["Yes", "yes", "Y", "y"]


class Round:
    def __init__(self, server_id=1):  # constructor
        self.drinks = {}  # create empty dictionary
        self.server_id = server_id

    def add_drink(self, drink_id, person_id):
        if drink_id in self.drinks.keys():
            self.drinks[drink_id] += [person_id]
        else:
            self.drinks[drink_id] = [person_id]

    # prints current order
    def print_current_order(self):
        os.system('clear')
        print(f"{barrier}\n| Server: {people_dict[self.server_id]}")
        print(f"{barrier}\n| id | Drink \n{barrier}")
        for key, value in self.drinks.items():
            print(f"| {key}  | {value}")
        print(f"{barrier}\n")

    # adds a person and drink to order list
    def add_to_order(self):
        # get the id of the person to add
        item = num_check(input("Enter the id of the person you would like to add. "), len(people_dict))
        # error handling
        while item < 0:
            if item == -2:
                item = input("Please enter a number. ")
                item = num_check(item, len(people_dict))
            if item == -1:
                item = input("Please enter a number in the correct range. ")
                item = num_check(item, len(people_dict))
        person_id_confirmed = item
        # get the id of the drink to add
        item = num_check(input(f"And what drink is {people_dict[person_id_confirmed]} ordering? \nChoose the id. "))
        # error handling
        while item < 0:
            if item == -2:
                item = input("Please enter a number. ")
                item = num_check(item, len(people_dict))
            if item == -1:
                item = input("Please enter a number in the correct range. ")
                item = num_check(item, len(people_dict))
        drink_id_confirmed = item
        self.add_drink(drink_id_confirmed, person_id_confirmed)
        self.persist()

    def persist(self):
        round_file = open("documentation/round.txt", "w+")
        round_file.write(str(self.server_id))  # first line is server id
        for drink_id in self.drinks.keys():
            round_file.write("\n" + str(drink_id) + "-" + str(self.drinks[drink_id]))
        round_file.close()

    def read_file(self):
        round_file = open("documentation/round.txt", "r+")
        lines = round_file.readlines()
        if len(lines) != 0:
            self.server_id = int(lines[0])
            del lines[0]
        if len(lines) != 0:
            for line in lines:
                split_line = line.split("-")
                drink_id = int(split_line[0])
                split_line = split_line[1][1:-1]
                people_id_list = split_line.split(",")
                for index, uid in enumerate(people_id_list):
                    uid = uid.strip(" ]")
                    people_id_list[index] = int(uid)
                self.drinks[drink_id] = people_id_list


# create welcome message
def create_welcome_message():
    welcome_message = "Welcome to BrUH v0.3! \nPlease select from the following options: "

    i = 0
    while i < len(menu_option_list):
        welcome_message += f"\n    [{i + 1}] {menu_option_list[i]}"
        i += 1
    return welcome_message


# function to print table to console
def make_table(name, type_dict):
    os.system('clear')  # clear terminal
    print(f"{barrier}\n| id | {name.upper()}\n{barrier}")  # print top line
    for key, value in type_dict.items():
        print(f"| {key}  | {value}")  # print next lines
    print(f"{barrier}\n")  # print final line


def print_preferences():
    os.system('clear')  # clear terminal
    print(f"{barrier}\n| id | PREFERENCES\n{barrier}")
    if len(people_dict) > 0:
        for key in sorted(people_dict.keys()):
            if key in id_dict.keys():
                print(f"| {key}  | {people_dict[key]} - {drinks_dict[id_dict[key]]}")
            else:
                print(f"| {key}  | {people_dict[key]} - ")
    print(f"{barrier}\n")


# appends a person to the correct list
def amend_people():
    item = input("Who would you like to add? ")  # ask user for name
    add_to_file(item.title(), "documentation/people.txt")  # add name to people.txt
    print("New table: ")


# remove a person from the list
def remove_person():
    person_id_chosen = int_input("Which person would you like to remove? \nChoose the id. ", len(people_dict))# save id as new variable

    # if they have preference - remove person from preferences.txt
    if person_id_chosen in id_dict.keys():
        id_file = open("documentation/preferences.txt", "r")
        lines = id_file.readlines()
        id_file.close()
        id_file = open("documentation/preferences.txt", "w")
        for line in lines:
            if line.strip("\n")[0] != str(person_id_chosen - 1):
                id_file.write(line)
    # remove person from people.txt
    people_file = open("documentation/people.txt", "r")
    lines = people_file.readlines()
    people_file.close()
    people_file = open("documentation/people.txt", "w")
    for line in lines:
        if line.strip("\n") != str(people_dict[person_id_chosen]):
            people_file.write(line)
    people_file.close()


# remove a drink from the list
def remove_drink():
    item = num_check(input("Which drink would you like to remove? \nChoose the id. "), len(drinks_dict))
    # error handling
    while item < 0:
        if item == -2:
            item = input("Please enter a number. ")
            item = num_check(item, len(drinks_dict))
        if item == -1:
            item = input("Please enter a number in the correct range. ")
            item = num_check(item, len(drinks_dict))
    drink_id_chosen = item  # save id as new variable
    # remove any preferences associated with drink
    id_file = open("documentation/preferences.txt", "r")
    lines = id_file.readlines()
    id_file.close()
    id_file = open("documentation/preferences.txt", "w")
    for line in lines:
        # FIX THIS BIT PLSPLSPLS
        if line.strip(",")[1] != str(drink_id_chosen):
            id_file.write(line)
    # remove person from drinks.txt
    drinks_file = open("documentation/drinks.txt", "r")
    lines = drinks_file.readlines()
    drinks_file.close()
    drinks_file = open("documentation/drinks.txt", "w")
    for line in lines:
        if line.strip("\n") != str(drinks_dict[drink_id_chosen]):
            drinks_file.write(line)
    drinks_file.close()


# adds an item to a file
def add_to_file(item, file_name):
    people_file = open(file_name, "a+")
    people_file.write(item + "\n")
    people_file.close()


# append a drink to the list
def amend_drinks():
    item = input("Which drink would you like to add? ")  # ask user for name
    add_to_file(item.title(), "documentation/drinks.txt")  # add name to people.txt
    print("New table: ")


# function that checks numeric user input for legality
def num_check(test_int, int_max):
    if not test_int.isdigit():  # test if string input is a digit
        return -2  # error code for non-digit string
    # error handling
    try:
        new_int = int(test_int)  # try type cast to int
    except ValueError as ve:
        print("Weird data type. " + str(ve))
        exit()
    if new_int > int_max:  # test if int input is within the correct range
        return -1  # error code for out of bound int
    return new_int


def int_input(message, limit=len(menu_option_list)):
    while True:
        item = num_check(input(message), limit)
        if item == -2:
            continue
        if item == -1:
            print("That is not a valid option.")
            continue

        return item


# function that prompts user to amend the preferences
def pref_amend():
    new_preference = True
    person_id_chosen = int_input("Whose preference would you like to amend? \nChoose the id. ", len(people_dict)) # save id as new variable
    if person_id_chosen in id_dict.keys():  # check if person_id_chosen already has a preference or not
        new_preference = False

    make_table("drinks", drinks_dict)  # now print drinks table

    # error handling
    drinks_id_chosen = int_input(f"What is {people_dict[person_id_chosen]}'s preference? \nChoose the id. ",
                     len(drinks_dict))


    #BUG FIX!!! REMOVED a "-1" TO CURE PREFERENCES ISSUE
    if new_preference:
        people_file = open("documentation/preferences.txt", "a")  # open the file for appending
        people_file.write(str(person_id_chosen) + "," + str(drinks_id_chosen) + "\n")  # add the string
        people_file.close()
    else:
        people_file = open("documentation/preferences.txt", "r")
        lines = people_file.readlines()
        people_file.close()
        people_file = open("documentation/preferences.txt", "w")
        for line in lines:
            if line[0] == str(person_id_chosen):
                line = str(person_id_chosen) + "," + str(drinks_id_chosen) + "\n"
            people_file.write(line)
        people_file.close()


# function that prompts user for amending the lists
def choose(selection):
    choice = input(f"Would you like to add to {selection}? \nType yes or no. ")
    return choice


# function that prints out main user menu
def main_menu():
    os.system('clear')
    print(create_welcome_message())  # print the welcome message
    num = int_input("Please enter a number. ")
    return num


# 'help' function
def help_menu():
    print("lmao")


# function that lets user know to press a button to return to menu
def return_to_menu():
    input("Press enter to return to menu. ")


# INITIALISE LISTS & DICTS
file = File()


def get_people():
    people_list = file.get_people()  # split string into string list using lines
    people_dictionary = {}  # create empty dictionary
    for i in range(0, len(people_list)):  # loop through string list
        if len(people_list[i]) > 0:  # non-empty line
            people_dictionary[i] = people_list[i]  # save elements of list into dictionary
        else:
            i -= 1

    return people_dictionary


def get_drinks():
    drinks_list = file.get_drinks()  # split string into string list using lines
    drinks_dictionary = {}  # create empty dictionary
    for i in range(0, len(drinks_list)):  # loop through string list
        if len(drinks_list[i]) > 0:  # dodge non-empty lines
            drinks_dictionary[i] = drinks_list[i]  # save elements of list into dictionary
        else:
            i -= 1

    return drinks_dictionary


def get_id():
    id_list = file.get_favourites()  # split string into string list using splitlines
    id_dictionary = {}  # create empty dictionary
    for elm in id_list:  # loop through string list
        split_elm = elm.split(",")  # split elements of string list with ","
        id_dictionary[int(split_elm[0])] = int(split_elm[1])  # save split elements in dictionary

    return id_dictionary


# MAIN BODY OF PROGRAM
# execute main loop
while True:
    # load all dicts
    people_dict = get_people()
    drinks_dict = get_drinks()
    id_dict = get_id()
    num_selection = main_menu()  # print main menu screen and get user selection
    if num_selection == 1:  # list of people
        while True:  # run until user decides against it
            people_dict = get_people()  # get the people dictionary
            make_table("people", people_dict)  # show table to user
            choice = choose("people")  # ask if user wants to amend the list
            if choice in yes:
                amend_people()  # amend people on file
            elif choice == "rm":  # cheeky remove person
                remove_person()
            else:
                break
        return_to_menu()
    elif num_selection == 2:  # list of drinks
        while True:  # run until user stops
            drinks_dict = get_drinks()  # get the drinks dictionary
            make_table("drinks", drinks_dict)  # show table to user
            choice = choose("drinks")  # ask user if they want to amend
            if choice in yes:
                amend_drinks()  # add to file
            elif choice == "rm":
                remove_drink()
            else:
                break
        return_to_menu()
    elif num_selection == 3:  # update preferences
        while True:  # run until user stops
            id_dict = get_id()  # update pref dictionary
            print_preferences()  # print preferences
            choice = choose("preferences")  # ask user if they want to amend
            if choice in yes:
                pref_amend()  # add to file
            else:
                break
        return_to_menu()
    elif num_selection == 4:  # orders
        while True:
            order = Round()
            order.read_file()
            order.print_current_order()
            choice = choose("orders")
            if choice in yes:
                order.add_to_order()
            else:
                break
        return_to_menu()
    elif num_selection == 5:  # help menu
        help_menu()
        return_to_menu()
    elif num_selection == 6:  # exit
        exit()
    else:
        print("You shouldn't really see this tbh. ")
