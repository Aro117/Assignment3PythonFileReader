from command import Command
from file_handler import FileHandler
from validator import Validator, ValidatorBuilder
from view import View
from db import DatabaseHandler
import pickle
import sys

try:
    database_name = sys.argv[1]
except IndexError:
    database_name = "db"
try:
    database = pickle.load(open(database_name + ".p", "rb"))
except FileNotFoundError:
    database = DatabaseHandler(ValidatorBuilder().build(), database_name)
    database.load()
    pickle.dump(database, open(database_name+".p", "wb"))
cli = Command(FileHandler(ValidatorBuilder().build()), database, View())
cli.cmdloop()

