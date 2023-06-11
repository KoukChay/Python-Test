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
        print("==>Enter <gad> to get Candidates Ranks.\n==>Enter <reg> to Register\n==>Enter <login> to Login")
        sms = input("Enter your choice: ")
        try:
            if sms == "gad":
                self.ranked_list()
            elif sms == "reg":
                self.register(sms)
            elif sms == "login":
                self.login()
            else:
                print("Wrong option, Try again!")
        except Exception as err:
            print(err)
            self.check_input()

    def register(self, sms):
        u_name = '__'
        print("\n" + "welcome to registration page".upper().center(80))
        while True:
            u_mail = input("%-30s: " % "Enter your mail to register")

            if not u_mail.endswith("@gmail.com"):
                print("Mail must be @gmail.com! Please try again.")
                while True:
                    try:
                        opt = int(input("==>Press 1 to try another.\n==>Press 2 to go to main"
                                        "page.\n==>"))

                        if opt == 1:
                            self.register(sms)
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
                        self.register(sms)
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
        check = True
        try:
            while check:
                while True:
                    l_mail = input("%-30s: " % "Enter your Email to Login")
                    if l_mail.endswith("@gmail.com"):
                        break
                    elif l_mail == "1":
                        self.check_input()
                    else:
                        print("Mail must be @gmail.com! Please try again.")

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
                opt = int(input("Press 1 to buy points to vote\nPress 2 to vote\nPress 3 to go Main Page\n==>"))
                if opt == 1:
                    self.point_shop(r_data)
                elif opt == 2:
                    self.voting_page(r_data)
                elif opt == 3:
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
                        voter = candidate["voter"]
                        voter.append(name)
                        points -= 200
                        u_sms = f"up:{money}:{points}:{name}".encode('utf-8')
                        client = self.run_client()
                        client.send(u_sms)

                        sms = f"candi_up:{v_mark}:{v_points}:{voter}:{v_id}".encode('utf-8')
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
