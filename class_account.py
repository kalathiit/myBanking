#!"C:/Python34/python.exe"

import mysql.connector
from database.db_config import config
import mlog

TAG="Class Account"

class Account():
    login_name=""
    login_key=""
    acc_number=0
    name=""
    bank_name=""
    ifsc_code=""
    branch_name=""
    balance=0

    #Constructor. Usage: obj_acc = Account()
    def __init__(self):
        mlog.debug(TAG,"Constructor()")

    def set_account_details(self,acc_number, acc_name,bank,branch,ifsc,balance_amt=0):
        self.acc_number = acc_number
        self.name = acc_name
        self.bank_name = bank
        self.branch_name = branch
        self.ifsc_code = ifsc
        self.__balance_amt = int(balance_amt)

    def set_user_details(self,acc_number,login_name,login_key):
        self.acc_number = acc_number
        self.login_name = login_name
        self.login_key = login_key

    def insert_to_account(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
        except Exception as e:
            mlog.error(TAG,"Unable to conenct to MyBanking Database.")
            print('''
        <h4>Unable to conenct to MyBanking Database.</h4>
            <div id="entry" >
                <a href="show_register.py">BACK</a>
            </div>
        ''')
            print(helperHTML.get_html_end_preset())
            sys.exit()

        insert_account = "INSERT INTO ACCOUNT(ACC_NUMBER, NAME, BANK_NAME, BRANCH_NAME, IFSC_CODE, BALANCE) "
        insert_account += "VALUES (" + str(self.acc_number) + ", '" + str(self.name) + "' , '" + str(self.bank_name) + "' , '" + str(self.branch_name) + "' ,"
        insert_account += "'" + str(self.ifsc_code) + "' , "+ str(self.__balance_amt) + ");"
        mlog.debug(TAG, insert_account)
        insert_status = False
        error = None
        try:
            cursor.execute(insert_account)
            conn.commit()
        except Exception as e:
            error = str(e)
            mlog.error(TAG,"Error: " + error)
            insert_status = True

        cursor.close()
        conn.close()

        return insert_status, error

    def insert_to_user(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
        except Exception as e:
            mlog.error(TAG,"Unable to conenct to MyBanking Database.")
            print('''
        <h4>Unable to conenct to MyBanking Database.</h4>
            <div id="entry" >
                <a href="show_register.py">BACK</a>
            </div>
        ''')
            print(helperHTML.get_html_end_preset())
            sys.exit()

        insert_user = "INSERT INTO USER (ACC_NUMBER, LOGIN_NAME, LOGIN_KEY) VALUES ( " + str(self.acc_number)
        insert_user += ", '" + str(self.login_name) + "' , '" + str(self.login_key) + "' );"
        mlog.debug(TAG, insert_user)
        insert_status = False
        error = None
        try:
            cursor.execute(insert_user)
            conn.commit()
        except Exception as e:
            error = str(e)
            mlog.error(TAG,"Error: " + error)
            insert_status = True

        cursor.close()
        conn.close()

        return insert_status, error

    def delete_account(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
        except Exception as e:
            mlog.error(TAG,"Unable to conenct to MyBanking Database.")
            print('''
        <h4>Unable to conenct to MyBanking Database.</h4>
            <div id="entry" >
                <a href="show_register.py">BACK</a>
            </div>
        ''')
            print(helperHTML.get_html_end_preset())
            sys.exit()

        delete_acc = "DELETE FROM ACCOUNT WHERE ACC_NUMBER = " + str(self.acc_number)
        error = None
        try:
            cursor.execute(delete_acc)
            conn.commit()
        except Exception as e:
            error = str(e)
            mlog.error(TAG,"Error: " + error)

        cursor.close()
        conn.close()
