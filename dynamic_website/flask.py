from flask import Flask, redirect, request, render_template
from source.db import *

app = Flask(__name__)

global_round_id = 0


@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "GET":
        return render_template("main_page.html", title="Main")


@app.route("/person", methods=["GET"])
def person_main():
    json_list_of_people = get_all_people()
    return render_template("person_master.html", title="People", data=json_list_of_people)


@app.route("/person-add", methods=["GET", "POST"])
def person_add():
    if request.method == "GET":
        return render_template("form_input_person.html", title="CreateForm")

    elif request.method == "POST":
        person_name = request.form.get("person-name")
        age = request.form.get("age")

        save_person(person_name, age)

        return render_template("form_output_person.html", title="FormDone", person=person_name, age=age)


@app.route("/round", methods=["GET", "POST"])
def round_main():
    global global_round_id
    if request.method == "GET":
        list_of_rounds = get_all_rounds_nice()
        empty_tuple = ()
        return render_template("round_view.html", round_list=list_of_rounds, empty_tuple=empty_tuple)

    elif request.method == "POST":
        global_round_id = request.form.get("round-id")
        return redirect("order")


@app.route("/round/create", methods=["GET", "POST"])
def round_create():
    if request.method == "GET":
        json_list_of_people = get_all_people_nice()
        return render_template("round_create.html", data=json_list_of_people)

    elif request.method == "POST":
        server_name = request.form.get("person-name")
        server_id = get_id_of_person_from_name(server_name)

        new_round(server_id)

        return render_template("round_created.html", server=server_name)


@app.route("/round/add", methods=["GET", "POST"])
def round_add():
    if request.method == "GET":
        return render_template("round_view.html")


@app.route("/order", methods=["GET", "POST"])
def order_main():
    if request.method == "GET":
        if global_round_id == 0:
            return render_template("order_oops.html")
        else:
            round_data = get_all_orders_nice(global_round_id)
            empty_tuple = ()
            server_name = get_name_of_person_from_id(get_server_id_from_round_id(global_round_id))
            return render_template("order_view.html", round_id=global_round_id, round_data=round_data, et=empty_tuple, server_name=server_name)

    elif request.method == "POST":
        round_id_chosen = request.form.get("round-id")
        round_data = get_all_orders_nice(round_id_chosen)
        empty_tuple = ()
        return render_template("order_view.html", round_id=round_id_chosen, round_data=round_data, empty_tuple=empty_tuple)


@app.route("/order/create", methods=["GET", "POST"])
def order_create():
    if request.method == "GET":
        list_of_favourites = get_all_favourites()
        return render_template("order_create.html", favourite_data=list_of_favourites)

    elif request.method == "POST":
        # initialise useful variables
        drink_name = ""
        no_drink = False

        person_name = request.form.get("person-name")
        person_id = get_id_of_person_from_name(person_name)
        person = get_person(person_id)
        drink_id = person[3]
        if drink_id:
            drink_name = get_drink(drink_id)[1]
            save_order_to_round(person_id, drink_id, global_round_id)
        else:
            no_drink = True

        return render_template("order_created.html", person=person_name, drink=drink_name, no_drink=no_drink)


@app.route("/order/complete", methods=["GET"])
def order_complete():
    if request.method == "GET":
        round_data = get_all_orders_nice(global_round_id)  # round_data comes as a list of tuples

        drink_dict = {}
        for order in round_data:
            drink_id = order[1]
            person_id = order[0]
            if drink_id not in drink_dict.keys():
                drink_dict[drink_id] = [person_id]
            else:
                drink_dict[drink_id].append(person_id)

        return render_template("order_complete.html", round_id=global_round_id, dict=drink_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
