
-------------------------------------------README------------------------------------------------------------

                Web Application : MyBanking
				OS				: Windows Server 16
				Database		: Mysql -> [Developed using mysql.connector library instead of C extension] 
                Python Version  : Python3.4(Accessible @ "C:/Python34/python.exe")

-------------------------------------------Pre-requisites----------------------------------------------------

                Server			: Wamp or similar server to run Apache 
				Database 		: Mysql [Used mysql server part of wamp server]
				Python Modules	: cgi, cgitb, mysql.connector, sys, datetime, re, logging
				
-------------------------------------------Database Design----------------------------------------------------

				Database config	: configured in database/db_config.py
									config = {
												"database":"my_banking",
												"host":"localhost",
												"user":"root",
												"password":"abcd1234"
											}
				Tables			: user, account, payee_list

-------------------------------------------Database Setup----------------------------------------------------

				run "database/setup_db_myBanking.py"	: creates database my_banking 
				run "database/setup_table_user.py"		: creates user table and inserts below values 
															for users- Kalathi and Arun with below details
															
															login_name 		login_key 	acc_number 
															kalathi 		password 	100001
															arun123 		welcome 	100002
				
				run "database/setup_table_account.py"	: creates account table and inserts values for Kalathi and Arun
				run "database/setup_table_payeelist.py"	: creates payee_list table and inserts a payee for users Kalathi and Arun
				
-------------------------------------------APPLICATION & PAGES--------------------------------------------------------
				
				Application starts with		: home.py
				Home page/Login page		: home.py, do_login.py
				Dashboard					: show_dashboard.py
				Add Payee					: show_add_payee.py, do_add_payee.py
				Remove Payee				: show_remove_payee.py, do_remove_payee.py
				Deposit Money				: show_dposit_money.py, do_deposit_money.py
				Money Transfer				: show_money_transfer.py, do_money_transfer.py
				Logout						: logout.py
				Register					: show_register.py, do_register.py
				Forgot Password?			: show_reset_password.py, do_reset_password.py
						
-------------------------------------------Modules & Other files--------------------------------------------------------

				helperHTML.py				: Helper module for HTML page layouts
				helperRegEx.py				: Helper module for field validation using re module
				helperSession.py			: Helper module to handle session files
				mlog						: helper module for logging
				def_style.css				: css template file
				session.txt					: File to store account number of user in active session
				my_banking_app.txt			: Log file to capture debug and error messages
				class_account.py			: Python class module to set values for user object and contain
											  methods to create new user and new account upon registration
												
-------------------------------------------END of README------------------------------------------------------------
