from __future__ import print_function
import sys
from abc import ABCMeta, abstractmethod
import re
import datetime as date


class IFileValidator(metaclass=ABCMeta):
    @abstractmethod
    def check_data_set(self, data_set):
        pass

    @abstractmethod
    def check_line(self, employee_attributes):
        pass

    @abstractmethod
    def check_all(self, employee_attributes):
        pass

    @abstractmethod
    def check_id(self, emp_id):
        pass

    @abstractmethod
    def check_age(self, age):
        pass

    @abstractmethod
    def check_sales(self, sales):
        pass

    @abstractmethod
    def check_bmi(self, bmi):
        pass

    @abstractmethod
    def check_salary(self, salary):
        pass

    @abstractmethod
    def check_birthday(self, birthday):
        pass

    @abstractmethod
    def check_gender(self, gender):
        pass

    @abstractmethod
    def check_birthday_against_age(self, birthday, age):
        pass


class Validator(IFileValidator):

    def __init__(self):
        self.id_rule = "^[A-Z][0-9]{3}$"
        self.gender_rule = "^(M|F)$"
        self.age_rule = "^[0-9]{2}$"
        self.sales_rule = "^[0-9]{3}$"
        self.bmi_rule = "^(Normal|Overweight|Obesity|Underweight)$"
        self.salary_rule = "^[0-9]{2,3}$"
        self.birthday_rule = "^[1-31]-[1-12]-[0-9]{4}$"
        self.attributes = {"EMPID", "GENDER", "AGE", "SALES", "BMI", "SALARY", "BIRTHDAY"}
        self.number_of_attributes = len(self.attributes)

    def set_rules(self, rules):
        try:
            self.id_rule = rules['id']
            self.gender_rule = rules['gender']
            self.age_rule = rules['age']
            self.sales_rule = rules['sales']
            self.bmi_rule = rules['bmi']
            self.salary_rule = rules['salary']
        except KeyError as missing_key:
            print('The key {} was missing from the rules.txt file'.format(missing_key), file=sys.stderr)

    def check_data_set(self, data_set):
        # Should be of form [{EMPID: B12, GENDER: M, AGE: 22, etc}, {EMPID: 55Y, GENDER: F, etc}]
        if len(data_set) == 0:
            print('The data was empty', file=sys.stderr)
            return False
        else:
            for employee in data_set:
                if not self.check_line(employee):
                    print('One or more of the lines of data was invalid', file=sys.stderr)
                    return False
        # Failing to invalidate is a success
        return True

    def check_line(self, employee_attributes):
        # Should be of form {EMPID: B12, GENDER: M, AGE: 22, etc}
        for attribute in self.attributes:
            if attribute not in employee_attributes:
                print('Missing attribute: {}'.format(attribute), file=sys.stderr)
                return False
        try:
            if not self.check_all(employee_attributes):
                return False
        except TypeError:
            print('The data was not bundled correctly', file=sys.stderr)
            return False
        # Failing to invalidate is a success
        return True

    def check_all(self, employee_attributes):
        result = self.check_birthday(employee_attributes["BIRTHDAY"]) \
                 and self.check_id(employee_attributes["EMPID"])  \
                 and self.check_age(employee_attributes["AGE"]) \
                 and self.check_gender(employee_attributes["GENDER"]) \
                 and self.check_sales(employee_attributes["SALES"]) \
                 and self.check_bmi(employee_attributes["BMI"]) \
                 and self.check_salary(employee_attributes["SALARY"]) \
                 and self.check_birthday_against_age(employee_attributes["BIRTHDAY"], employee_attributes["AGE"])
        return result

    # rule_name like "salary_rule",attr_name like "Salary"
    def check_attr_match(self, rule_name, attr_name, attr_val):
        try:
            if not re.match(self.__getattribute__(rule_name), str(attr_val)):
                print('{} is invalid '.format(attr_val) + attr_name + ' !', file=sys.stderr)
                return False
        except TypeError:
            return False
        return True

    def check_id(self, emp_id):
        # Should be in form of [A-Z][0-9]{3}
        return self.check_attr_match("id_rule", "id", emp_id)

    def check_age(self, age):
        # Should be between 1-99
        return self.check_attr_match("age_rule", "age", age)

    def check_gender(self, gender):
        return self.check_attr_match("gender_rule", "gender", gender)

    def check_sales(self, sales):
        return self.check_attr_match("sales_rule", "sales", sales)

    def check_bmi(self, bmi):
        return self.check_attr_match("bmi_rule", "BMI", bmi)

    def check_salary(self, salary):
        return self.check_attr_match("salary_rule", "Salary", salary)

    def check_birthday(self, birthday):
        try:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            date.datetime(year, month, day)
            return True
        except ValueError:
            print('The date was invalid', file=sys.stderr)
            return False
        except AttributeError:
            print('The date was in an invalid format', file=sys.stderr)
            return False

    def check_birthday_against_age(self, birthday, age):
        if not self.check_birthday(birthday):
            return False
        else:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            # adding age because we just want to compare month and day
            birth = date.datetime(year, month, day)
            today = date.datetime.today()
            if birth.month < today.month:
                # Had a birthday already this year
                return int(age) == today.year - year
            elif birth.month == today.month and birth.day < today.day:
                # Had a birthday already this year (this month)
                return int(age) == today.year - year
            else:
                # Hasn't had a birthday yet this year.
                return int(age) == today.year - year - 1

    def check_in_attributes(self, query_attribute):
        try:
            return query_attribute.upper() in self.attributes
        except AttributeError:
            return False


class ValidatorBuilder:
    def __init__(self):
        self.rules = {}
        self.rules['id'] = "^[A-Z][0-9]{3}$"
        self.rules['gender'] = "^(M|F)$"
        self.rules['age'] = "^[0-9]{2}$"
        self.rules['sales'] = "^[0-9]{3}$"
        self.rules['bmi'] = "^(Normal|Overweight|Obesity|Underweight)$"
        self.rules['salary'] = "^[0-9]{2,3}$"

    def id(self, id):
        self.rules['id'] = id
        return self

    def gender(self, gen):
        self.rules['gender'] = gen
        return self

    def age(self, age):
        self.rules['age'] = age
        return self

    def sales(self, sales):
        self.rules['sales'] = sales
        return self

    def bmi(self, bmi):
        self.rules['bmi'] = bmi
        return self

    def salary(self, salary):
        self.rules['salary'] = salary
        return self

    def build(self):
        val = Validator()
        val.set_rules(self.rules)
        return val

# if we need to change the rules in the future, build a new validator and reset some rules

# builder = ValidatorBuilder()
# builder.salary("^[0-9]{2,3}$")
# my_validator = builder.build()




