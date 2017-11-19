import unittest
from file_handler import FileHandler
from validator import Validator

class FilehandlerTests(unittest.TestCase):

    def test_csv(self):
        fh = FileHandler(Validator())
        actual = fh.open('testfiles/csvTest.csv')[0]
        expected = {'EMPID': 'A001',
                    'GENDER': 'F',
                    'AGE': '21',
                    'SALES': '001',
                    'BMI': 'Normal',
                    'SALARY': '12',
                    'BIRTHDAY': '1-1-1996'}
        self.assertEquals(actual, expected)

    def test_txt(self):
        fh = FileHandler(Validator())
        actual = fh.open('testfiles/txtTest.txt')[0]
        expected = {'EMPID': 'A001',
                    'GENDER': 'F',
                    'AGE': '21',
                    'SALES': '001',
                    'BMI': 'Normal',
                    'SALARY': '12',
                    'BIRTHDAY': '1-1-1996'}
        self.assertEquals(actual, expected)

    def test_xlsx(self):
        fh = FileHandler(Validator())
        actual = fh.open('testfiles/testingdata.xlsx')[0]

        expected = {'EMPID': 'A001',
                    'GENDER': 'F',
                    'AGE': '21',
                    'SALES': '001',
                    'BMI': 'Normal',
                    'SALARY': '12',
                    'BIRTHDAY': '1-1-1996'}
        self.assertEquals(actual, expected)

suite = unittest.TestLoader().loadTestsFromTestCase(FilehandlerTests)
unittest.TextTestRunner(verbosity=1).run(suite)