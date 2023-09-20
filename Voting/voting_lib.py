class Voting:
    def __init__(self):

        print("this is a voting system".upper().center(80))
        self.students: dict = {0: {"name": "James", "v_mark": 0, "v_points": 0, "voter": []},
                               1: {"name": "John", "v_mark": 0, "v_points": 0, "voter": []},
                               2: {"name": "Rooney", "v_mark": 0, "v_points": 0, "voter": []},
                               3: {"name": "Ronaldo", "v_mark": 0, "v_points": 0, "voter": []},
                               4: {"name": "Messi", "v_mark": 0, "v_points": 0, "voter": []}}

        self.db: dict = {}
        self.id: int = 0
        self.l_id: int = 0
        self.load_data()
        self.record_data()

    def main_page(self):
        print("welcome to main page".upper().center(79))
        try:
            opt = int(input("Press 1 to Register\nPress 2 to Login\nPress 3 to Exit\n==>"))
            if opt == 1:
                self.registration_page()
            elif opt == 2:
                self.login_page()
            elif opt == 3:
                exit(1)
            else:
                print("Invalid Option! Try again.")
                self.main_page()
        except ValueError:
            print("Press only Number!")
            self.main_page()

    def registration_page(self):
        print("\n" + "welcome to registration page".upper().center(80))
        while True:
            u_mail = input("%-30s: " % "Enter your mail to register")
            if u_mail.endswith("@gmail.com"):
                break
            else:
                print("Mail must be @gmail.com! Please try again.")
                while True:
                    try:
                        opt = int(input(
                            "==>Press 1 to try another.\n==>Press 2 to go to main"
                            "page.\n==>"))

                        if opt == 1:
                            self.registration_page()
                        elif opt == 2:
                            self.main_page()
                        else:
                            print("Wrong option. Please Try Again!")
                    except ValueError:
                        print("Press only Number!")

        mail_check = self.user_exist(u_mail, name=None)

        if mail_check is not None:
            print(f'\nEmail <{u_mail}> already exit!')
            while True:
                try:
                    opt = int(input(
                        "==>Press 1 to try another.\n==>Press 2 to login with this Email.\n==>Press 3 to go to main "
                        "page.\n==>"))

                    if opt == 1:
                        self.registration_page()
                    elif opt == 2:
                        self.login_page()
                    elif opt == 3:
                        self.main_page()
                    else:
                        print("Wrong option. Please Try Again!")
                except ValueError:
                    print("Press only Number!")

        else:
            # global name
            name = True
            while name:
                f_name = input("%-30s: " % "Enter your First Name")
                l_name = input("%-30s: " % "Enter your Last Name")
                u_name = f_name.title() + ' ' + l_name.title()
                name_check = self.user_exist(mail=u_mail, name=u_name)
                if name_check is not None:
                    print(f'\nName <{u_name}> already exit!')
                    while True:
                        try:
                            opt = int(input(
                                "==>Press 1 to try another.\n==>Press 2 to login with this name."
                                "\n==>Press 3 to go to main "
                                "page.\n==>"))
                            if opt == 1:
                                break
                            elif opt == 2:
                                name = False
                                self.login_page()
                            elif opt == 3:
                                self.main_page()
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
            self.id = len(self.db)
            data_base = {self.id:
                             {"mail": u_mail, "name": u_name, "password": u_pass, "address": address, "phone": phone,
                              "age": age, "money": money, "points": points}}
            self.db.update(data_base)
            # voters.insert_one(data_base)
            self.record_data()
            print("Registration Success!\n".center(80))
            self.main_page()

    def login_page(self):
        print("\n" + "welcome to login page".upper().center(80))
        user_found = -1
        while True:
            l_mail = input("%-30s: " % "Enter your Email to Login")
            if l_mail.endswith("@gmail.com"):
                break
            else:
                print("Mail must be @gmail.com! Please try again.")

        for i in range(len(self.db)):
            if self.db[i]["mail"] == l_mail:
                user_found = i
                break

        if user_found == -1:
            print("User Not Found. You Should Register First!\n")
            self.main_page()

        l_pass = input("%-30s: " % "Enter your password to Login")
        while self.db[user_found]["mail"] == l_mail:
            if self.db[user_found]["password"] == l_pass:
                self.l_id = user_found
                self.profile_page(self.l_id)
                break
            else:
                while True:
                    opt = input("%-40s: " % "Password wrong. Try again!\n""%-10s" % "<OR>\nPress 1 to go Main Page")
                    if opt == "1":
                        self.main_page()
                        break
                    else:
                        l_pass = opt
                        break

    def profile_page(self, l_id):
        print("\n" + "welcome to profile page".upper().center(80))
        print(
            f'Welcome {self.db[l_id]["name"]} (Your money: ${self.db[l_id]["money"]},'
            f' Your points: {self.db[l_id]["points"]})')
        if self.db[l_id]["points"] < 200:
            print("You need at least 200 points to vote. Buy first!")
        try:
            opt = int(input("Press 1 to buy points to vote\nPress 2 to vote\nPress 3 to go Main Page\n==>"))
            if opt == 1:
                self.point_shop(l_id)
            elif opt == 2:
                self.voting_page(l_id)
            elif opt == 3:
                self.main_page()
            else:
                print("Invalid Option! Please try again.")
        except ValueError:
            print("Invalid option! Press only Numbers.")

    def voting_page(self, l_id):

        print("\n" + "voting list<1 vote = 200 points>".title().center(80))
        print(
            f'Welcome {self.db[l_id]["name"]} (Your money: ${self.db[l_id]["money"]},'
            f' Your points: {self.db[l_id]["points"]})')
        sorted_candidates = sorted(self.students.items(), key=lambda x: x[1]["v_mark"], reverse=True)
        for i in range(len(sorted_candidates)):
            print(
                f'ID: {i} - Name: {sorted_candidates[i][1]["name"]} - '
                f'Current Vote Mark: {sorted_candidates[i][1]["v_mark"]} - Voting Points: {sorted_candidates[i][1]["v_points"]}')

        while True:
            try:
                v_id = int(input("%-30s: " % "Enter an ID Number to vote"))
                vi_id = len(self.students)
                if self.db[l_id]["points"] < 200:
                    print(
                        "You don't have enough points to vote! You can buy by pressing 1 <OR> Press 2 to back to "
                        "Main page.")
                    while True:
                        try:
                            opt = int(input("==>"))
                            if opt == 1:
                                self.point_shop(l_id)
                            elif opt == 2:
                                self.main_page()
                            else:
                                print("Invalid option! Try again.")
                        except ValueError:
                            print("Press only Number!")

                else:
                    if v_id < vi_id:
                        sorted_candidates[v_id][1]["v_mark"] += 1
                        sorted_candidates[v_id][1]["v_points"] += 200
                        self.db[l_id]["points"] -= 200
                        sorted_candidates[v_id][1]["voter"].append(self.db[l_id]["name"])
                        self.students = dict(sorted_candidates)
                        self.record_data()
                        print(f'Thank Millions for you voting!\n{sorted_candidates[v_id][1]["name"]}'
                              f' now voting mark is < {sorted_candidates[v_id][1]["v_mark"]} > '
                              f'And voting point is < {sorted_candidates[v_id][1]["v_points"]} >')
                        for i in range(len(sorted_candidates[v_id][1]["voter"])):
                            print("Voter: ", sorted_candidates[v_id][1]["voter"][i])

                            while True:
                                try:
                                    vote_option = int(
                                        input(
                                            "Press 1 to Vote Again!\nPress 2 to get Main Page!\nPress 3 to Force Quit:"))
                                    if vote_option == 1:
                                        self.voting_page(l_id)
                                        break
                                    elif vote_option == 2:
                                        self.main_page()
                                        break
                                    elif vote_option == 3:
                                        exit(1)
                                    else:
                                        print("Invalid option after vote!")
                                except ValueError:
                                    print("Press only Number!")
                    else:
                        print("Choose correct ID!")
            except ValueError:
                print("Press only Number!")

    def point_shop(self, l_id):
        print("\n" + "welcome to point shop<1 point = $5>".upper().center(80))
        print(
            f'Welcome {self.db[l_id]["name"]} (Your money: ${self.db[l_id]["money"]},'
            f' Your points: {self.db[l_id]["points"]})')
        try:
            b_point = int(input("%-30s: " % "Enter amount of point you want to buy"))
            if self.db[l_id]["money"] >= (b_point * 5):
                self.db[l_id]["points"] += b_point
                self.db[l_id]["money"] -= (b_point * 5)
                print(f'Congratulation! You own now {self.db[l_id]["points"]} points')
                self.record_data()
                self.profile_page(l_id)
            else:
                while True:
                    opt = input("Not enough money to buy point. Do you want to Refill money? (y/n)".lower())
                    if opt == 'y':
                        n_money = int(input("%-30s: " % "Please refill you money: $"))
                        self.db[l_id]["money"] += n_money
                        self.record_data()
                        self.point_shop(l_id)
                        break
                    elif opt == 'n':
                        self.point_shop(l_id)
                        break
                    else:
                        print("Invalid Option! Please enter 'y' or 'n'")
        except ValueError:
            print("Amount must be only Numbers!")

    def user_exist(self, mail, name):
        length = len(self.db)
        for i in range(length):
            if self.db[i]["mail"] == mail or self.db[i]["name"] == name:
                return i

    def record_data(self):

        with open("data.txt", "w") as f:

            f.write("students:\n")
            for key, value in self.students.items():
                f.write(f"{key}:{value}\n")

            f.write("db:\n")
            for key, value in self.db.items():
                f.write(f"{key}:{value}\n")

    def load_data(self):
        try:
            with open("data.txt", "r") as f:
                current_dict = None
                students = {}
                db = {}

                for line in f:
                    line = line.strip()

                    if line == "students:":
                        current_dict = students
                    elif line == "db:":
                        current_dict = db
                    elif line:
                        key, value = line.split(":", 1)
                        current_dict[int(key)] = eval(value)

                self.students = students
                self.db = db

        except FileNotFoundError:
            self.students = {}
            self.db = {}
