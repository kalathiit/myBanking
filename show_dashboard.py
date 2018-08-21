#!"C:/Python34/python.exe"

import cgi, cgitb
import mysql.connector
import sys
import helperHTML
import helperSession
from database.db_config import config
import mlog

TAG = "DASHBOARD"
mlog.debug(TAG, "At dashboard!")
cgitb.enable()
print(helperHTML.get_html_init())
print(helperHTML.get_html_start_preset())

if(helperSession.any_session_active() == False):
    #Show session inactive..
    mlog.debug(TAG,"In dashboard with no active session. So prompting to sign in again..")
    print(helperHTML.get_html_invalid_session_preset())
    print(helperHTML.get_html_end_preset())
    sys.exit()
mlog.debug(TAG,"In dashboard with active session..")
try:
    mlog.debug(TAG, "Establishing database connection..")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
except Exception as e:
    mlog.error(TAG,"Unable to conenct to MyBanking Database.")
    helperSession.end_session()
    print('''
            <h4>Unable to conenct to MyBanking Database.</h4>
            <div id="entry" >
                <a href="index.py">HOME</a>
            </div>
        ''')
    print(helperHTML.get_html_end_preset())
#    print(e)
    sys.exit()

all_recs = None
account_number = helperSession.get_session_accout_no()
try:    
    query_user = "SELECT login_name FROM user WHERE acc_number="+str(account_number)+";"
    cursor.execute(query_user)
    all_recs = cursor.fetchall()
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

db_login_name = ""
if all_recs != None :
    for item in all_recs:
        db_login_name = item[0]
#--------------------------------------------MENU DETAILS----------------------------------------------------
#Greet user and show MENU..
print('''
        <div id="entry" >
            <a id="dashboard_menu_a" href="show_add_payee.py">Add Payee</a>
            <a id="dashboard_menu_a" href="show_remove_payee.py">Remove Payee</a>
            <a id="dashboard_menu_a" href="show_deposit_money.py">Deposit Money</a>
            <a id="dashboard_menu_a" href="show_money_transfer.py">Money Transfer</a>
            <a id="dashboard_menu_a" href="logout.py">Logout</a>
        </div>
    ''')
print("<div id=\"entry\" >")
mlog.debug(TAG,"Welcoming user: " + str(db_login_name))
print("<h2> Welcome " + str(db_login_name) + "!</h2><br><br>")
print("</div>")
#--------------------------------------------ACCOUNT DETAILS----------------------------------------------------
#1.Get account details as dictonary and display as table.
try:
    query_account = "SELECT name, acc_number, ifsc_code, bank_name, branch_name, balance FROM account WHERE acc_number="+str(account_number)+";"
    cursor.execute(query_account)
    all_recs = cursor.fetchall()
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

account_details = '''
        <div id="entry_dashboard_acc_details" >
            <p>Account details:</p>
            <table border=1>
            <tr>
                <th>ACC HOLDER NAME</th>
                <th>ACCOUNT NO</th>
                <th>BANK IFSC CODE</th>
                <th>BANK NAME</th>
                <th>BRANCH NAME</th>
                <th>BALANCE</th>
            </tr>
    '''

if all_recs != None :
    for item in all_recs:
        account_details += "<tr>"
        account_details += "<td>" + str(item[0]) + "</td>"
        account_details += "<td>" + str(item[1]) + "</td>"
        account_details += "<td>" + str(item[2]) + "</td>"
        account_details += "<td>" + str(item[3]) + "</td>"
        account_details += "<td>" + str(item[4]) + "</td>"
        account_details += "<td>" + str(item[5]) + "</td>"
        account_details += "</tr>"
else:
    account_details += "<tr>"
    for index in range(0,5):
        account_details += "<td>Null</td>"
    account_details += "</tr>"
account_details += "</table></div>"
print(account_details)

#--------------------------------------------PAYEE DETAILS----------------------------------------------------
#3.Get list of payees and display as table.
try:
    #payee_list(payee_name,owner_account,payee_account,payee_bank,payee_branch,payee_ifsc_code)
    query_payee_list = "SELECT payee_name, payee_account, payee_bank, payee_branch, payee_ifsc_code FROM payee_list WHERE owner_account="+str(account_number)+";"
    cursor.execute(query_payee_list)
    all_recs = cursor
except Exception as e:
    mlog.error(TAG,"Error: " + str(e))

payee_details = '''
        <div id="entry_dashboard_payees" >
            <br><p>Available payees:</p>
            <table border=1>
            <tr>
                <th>PAYEE NAME</th>
                <th>PAYEE ACCOUNT</th>
                <th>PAYEE BANK</th>
                <th>BANK BRANCH</th>
                <th>IFSC CODE</th>
            </tr>
    '''

if all_recs != None :
    rows = all_recs.fetchmany(size=5)
    while (rows):
        for item in rows:
            payee_details += "<tr>"
            payee_details += "<td>" + str(item[0]) + "</td>"
            payee_details += "<td>" + str(item[1]) + "</td>"
            payee_details += "<td>" + str(item[2]) + "</td>"
            payee_details += "<td>" + str(item[3]) + "</td>"
            payee_details += "<td>" + str(item[4]) + "</td>"
            payee_details += "</tr>"
        rows = all_recs.fetchmany(size=5)
else:
    payee_details += "<tr>"
    for index in range(0,5):
        payee_details += "<td>Null</td>"
    payee_details += "</tr>"
payee_details += "</table></div>"
print(payee_details)

#CLOSE DB CONNECTION
cursor.close()
conn.close()

print(helperHTML.get_html_end_preset())
