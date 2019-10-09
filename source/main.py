import sys
import os
import source.db as db
from source.printing import print_people_nice, print_drink_nice, print_preferences
from source.round import *


# system setting
arg_list = sys.argv
os.system('clear')

# string stuff
menu_option_list = ["List of people", "List of drinks", "Show preferences", "Create Round", "Help", "Exit", "DB Clean"]
yes = ["Yes", "yes", "Y", "y", "ye", "yeh boi", "yes please", "yeah boi"]


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
    db.save_person(name)


# append a drink to the list
def amend_drinks():
    name = input("Which drink would you like to add? ")  # ask user for name
    db.save_drink(name)


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
    if not test_int.lstrip("-").isdigit():  # test if string input is a digit
        return -2  # error code for non-digit string
    try:
        new_int = int(test_int)  # try type cast to int
    except ValueError as ve:
        print("Weird data type. " + str(ve))
        exit()
    if new_int > int_max or new_int < 0:  # test if int input is within the correct range
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
    print_people_nice()
    person_id_chosen = int_input("Whose preference would you like to amend? \nChoose the id. ",
                                 db.get_number_of("person"))

    name_of_person_chosen = db.get_name_of_person_from_id(person_id_chosen)
    print_drink_nice()
    drinks_id_chosen = int_input(f"What is {name_of_person_chosen}'s preference? \nChoose the id. ",
                                 db.get_number_of("drink"))

    db.update_drink_preference_of_person(person_id_chosen, drinks_id_chosen)


def not_enough_drinks_for_favourite():
    print("Cannot add favourites as there aren't any drinks present in database. ")
    print("Add drinks before editing preferences.")


# function that prompts user for amending the lists
def choose(item):
    selection = input(f"Would you like to add to {item}? \nType yes or no. ")
    return selection


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


def choose_who_to_add_to_order(round_id):
    print_people_nice()
    question = "Which person would you like to add to the order? \nSelect the id from the list above: "
    id_of_person_chosen = int_input(question, db.get_number_of("person"))

    in_round = db.check_if_person_in_round(round_id, id_of_person_chosen)

    print_drink_nice()
    question = f"And what would {db.get_name_of_person_from_id(id_of_person_chosen)} like to drink? "
    id_of_drink_chosen = int_input(question, db.get_number_of("drink"))

    return [id_of_person_chosen, id_of_drink_chosen, in_round]


# MAIN BODY OF PROGRAM
# execute main loop
if __name__ == '__main__':
    while True:
        num_selection = main_menu()  # print main menu screen and get user selection
        if num_selection == 1:  # list of people
            while True:
                print_people_nice()
                choice = choose("people")  # ask if user wants to amend
                if choice in yes:
                    amend_people()
                elif choice == "rm":  # cheeky remove person
                    remove_person()
                else:
                    break
            return_to_menu()
        elif num_selection == 2:  # list of drinks
            while True:
                print_drink_nice()
                choice = choose("drinks")  # ask user if they want to amend
                if choice in yes:
                    amend_drinks()
                elif choice == "rm":
                    remove_drink()
                else:
                    break
            return_to_menu()
        elif num_selection == 3:  # update favourites
            while True:
                print_preferences()
                if db.get_all_drinks() != ():
                    choice = choose("preferences")  # ask user if they want to amend
                    if choice in yes:
                        pref_amend()
                    else:
                        break
                else:
                    not_enough_drinks_for_favourite()
                    break
            return_to_menu()
        elif num_selection == 4:  # orders
            round_initialised = True
            current_round = Round()
            if not current_round.initialise_round():
                round_initialised = False
                print("No people in database to start a round. \nPlease add a person before trying to create a round.")
            while round_initialised:
                current_round.print_current_order()
                choice = choose("orders")
                if choice in yes:
                    order_to_add = choose_who_to_add_to_order(current_round.round_id)
                    if order_to_add[2]:
                        current_round.add_order_to_db(order_to_add[0], order_to_add[1])
                    else:
                        current_round.update_order_in_db(order_to_add[0], order_to_add[1])
                else:
                    break
            return_to_menu()
        elif num_selection == 5:  # help menu
            help_menu()
            return_to_menu()
        elif num_selection == 6:  # exit
            exit()
        elif num_selection == 7:  # exit
            db.db_clean()
            exit()
        else:
            print("You shouldn't really see this tbh. ")
