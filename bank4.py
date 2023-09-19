import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sub@08051997"
    )
    cursor = mydb .cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS banknew")
    cursor.execute("USE banknew")
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (account_id INT PRIMARY KEY AUTO_INCREMENT, acc_name VARCHAR(100), address VARCHAR(100), mobile_no INT, balance FLOAT(7,3))")

except mysql.connector.Error as err:
    print("Error:", err)
else:
    mydb.close()


def create_account():
    try:
        acc_name = input("Enter your name: ")
        address = input("Enter Address: ")
        mobile_no = input("Enter Mobile Number: ")

        while True:
            balance = float(input("Initial amount (minimum 1000): "))
            if balance < 1000:
                print("Minimum initial amount is 1000. Please enter a sufficient amount.")
            else:
                break  # Break the loop when a valid amount is entered

        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sub@08051997",
            database="banknew"
        )
        cursor = mydb.cursor()

        # Insert a new account record with the initial balance
        cursor.execute("INSERT INTO accounts (acc_name, address, mobile_no, balance) VALUES (%s, %s, %s, %s)",
                       (acc_name, address, mobile_no, balance,))
        mydb.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        account_id = cursor.fetchone()[0]

        print("Account created successfully!")
        print("Your account ID is:", account_id)

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        mydb.close()

def deposit():
    try:
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter Amount to Deposit: "))

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sub@08051997",
            database="banknew"
        )
        cursor = mydb.cursor()

        cursor.execute("UPDATE accounts SET Balance = Balance + %s WHERE account_id = %s", (amount, account_id))
        mydb.commit()

        print("Deposit successful!")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        mydb.close()

# Function to withdraw money from an account
def withdraw():
    try:
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter Amount to Withdraw: "))

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sub@08051997",
            database="banknew"
        )
        cursor = mydb.cursor()

        cursor.execute("SELECT Balance FROM accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()

        if result:
            balance = result[0]
            if balance >= amount:
                # Update the balance after withdrawal
                cursor.execute("UPDATE accounts SET Balance = Balance - %s WHERE account_id = %s", (amount, account_id))
                mydb.commit()
                print("Withdrawal successful!")
            else:
                print("Insufficient balance for withdrawal.")
        else:
            print("Account not found.")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        mydb.close()

# Function to check account balance
def balance_inquiry():
    try:
        account_id = int(input("Enter Account ID: "))

        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sub@08051997",
            database="banknew"
        )
        cursor = mydb.cursor()

        # Retrieve the account balance
        cursor.execute("SELECT account_id, Balance FROM accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()

        if result is not None:
            account_id, balance = result
            print(f"Account ID: {account_id}, Balance: {balance}")
        else:
            print("Account not found.")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        mydb.close()
while True:
    print("\nBanking System Menu:")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Balance Inquiry")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        balance_inquiry()
    elif choice == "5":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please select a valid choice")