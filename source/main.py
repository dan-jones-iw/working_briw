import sys
import os
from prettytable import PrettyTable
from source.file import *
from source.db import *
from source.round import *


# system setting
arg_list = sys.argv
os.system('clear')

# string stuff
menu_option_list = ["List of people", "List of drinks", "Show preferences", "Create Round", "Help", "Exit", "DB Clean"]
barrier = "+ = = = = = = = = = = = ="
yes = ["Yes", "yes", "Y", "y"]


# create welcome message
def create_welcome_message():
    welcome_message = "Welcome to BrUH v0.3! \nPlease select from the following options: "

    if check_if_round_exists():
        menu_option_list[3] = "View Round"
    else:
        menu_option_list[3] = "Create Round"

    i = 0
    while i < len(menu_option_list):
        welcome_message += f"\n    [{i + 1}] {menu_option_list[i]}"
        i += 1
    return welcome_message


# appends a person to the correct list
def amend_people():
    name = input("Who would you like to add? ")  # ask user for name
    save_person(name)


# append a drink to the list
def amend_drinks():
    name = input("Which drink would you like to add? ")  # ask user for name
    save_drink(name)


# TODO THIS DOESNT WORK LOL
# remove a person from the list
def remove_person():
    person_id_chosen = int_input("Which person would you like to remove? \nChoose the id. ", len(people_dict))

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


# TODO OR THIS
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
    print_people_nice()
    person_id_chosen = int_input("Whose preference would you like to amend? \nChoose the id. ", 100000) # save id as new variable

    # CHECK IF IN DB
    # if person_id_chosen in id_dict.keys():  # check if person_id_chosen already has a preference or not
    #     new_preference = False

    print_drink_nice()

    # error handling
    name_of_person_chosen = get_name_of_person_from_id(person_id_chosen)
    drinks_id_chosen = int_input(f"What is {name_of_person_chosen}'s preference? \nChoose the id. ",
                                 1000000)

    update_drink_preference_of_person(person_id_chosen, drinks_id_chosen)


# function that prompts user for amending the lists
def choose(item):
    selection = input(f"Would you like to add to {item}? \nType yes or no. ")
    return selection


def check_if_round_exists():
    # an empty table returns an empty tuple from get_round
    data_from_round = get_round()
    empty_tuple = ()
    if data_from_round == empty_tuple:
        return False
    else:
        return True


# menus
def main_menu():
    os.system('clear')
    print(create_welcome_message())  # print the welcome message
    num = int_input("Please enter a number. ")
    return num


def help_menu():
    print("lmao")


def return_to_menu():
    input("Press enter to return to menu. ")


def create_new_round():
    print_people_nice()
    server_id_chosen = int_input("Which person is serving this round? \nChoose the id.", get_number_of("person"))
    return server_id_chosen


# all the table printing
def print_people_nice():
    os.system('clear')
    pref_table = PrettyTable()
    pref_table.field_names = ["id", "name"]
    for row in get_all_people_nice():
        pref_table.add_row([row[0], row[1]])
    print(pref_table)


def print_drink_nice():
    os.system('clear')
    print(f"{barrier}\n|(id, drink)\n{barrier}")
    for row in get_all_drink_nice():
        print(f"| {row}")
    print(barrier)


def print_preferences():
    os.system('clear')
    pref_table = PrettyTable()
    pref_table.field_names = ["name", "drink"]
    for row in get_all_favourites():
        pref_table.add_row([row[1], row[2]])
    print(pref_table)


def choose_who_to_add_to_order():
    print_people_nice()
    question = "Which person would you like to add to the order? \nSelect the id from the list above: "
    id_of_person_chosen = input(question)

    print_drink_nice()
    question = f"And what would {get_name_of_person_from_id(id_of_person_chosen)} like to drink? "
    id_of_drink_chosen = input(question)

    return [id_of_person_chosen, id_of_drink_chosen]


# MAIN BODY OF PROGRAM
# execute main loop
while True:
    num_selection = main_menu()  # print main menu screen and get user selection
    if num_selection == 1:  # list of people
        while True:  # run until user decides against it
            print_people_nice()
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
            print_drink_nice()
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
            print_preferences()  # print preferences
            choice = choose("preferences")  # ask user if they want to amend
            if choice in yes:
                pref_amend()  # add to file
            else:
                break
        return_to_menu()
    elif num_selection == 4:  # orders
        if not check_if_round_exists():
            server_id = create_new_round()
            current_round = Round(server_id=server_id)
            current_round.create_new_round_in_db()
        else:
            round_id = get_max_round_id()
            current_round = Round(round_id=round_id)
            current_round.load_round()
        while True:
            current_round.print_current_order()
            choice = choose("orders")
            if choice in yes:
                order_to_add = choose_who_to_add_to_order()
                current_round.add_order_to_db(order_to_add[0], order_to_add[1])
            else:
                break
        return_to_menu()
    elif num_selection == 5:  # help menu
        help_menu()
        return_to_menu()
    elif num_selection == 6:  # exit
        exit()
    elif num_selection == 7:  # exit
        db_clean()
        exit()
    else:
        print("You shouldn't really see this tbh. ")
