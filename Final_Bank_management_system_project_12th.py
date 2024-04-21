import mysql.connector
import random
import datetime
import pickle
import csv

now = datetime.datetime.now()

logo = """



  ____              _      __  __                                                   _   
 |  _ \            | |    |  \/  |                                                 | |  
 | |_) | __ _ _ __ | | __ | \  / | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
 |  _ < / _` | '_ \| |/ / | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
 | |_) | (_| | | | |   <  | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
 |____/ \__,_|_| |_|_|\_\ |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
                                                     __/ |                              
                                                    |___/



                                                    """


print("\n\n")

# creating database :-

mydb = mysql.connector.connect(host="localhost", user="root", passwd="lvm123")

mycursor = mydb.cursor()

mycursor.execute("create database if not exists Bank_System")

mycursor.execute("use Bank_System")

# creating required tables :-

mycursor.execute("create table if not exists bank_master(acc_no char(3) primary key,name varchar(30),city varchar("
                 "20),mobileno char(10),balance int(7), passcode varchar(5))")

mycursor.execute("create table if not exists banktrans(acc_no char(15),amount int(6),date_of_transaction varchar(50),"
                 "transaction_type char(10),foreign key (acc_no) references bank_master(acc_no))")

mydb.commit()

while True:

    print(logo)

    print("=> 1=Create account")

    print("=> 2=Deposit money")

    print("=> 3=Withdraw money")

    print("=> 4=Display account")

    print("=> 5=Display First transactions")

    print("=> 6=Forgot Account number")

    print("=> 7=Delete Account")

    print("=> 8=Update Name, City or mobile number")

    print("=> 9=Update Password")

    print("=> 10=Exit")

    ch = int(input("=> Enter your choice:"))

    # PROCEDURE FOR CREATING A NEW ACCOUNT OF THE APPLICANT :-

    if ch == 1:

        mycursor.execute("select mobileno from bank_master")

        mob = []
        for i in mycursor:
            mob += i

        mycursor.execute("select acc_no from bank_master")

        acnoo = []

        for i in mycursor:
            acnoo += i

        number = str(random.randint(100, 999))

        if number in acnoo:
            number = str(random.randint(100, 999))

        else:
            pass

        with open("account_numbers.txt", "a+") as f:
            f.write(number + "," + "\n")
            result = f.readlines()
            f.close()
            if number in result:
                del result[-1]
                number = random.randint(100, 999)
                with open("acc.txt", "w") as fi:
                    result += number
                    for i in result:
                        fi.write(i + "," + "\n")
                    fi.close()
            else:
                pass

        with open("account_number.dat", "ab+") as f:
            pickle.dump(number + "," + "\n", f)
            # result = pickle.load(f)
            f.close()
            if number in result:
                del result[-1]
                number = random.randint(100, 999)
                with open("acc.dat", "wb") as fi:
                    result += number
                    for i in result:
                        pickle.dump(i + "," + "\n", fi)
                    fi.close()
            else:
                pass

        print("\n\n\n")

        print("=> All information prompted are mandatory to be filled")

        acno = number
        print("=> The account number given to you is ", number, ",Keep it safe to use this account")

        name = input("=> Enter name (limit 35 characters):")

        city = str(input("=> Enter State & City name:"))

        balance = str(input("=> Deposit some money to get this account working (MIN BALANCE :- 500) :"))

        if int(balance) <= 500:
            print("=> Balance is less than 2000, Couldn't start the account...")
            balance = str(input("=> Deposit some money to get this account working (MIN BALANCE :- 500) :"))
        else:
            pass

        mn = str(input("=> Enter mobile number :"))

        password = input("=> Create a 5 digit passcode :- ")

        if len(mn) < 10:
            print("=> Length of the mobile number is less than 10 !")
            print("=> Enter a valid phone number ")
            mn = str(input("=> Enter mobile number :"))
        else:
            pass

        if mn in mob:
            print("=> Mobile number already used, Use another number")
            mn = str(input("=> Enter another mobile number :"))
            del mob[-1]
            mob += mn
        else:
            pass

        with open("phone_numbers.txt", "a+") as f:
            f.write(mn + "," + "\n")
            res = f.readlines()

        mycursor.execute(
                'insert into bank_master values(\'' + acno + "','" + name + "','" + city + "','" + mn + "','" + str(
                    balance) + "','" + password + "')")

        mydb.commit()

        print("=> Account is successfully created !!!")
        print("\n\n\n")

    # PROCEDURE FOR UPDATIONG DETAILS AFTER THE DEPOSITION OF MONEY BY THE APPLICANT :-

    elif ch == 2:

        acno = str(input("=> Enter account number:"))

        dp = int(input("=> Enter amount to be deposited:"))

        pas = input("=> Enter the passcode :- ")

        dot = now.strftime('%H:%M:%S on %A, %B the %dth, %Y')

        ttype = "Deposit"

        mycursor.execute("select passcode from bank_master where acc_no ='" + acno + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(pass3) == int(pas):

            mycursor.execute("insert into banktrans values('" + acno + "','" + str(dp) + "','" + dot + "','" + ttype + "')")

            mycursor.execute("update bank_master set balance = balance+'" + str(dp) + "' where acc_no='" + acno + "'")

            mydb.commit()

            print("=> money has been deposited successfully !")
            print("\n\n\n")

        else:
            print("=> The Password entered is wrong...")
            print("=> Couldn't Complete the transaction...")
            print("\n\n")

    # PROCEDURE FOR UPDATING THE DETAILS OF ACCOUNT AFTER THE WITHDRAWL OF MONEY BY THE APPLICANT :-

    elif ch == 3:

        acno = str(input("=> Enter account number:"))

        wd = int(input("=> Enter amount to be withdrawn:"))

        dot = now.strftime('%H:%M:%S on %A, %B the %dth, %Y')

        ps = input("=> Enter the passcode :- ")

        ttype = "Withdraw"

        mycursor.execute("select passcode from bank_master where acc_no ='" + acno + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(ps) == int(pass3):

            mycursor.execute("select balance from bank_master where acc_no ='" + acno + "'")

            balance1 = mycursor.fetchall()

            balance2 = balance1[0]
            balance = balance2[0]

            if int(balance) < wd:
                print('=> Balance = ', balance)
                print("=> balance is less than the amount you need to withdraw")
                print("=> Can not withdraw the money ")

            else:
                mycursor.execute("insert into banktrans values('" + acno + "','" + str(wd) + "','" + dot + "','" + ttype + "')")

                mycursor.execute("update bank_master set balance=balance-'" + str(wd) + "' where acc_no='" + acno + "'")

                print("=> Money withdrawn successfully !")

            mydb.commit()
            print("\n\n\n")

        else:
            print("=> The Password entered is wrong...")
            print("=> Couldn't Complete the transaction...")
            print("\n\n")

# PROCEDURE FOR DISPLAYING THE ACCOUNT OF THE ACCOUNT HOLDER AFTER HE / SHE ENTERS HIS / HER ACCOUNT NUMBER :-

    elif ch == 4:

        AcNo = str(input("=> Enter Account number :"))

        pwd = input("=> Enter the passcode :- ")

        mycursor.execute("select passcode from bank_master where acc_no ='" + AcNo + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(pwd) == int(pass3):

            mycursor.execute("select * from bank_master where acc_no='" + AcNo + "'")

            Disp = []
            for i in mycursor:
                Disp += i

            print("\n\n")
            print("Account number = ", Disp[0], ", name = ", Disp[1], ", city = ", Disp[2], ", mobile number = ", Disp[3],
                  ", Balance = ", Disp[4])
            print("\n")

            fields = ["Account number", "Name", "City", "Mobile number", "Balance"]
            row = Disp
            fl = Disp[1] + ".csv"

            with open(fl, 'a+', newline='') as f:
                csv_w = csv.writer(f, delimiter=',')
                csv_w.writerow(fields)
                csv_w.writerow(row)

            print("=> To see Details of the account open", fl, " file")
            print("\n\n")

        else:
            print("=> The Password entered is wrong...")
            print("=> Couldn't Complete the transaction...")
            print("\n\n")

    # PROCEDURE FOR DISPLAYING THE RECENT TRANSACTIONS OF THE ACCOUNT HOLDER AFTER HE / SHE ENTERS HIS / HER ACCOUNT NUMBER :-

    elif ch == 5:

        AcN = str(input("=> Enter Account number :"))

        pwd2 = input("=> Enter the passcode :- ")

        mycursor.execute("select passcode from bank_master where acc_no ='" + AcN + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(pwd2) == int(pass3):
            mycursor.execute("select * from banktrans where acc_no='" + AcN + "'")

            Displ = []
            for i in mycursor:
                Displ += i

            print("\n\n")
            print("=> Account number = ", Displ[0], ", Amount = ", Displ[1], ", Date of Transaction = ", Displ[2],
                  ",Transaction type = ", Displ[3])
            print("\n")

            fields = ["Account number", "Amount", "Date of Transaction", "Transaction Type"]
            row = Displ
            file = Displ[0] + ".csv"

            with open(file, 'a+', newline='') as f:
                csv_w = csv.writer(f, delimiter=',')
                csv_w.writerow(fields)
                csv_w.writerow(row)

            print("=> To see Details of the recent transaction in the account open", file, " file")
            print("\n\n")

        else:
            print("=> The Password entered is wrong...")
            print("=> Couldn't Complete the transaction...")
            print("\n\n")

    # PROCEDURE FOR DISPLAYING THE ACCOUNT NUMBER OF THE ACCOUNT HOLDER AFTER HE / SHE ENTERS HIS / HER MOBILE NUMBER :-

    elif ch == 6:
        print("\n\n")

        print("=> Enter your mobile number to get your account number")
        mo = input("=> enter your mobile number :- ")

        passs = input("=> Enter the passcode :- ")

        mycursor.execute("select passcode from bank_master where mobileno ='" + mo + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(passs) == int(pass3):
            mycursor.execute("select acc_no from bank_master where mobileno='" + mo + "'")

            acc2 = mycursor.fetchall()
            acc1 = acc2[0]
            acc = acc1[0]

            print("=> The account number linked to this mobile number is = ", acc)

            print("\n\n")

        else:
            print("=> The Password entered is wrong...")
            print("=> Couldn't Complete the transaction...")
            print("\n\n")

    # Procedure to Delete an applicant's Account :-

    elif ch == 7:

        acno = input("Enter your account number : ")
        mn = input("Enter your mobile number : ")
        passss = input("Enter the passcode : ")

        mycursor.execute("select passcode from bank_master where mobileno ='" + mn + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(passss) == int(pass3):
            choice = input("Type 'y' to continue & 'n' to stop deleting : ")

            if choice in "Yy":

                    mycursor.execute("delete from banktrans where acc_no='" + acno + "'")
                    mycursor.execute("delete from bank_master where acc_no='" + acno + "'")

                    print("\n\n")
                    print("Your account is successfully deleted !")
                    print("\n\n")

            else:
                print("\n\nStopped the process...\n Account is not deleted !\n\n")

        else:
            print("=> The Password entered is wrong...")
            print("=> Couldn't Complete the Work...")
            print("\n\n")

    # Procedure to change the Name, City or Mobile number of an applicant :-

    elif ch == 8:
        acno = input("Enter your account number : ")
        passss = input("Enter the passcode : ")

        mycursor.execute("select passcode from bank_master where acc_no ='" + acno + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        choice = int(input("What do you want to change?\n 1) Name\n 2) City\n 3) Mobile number \n ==>"))

        if choice == 1:
            name = input("Enter the new name : ")
            mycursor.execute(" update bank_master set name ='" + name + "' where acc_no ='" + acno + "'")
            print("Name changed successfully")

        elif choice == 2:
            city = input("Enter the city name : ")
            mycursor.execute(" update bank_master set city ='" + city + "' where acc_no ='" + acno + "'")
            print("City changed successfully")

        elif choice == 3:
            mobile_number = input("Enter the new Mobile Number : ")
            mycursor.execute(" update bank_master set mobileno ='" + mobile_number + "' where acc_no ='" + acno + "'")
            print("Mobile Number changed successfully")

    # Procedure to change the password of the applicant :-

    elif ch == 9:
        acno = input("Enter your account number : ")
        mn = input("Enter your Mobile number : ")
        passs = input("Enter the new passcode (5 characters long) : ")

        mycursor.execute("select mobileno from bank_master where acc_no ='" + acno + "'")
        mn1 = mycursor.fetchall()
        mn2 = mn1[0]
        mn3 = int(mn2[0])

        if int(mn) == int(mn3):
            mycursor.execute(" update bank_master set passcode ='" + passs + "' where mobileno ='" + mn + "'")
            print("Passcode changed successfully")

        else:
            print("This mobile number is not linked to the entered account number\n please check and try again")

    # PROCEDURE FOR EXITING THE CODE :-

    elif ch == 10:

        print("\n\n")
        print("\n\n")

        print("=> Closing the program...")
        print("=> Thanks for visiting \nGoodbye!")

        print("\n\n")
        print("\n\n")

        break
