#!"C:/Python34/python.exe"

import cgi, cgitb
import mysql.connector
import sys
import helperHTML
import helperSession
from database.db_config import config
import mlog
from helperRegEx import Validator
from class_account import Account

TAG = "DO_REGISTER"
mlog.debug(TAG, "Trying to register new user..")
cgitb.enable()
print(helperHTML.get_html_init())
print(helperHTML.get_html_start_preset())

print("<div id=\"entry\" >")
print("<h4> Register new user status:</h4><br><br>")
print("</div>")

full_name = ""
login_name = ""
login_key = ""
login_key_confirm = ""
acc_number = ""
bank_name = ""
branch_name = ""
ifsc_code = ""
mlog.debug(TAG,"Fetching form values..")
try:
    form_entries = cgi.FieldStorage()
    full_name = form_entries.getvalue("full_name")
    login_name = form_entries.getvalue("login_name")
    login_key = form_entries.getvalue("login_key")
    login_key_confirm = form_entries.getvalue("login_key_confirm")
    acc_number = form_entries.getvalue("acc_number")
    bank_name = form_entries.getvalue("bank_name")
    branch_name = form_entries.getvalue("branch_name")
    ifsc_code = form_entries.getvalue("ifsc_code")
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

#if invalid attributes, show error and eixt.
error_message = None
if(full_name == None or login_name == None or login_key == None or login_key_confirm == None or acc_number == None or bank_name == None or branch_name == None or ifsc_code == None) :
    error_message = "<br><p>Failed to register! Invalid attributes provided. Register again with valid attributes</p>"
else:
    register_validator = Validator()
    if register_validator.validate_generic_name(full_name,4,15) == False:
        error_message = register_validator.message
    elif register_validator.validate_login_name(login_name,6,15) == False:
        error_message = register_validator.message
    elif register_validator.validate_login_key(login_key,6,12) == False:
        error_message = register_validator.message
    elif login_key != login_key_confirm:
        error_message = "<P>Passwords do not match!</p>"
    elif register_validator.validate_bank_name(bank_name,3,10) == False:
        error_message = register_validator.message
    elif register_validator.validate_branch_name(branch_name,4,10) == False:
        error_message = register_validator.message
    elif register_validator.validate_ifsc_code(ifsc_code) == False:
        error_message = register_validator.message

mlog.error(TAG,"Register validator error message: " + str(error_message))
if error_message != None:
    print('''
        <p>Failed to register:</p>
        <div id="entry" >
    ''')
    print(error_message)
    print('''
        </div>
        <div id="entry" >
            <a href="show_register.py">Register</a>
        </div>
        <div id="entry" >
            <a href="home.py">Sign In</a>
        </div>
    ''')
    print(helperHTML.get_html_end_preset())
    sys.exit()


register_failed = False
create_account = False
create_user = False
error_message = None

obj_new_user = Account()
obj_new_user.set_account_details(acc_number,full_name,bank_name,branch_name,ifsc_code,0)

create_account, error_message = obj_new_user.insert_to_account()

if(create_account != True):
    obj_new_user.set_user_details(acc_number,login_name,login_key)
    create_user, error_message = obj_new_user.insert_to_user()

    if(create_user == True):
        obj_new_user.delete_account()

if( create_account != False or create_user != False ):
    register_failed = True


print('''<div id="entry" >''')
if(register_failed == True):
    print("<br><p>Failed to register! "+error_message+". Register again.</p>")        
else:
    print("<br><p>Congratulations. Registration successfull!</p>")
print("</div>")
print('''
    <div id="entry" >
        <a href="show_register.py">Register</a>
    </div>
    <div id="entry" >
        <a href="home.py">Sign In</a>
    </div>
''')

print(helperHTML.get_html_end_preset())

