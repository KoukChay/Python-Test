import json
import socket

import encry_decrypt


class Auction_client:

    def __init__(self):
        self.target_ip = "localhost"
        self.target_port = 9190
        self.userKey = self.getting_key()
        self.client_menu()

    def getting_key(self):
        userKey: str = input("Enter your encryption key for the whole process:")
        return userKey

    def client_runner(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client

    def client_menu(self):
        # client = self.client_runner()
        print("\n" + "<This is client menu>".upper().center(80))
        user_data = input("get : to get all information\nlogin : to login\nreg : to register"
                          "\nPress 1 to get auction info:\nPress 2 To Exit:")

        if user_data == '1':
            raw_data: str = 'info'
            self.info(raw_data)

        elif user_data == 'login':
            raw_data = 'login'
            self.login(raw_data)

        elif user_data == 'reg':
            raw_data = 'Bidder_reg'
            self.bidder_reg(raw_data)

        elif user_data == 'get':
            pass

    def sending_encrypted(self, raw_data: str):
        client = self.client_runner()
        encry = encry_decrypt.A3Encryption()
        decry = encry_decrypt.A3Decryption()
        encrypted_data = encry.start_encryption(raw_data, self.userKey)
        client.send(bytes(encrypted_data, "utf-8"))
        recv_info = client.recv(4096)
        recv_encrypted = recv_info.decode("utf-8")
        recv_decrypted = decry.startDecryption(recv_encrypted)
        # print(recv_decrypted)
        # client.close()
        return recv_decrypted

    def info(self, raw_data):
        print("\n" + "item and price list\n".upper().center(80))
        decrypted_str = self.sending_encrypted(raw_data)
        decrypted_dict = {}
        try:
            decrypted_dict = json.loads(decrypted_str)
        except Exception as err:
            print(str(err))
        for key, value in decrypted_dict.items():
            print(f'ID: {key} - Item: {value["Item"]} - '
                  f'Price: ${value["Price"]}')

    def bidder_reg(self, raw_data):
        print("\nWelcome to bidder registration page".upper().center(80))
        b_name = "_"
        try:
            while True:
                b_mail = input("Enter your Email to register: ")
                mail_check = self.email_validation(b_mail)
                if mail_check == 0:
                    print("Mail you entered is Invalid! Please try again.")
                    while True:
                        try:
                            opt = int(input("==>Press 1 to try another.\n==>Press 2 to go to main"
                                            "page.\n==>"))

                            if opt == 1:
                                self.bidder_reg(raw_data)
                                break
                            elif opt == 2:
                                self.client_menu()
                                break
                            else:
                                print("Wrong option. Please Try Again!")
                        except ValueError:
                            print("Press only Number!")
                else:
                    exit_check = self.user_exist(b_mail, b_name, raw_data)
                    if exit_check == 1:
                        print(f'\nEmail <{b_mail}> already exit!')
                        while True:
                            try:
                                opt = int(input(
                                    "==>Press 1 to try another.\n==>Press 2 to login with this Email.\n==>Press 3 to "
                                    "go to main page.\n==>"))

                                if opt == 1:
                                    self.bidder_reg(raw_data)
                                    break
                                elif opt == 2:
                                    # self.login()
                                    break
                                elif opt == 3:
                                    self.client_menu()
                                    break
                                else:
                                    print("Wrong option. Please Try Again!")
                            except ValueError:
                                print("Press only Number!")
                    else:
                        break
            name = True
            while name:
                f_name = input("%-30s: " % "Enter your First Name")
                l_name = input("%-30s: " % "Enter your Last Name")
                if l_name == "":
                    b_name = f_name.title()
                else:
                    b_name = f_name.title() + ' ' + l_name.title()
                name_check = self.user_exist(b_mail, b_name, raw_data)
                if name_check == 1:
                    print(f'\nName <{b_name}> already exit!')
                    while True:
                        try:
                            opt = int(input("==>Press 1 to try another.\n==>Press 2 to login with this name."
                                            "\n==>Press 3 to go to main "
                                            "page.\n==>"))
                            if opt == 1:
                                break
                            elif opt == 2:
                                name = False
                                # self.login()
                                break
                            elif opt == 3:
                                self.client_menu()
                                break
                            else:
                                print("Wrong option. Please Try Again!")
                        except ValueError:
                            print("Press only Number!")
                else:
                    break

            while True:
                b_pass = input("%-30s: " % "Enter password to register")
                c_pass = input("%-30s: " % "Retype password again to confirm")
                if b_pass == c_pass:
                    break
                else:
                    print("Passwords do not match! Try again.")

            while True:
                try:
                    phone = int(input("%-30s: " % "Enter your phone"))
                    break
                except ValueError:
                    print("Fill only Numbers. please try again.")

            while True:
                try:
                    money = int(input("%-30s: $" % "Show your money"))
                    break
                except ValueError:
                    print("Fill only Numbers. please try again.")

            db = f"{raw_data}:{b_mail}:{b_name}:{b_pass}:{str(phone)}:{str(money)}"
            self.sending_encrypted(db)
            print("Registration Successes")

        except Exception as err:
            print(str(err))
        self.client_menu()

    def login(self, raw_data):
        print("\n" + "welcome to voter login page".upper().center(80))
        check = True
        try:
            while check:

                while True:
                    l_mail = input("%-30s: " % "Enter your Email to Login")
                    email_check = self.email_validation(l_mail)
                    if email_check == 1:
                        break
                    elif l_mail == "1":
                        self.client_menu()
                    else:
                        print("Mail you entered is Invalid! Please try again.")

                l_pass = input("Enter your password to login: ")

                sms = f"{raw_data}:{l_mail}:{l_pass}"

                flag = self.sending_encrypted(sms)

                if flag == 'Login Fail':
                    print("Email or Password is Invalid. Please Try Again! OR press (1) to exit.")
                    check = True

                else:
                    u_info_list = flag.split(':')
                    print(f"Hi {u_info_list[0]}, you are Logged in.")
                    self.u_profile(sms)
                    check = False

        except Exception as err:
            print(err)

    def u_profile(self, sms):

        updated_info_list = self.sending_encrypted(sms).split(":")
        name = updated_info_list[0]
        money = int(updated_info_list[1])

        print("\n" + "welcome to profile page".upper().center(80))
        print(f'Welcome {name} (Your money: ${money})')

        try:
            while True:
                opt = int(input(
                    "\nPress 1 to get Items and Floor Prices\nPress 2 to get money"
                    "\nPress 3 to transfer your money\nPress 4 to change your information"
                    "\nPress 5 to Delete account\nPress 6 to go Main Page\n==>"))
                if opt == 1:
                    self.info('info')
                elif opt == 2:
                    self.get_money(updated_info_list, sms)
                elif opt == 3:
                    self.transfer_money(updated_info_list, sms)
                elif opt == 4:
                    self.change_info(updated_info_list, sms)
                elif opt == 5:
                    self.acc_del(updated_info_list, sms)
                elif opt == 6:
                    self.client_menu()
                else:
                    print("Invalid Option! Please try again.")

        except ValueError:
            print("Invalid option! Press only Numbers.")

    def get_money(self, updated_info_list, sms):
        name = updated_info_list[0]
        money = int(updated_info_list[1])
        n_money = int(input("%-30s: " % "Enter amount of money you want to get: $"))

        up_m_sms = f"get_money:{name}:{n_money}"
        self.sending_encrypted(up_m_sms)
        print(f"Congratulation! Now you have: ${money}")
        self.u_profile(sms)

    def transfer_money(self, updated_info_list, sms):
        u_name = ""
        u_money = 0
        name = updated_info_list[0]
        money = int(updated_info_list[1])
        mail = updated_info_list[2]
        gud_sms = "get user data"
        from_server = self.sending_encrypted(gud_sms)
        udata_dict = json.loads(from_server)
        print("\n" + "welcome to transfer page".upper().center(80))
        print(f'Welcome {name} (Your money: {money})')
        for key, value in udata_dict.items():
            print(f'Name: {value["name"]} - Email: {value["mail"]} - Money: {value["money"]}')
        try:
            while True:
                mailchk = 0
                umail = input("Enter email you want to Transfer: ")
                if umail == mail:
                    print("You can't transfer your own account")
                else:
                    for key, value in udata_dict.items():
                        if value["mail"] == umail:
                            u_name = value["name"]
                            u_money = value["money"]
                            mailchk = 1
                            break
                    if mailchk == 1:
                        if money > 0:
                            print(f"\nName: {u_name} - Mail: {umail} - Money: {u_money}")

                            while True:
                                try:
                                    t_money = int(input("Enter amount of money you want to transfer: "))
                                    if t_money <= money:
                                        tf_sms = f'money_transfer:{money}:{t_money}:{name}:{u_name}'
                                        decrypted_list = self.sending_encrypted(tf_sms).split(":")
                                        money = decrypted_list[0]
                                        u_money = decrypted_list[1]
                                        print(
                                            f"Transfer Done!\n{u_name}'s money is ${u_money} "
                                            f"and Your money is ${money} now.")

                                        self.u_profile(sms)
                                        break
                                    else:
                                        print("You don't have enough point to transfer. Buy first!")
                                        self.u_profile(sms)
                                        break
                                except Exception as err:
                                    print(err, "\nEnter only Number!")

                        else:
                            print("You don't have any money to transfer. Buy first!")
                            self.u_profile(sms)
                    else:
                        print("Email you entered is Invalid! Please try again.")
        except Exception as err:
            print(err)

    def change_info(self, updated_info_list, sms):
        print("\nSelect to change your information.")
        n_mail = ""
        name = updated_info_list[0]
        mail = updated_info_list[2]
        password = updated_info_list[3]
        while True:
            try:
                opt = int(input(
                    "Press 1 to change your Email\nPress 2 to change your Name\nPress 3 to change your "
                    "Password\nPress 4 to go Back\n==>"))
                if opt == 1:
                    flag = True

                    while flag:
                        n_mail = input("Enter New email : ")
                        if n_mail == "1":
                            self.u_profile(sms)
                            break
                        email_check = self.email_validation(n_mail)

                        if email_check == 0:
                            print("Mail you entered is Invalid! Please try again <OR> Press 1 to cancel!")

                        else:

                            # break

                            n_name = "_"
                            mail_check = self.user_exist(n_mail, n_name, "Bidder_reg")

                            if mail_check == 1:
                                print(f'\nEmail <{n_mail}> already exit!')
                                while True:
                                    try:
                                        opt = int(input("==>Press 1 to try another.\n==>Press 2 to cancel\n==>"))

                                        if opt == 1:
                                            flag = True
                                            # self.change_info(updated_info_list, sms)
                                            break
                                        elif opt == 2:
                                            self.u_profile(sms)
                                            break
                                        else:
                                            print("Wrong option. Please Try Again!")
                                    except ValueError:
                                        print("Press only Number!")

                            else:
                                to_send = f"info_change:{name}:{n_mail}:{password}:{name}"
                                self.sending_encrypted(to_send)
                                print(f"Your new Email {n_mail} is updated!Login Back")
                                self.login("login")

                elif opt == 2:

                    while True:
                        f_name = input("%-30s: " % "Enter your First New Name")
                        l_name = input("%-30s: " % "Enter your Last New Name")
                        if l_name == "":
                            n_name = f_name.title()
                        else:
                            n_name = f_name.title() + ' ' + l_name.title()
                        name_check = self.user_exist(n_mail, n_name, "Bidder_reg")
                        if name_check == 1:
                            print(f'\nName <{n_name}> already exit!')
                            n_flag = True
                            while n_flag:
                                try:
                                    opt = int(input("==>Press 1 to try another.\n==>Press 2 to cancel\n==>"))

                                    if opt == 1:
                                        n_flag = True
                                        break
                                    elif opt == 2:
                                        self.u_profile(sms)
                                        break
                                    else:
                                        print("Wrong option. Please Try Again!")
                                except ValueError:
                                    print("Press only Number!")
                        else:
                            to_send = f"info_change:{n_name}:{mail}:{password}:{name}"
                            self.sending_encrypted(to_send)
                            print(f"Your new Name {n_name} is updated! Login back")
                            self.login("login")

                elif opt == 3:
                    while True:
                        u_pass = input("%-30s: " % "Enter password to change")
                        n_pass = input("%-30s: " % "Retype password again to confirm")
                        if u_pass == n_pass:
                            pass_check = f"pass_check:{n_pass}:{name}"
                            flag = self.sending_encrypted(pass_check)
                            if flag == "Same Password":
                                print("You Entered current password! Please enter a new password.")
                            else:
                                to_send = f"info_change:{name}:{mail}:{n_pass}:{name}"
                                self.sending_encrypted(to_send)
                                print(f"Your new Password {n_pass} is updated! Login back")
                                self.login("login")

                        else:
                            print("Passwords do not match! Try again.")

                elif opt == 4:
                    self.u_profile(sms)
                else:
                    print("Invalid Number! Choose again.")
            except Exception as err:
                print(err, "\nEnter only number!")

    def acc_del(self, updated_info_list, sms):
        upass = updated_info_list[3]
        while True:
            try:
                c_pass = input("Enter your password to confirm for deletion: ")
                if upass == c_pass:
                    name = f"Account_delete:{updated_info_list[0]}"
                    self.sending_encrypted(name)
                    print("Your account was successfully deleted")
                    self.client_menu()
                    break
                elif c_pass == "1":
                    self.u_profile(sms)
                else:
                    print("Invalid password! Please try again. <OR> Enter '1' to Quit.")
            except Exception as err:
                print(err)

    def email_validation(self, b_mail):
        j = -1
        mail_domain = ""
        mail_name = ""
        flag = -1
        while flag == -1:
            for i in range(len(b_mail)):
                if b_mail[i] == '@':
                    mail_name = b_mail[0:i]
                    mail_domain = b_mail[i + 1:]
                    j = 1
                    break
                else:
                    j = 0
            if j == 1 and len(mail_name) > 0:
                if mail_domain in ["gmail.com", "yahoo.com", "mail.ru", "outlook.com", "apple.com"]:
                    for char in mail_name:
                        n = ord(char)
                        if 31 < n < 48 or 57 < n < 64 or 90 < n < 97 or 122 < n < 127:
                            flag = 0
                            break

                        else:
                            flag = 1
                else:
                    flag = 0
            else:
                flag = 0

        if flag == 1:
            return flag
        else:
            return 0

    def user_exist(self, b_mail, b_name, raw_data):
        sms = f"{raw_data}:{b_mail}:{b_name}"
        flag = self.sending_encrypted(sms)
        if flag == "Email Already Existed" or flag == "Name Already Existed":
            return 1
        else:
            return 0


if __name__ == "__main__":
    auction_client: Auction_client = Auction_client()

    while True:
        auction_client.client_menu()
