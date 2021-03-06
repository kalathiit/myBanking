#!"C:/Python34/python.exe"

import cgi, cgitb
import mysql.connector
import sys
import helperHTML
import helperSession
from database.db_config import config
import mlog
import datetime
from helperRegEx import Validator

TAG = "DO_MONEY_TRANSFER"
mlog.debug(TAG, "Trying to do money transfer..")
cgitb.enable()
print(helperHTML.get_html_init())
print(helperHTML.get_html_start_preset())

#Validate session..
if(helperSession.any_session_active() == False):
    #Show session inactive..
    mlog.debug(TAG,"No active session. So prompting to sign in again..")
    print(helperHTML.get_html_invalid_session_preset())
    print(helperHTML.get_html_end_preset())
    sys.exit()

account_number = helperSession.get_session_accout_no()
beneficiery_name = ''
beneficiery_account = 0
beneficiery_bank = ''
beneficiery_branch = ''
beneficiery_ifsc_code = ''
transfer_amount = 0
mlog.debug(TAG,"Fetching form values..")
try:
    form_entries = cgi.FieldStorage()
    beneficiery_name = form_entries.getvalue("beneficiery_name")
    beneficiery_account = form_entries.getvalue("beneficiery_account")
    beneficiery_bank = form_entries.getvalue("beneficiery_bank")
    beneficiery_branch = form_entries.getvalue("beneficiery_branch")
    beneficiery_ifsc_code = form_entries.getvalue("beneficiery_ifsc_code")
    transfer_amount = form_entries.getvalue("transfer_amount")
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

mlog.debug(TAG, "Showing menu..")
#--------------------------------------------MENU DETAILS----------------------------------------------------
#Show MENU..
print('''
        <div id="entry" >
            <a id="dashboard_menu_a" href="show_dashboard.py">DASHBOARD</a>
            <a id="dashboard_menu_a" href="show_add_payee.py">Add Payee</a>
            <a id="dashboard_menu_a" href="show_remove_payee.py">Remove Payee</a>
            <a id="dashboard_menu_a" href="show_transfer_money.py">Deposit Money</a>
            <a id="dashboard_menu_a" href="show_money_transfer.py">Money Transfer</a>
            <a id="dashboard_menu_a" href="logout.py">Logout</a>
        </div>
    ''')
print("<div id=\"entry\" >")
print("<h4> Transfer money status:</h4><br><br>")
print("</div>")

#--------------------------------------------MENU DETAILS----------------------------------------------------

mlog.debug(TAG, "Evaluating input attributes..")
error_message = None
if(beneficiery_name == None or beneficiery_account == None or beneficiery_bank == None or beneficiery_branch == None or  beneficiery_ifsc_code == None or transfer_amount == None) :
    error_message = "<br><p>Failed to do money transfer! Invalid attributes provided. Try to transfer again with valid attributes</p>"
else:
    transfer_validator = Validator()
    if transfer_validator.validate_generic_name(beneficiery_name,4,15) == False:
        error_message = transfer_validator.message
    elif int(beneficiery_account)<10000 or int(beneficiery_account) > 999999:
        error_message = "<P>Beneficiary Account number must be greater than 10000 and less than 999999!</p>"
    elif transfer_validator.validate_bank_name(beneficiery_bank,3,10) == False:
        error_message = transfer_validator.message
    elif transfer_validator.validate_branch_name(beneficiery_branch,4,10) == False:
        error_message = transfer_validator.message
    elif transfer_validator.validate_ifsc_code(beneficiery_ifsc_code) == False:
        error_message = transfer_validator.message
    elif int(transfer_amount)<0 or int(transfer_amount)>100000:
        error_message = "<P>Transfer amount must be greater than 0 and less than 100000!</p>"

mlog.error(TAG,"Money transfer validator error message: " + str(error_message))
if error_message != None:
    print('''
        <div id="entry" >        
            <p>Failed to do money transfer:</p>
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

#------------------------------------------------------------------------------------------------------------


mlog.debug(TAG, "Input attributes seems to be fine. Now validating against DB values..")
available_balance_to_transfer = 0
try:
    sql_select = "SELECT balance FROM account WHERE acc_number=" + str(account_number) + ";"
    cursor.execute(sql_select)
    all_recs = cursor.fetchall()
    if all_recs != None :
        for item in all_recs:
            available_balance_to_transfer = item[0]
except Exception as e:
    mlog.error(TAG,"Unable to get available balance:"+str(e))
#    print(e)

#Check balance is enough to do transfer
mlog.debug(TAG, "Checking balance is enough to do transfer or not..")
if(int(available_balance_to_transfer) < int(transfer_amount)):
    conn.close()
    print('''<div id="entry" >''')
    print('''<div id="entry" >''')
    print("<p>Failed to transfer amount. You are trying to transfer " + transfer_amount +", but your account balance is " + str(available_balance_to_transfer) + " only.</p>") 
    print("<p>Try to transfer again with lesser amount OR first deposit some more money to your account.</p>")
    print("</div></div>")
    print(helperHTML.get_html_end_preset())
    sys.exit()

#ELSE ALL IS WELL so far, go ahead and:
transfer_money_failed = False
final_available_balance = 0
mlog.debug(TAG, "All is well to do the transfer..making it real now..")
try:
    #------------------------------------------------------------------------------------------------------------
    #1. Update balance in account table.
    sql_update = "UPDATE account SET balance=balance-" + transfer_amount + " WHERE acc_number=" + str(account_number) + ";"
    cursor.execute(sql_update)
    conn.commit()
    mlog.debug(TAG, "Deducted from source balance. Fetching udpated balance of source..")
    sql_select = "SELECT balance FROM account WHERE acc_number=" + str(account_number) + ";"
    cursor.execute(sql_select)
    all_recs = cursor.fetchall()
    if all_recs != None :
        for item in all_recs:
            final_available_balance = item[0]
    #------------------------------------------------------------------------------------------------------------
    #2. Lastly, update balance of beneficiery if exists in account DB.
    mlog.debug(TAG, "Lastly, updating balance of beneficiery if exists in account DB..")
    try:
        sql_update = "UPDATE account SET balance=balance+" + transfer_amount + " WHERE acc_number=" + beneficiery_account + ";"
        mlog.debug(TAG, sql_update)
        cursor.execute(sql_update)
        conn.commit()
    except Exception as e:
        mlog.error(TAG,"Unable to insert transfer event to transaction table:"+str(e))
except Exception as e:
    mlog.error(TAG,"Unable to insert transfer event to transaction table:"+str(e))
    transfer_money_failed = True    

#Finally..
cursor.close()
conn.close()
mlog.debug(TAG, "All steps of transfer process are done. Final status of transfer_money_failed:"+str(transfer_money_failed))
print('''<div id="entry" >''')
print('''<div id="entry" >''')
if(transfer_money_failed == True) :
    print("<p>Unable to transfer amount! Try again.</p>")
else:
    print("<p>Successfully transferred the amount! Now, available balance is " + str(final_available_balance) + "</p>")
print("</div>")
print("</div>")

print(helperHTML.get_html_end_preset())

