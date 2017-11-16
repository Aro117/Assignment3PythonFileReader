from __future__ import print_function
import sys
from file_reader import CSVReader, TXTReader, XLSXReader


class FileHandler:
    def __init__(self, new_validator):
        self.validator = new_validator
        self.file_type = {'csv': CSVReader(self.validator),
                           'txt': TXTReader(self.validator),
                           'xlsx': XLSXReader(self.validator)
        }

    def open(self, file_path):
        extension = file_path.split(".")[-1]
        if extension in self.file_type.keys():
            return self.file_type[extension].read_file(file_path)
        else:
            print('Invalid file extension', file=sys.stderr)
            print(extension)
            return False

    # Tim
    @staticmethod
    def open_rules():
        try:
            file = open('rules.txt', "r")
        except FileNotFoundError:
            print('Cannot find rules.txt', file=sys.stderr)
            return False
        rules = {}
        for line in file:
            if len(line.split("=")) == 2:
                key = line.split("=")[0]
                value = line.split("=")[1]
                value = value.rstrip('\n')
                rules[key] = value
            else:
                print('The file was in an invalid format', file=sys.stderr)
                return False
        return rules
        

    def set_rules(self):
        self.validator.set_rules(self.open_rules())

    # Rosemary
    @staticmethod
    def open_help(help_command):

        try:
            file = open("help.txt", "r")
            for line in file:
                if len(line.split("=")) == 2:
                    entries = line.split("=")
                    if help_command == entries[0]:
                        return entries[1].rstrip('\n')
                else:
                    print("Invalid help file format!")
        except FileNotFoundError:
            print('The help file was not found', file=sys.stderr)
        return "No such command."

