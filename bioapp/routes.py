from flask import Blueprint
from services import DeathService as ds

main = Blueprint("controller", __name__)

@main.route("/")
def hello_word():
    return "hello_word"

@main.route("/get_list_of_death_types", methods=['GET'])
def get_death_types():

    return "hello_word"


@main.route("/get_death_for_death_type_id", methods=['GET'])
def get_deaths(id_death_type: int):

    return "hello_word"


@main.route("/add_death_type")
def add_death_type(death_type: dict):
    return "hello_word"


@main.route("/remove_death_type")
def remove_death_type(death_type_id: int):
    return "hello_word"


@main.route("/add_death")
def add_death(death: dict):
    return "hello_word"


@main.route("/update_death")
def update_death(death: dict):
    return "hello_word"


@main.route("/remove_death")
def remove_death(death: dict):
    return "hello_word"


