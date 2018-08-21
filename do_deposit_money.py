#!"C:/Python34/python.exe"

import cgi, cgitb
import mysql.connector
import sys
import helperHTML
import helperSession
from database.db_config import config
import mlog
import datetime

TAG = "DO_DEPOSIT"
mlog.debug(TAG, "Trying to do deposit..")
cgitb.enable()
print(helperHTML.get_html_init())
print(helperHTML.get_html_start_preset())

#Validate session..
if(helperSession.any_session_active() == False):
    #Show session inactive..
    mlog.debug(TAG,"In do_deposit_money with no active session. So prompting to sign in again..")
    print(helperHTML.get_html_invalid_session_preset())
    print(helperHTML.get_html_end_preset())
    sys.exit()

account_number = helperSession.get_session_accout_no()
deposit_amount = 0
mlog.debug(TAG,"Fetching form values..")
try:
    form_entries = cgi.FieldStorage()
    deposit_amount = form_entries.getvalue("deposit_amount")
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

#--------------------------------------------MENU DETAILS----------------------------------------------------
#Show MENU..
print('''
        <div id="entry" >
            <a id="dashboard_menu_a" href="show_dashboard.py">DASHBOARD</a>
            <a id="dashboard_menu_a" href="show_add_payee.py">Add Payee</a>
            <a id="dashboard_menu_a" href="show_remove_payee.py">Remove Payee</a>
            <a id="dashboard_menu_a" href="show_deposit_money.py">Deposit Money</a>
            <a id="dashboard_menu_a" href="show_money_transfer.py">Money Transfer</a>
            <a id="dashboard_menu_a" href="logout.py">Logout</a>
        </div>
    ''')
print("<div id=\"entry\" >")
print("<h4> Deposit money status:</h4><br><br>")
print("</div>")
#------------------------------------------------------------------------------------------------------------

error_message = None
if(deposit_amount == None) :
    error_message = "<br><p>Failed to deposit amount. No balance value provided! Make sure balance is greater than 0.</p>"
elif int(deposit_amount)<=0 or int(deposit_amount)>100000:
    error_message = "<br><p>Failed to deposit amount. Make sure balance is greater than 0 and less than 100000.</p>"

mlog.error(TAG,"Deposit money error message: " + str(error_message))
if error_message != None:
    print('''
        <div id="entry" >        
            <p>Failed to deposit money:</p>
            <div id="entry" >
    ''')
    print(error_message)
    print('''</div></div>''')
    print(helperHTML.get_html_end_preset())
    sys.exit()


try:
    mlog.debug(TAG, "Establishing database connection..")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
except Exception as e:
    mlog.error(TAG,"Unable to conenct to MyBanking Database.")
    print('''
            <h4>Unable to conenct to MyBanking Database.</h4>
            <div id="entry" >
                <a href="show_dashboard.py">BACK</a>
            </div>
        ''')
    print(helperHTML.get_html_end_preset())
#    print(e)
    sys.exit()

deposit_money_failed = False
final_available_balance = 0
try:
    sql_update = "UPDATE account SET balance=balance+" + deposit_amount + " WHERE acc_number=" + str(account_number) + ";"
    cursor.execute(sql_update)
    conn.commit()
    sql_select = "SELECT balance FROM account WHERE acc_number=" + str(account_number) + ";"
    cursor.execute(sql_select)
    all_recs = cursor.fetchall()
    if all_recs != None :
        for item in all_recs:
            final_available_balance = item[0]
except Exception as e:
    deposit_money_failed = True
    mlog.error(TAG,"Unable to add payee to database:"+str(e))

#Close cursor and connection
cursor.close()
conn.close()

print('''<div id="entry" >''')
print('''<div id="entry" >''') # to give margin
if(deposit_money_failed == True) :
    print("<br><p>Unable to add deposit amount to MyBanking Account Database.!</p>")
else:
    print("<br><p>Successfully deposited amount! Now, available balance is " + str(final_available_balance) + "</p>")
print("</div>")
print("</div>")
print(helperHTML.get_html_end_preset())

