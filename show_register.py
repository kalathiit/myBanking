#!"C:/Python34/python.exe"

import cgi, cgitb
import sys
import helperHTML
import helperSession
import mlog
import mysql.connector
from database.db_config import config

TAG = "SHOW_REGISTER.py"
mlog.debug(TAG, "At show_register.py!")
cgitb.enable()
print(helperHTML.get_html_init())

try:
    mlog.debug(TAG, "Establishing database connection..")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
except Exception as e:
    mlog.error(TAG,"Unable to conenct to MyBanking Database:" +  str(e))
    print('''
            <h4>Unable to conenct to MyBanking Database.</h4>
            <div id="entry" >
                <a href="home.py">BACK</a>
            </div>
        ''')
    print(helperHTML.get_html_end_preset())
    sys.exit()

all_recs = None
try:
    select_max_acc = "select max(acc_number) as maximum from account"
    cursor.execute(select_max_acc)
    all_recs = cursor.fetchall()
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

available_acc_num = ""
if all_recs != None :
    for item in all_recs:
        available_acc_num = int(item[0] + 1)
#close conn and cursor
cursor.close()
conn.close()

#Dump register page content..
content = '''
    <h4>Register/Sign up:</h4>
    <form action="/myBanking/do_register.py" method="post">
       <div id="entry">
            <label>Full Name</label>
            <input type="text" placeholder="Enter Full Name" name="full_name" required>
	   </div>
       <div id="entry">
            <label>Username</label>
            <input type="text" placeholder="Enter Username" name="login_name" required>
	   </div>
	   <div id="entry">
            <label>Password</b></label>
            <input type="password" placeholder="Enter Password" name="login_key" required>
       </div>
       <div id="entry">
            <label>Confirm Password</b></label>
            <input type="password" placeholder="Confirm Password" name="login_key_confirm" required>
       </div>
       <div id="entry">
            <label>Account Number</b></label>
            <input type="number" name="acc_number" value='''
content += str(available_acc_num) + " readonly>"
content += '''
       </div>
       <div id="entry">
            <label>Bank Name</b></label>
            <input type="text" placeholder="Enter Bank Name" name="bank_name" required>
       </div>
       <div id="entry">
            <label>Bank Branch</b></label>
            <input type="text" placeholder="Enter Bank Branch" name="branch_name" required>
       </div>
       <div id="entry">
            <label>IFSC Code</b></label>
            <input type="text" placeholder="Enter IFSC Code" name="ifsc_code" required>
       </div>

       <div id="entry" >
            <button type="submit">Register</button>
       </div>
       <div id="entry" >
            <a href="home.py">Sign In</a>
        </div>
    </form>
'''

print(helperHTML.get_html_start_preset())
print(content)
print(helperHTML.get_html_end_preset())



