from source.db import *
import os
barrier = "+ = = = = = = = = = = ="


class Round:
    def __init__(self, server_id=-1, round_id=-1):
        self.server_id = server_id
        self.round_id = round_id

    def load_round(self):
        self.server_id = get_server_id_from_round_id(self.round_id)

    def create_new_round_in_db(self):
        self.round_id = new_round(self.server_id)

    def add_order_to_db(self, person_id, drink_id):
        save_order_to_round(person_id, drink_id, self.round_id)

    def print_current_order(self):
        os.system('clear')
        print(f"{barrier}\n| Server: {get_name_of_person_from_id(self.server_id)}\n| (person, drink)\n{barrier}")
        for row in get_all_orders_nice(self.round_id):
            print(f"| {row}")
        print(barrier)
