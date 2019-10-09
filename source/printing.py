import os
from prettytable import PrettyTable
from source.db import *

barrier = "+ = = = = = = = = = = = ="


# all the table printing
def print_people_nice():
    os.system('clear')
    pref_table = PrettyTable()
    pref_table.field_names = ["id", "Name"]
    for row in get_all_people_nice():
        pref_table.add_row([row[0], row[1]])
    print(pref_table)


def print_drink_nice():
    os.system('clear')
    pref_table = PrettyTable()
    pref_table.field_names = ["id", "Name"]
    for row in get_all_drink_nice():
        pref_table.add_row([row[0], row[1]])
    print(pref_table)


def print_preferences():
    os.system('clear')
    pref_table = PrettyTable()
    pref_table.field_names = ["Name", "Drink"]
    for row in get_all_favourites():
        pref_table.add_row([row[1], row[2]])
    print(pref_table)


def print_round(round_id, server_id):
    os.system('clear')
    pref_table = PrettyTable()
    pref_table.title = f"Server: {get_name_of_person_from_id(server_id)}"
    pref_table.field_names = ["Person", "Drink"]
    for row in get_all_orders_nice(round_id):
        pref_table.add_row([row[0], row[1]])
    print(pref_table)


def no_people_to_start_round():
    message = "There aren't any people to host your round. \nPlease add people to the list before creating a round."
    print(message)

