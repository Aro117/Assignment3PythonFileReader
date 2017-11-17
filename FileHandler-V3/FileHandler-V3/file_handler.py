from __future__ import print_function
import sys
import csv
import re
import openpyxl
from validator import Validator
from abc import ABCMeta, abstractmethod

class IDataReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass

class CSVDataReader(IDataReader):
    def __init__(self,file_path,validator):
        self.fpath = file_path
        self.validator = validator

    def read(self):
        try:
            with open(self.fpath) as f_obj:
                reader = csv.DictReader(f_obj, delimiter=',')
                the_list = []
                for line in reader:
                    employee = dict()
                    employee["EMPID"] = line["emp_id"]
                    employee["GENDER"] = line["gender"]
                    employee["AGE"] = line["age"]
                    employee["SALES"] = line["sales"]
                    employee["BMI"] = line["bmi"]
                    employee["SALARY"] = line["salary"]
                    employee["BIRTHDAY"] = line["birthday"]

                    if self.validator.check_line(employee):
                        the_list.append(employee)
                    else:
                        print('Entry failed validation', file=sys.stderr)
                if self.validator.check_data_set(the_list):
                    return the_list
                else:
                    print("There were no valid entries in the file", file=sys.stderr)
                    return False
        except FileNotFoundError:
            print('The file was not found', file=sys.stderr)
            return False


class TxtDictReader(IDataReader):
    def __init__(self,file_path,validator):
        self.fpath = file_path
        self.validator = validator

    def read(self):
        try:
            file = open(self.fpath, "r")
        except FileNotFoundError:
            print('The file was not found', file=sys.stderr)
            return False
        the_list = []
        for line in file:
            dictionary = {}
            entries = line.split(";")
            for entry in entries:
                if len(entry.split("=")) == 2:
                    key = entry.split("=")[0]
                    value = entry.split("=")[1]
                    value = value.rstrip('\n')
                    dictionary[key] = value
                else:
                    print('The file was in an invalid format', file=sys.stderr)
                    return False
            if self.validator.check_line(dictionary):
                the_list.append(dictionary)
            else:
                print('Entry failed validation', file=sys.stderr)
        if self.validator.check_data_set(the_list):
            return the_list
        else:
            print("There were no valid entries in the file", file=sys.stderr)
            return False

class ExcelReader(IDataReader):
    def __init__(self,file_path,validator):
        self.fpath = file_path
        self.validator = validator

    def read(self):
        try:
            wb = openpyxl.load_workbook(self.fpath)
            sheet = wb.active
            the_list = []
            for x in range(2, 29):
                employee = dict()
                employee["EMPID"] = sheet.cell(column=1, row=x).value
                employee["GENDER"] = sheet.cell(column=2, row=x).value
                employee["AGE"] = sheet.cell(column=3, row=x).value
                employee["SALES"] = sheet.cell(column=4, row=x).value
                employee["BMI"] = sheet.cell(column=5, row=x).value
                employee["SALARY"] = sheet.cell(column=6, row=x).value
                employee["BIRTHDAY"] = sheet.cell(column=7, row=x).value
                if self.validator.check_line(employee):
                    the_list.append(employee)
                else:
                    print('Entry failed validation', file=sys.stderr)
            if self.validator.check_data_set(the_list):
                return the_list
            else:
                print("There were no valid entries in the file", file=sys.stderr)
                return False
        except FileNotFoundError:
            print("File not found!", file=sys.stderr)
            return False


class FileHandler:
    def __init__(self, new_validator):
        self.validator = new_validator

    def open(self, file_path):
        if re.search(r'\.csv$', file_path):
            return CSVDataReader(file_path,self.validator).read()
        elif re.search(r'\.txt$', file_path):
            return TxtDictReader(file_path,self.validator).read()
        elif re.search(r'\.xlsx$', file_path):
            result = ExcelReader(file_path,self.validator).read()
            if result and self.validator.check_data_set(result):
                return result
            else:
                print("There were no valid entries in the file", file=sys.stderr)
                return False
        else:
            print('Invalid file extension', file=sys.stderr)
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

    # Tim
    def set_rules(self):
        self.validator.set_rules(self.open_rules())

    # Rosemary
    @staticmethod
    def open_help(help_command):
        """
        >>> f = FileHandler(new_validator=Validator)
        >>> print(f.open_help('line'))
        line command vitualize the data.
        >>> print(f.open_help('help'))
        help command brings out all command.
        >>> print(f.open_help('helpp'))
        No such command.
        """
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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
