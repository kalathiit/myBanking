#!"C:/Python34/python.exe"

import mysql.connector
from db_config import config

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
except Exception as e:    
    print(e)
#-------------------------------------------------DROP------------------------------------------------------------
print("\n--------------------------------------DROP-account---------------------------------------")
query_drop_table = "DROP TABLE account"
try:
    print("Query: ",query_drop_table)
    cursor.execute(query_drop_table)
    print("Result: Successfully dropped table.")
except Exception as e:    
    print(e)
#-------------------------------------------------CREATE------------------------------------------------------------
print("\n--------------------------------------CREATE-account---------------------------------------")
query_create_account = '''CREATE TABLE account (
  acc_number INT NOT NULL,
  name VARCHAR(45) NOT NULL,
  ifsc_code VARCHAR(10) NOT NULL,
  bank_name VARCHAR(45) NOT NULL,
  branch_name VARCHAR(45) NOT NULL,
  balance INT NOT NULL,
  PRIMARY KEY (acc_number));'''
try:
    print("Query: ",query_create_account)
    cursor.execute(query_create_account)
    print("Result: Successfully created.")
except Exception as e:
    print("Error occured!");
    print(e)

#---------------------------------------------------INSERT----------------------------------------------------------
print("\n--------------------------------------INSERT-account---------------------------------------")
try:
    sql_insert1 = "INSERT INTO account(acc_number,name,ifsc_code,bank_name,branch_name,balance)"
    sql_insert1 += " VALUES(100001,'Kalathi', 'HDFC002406', 'HDFC', 'Bangalore',1000)"
    cursor.execute(sql_insert1)
    sql_insert2 = "INSERT INTO account(acc_number,name,ifsc_code,bank_name,branch_name,balance)"
    sql_insert2 += " VALUES(100002,'Arun', 'ICIC009765', 'ICICI', 'Panjab',2000)"
    cursor.execute(sql_insert2)
    print("Result: Successfully inserted.")
except Exception as e:
    print("Insert error!")
    print(e)

#---------------------------------------------------UPDATE-balance----------------------------------------------------------
print("\n--------------------------------------UPDATE-account---------------------------------------")
try:
    sql_update1 = "UPDATE account SET balance=1500 WHERE acc_number=100001"
    cursor.execute(sql_update1)
    print("Result: Successfully updated.")
except Exception as e:
    print("Insert error!")
    print(e)

print("\n--------------------------------------DONE---------------------------------------")
conn.commit()
cursor.close()
conn.close()

