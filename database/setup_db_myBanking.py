#!"C:/Python34/python.exe"

import mysql.connector
from db_config import create_db

try:
    conn = mysql.connector.connect(**create_db)
    cursor = conn.cursor()
except Exception as e:    
    print(e)
#-------------------------------------------------DROP DB------------------------------------------------------------
print("\n--------------------------------------DROP-myBanking---------------------------------------")
query_drop_db = "DROP DATABASE my_banking;"
try:
    print("Query: ",query_drop_db)
    cursor.execute(query_drop_db)
    print("Result: Successfully dropped DB.")
except Exception as e:    
    print(e)
#-------------------------------------------------CREATE------------------------------------------------------------
print("\n--------------------------------------CREATE-account---------------------------------------")
query_create_account = "CREATE DATABASE my_banking;"
try:
    print("Query: ",query_create_account)
    cursor.execute(query_create_account)
    print("Result: Successfully created.")
except Exception as e:
    print("Error occured!");
    print(e)

print("\n--------------------------------------DONE---------------------------------------")
conn.commit()
cursor.close()
conn.close()

