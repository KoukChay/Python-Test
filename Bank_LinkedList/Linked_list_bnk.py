import atexit

import pymongo

from linked_Link import UserLinkedList

connection = pymongo.MongoClient("localhost", 27017)
Bank_db = connection["Bank_db"]
users = Bank_db["users"]


class Node:
    def __init__(self, name: str, mail: str, pss: str, amount: int, phone: int, ):
        self.name = name
        self.mail = mail
        self.password = pss
        self.amount = amount
        self.phone = phone
        self.next = None


class Bnk:
    def __init__(self):
        self.user_list = UserLinkedList()
        atexit.register(self.user_list.save_user)

        for i in users.find({}):
            user = Node(i["name"], i["mail"], i["pass"], i["amount"], i["phone"])
            self.user_list.add_old_user(user)
        users.delete_many({})

        self.menu()

    def menu(self):
        while True:
            try:
                opt = int(input("Press 1 to register, 2 to Login, 0 to exit: "))
                if opt == 1:
                    self.Reg()
                elif opt == 2:
                    self.Login()
                elif opt == 0:
                    exit()
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def Reg(self):
        f_name = input("Enter your first name: ").title()
        l_name = input("Enter your last name: ").title()
        name = f_name + " " + l_name
        mail = ""
        name_check = self.user_list.check_user(mail, name, phone=None)
        if name_check is not None:
            print("Name already exit! Try another one.")
            self.Reg()
        else:
            pass

        while True:
            mail = input("Enter email: ")
            mail_type = self.mail_type(mail)
            if mail_type == 0:
                print("Email combination invalid! Try another one.")
            else:
                mail_check = self.user_list.check_user(mail, name, phone=None)
                if mail_check is not None:
                    print("Email already exit! Try another one.")
                else:
                    break

        pss = input("Enter password: ")
        while True:
            try:
                amount = int(input("Enter amount of money: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        while True:
            try:
                phone = int(input("Enter phone no: "))
                phone_check = self.user_list.check_user(mail, name, phone)
                if phone_check is not None:
                    print("Phone number already exit! Try another one.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        user = Node(name, mail, pss, amount, phone)
        self.user_list.add_user(user)
        self.menu()

    def Login(self):
        l_mail = input("Enter mail to login: ")
        l_pass = input("Enter password to login: ")
        user = self.user_list.check_user(l_mail, name="", phone=None)
        if user and user.password == l_pass:
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
                opt = int(input("Press 1 to Transfer Money\nPress 2 to exit\n==>"))
                if opt == 1:
                    self.Transfer(user)
                elif opt == 2:
                    self.menu()
            except ValueError:
                print("Enter Only Number!")

    def Transfer(self, user):
        current_user = self.user_list.get_user(user.name)
        for i in current_user:
            print(f"Name: {i['name']}\nMail: {i['mail']}\nAmount: {i['amount']}\n")

        t_mail = input("Enter email you want to transfer: ")
        t_info = self.user_list.check_user(t_mail, name="", phone=None)
        if t_info is None:
            print("There is no user except you for now!")
            self.user_profile(user)
        else:
            t_amount = t_info.amount
            if user.amount > 0:
                while True:
                    try:
                        t_money = int(input("Enter amount of money you want to transfer: "))
                        if user.amount >= t_money:
                            t_amount += t_money
                            user.amount -= t_money
                            self.user_list.money_update(t_info, t_amount, user, user.amount)
                            print(f"\nTransfer Successes!\nYour current amount: {user.amount}\n{t_info.name}'s current "
                                  f"amount: {t_amount}")
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


if __name__ == "__main__":
    # bank_system = Bnk()
    try:
        bank_system = Bnk()
    except Exception as err:
         print(err)
