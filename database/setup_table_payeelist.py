#!"C:/Python34/python.exe"

import mysql.connector
from db_config import config

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
except Exception as e:
    print(e)
#-------------------------------------------------DROP------------------------------------------------------------
print("\n--------------------------------------DROP-payee_list---------------------------------------")
query_drop_table = "DROP TABLE payee_list"
try:
    print("Query: ",query_drop_table)
    conn.query(query_drop_table)
    print("Result: Successfully dropped table.")
except Exception as e:    
    print(e)

#-------------------------------------------------CREATE------------------------------------------------------------
print("\n--------------------------------------CREATE-payee_list---------------------------------------")
query_create_payee_list = '''CREATE TABLE payee_list (
  id INT NOT NULL AUTO_INCREMENT,
  payee_name VARCHAR(45) NOT NULL,
  owner_account INT NOT NULL,
  payee_account INT NOT NULL,
  payee_bank VARCHAR(45) NOT NULL,
  payee_branch VARCHAR(45) NOT NULL,
  payee_ifsc_code VARCHAR(10) NOT NULL,
  PRIMARY KEY (id));'''
try:
    print("Query: ",query_create_payee_list)
    cursor.execute(query_create_payee_list)
    print("Result: Successfully executed.")    
except Exception as e:
    print("Error occured!");
    print(e)

#---------------------------------------------------INSERT----------------------------------------------------------
print("\n--------------------------------------INSERT-payee_list---------------------------------------")
try:
    sql_insert1 = "INSERT INTO payee_list(payee_name,owner_account,payee_account,payee_bank,payee_branch,payee_ifsc_code)"
    sql_insert1 += " VALUES('Bharath', 100001, 200002, 'PNB', 'Panjab','PNBB123456')"
    cursor.execute(sql_insert1)
    sql_insert2 = "INSERT INTO payee_list(payee_name,owner_account,payee_account,payee_bank,payee_branch,payee_ifsc_code)"
    sql_insert2 += " VALUES('Naveen', 100002, 200001, 'SBI', 'Bangalore','SBIB123456')"
    cursor.execute(sql_insert2)
    conn.commit()
    print("Result: Successfully inserted.")
except Exception as e:
    print("Insert error!")
    print(e)
print("\n--------------------------------------DONE---------------------------------------")

#Close cursor and conn
cursor.close()
conn.close()
