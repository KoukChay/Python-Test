import json
import socket


class mongo_client:
    def __init__(self):
        self.target_ip = "localhost"
        self.target_port = 9996

    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client

    def check_input(self):
        print(
            "==>Enter <gad> to get Candidates Ranks.\n==>Enter <ureg> for User Register\n==>Enter <creg> for "
            "Candidate Register\n==>Enter <login> to Login as voter\n==>Enter <clogin> to Login as candidate")
        sms = input("Enter your choice: ")
        try:
            if sms == "gad":
                self.ranked_list()
            elif sms == "ureg":
                self.u_register(sms)
            elif sms == "creg":
                self.c_register(sms)
            elif sms == "login":
                self.login()
            elif sms == "clogin":
                self.candidate_login()
            else:
                print("Wrong option, Try again!")
        except Exception as err:
            print(err)
            self.check_input()

    def c_register(self, sms):
        c_name = '__'
        print("\n" + "welcome to candidate registration page".upper().center(80))
        while True:
            c_mail = input("%-30s: " % "Enter your mail to register")
            email_check = self.email_validation(c_mail)

            if email_check == 0:
                print("Mail you entered is Invalid! Please try again.")
                while True:
                    try:
                        opt = int(input("==>Press 1 to try another.\n==>Press 2 to go to main"
                                        "page.\n==>"))

                        if opt == 1:
                            self.c_register(sms)
                            break
                        elif opt == 2:
                            self.check_input()
                            return
                        else:
                            print("Wrong option. Please Try Again!")
                    except ValueError:
                        print("Press only Number!")
            else:
                break

        mail_check = self.user_exist(c_mail, c_name, sms)
        if mail_check is not None:
            print(f'\nEmail <{c_mail}> already exit!')

            while True:
                try:
                    opt = int(input(
                        "==>Press 1 to try another.\n==>Press 2 to login with this Email.\n==>Press 3 to go to main "
                        "page.\n==>"))

                    if opt == 1:
                        self.c_register(sms)
                        break
                    elif opt == 2:
                        self.login()
                        break
                    elif opt == 3:
                        self.check_input()
                        break
                    else:
                        print("Wrong option. Please Try Again!")
                except ValueError:
                    print("Press only Number!")

        else:

            name = True
            while name:
                f_name = input("%-30s: " % "Enter your First Name")
                l_name = input("%-30s: " % "Enter your Last Name")
                c_name = f_name.title() + ' ' + l_name.title()
                name_check = self.user_exist(c_mail, c_name, sms)
                if name_check is not None:
                    print(f'\nName <{c_name}> already exit!')
                    while True:
                        try:
                            opt = int(input("==>Press 1 to try another.\n==>Press 2 to login with this name."
                                            "\n==>Press 3 to go to main "
                                            "page.\n==>"))
                            if opt == 1:
                                break
                            elif opt == 2:
                                name = False
                                self.login()
                                break
                            elif opt == 3:
                                self.check_input()
                                break
                            else:
                                print("Wrong option. Please Try Again!")
                        except ValueError:
                            print("Press only Number!")
                else:
                    break

            while True:
                u_pass = input("%-30s: " % "Enter password to register")
                c_pass = input("%-30s: " % "Retype password again to confirm")
                if u_pass == c_pass:
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
                    age = int(input("%-30s: " % "Enter your age(Must be 18+)"))
                    if age >= 18:
                        break
                    else:
                        print("Age must be 18 and over.")
                except ValueError:
                    print("Age must be only Numbers. Please try again.")

            mark = 0
            points = 0
            db = c_mail + ':' + c_name + ':' + u_pass + ':' + str(phone) + ':' + str(age) + ':' + str(
                mark) + ':' + str(points)

            db = bytes(db, "utf-8")
            client = self.run_client()
            client.send(db)
            print("Registration Success!\n".center(80))
            client.close()
            self.check_input()

    def u_register(self, sms):
        u_name = '__'
        print("\n" + "welcome to voter registration page".upper().center(80))
        while True:
            u_mail = input("%-30s: " % "Enter your mail to register")
            email_check = self.email_validation(u_mail)

            if email_check == 0:
                print("Mail you entered is Invalid! Please try again.")
                while True:
                    try:
                        opt = int(input("==>Press 1 to try another.\n==>Press 2 to go to main"
                                        "page.\n==>"))

                        if opt == 1:
                            self.u_register(sms)
                            break
                        elif opt == 2:
                            self.check_input()
                            return
                        else:
                            print("Wrong option. Please Try Again!")
                    except ValueError:
                        print("Press only Number!")
            else:

                break

        mail_check = self.user_exist(u_mail, u_name, sms)

        if mail_check is not None:
            print(f'\nEmail <{u_mail}> already exit!')
            while True:
                try:
                    opt = int(input(
                        "==>Press 1 to try another.\n==>Press 2 to login with this Email.\n==>Press 3 to go to main "
                        "page.\n==>"))

                    if opt == 1:
                        self.u_register(sms)
                        break
                    elif opt == 2:
                        self.login()
                        break
                    elif opt == 3:
                        self.check_input()
                        break
                    else:
                        print("Wrong option. Please Try Again!")
                except ValueError:
                    print("Press only Number!")

        else:

            name = True
            while name:
                f_name = input("%-30s: " % "Enter your First Name")
                l_name = input("%-30s: " % "Enter your Last Name")
                u_name = f_name.title() + ' ' + l_name.title()
                name_check = self.user_exist(u_mail, u_name, sms)
                if name_check is not None:
                    print(f'\nName <{u_name}> already exit!')
                    while True:
                        try:
                            opt = int(input("==>Press 1 to try another.\n==>Press 2 to login with this name."
                                            "\n==>Press 3 to go to main "
                                            "page.\n==>"))
                            if opt == 1:
                                break
                            elif opt == 2:
                                name = False
                                self.login()
                                break
                            elif opt == 3:
                                self.check_input()
                                break
                            else:
                                print("Wrong option. Please Try Again!")
                        except ValueError:
                            print("Press only Number!")
                else:
                    break

            while True:
                u_pass = input("%-30s: " % "Enter password to register")
                c_pass = input("%-30s: " % "Retype password again to confirm")
                if u_pass == c_pass:
                    break
                else:
                    print("Passwords do not match! Try again.")

            address = input("%-30s: " % "Enter your address")
            while True:
                try:
                    phone = int(input("%-30s: " % "Enter your phone"))
                    break
                except ValueError:
                    print("Fill only Numbers. please try again.")
            while True:
                try:
                    age = int(input("%-30s: " % "Enter your age(Must be 18+)"))
                    if age >= 18:
                        break
                    else:
                        print("Age must be 18 and over.")
                except ValueError:
                    print("Age must be only Numbers. Please try again.")

            while True:
                try:
                    money = int(input("%-30s: $" % "Show your money"))
                    break
                except ValueError:
                    print("Fill only Numbers. please try again.")
            points = 0
            db = u_mail + ':' + u_name + ':' + u_pass + ':' + address + ':' + str(phone) + ':' + str(age) + ':' + str(
                money) + ':' + str(points)

            db = bytes(db, "utf-8")
            client = self.run_client()
            client.send(db)
            print("Registration Success!\n".center(80))
            client.close()
        self.check_input()

    def login(self):
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
                        self.check_input()
                    else:
                        print("Mail you entered is Invalid! Please try again.")

                l_pass = input("Enter your password to login: ")
                client = self.run_client()
                sms = f"login:{l_mail}:{l_pass}".encode('utf-8')
                client.send(sms)
                r_data = client.recv(1024).decode("utf-8").split(",")

                if r_data[0] == '1':
                    print("Email or Password is Invalid. Please Try Again! OR press (1) to exit.")
                    check = True

                else:

                    self.profile_page(r_data)

                client.close()
        except Exception as err:
            print(err)
        self.check_input()

    def candidate_login(self):
        print("\n" + "welcome to candidate login page".upper().center(80))
        check = True
        try:
            while check:
                while True:
                    l_mail = input("%-30s: " % "Enter your Email to Login")
                    email_check = self.email_validation(l_mail)
                    if email_check == 1:
                        break
                    elif l_mail == "1":
                        self.check_input()
                    else:
                        print("Mail you entered is Invalid! Please try again.")

                l_pass = input("Enter your password to login: ")
                client = self.run_client()
                sms = f"clogin:{l_mail}:{l_pass}".encode('utf-8')
                client.send(sms)
                r_data = client.recv(1024).decode("utf-8").split(",")

                if r_data[0] == '1':
                    print("Email or Password is Invalid. Please Try Again! OR press (1) to exit.")
                    check = True

                else:

                    self.candidate_profile_page(r_data)

                client.close()
        except Exception as err:
            print(err)
        self.check_input()

    def candidate_profile_page(self, r_data):
        name = r_data[0]
        client = self.run_client()
        sms = f"get_cdata:{name}".encode('utf-8')
        client.send(sms)
        n_data = client.recv(1024).decode("utf-8").split(",")

        money = int(n_data[1])
        points = int(n_data[2])
        print("\n" + "welcome to profile page".upper().center(80))
        print(f'Welcome {name} (Your money: ${money},'
              f' Your points: {points})')
        try:
            c_points = int(input("%-30s: " % "Enter amount of point you want to change<1point = $5>"))
            if points >= c_points:
                points -= c_points
                money += (c_points * 5)
                print(f'Congratulation! You have changed ${c_points*5} and You totally own ${money} now.')

                sms = f"c_up:{money}:{points}:{name}".encode('utf-8')
                client = self.run_client()
                client.send(sms)
                try:
                    while True:
                        opt = int(input("Press <1> to change more.\nPress <2> to go Main page.\n==>"))
                        if opt == 1:
                            self.candidate_profile_page(r_data)
                            break
                        elif opt == 2:
                            self.check_input()
                            break
                        else:
                            print("Invalid Option! Please try again.")

                except ValueError:
                    print("Invalid option! Press only Numbers.")

            else:
                print("Not enough points to change money.")
                self.check_input()
        except ValueError:
            print("Amount must be only Numbers!")

    def profile_page(self, r_data):
        name = r_data[0]
        client = self.run_client()
        sms = f"get_udata:{name}".encode('utf-8')
        client.send(sms)
        n_data = client.recv(1024).decode("utf-8").split(",")

        money = int(n_data[1])
        points = int(n_data[2])
        print("\n" + "welcome to profile page".upper().center(80))
        print(f'Welcome {name} (Your money: ${money},'
              f' Your points: {points})')
        if points < 200:
            print("You need at least 200 points to vote. Buy first!")
        try:
            while True:
                opt = int(input(
                    "Press 1 to buy points to vote\nPress 2 to vote\nPress 3 to transfer your points\nPress 4 to "
                    "change your information\nPress 5 to Delete account\nPress 6 to go Main Page\n==>"))
                if opt == 1:
                    self.point_shop(r_data)
                elif opt == 2:
                    self.voting_page(r_data)
                elif opt == 3:
                    self.transfer_point(r_data, n_data)
                elif opt == 4:
                    self.change_info(sms, r_data, n_data)
                elif opt == 5:
                    self.acc_del(n_data,r_data)
                elif opt == 6:
                    self.check_input()
                else:
                    print("Invalid Option! Please try again.")

        except ValueError:
            print("Invalid option! Press only Numbers.")

    def voting_page(self, r_data):
        name = r_data[0]
        client = self.run_client()
        sms = f"get_udata:{name}".encode('utf-8')
        client.send(sms)
        n_data = client.recv(1024).decode("utf-8").split(",")
        money = int(n_data[1])
        points = int(n_data[2])
        print("\n" + "voting list<1 vote = 200 points>".title().center(80))
        client = self.run_client()
        gad = f"gad".encode("utf-8")
        client.send(gad)
        from_server = client.recv(1024)
        data_dict = json.loads(from_server.decode('utf-8'))
        print(f'Welcome {name} (Your money: ${str(money)},'
              f' Your points: {str(points)})')
        for key, value in data_dict.items():
            print(f'ID: {key} - Name: {value["name"]} - '
                  f'Current Vote Mark: {value["v_mark"]} - Voting Points: {value["v_points"]}')

        while True:
            try:
                v_id = int(input("%-30s: " % "Enter an ID Number to vote"))
                vi_id = len(data_dict) + 1

                if points < 200:
                    print("You don't have enough points to vote! You can buy by pressing 1 <OR> Press 2 to back to "
                          "Main page.")
                    while True:
                        try:
                            opt = int(input("==>"))
                            if opt == 1:
                                self.point_shop(r_data)
                            elif opt == 2:
                                self.check_input()
                            else:
                                print("Invalid option! Try again.")
                        except ValueError:
                            print("Press only Number!")

                else:
                    if 0 < v_id < vi_id:

                        candidate = data_dict[str(v_id)]
                        candidate["v_mark"] += 1
                        v_mark = candidate["v_mark"]
                        candidate["v_points"] += 200
                        v_points = candidate["v_points"]
                        points -= 200
                        u_sms = f"up:{money}:{points}:{name}".encode('utf-8')
                        client = self.run_client()
                        client.send(u_sms)

                        sms = f"candi_up:{v_mark}:{v_points}:{name}:{v_id}".encode('utf-8')
                        client = self.run_client()
                        client.send(sms)

                        print(f'Thank you for your vote!\n{name} has voted for {candidate["name"]}. '
                              f'The candidate now has a voting mark of {v_mark} '
                              f'and voting points of {v_points}')

                        print("Voter: ", name)
                        self.profile_page(r_data)

                    else:
                        print("Choose correct ID!")
            except Exception as err:
                print(err)

    def point_shop(self, r_data):
        name = r_data[0]
        client = self.run_client()
        sms = f"get_udata:{name}".encode('utf-8')
        client.send(sms)
        n_data = client.recv(1024).decode("utf-8").split(",")

        money = int(n_data[1])
        points = int(n_data[2])
        print("\n" + "welcome to point shop<1 point = $5>".upper().center(80))
        print(f'Welcome {name} (Your money: ${money},'
              f' Your points: {points})')
        try:
            b_point = int(input("%-30s: " % "Enter amount of point you want to buy"))
            if money >= (b_point * 5):
                points += b_point
                money -= (b_point * 5)
                print(f'Congratulation! You own now {points} points')

                sms = f"up:{money}:{points}:{name}".encode('utf-8')
                client = self.run_client()
                client.send(sms)
                self.profile_page(r_data)
            else:
                while True:
                    opt = input("Not enough money to buy point. Do you want to Refill money? (y/n)".lower())
                    if opt == 'y':
                        n_money = int(input("%-30s: " % "Please refill you money: $"))
                        money += n_money
                        sms = f"up:{money}:{points}:{name}".encode('utf-8')
                        client = self.run_client()
                        client.send(sms)
                        self.point_shop(r_data)
                        break
                    elif opt == 'n':
                        self.profile_page(r_data)
                        break
                    else:
                        print("Invalid Option! Please enter 'y' or 'n'")
        except ValueError:
            print("Amount must be only Numbers!")

    def transfer_point(self, r_data, n_data):
        global u_name, u_points
        print(r_data)
        name = r_data[0]
        points = int(n_data[2])
        mail = n_data[3]
        client = self.run_client()
        sms = f"get user data".encode("utf-8")
        client.send(sms)
        from_server = client.recv(1024)
        udata_dict = json.loads(from_server.decode('utf-8'))
        print("\n" + "welcome to transfer page".upper().center(80))
        print(f'Welcome {name} (Your points: {points})')
        for key, value in udata_dict.items():
            print(f'Name: {value["name"]} - Email: {value["mail"]} - Voting Points: {value["points"]}')
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
                            u_points = value["points"]
                            mailchk = 1
                            break
                    if mailchk == 1:
                        if points > 0:
                            print(f"\nName: {u_name} - Mail: {umail} - Points: {u_points}")

                            while True:
                                try:
                                    t_point = int(input("Enter amount of point you want to transfer: "))
                                    if t_point <= points:
                                        u_points += t_point
                                        points -= t_point
                                        print(
                                            f"Transfer Done!\n{u_name}'s point is {u_points} and Your point is {points} now")
                                        sms = f'u_p_up:{points}:{u_points}:{name}:{u_name}'.encode('utf-8')
                                        client = self.run_client()
                                        client.send(sms)
                                        self.profile_page(r_data)
                                        break
                                    else:
                                        print("You don't have enough point to transfer. Buy first!")
                                        self.profile_page(r_data)
                                        break
                                except Exception as err:
                                    print(err, "\nEnter only Number!")

                        else:
                            print("You don't have any points to transfer. Buy first!")
                            self.profile_page(r_data)
                    else:
                        print("Email you entered is Invalid! Please try again.")
        except Exception as err:
            print(err)
        client.close()

    def change_info(self, sms, r_data, n_data):
        print("\nSelect to change your information.")
        name = n_data[0]
        mail = n_data[3]
        password = n_data[4]
        while True:
            try:
                opt = int(input(
                    "Press 1 to change your Email\nPress 2 to change your Name\nPress 3 to change your "
                    "Password\nPress 4 to go Back\n==>"))
                if opt == 1:

                    while True:
                        n_mail = input("Enter New email : ")
                        if n_mail == "1":
                            self.profile_page(r_data)
                            break
                        email_check = self.email_validation(n_mail)

                        if email_check == 0:
                            print("Mail you entered is Invalid! Please try again <OR> Press 1 to cancel!")

                        else:

                            break

                    mail_check = self.user_exist(n_mail, None, sms="ureg")

                    if mail_check is not None:
                        print(f'\nEmail <{n_mail}> already exit!')
                        while True:
                            try:
                                opt = int(input("==>Press 1 to try another.\n==>Press 2 to cancel\n==>"))

                                if opt == 1:
                                    self.change_info(sms, r_data, n_data)
                                    break
                                elif opt == 2:
                                    self.profile_page(r_data)
                                    break
                                else:
                                    print("Wrong option. Please Try Again!")
                            except ValueError:
                                print("Press only Number!")

                    else:
                        tosend = f"info_change:{name}:{n_mail}:{password}:{name}".encode('utf-8')
                        client = self.run_client()
                        client.send(tosend)
                        print(f"Your new Email {n_mail} is updated!Login Back")
                        self.login()

                elif opt == 2:

                    while True:
                        f_name = input("%-30s: " % "Enter your First New Name")
                        l_name = input("%-30s: " % "Enter your Last New Name")
                        n_name = f_name.title() + ' ' + l_name.title()
                        name_check = self.user_exist(None, n_name, sms="ureg")
                        if name_check is not None:
                            print(f'\nName <{n_name}> already exit!')
                            while True:
                                try:
                                    opt = int(input("==>Press 1 to try another.\n==>Press 2 to cancel\n==>"))

                                    if opt == 1:
                                        self.change_info(sms, r_data, n_data)
                                        break
                                    elif opt == 2:
                                        self.profile_page(r_data)
                                        break
                                    else:
                                        print("Wrong option. Please Try Again!")
                                except ValueError:
                                    print("Press only Number!")
                        else:
                            tosend = f"info_change:{n_name}:{mail}:{password}:{name}".encode('utf-8')
                            client = self.run_client()
                            client.send(tosend)
                            print(f"Your new Name {n_name} is updated! Login back")
                            self.login()

                elif opt == 3:
                    while True:
                        u_pass = input("%-30s: " % "Enter password to register")
                        n_pass = input("%-30s: " % "Retype password again to confirm")
                        if u_pass == n_pass:
                            passcheck = bytes(f"passcheck:{n_pass}:{name}", "utf-8")
                            client = self.run_client()
                            client.send(passcheck)
                            flag = client.recv(1024).decode("utf-8")
                            if flag == "1":
                                print("You Entered current password! Please enter a new password.")
                            else:
                                tosend = f"info_change:{name}:{mail}:{n_pass}:{name}".encode('utf-8')
                                client = self.run_client()
                                client.send(tosend)
                                print(f"Your new Password {n_pass} is updated! Login back")
                                self.login()

                        else:
                            print("Passwords do not match! Try again.")

                elif opt == 4:
                    self.profile_page(r_data)
                else:
                    print("Invalid Number! Choose again.")
            except Exception as err:
                print(err, "\nEnter only number!")

    def acc_del(self,n_data,r_data):
        upass = n_data[4]
        while True:
            try:
                c_pass = input("Enter your password to confirm for deletion!")
                if upass == c_pass:
                    name = f"del:{n_data[0]}".encode('utf-8')
                    client = self.run_client()
                    client.send(name)
                    print("Your account was successfully deleted")
                    self.check_input()
                    break
                elif c_pass == "q":
                    self.profile_page(r_data)
                else:
                    print("Invalid password! Please try again. <OR> Enter 'q' to Quit.")
            except Exception as err:
                print(err)


    def email_validation(self, u_mail):
        global domain, mail_name, j
        length = len(u_mail)
        flag = -1
        d_flag = -1
        while flag == -1:

            for i in range(length):
                if u_mail[i] == '@':
                    mail_name = u_mail[0:i]
                    domain = u_mail[i + 1:]
                    j = 1
                    break
                else:
                    j = 0
            if j == 1:
                if domain in ["gmail.com", "yahoo.com", "mail.ru", "outlook.com", "apple.com"]:
                    d_flag = 1
                else:
                    d_flag = 0

                for char in mail_name:
                    n = ord(char)
                    if 31 < n < 48 or 57 < n < 64 or 90 < n < 97 or 122 < n < 127:
                        flag = 0
                        break
                    else:
                        flag = 1
            else:
                flag = 0

        if flag == 1 and d_flag == 1:
            return 1
        else:
            return 0

    def user_exist(self, u_mail, u_name, sms):
        client = self.run_client()
        try:
            sms = f"{sms}:{u_mail}:{u_name}".encode("utf-8")
            client.send(sms)

            received_from_server = client.recv(1024).decode("utf-8")

            if received_from_server == "1":
                return u_mail, u_name
            else:
                return None

        except Exception as err:
            print(err)
            self.user_exist(u_mail, u_name, sms)
        client.close()

    def ranked_list(self):
        client = self.run_client()
        gad = f"gad".encode("utf-8")
        client.send(gad)
        from_server = client.recv(1024)
        data_dict = json.loads(from_server.decode('utf-8'))

        sorted_candidates = sorted(data_dict.items(), key=lambda x: x[1]["v_mark"], reverse=True)

        for i in range(len(sorted_candidates)):
            print(f'ID: {i + 1} - Name: {sorted_candidates[i][1]["name"]} - '
                  f'Current Vote Mark: {sorted_candidates[i][1]["v_mark"]} - '
                  f'Voting Points: {sorted_candidates[i][1]["v_points"]} - '
                  f'Voters: {sorted_candidates[i][1]["voter"]}')
        self.check_input()


if __name__ == "__main__":
    while True:
        client_r = mongo_client()
        client_r.check_input()
