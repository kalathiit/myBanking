#!"C:/Python34/python.exe"

import cgi, cgitb
import mysql.connector
import sys
import helperHTML
import helperSession
from database.db_config import config
import mlog
from helperRegEx import Validator

TAG = "DOLOGIN"
mlog.debug(TAG, "Trying to login..")
cgitb.enable()
print(helperHTML.get_html_init())
login_name = ""
login_key = ""
mlog.debug(TAG,"Fetching form values..")
try:
    form_entries = cgi.FieldStorage()
    login_name = form_entries.getvalue("login_name")
    login_key = form_entries.getvalue("login_key")
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

#if invalid attributes, show error and eixt.
error_message = None
login_validator = Validator()
if login_validator.validate_login_name(login_name,6,15) == False:
    error_message = login_validator.message
elif login_validator.validate_login_key(login_key,6,12) == False:
    error_message = login_validator.message

mlog.error(TAG,"login validator error message: " + str(error_message))
if error_message != None:
    print(helperHTML.get_html_start_preset())
    print('''
        <h4>Failed to login:</h4>
        <div id="entry" >
    ''')
    print(error_message)
    print('''
        </div>
        <div id="entry" >
            <br><a href="home.py">Sign In</a>
        </div>
    ''')
    print(helperHTML.get_html_end_preset())
    sys.exit()

try:
    mlog.debug(TAG, "Establishing database connection..")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
except Exception as e:
    mlog.error(TAG,"Unable to connect to MyBanking Database.")
    print(helperHTML.get_html_init())
    print(helperHTML.get_html_start_preset())
    print('''
            <h4>Unable to connect to MyBanking Database.</h4>
            <div id="entry" >
                <a href="home.py">HOME</a>
            </div>
        ''')
    print(helperHTML.get_html_end_preset())
#    print(e)
    sys.exit()

all_recs = None
try:
    query_login = "SELECT login_key, acc_number FROM user WHERE login_name='"+login_name+"';"
    cursor.execute(query_login)
    all_recs = cursor.fetchall()
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

account_number = 0
if all_recs != None :
    for item in all_recs:
        db_login_key = item[0]
        db_account_number = item[1]
        #print("<br> db_login_key:{0} and login_key:{1} ".format(db_login_key, login_key))
        if(str(login_key) == str(db_login_key)):
            account_number = db_account_number
            #print("<br> account number found to be:{0}".format(account_number))

#CLOSE DB CONNECTION
cursor.close()
conn.close()

#Validate session iff login_attempt
#First clear any previous sessions:
helperSession.end_session()
if login_name != None and int(account_number) > 0:
    #Overrite any current session
    helperSession.start_session(account_number)

mlog.debug(TAG,"any_session_active:"+str(helperSession.any_session_active()))
if(helperSession.any_session_active()):
    #Redirect to dashboard..
    print(helperHTML.get_html_content_with_redirect("/myBanking/show_dashboard.py"))
else :
    print(helperHTML.get_html_init())
    print(helperHTML.get_html_start_preset())
    print("<div id=\"entry\" >")
    print("Unable to sign in. Try again!<br>")
    print("</div>")
    print('''
        <div id="entry" >
            <a href="home.py">Sign In</a>
        </div>
    ''')
    print(helperHTML.get_html_end_preset())


