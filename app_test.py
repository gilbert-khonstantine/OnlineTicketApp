import urllib
from flask import Flask
from flask_testing import LiveServerTestCase,TestCase
import unittest
from urllib.request import urlopen
import mechanicalsoup
import time

#BLACKBOX TEST FOR REGISTRATION PROCESS

## EMAIL
#VALID EMAIL: UNUSED
#INVALID EMAIL: USED, without @ sign

## PASSWORD
#VALID PWD: LENGTH >= 8, INCLUDE AT LEAST ONE UPPERCASE, ONE LOWER CASE, ONE SPECIAL CHARACTERS, ONE NUMBER
#INVALID EMAIL: NEGATION OF VALID

# TEST DATA
# 1. ACCEPT: unused email, valid pwd
# 2. REJECT: used email, valid pwd
# 3. REJECT: unused email, length = 7
# 4. REJECT: unused email, no uppercase
# 5. REJECT: unused email, no lowercase
# 6. REJECT: unused email, no special char
# 7. REJECT: unused email, no number
# 8. REJECT: invalid email, valid pwd

SUCCESS_MESSAGE ="Account created!"
UNKNOWN_FAILED_MESSAGE = "Account creation failed! Unknown error!"
EMAIL_FAILED_MESSAGE = "Invalid email!"
PASSWORD_FAILED_MESSAGE ="Password must contain at least 1 Integer, 1 uppercase letter, 1 lowercase letter, 1 special character and must be of length more than 8"
class TestRenderTemplates(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 5000
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    render_templates = False

    def test_valid_input(self):
        browser = mechanicalsoup.StatefulBrowser()

        #Test case 1
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "jerry"
        browser["email"] = "jerry"+str(time.time()).replace(".","")+"@gmail.com"
        browser["password"] = "Password!12345"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(SUCCESS_MESSAGE), -1) #means that it is successfully created

    def test_used_email(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 2
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry@yahoo.com"
        browser["password"] = "Password!12345"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(EMAIL_FAILED_MESSAGE), -1)

    def test_len_err(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 3
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry_unused@yahoo.com"
        browser["password"] = "Pwd!123"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(PASSWORD_FAILED_MESSAGE), -1)

    def test_uppercase_err(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 4
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry_unused@yahoo.com"
        browser["password"] = "password!12345"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(PASSWORD_FAILED_MESSAGE), -1)

    def test_lowercase_err(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 5
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry_unused@yahoo.com"
        browser["password"] = "PASSWORD!12345"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(PASSWORD_FAILED_MESSAGE), -1)

    def test_special_char_err(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 6
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry_unused@yahoo.com"
        browser["password"] = "Password12345"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(PASSWORD_FAILED_MESSAGE), -1)

    def test_num_err(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 7
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry_unused@yahoo.com"
        browser["password"] = "Password!!!!"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(PASSWORD_FAILED_MESSAGE), -1)
    
    def test_email_err(self):
        browser = mechanicalsoup.StatefulBrowser()
        #Test case 8
        browser.open("http://localhost:5000/register")
        browser.select_form('#registration_form')
        browser["name"] = "MechanicalSoup"
        browser["email"] = "jerry_unused"
        browser["password"] = "Password!12345"
        res = browser.submit_selected()

        self.assertNotEqual(str(res.content).find(EMAIL_FAILED_MESSAGE), -1)
        

if __name__ == '__main__':
    unittest.main()


