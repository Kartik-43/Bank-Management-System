import mysql.connector
import csv
import datetime
import pickle

now = datetime.datetime.now()

logo = ("PAYTM MANAGEMENT")

mydb = mysql.connector.connect(host="localhost", user="root", passwd="kartik")
mycursor = mydb.cursor()
mycursor.execute("Create database if not exists Paytm")
mycursor.execute("use Paytm")
mycursor.execute("create table if not exists Management(name varchar(35),city varchar(25),"
                 "mobileno char(10) primary key,adhaar_no char(12), balance int(8), pin char(4))")
mycursor.execute("create table if not exists transaction(mobileno char(10), amount int(7),date varchar(100),"
                 "trans_type char(10), foreign key(mobileno) references Management(mobileno))")
mydb.commit()

while True:
    print(logo)
    print("1) Create Account")
    print("2) Deposit")
    print("3) Pay")
    print("4) Display Account")
    print("5) Update Name or City")
    print("6) Forgot Pin")
    print("7) Delete Account")
    print("8) Exit")

    choice = int(input("Enter Your Choice:"))
    #To Create Account
    if choice == 1:
        mycursor.execute("select mobileno from Management")

        mob = []
        for i in mycursor:
            mob += i
        pn = str(input("Enter Mobile Number:"))
        name = input("Enter Your Name:")
        city = input("Enter City Name:")
        if len(pn) < 10:
            print("Mobile Number Not Valid...\n Enter A Valid Phone Number.")
            pn = str(input("Enter Mobile Number:"))
        else:
            pass
        adhrno = str(input("Enter 12 Digit Adhaar Number:"))
        if len(adhrno) < 12:
            print("Adhaar Number Provided Is Wrong..")
            adhrno = str(input("Enter 12 Digit Adhaar Number:"))
        elif len(adhrno) > 12:
            print("Adhaar Number Provided Is Wrong..")
            adhrno = str(input("Enter 12 Digit Adhaar Number:"))
        else:
            pass

        balance = int(input("Deposit Money To Open Account(Min. 1000):"))
        if int(balance) < 1000:
            print("Min Amount Required To Open Account Is 1000")
            balance = int(input("Deposit Money To Open Account(Min. 1000):"))
        else:
            pass
        pin = input("Create A 4 Digit Pin:")
        if pn in mob:
            print("This Mobile Number Already Has An Account Linked. ")
            pn = str(input("Enter Different Mobile Number:"))
            del mob[-1]
            mob += pn
        else:
            pass
        with open("MobileNumbers.txt", "a+") as f:
            f.write(pn + "," + "\n")
            r = f.readlines()
        with open("Adhaar Numbers.txt", "a+") as f:
            f.write(adhrno + "," + "\n")
            s = f.readlines()
        mycursor.execute(
            'insert into Management values(\'' + name + "','" + city + "','" + pn + "','" + adhrno + "','" + str(
                balance) + "','" + pin + "')")
        mydb.commit()
        print("Account Created Successfully.")

    #Depositing Monney     
    elif choice == 2:
        pn = str(input("Enter Mobile Number:"))

        mn = int(input("Enter Amount To Deposit:"))

        pin = int(input("Enter Your Pin:"))

        dt = now.strftime('%H:%M:%S on %A, %B the %dth, %Y')
        type = "Deposit"

        mycursor.execute("select pin from Management where mobileno ='"+pn+"'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(pass3) == int(pin):
            mycursor.execute("insert into transaction values('" + pn + "','" + str(mn) + "','" + dt + "','" + type + "')")
            mycursor.execute("update Management set balance= balance+'"+ str(mn) +"'where mobileno ='" + pn + "'")

            mydb.commit()
            print(mn, "Deposited Successfully")
        else:
            print("Wrong PIN")
            print("Transaction Timed Out")
            
    #Making a Payment
    elif choice == 3:
        pn = str(input("Enter Your Phone Number:"))

        pay = int(input("Enter Amount To Be Payed:"))

        dot = now.strftime('%H:%M:%S on %A, %B the %dth, %Y')

        password= input("Enter PIN:")

        type = "Payment"
        mycursor.execute("select pin from Management where mobileno ='" + pn + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = pass2[0]

        if int(password) == int(pass3):
            mycursor.execute("select balance from Management where mobileno = '" +pn+ "'")
            balance1 = mycursor.fetchall()
            balance2 = balance1[0]
            balance = balance2[0]

            if int(balance) < pay:
                print('=> Balance = ', balance)
                print("=> You Dont Have Enough Balance To Pay.")


            else:
                mycursor.execute(
                    "insert into transaction values('" + pn + "','" + str(pay) + "','" + dot + "','" + type + "')")

                mycursor.execute("update Management set balance=balance-'" + str(pay) + "' where mobileno='" + pn + "'")

                print("=> Money withdrawn successfully !")

            mydb.commit()
            print("\n\n\n")

        else:
            print("Invalid PIN")
            print("Transaction Cancelled")
            print("\n\n")

    #Displaying Account Information
    elif choice == 4:

        PN=str(input("Enter Mobile Number:"))

        pwd = input("Enter PIN:")

        mycursor.execute("select pin from Management where mobileno ='" + PN + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        if int(pwd) == int(pass3):

            mycursor.execute("select * from Management where mobileno ='" + PN + "'")

            Disp = []
            for i in mycursor:
                Disp += i

            print("\n\n")
            print("Name : ", Disp[0], "\nCity : ", Disp[1], "\nMobile Number : ", Disp[2],
                  "\nAdhaar Number : ", Disp[3],"\nBalance :",Disp[4])
            print("\n")

            fields = ["Name", "City", "Mobile number", "Balance"]
            row = Disp
            fl = Disp[1] + ".csv"

            with open(fl, 'a+', newline='') as f:
                csv_w = csv.writer(f, delimiter=',')
                csv_w.writerow(fields)
                csv_w.writerow(row)

            print("=> To see Details of the account open", fl, " file")
            print("\n\n")

        else:
            print("Invalid PIN")
            print("Transaction Cacelled")
            print("\n\n")

    #Updating Name Or City        
    elif choice == 5:
        PN = str(input("Enter Mobile Number:"))

        pwd1 = int(input("Enter PIN:"))

        mycursor.execute("select pin from Management where mobileno ='" + PN + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = pass2[0]

        if int(pass3) == int(pwd1):
            pref = int(input("Press 1 for change in Name Press 2 for change in City:\n"))
            if pref == 1:
                name = input("Enter the new name : ")
                mycursor.execute(" update Management set name ='" + name + "' where mobileno ='" + PN + "'")
                print("\nName changed successfully\n")

            elif pref == 2:
                city = input("Enter the city name : ")
                mycursor.execute(" update Management set city ='" + city + "' where mobileno ='" + PN + "'")
                print("\nCity changed successfully\n")

        else:
            print("Password entered is wrong\nPlease Try Again... ")

    #Changing PIN
    elif choice == 6:
        mn = int(input("Enter Mobile number : "))
        adhr= input("Enter Adhaar Number: ")
        passs = input("Enter New 4 Digit Pin : ")

        mycursor.execute("select mobileno from Management where adhaar_no  ='" + adhr + "'")
        mn1 = mycursor.fetchall()
        mn2 = mn1[0]
        mn3 = int(mn2[0])

        if mn == mn3:
            mycursor.execute(" update Management set pin ='" + passs + "' where mobileno ='" + str(mn) + "'")
            print("Passcode changed successfully")

        else:
            print("This Adhaar Number Is Not Linked To The Entered Mobile Number\nRequest Cancelled.")

    #Deleting Account
    elif choice == 7:
        mn = input("Enter Mobile Number: ")
        passss = input("Enter PIN : ")

        mycursor.execute("select pin from Management where mobileno ='" + mn + "'")
        pass1 = mycursor.fetchall()
        pass2 = pass1[0]
        pass3 = int(pass2[0])

        ch = input("Type 'y' to continue & 'n' to stop deleting : ")
        if ch == 'y' or 'Y':
            if int(passss) == int(pass3):
                mycursor.execute("delete from transaction where mobileno='" + mn + "'")
                mycursor.execute("delete from Management where mobileno='" + mn + "'")
                print("Your account is successfully deleted !")
            else:
                print("Wrong PIN")
                print("Process Failed!")

        elif ch == 'n' or 'N':
            print("Command Terminated")
            break

        else:
            print("Wrong Choice Entered")

    #Closing Program
    elif choice == 8:
        print("Thanks For Using Paytm.")
        print("Closing Program...")

        break
