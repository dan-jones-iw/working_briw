import os
from source.db import *
from source.printing import *
barrier = "+ = = = = = = = = = = ="


def check_if_round_exists():
    # an empty table returns an empty tuple from get_round
    data_from_round = get_all_rounds()
    empty_tuple = ()
    if data_from_round == empty_tuple:
        return False
    else:
        return True


def get_server_id_for_new_round():
    print_people_nice()
    server_id_chosen = input("Which person is serving this round? \nChoose the id. ")
    return server_id_chosen


class Round:
    def __init__(self, server_id=-1, round_id=-1):
        self.server_id = server_id
        self.round_id = round_id

    def set_server_id(self, server_id):
        self.server_id = server_id

    def set_round_id(self, round_id):
        self.round_id = round_id

    def initialise_round(self):
        if not check_if_round_exists():
            # no round exists
            if get_number_of("person"):
                server_id = get_server_id_for_new_round()
                self.set_server_id(server_id)
                self.create_new_round_in_db()
                return True
            else:
                self.delete_round()
                return False
        else:
            # round exists
            round_id = get_max_round_id()
            self.set_round_id(round_id)
            self.load_round()
            return True

    def load_round(self):
        self.server_id = get_server_id_from_round_id(self.round_id)

    def create_new_round_in_db(self):
        self.round_id = new_round(self.server_id)

    def add_order_to_db(self, person_id, drink_id):
        save_order_to_round(person_id, drink_id, self.round_id)

    def update_order_in_db(self, person_id, drink_id):
        update_order_in_round(person_id, drink_id, self.round_id)

    def print_current_order(self):
        print_round(self.round_id, self.server_id)

    def delete_round(self):
        self.server_id = -1
        self.round_id = -1
