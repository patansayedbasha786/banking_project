import psycopg2

import datetime

class Royal_bank:
    def __init__(self):
        self.user = 'sk'
        self.password = '00'

    # Establishes connection to PostgreSQL database
    def connect_db(self):
        return psycopg2.connect(
            dbname="royal_bank_of_india",
            user="postgres",
            password="root",
            host="localhost",
            port=5432
        )

    # Function to deposit money into user's account
    def deposit_amount(self, conn, cursor, table_name, result):
        print("\nUser found. Last transaction:")
        print("Aadhar:", result[0])# result[0] is AADHAR_NO
        print("Name:", result[1])# result[1] is name_of_user
        print("Balance:", result[5])# result[5] is BALANCE
        print("WITHDRAWL:", result[6])# result[6] is WITHDRAWL
        print("Deposit:", result[7])# result[7] is DEPOSIT 

        # Ask for deposit amount and calculate new balance
        new_deposit = int(input("Enter Deposit Amount: "))
        new_balance = result[5] + new_deposit

        # Insert new transaction record into the table using .format()
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO {} (
                AADHAR_NO, name_of_user, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR_no, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {})
        """.format(table_name, result[0], result[1], result[2], result[3], result[4], new_balance, 0, new_deposit))

        conn.commit()
        print("New deposit recorded.")

    # Function to WITHDRAWL money from user's account
    def WITHDRAWL(self, conn, cursor, table_name, result):
        print("\nUser found. Last transaction:")
        print("Aadhar:", result[0])
        print("Name:", result[1])
        print("Balance:", result[5])

        WITHDRAWL = int(input("Enter WITHDRAWL Amount: "))

        # Check for sufficient balance
        if WITHDRAWL > result[5]:
            print("Insufficient balance.")
            return

        new_balance = result[5] - WITHDRAWL

        # Insert WITHDRAWL transaction record
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO {} (
                AADHAR_NO, name_of_user, ADDRESS, PHONE_NO,
                nominee_aadhar_no, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {})
        """.format(table_name, result[0], result[1], result[2], result[3], result[4], new_balance, WITHDRAWL, 0))

        conn.commit()
        print("New WITHDRAWL recorded.")
        

    def mini_statement(self,conn,cursor,table_name,result):
        print("----ROYAL BANK OF INDIA----")
        print("Aadhar \t:\t",result[0])
        print("Name \t:\t",result[1])
        print("phone_no \t:\t",result[3])
        print("Time \t:\t",datetime.datetime.now())
        print("Current Balance \t:\t",result[5])

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM {} WHERE AADHAR_NO = {}
        """.format(table_name, result[0]))
        transactions = cursor.fetchall()
        print("\n----TRANSACTION HISTORY----")
        print("withdrawl Amount || Deposit Amount || Balance")
        for transaction in transactions: 
            if transaction[6] != 0:
                withdrawl = transaction[6]
            else:
                withdrawl = 0 
            if transaction[7] != 0:
                deposit = transaction[7]
            else:
                deposit = 0 
            if transaction[5] != 0:
                balance = transaction[5]
            else:
                balance = 0
            print(" {} \t\t |{}\t\t    |{}".format(withdrawl, deposit, balance))
        cursor.close()

    def balance_enquiry(self,result):
        print("Time",datetime.datetime.now())
        print("Name :",result[1])
        print("Current balance :",result[5])

    def cancel(self, conn, cursor):
        print("\n------Thank you for using our Bank!-----")
        print("*Visit again!*")
    # Create a new user record if not found in DB
    def create_user(self, conn, cursor, table_name, aadhar_no):
        # Collect all user details from input
        name_of_user = input("Enter Full Name: ")
        aadhar_no=int(input("enter aadhar number: "))
        if not aadhar_no==aadhar_no:
            print("inviled aadhar number  please enter valid aadhar number")
        address = input("Enter Address: ")
        phone_no = int(input("Enter Phone Number: "))
        nominee_aadhar_no = int(input("Enter Nominee Aadhar Number: "))
        balance = int(input("Enter Initial Balance: "))
        WITHDRAWL = int(input("Enter WITHDRAWL Amount: "))
        deposit = int(input("Enter Deposit Amount: "))

        # Insert new user record into the table
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO {} (
                AADHAR_NO, name_of_user, ADDRESS, PHONE_NO,
                nominee_aadhar_no, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {})
        """.format(table_name, aadhar_no, name_of_user, address, phone_no,
                   nominee_aadhar_no, balance, WITHDRAWL, deposit))
        conn.commit()
        print("New user created.")

    # Login and main program logic
    def login(self):
        # Check for correct username
        entered_user = input("Please enter the username: ")
        if entered_user == self.user:
            # Check for correct password
            entered_password = input("Please enter the password: ")
            if entered_password == self.password:
                print("Login successful!")

                try:
                    # Connect to database and get cursor
                    conn = self.connect_db()
                    print("Database connected")
                    cursor = conn.cursor()

                    # Ask for table name
                    table_name = input("Enter Table Name: ").strip()

                    # Try creating the table (fails if it already exists)
                    try:
                        cursor.execute("""
                            CREATE TABLE {} (
                                AADHAR_NO BIGINT,
                                name_of_user VARCHAR(50),
                                ADDRESS VARCHAR(50),
                                PHONE_NO BIGINT,
                                nominee_aadhar_no BIGINT,
                                BALANCE BIGINT,
                                WITHDRAWL INT,
                                DEPOSIT BIGINT
                            );
                        """.format(table_name))
                        conn.commit()
                        print("Table '{}' created.".format(table_name))
                    except psycopg2.errors.DuplicateTable:
                        # If table exists, rollback the failed transaction
                        conn.rollback()
                        print("Table '{}' already exists.".format(table_name))

                    # Ask for Aadhar number and check if user exists
                    Aadhar_no = int(input("Enter Aadhar Number: "))
                    cursor.execute("""
                        SELECT * FROM {} 
                        WHERE AADHAR_NO = {}
                        ORDER BY ctid DESC LIMIT 1 
                    """.format(table_name, Aadhar_no))
                    result = cursor.fetchone()
                    # ctid is a hidden system column in PostgreSQL that refers to the physical location of a row. 
                    # It can be used to retrieve the most recent record for a given Aadhar number.
                    # But ctid is not meant for application logic, and it's not very beginner-friendly.
                    # It's recommended to use a more explicit identifier for application logic.
                    # If user exists, offer deposit or WITHDRAWL
                    if result:  # if result is not None  
                        
                        print("\nUser already exists.")
                        print("1. Deposit")
                        print("2. WITHDRAWL")
                        print("3. ministatement")
                        print("4. balance enquiry")
                        print("5. cancal")
                        choice = input("Choose option (1/2/3/4/5): ")

                        if choice == '1':
                            self.deposit_amount(conn, cursor, table_name, result)
                        elif choice == '2':
                            self.WITHDRAWL(conn, cursor, table_name, result)
                        elif choice == '3':
                            self.mini_statement(conn, cursor ,table_name , result)
                        elif choice == '4':
                            self.balance_enquiry(result)
                        elif choice == '5':
                            self.cancel(conn,cursor)
                        else:
                            print("Invalid choice.")
                    else:
                        # If user not found, create new user
                        print("User not found. Creating new user.")
                        self.create_user(conn, cursor, table_name, Aadhar_no)

                except Exception as e:
                    print("ERROR:", e)

            else:
                print("Incorrect password.")
        else:
            print("Incorrect username.")
Royal_bank().login()