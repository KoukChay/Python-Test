import mysql.connector

dbConnection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="koukchay3")
dbCursor = dbConnection.cursor()
dbCursor.execute("CREATE DATABASE IF NOT EXISTS userdb")
dbCursor.execute("USE userdb")
dbCursor.execute("CREATE TABLE IF NOT EXISTS userinfo(name VARCHAR(30),email VARCHAR(30),"
                 "password VARCHAR(30),phone SMALLINT,amount BIGINT)")


class Node:
    def __init__(self, user):
        self.name = user[0]
        self.mail = user[1]
        self.password = user[2]
        self.phone = user[3]
        self.amount = user[4]
        self.left = None
        self.right = None


class Bnk:
    def __init__(self):
        self.data = None
        self.rootNode = None
        dbCursor.execute("SELECT * FROM userinfo")
        for db in dbCursor:
            user = [db[0], db[1], db[2], db[3], db[4]]
            self.rootNode = self.insert(user, self.rootNode)
        self.menu()

    def menu(self):
        while True:
            try:
                opt = int(input("Press 1 to add new user\nPress 2 to Login\nPress 0 to exit\n==> "))
                if opt == 1:
                    self.Add_new()
                elif opt == 2:
                    pass
                    self.Login()
                elif opt == 0:
                    exit()
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def Add_new(self):
        while True:
            f_name = input("Enter your first name: ").title()
            l_name = input("Enter your last name: ").title()
            name = f_name + " " + l_name
            name_check = self.get_all_user(self.rootNode)
            if name_check is None:
                break
            elif name in name_check:
                print("Name already exit! Try another one.")
            else:
                break

        while True:
            mail = input("Enter email: ")
            mail_type = self.mail_type(mail)
            if mail_type == 0:
                print("Email combination invalid! Try another one.")
            else:
                mail_check = self.get_all_user(self.rootNode)
                if mail_check is None:
                    break
                elif mail in mail_check:
                    print("Email already exit! Try another one.")
                else:
                    break

        while True:
            pss = input("Enter password (1st char Uppercase and at least three digits)\n==>")
            pss_check = self.strong_pss_check(pss)
            if pss_check == 1:
                break
            else:
                print("Password too weak! Try again.")

        while True:
            try:
                amount = int(input("Enter amount of money: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        while True:
            try:
                phone = int(input("Enter phone no(must 3 Digit): "))
                if len(str(phone)) != 3:
                    print("Phone number must be 3 Digits")
                else:
                    phone_check = self.get_all_user(self.rootNode)
                    if phone_check is None:
                        break
                    elif phone in phone_check:
                        print("Phone number already exit! Try another one.")
                    else:
                        break

            except ValueError:
                print("Invalid input. Please enter a valid number.")

        user = [name, mail, pss, phone, amount]
        self.rootNode = self.insert(user, self.rootNode)
        DataType = "INSERT INTO userinfo(name,email,password,phone,amount)VALUES(%s,%s,%s,%s,%s)"
        dbCursor.execute(DataType, user)
        dbConnection.commit()
        print("Thank you. Your registration was successful!")
        self.menu()

    def Login(self):
        self.show_all_data(self.rootNode)
        l_mail = input("Enter mail to login: ")
        l_pass = input("Enter password to login: ")
        user = self.login_check(self.rootNode, l_mail, l_pass)
        if user is None:
            while True:
                try:
                    opt = int(input("Login Failed!\nPress 1 to exit\nPress 2 to Try Again\n==>"))
                    if opt == 1:
                        self.menu()
                    elif opt == 2:
                        self.Login()
                except ValueError:
                    print("Enter only Number!")

        elif user and user.password == l_pass:
            self.user_profile(user)

        else:
            while True:
                try:
                    opt = int(input("Login Failed!\nPress 1 to exit\nPress 2 to Try Again\n==>"))
                    if opt == 1:
                        self.menu()
                    elif opt == 2:
                        self.Login()
                except ValueError:
                    print("Enter only Number!")

    def user_profile(self, user):
        print(f"\nHi {user.name}, You are Welcome!\nYour Amount = {user.amount}")
        while True:
            try:
                opt = int(input("Press 1 to Transfer Money\nPress 2 to delete your account\nPress 3 to go back\nPress "
                                "0 to exit\n==>"))
                if opt == 1:
                    self.Transfer(user)
                elif opt == 2:
                    while True:
                        option = input("Do you really want to Delete your account? (y/n)\n==>").lower()
                        if option == "y":

                            DataType = f"DELETE FROM userinfo WHERE email=%s"
                            Data = [user.mail]
                            dbCursor.execute(DataType, Data)
                            dbConnection.commit()
                            remain_node = self.delete(self.rootNode, user.mail)
                            if remain_node is None:
                                self.rootNode = None
                            print(f"Bye {user.name}, your account was successfully deleted.")
                            self.menu()
                        elif option == "n":
                            self.user_profile(user)
                        else:
                            print("Enter either y or n!")
                elif opt == 3:
                    self.menu()
                elif opt == 0:
                    exit()
            except ValueError:
                print("Enter Only Number!")

    def Transfer(self, user):

        print(f"\nName: {user.name}\nMail: {user.mail}\nAmount: {user.amount}\n\nEnter email you want to transfer!")
        self.show_others_data(self.rootNode, user.mail)
        t_mail = input("==> ")
        t_info = self.check_user(self.rootNode, t_mail)
        if t_info is None:
            print(f"There is no user with Email {t_mail}!")
            self.user_profile(user)
        else:
            if user.amount > 0:
                while True:
                    try:
                        t_money = int(input("Enter amount of money you want to transfer: "))
                        if user.amount >= t_money:
                            t_info.amount += t_money
                            user.amount -= t_money
                            self.upload_db(user.mail, t_mail, user.amount, t_info.amount)
                            print(f"\nTransfer Successes!\nYour current amount: {user.amount}\n{t_info.name}'s current "
                                  f"amount: {t_info.amount}")
                            self.user_profile(user)
                        else:
                            print("You can't transfer more than you have!")
                    except ValueError:
                        print("Enter only Number!")
            else:
                print("You don't have enough money to transfer!")
                self.user_profile(user)

    def mail_type(self, mail):
        length = len(mail)
        while True:
            for i in range(length):
                if mail[i] == '@':
                    mail_name = mail[:i]
                    mail_domain = mail[i:]
                    for char in mail_name:
                        n = ord(char)
                        if 31 < n < 48 or 57 < n < 64 or 90 < n < 97 or 122 < n < 127:
                            return 0
                        else:
                            pass
                    if mail_domain in ["@gmail.com", "@yahoo.com", "@mail.ru", "@outlook.com", "@apple.com"]:
                        return 1
                    else:
                        return 0
            return 0

    def strong_pss_check(self, pss):
        count = 0
        capital_flag = 0
        threeDigits_flag = 0
        if "A" <= pss[0] <= "Z":
            capital_flag = 1

        for i in pss:
            if "0" <= i <= "9":
                count += 1

        if count >= 3:
            threeDigits_flag = 1

        if capital_flag == 1 and threeDigits_flag == 1:
            return 1
        else:
            return None

    def insert(self, udata, root):

        if root is None:
            root = Node(udata)
            return root

        if udata[1] < root.mail:
            root.left = self.insert(udata, root.left)

        elif udata[1] > root.mail:
            root.right = self.insert(udata, root.right)

        return root

    def get_all_user(self, root):
        self.data = []
        return self.traversal(root)

    def traversal(self, root):
        if root:
            self.traversal(root.left)
            users = [root.mail, root.phone, root.name]
            self.data.extend(users)
            self.traversal(root.right)
        return self.data

    def login_check(self, root, mail, pss):
        if root is None or (root.mail == mail and root.password == pss):
            return root
        if mail < root.mail:
            return self.login_check(root.left, mail, pss)
        if mail > root.mail:
            return self.login_check(root.right, mail, pss)

    def check_user(self, root, mail):
        if root is None or root.mail == mail:
            return root
        if mail < root.mail:
            return self.check_user(root.left, mail)
        if mail > root.mail:
            return self.check_user(root.right, mail)

    def show_all_data(self, root):

        if root:
            self.show_all_data(root.left)
            print("Email: ", root.mail)
            self.show_all_data(root.right)

    def show_others_data(self, root, mail):

        if root:
            self.show_others_data(root.left, mail)
            if root.mail == mail:
                pass
            else:
                print("Email: ", root.mail)
            self.show_others_data(root.right, mail)

    def delete(self, root, mail):
        if root is None:
            print("There is no user!")
            return root
        if root.left is None and root.right is None and root.mail == mail:
            return None
        if mail < root.mail:
            root.left = self.delete(root.left, mail)
        elif mail > root.mail:
            root.right = self.delete(root.right, mail)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            else:
                c_node = root.left
                while c_node.right:
                    c_node = c_node.right
                root.mail = c_node.mail
                root.left = self.delete(root.left, root.mail)
        return root

    def upload_db(self, u_mail, t_mail, u_money, t_money):
        DataType = f"UPDATE userinfo SET amount = %s WHERE email = %s"
        Data = [(u_money, u_mail), (t_money, t_mail)]
        dbCursor.executemany(DataType, Data)
        dbConnection.commit()


if __name__ == "__main__":
    try:
        bank_system = Bnk()
    except Exception as err:
        print(err)