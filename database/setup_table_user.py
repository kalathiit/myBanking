#!/usr/bin/python3

import mysql.connector
from db_config import config



try:
    conn = mysql.connector.connect(**config)
except Exception as e:    
    print(e)

cursor = conn.cursor()
#-------------------------------------------------DROP------------------------------------------------------------
print("\n--------------------------------------DROP-user---------------------------------------")
query_drop_table = "DROP TABLE user"
try:
    print("Query: ",query_drop_table)
    cursor.execute(query_drop_table)
    print("Result: Successfully dropped table.")
except Exception as e:    
    print(e)

#---------------------------------------------------CREATE----------------------------------------------------------
print("\n--------------------------------------CREATE-user---------------------------------------")
query_create_user = '''CREATE TABLE user (
  login_name VARCHAR(20) UNIQUE NOT NULL,
  login_key VARCHAR(20) NOT NULL,
  acc_number INT NOT NULL,
  PRIMARY KEY (acc_number));'''
try:
    print("Query: ",query_create_user)
    cursor.execute(query_create_user)
    print("Result: Successfully executed.")
    
except Exception as e:
    print("Error occured!");
    print(e)
#---------------------------------------------------INSERT----------------------------------------------------------
print("\n--------------------------------------INSERT-user---------------------------------------")
try:
    sql_insert1 = "INSERT INTO user(acc_number,login_name,login_key)"
    sql_insert1 += " VALUES(100001,'kalathi', 'password')"
    cursor.execute(sql_insert1)
    sql_insert2 = "INSERT INTO user(acc_number,login_name,login_key)"
    sql_insert2 += " VALUES(100002,'arun123', 'welcome')"
    cursor.execute(sql_insert2)
    print("Result: Successfully inserted.")
except Exception as e:
    print("Insert error!")
    print(e)
print("\n--------------------------------------DONE---------------------------------------")
#Commit and Close
conn.commit()
cursor.close()
conn.close()
