import json
import random
import socket

import pymongo

connection = pymongo.MongoClient("localhost", 27017)
V_data = connection["v_db"]
col = V_data["candidates"]
col1 = V_data["users"]


class mongo_server:
    def __init__(self):
        server_ip = "localhost"
        server_port = 9996
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, server_port))
        server.listen()
        print(f"Server is listening on port: {server_port} and ip: {server_ip}")
        try:
            while True:
                client, address = server.accept()
                print(f"Connection Accepted from {address[0]}: {address[1]}>")
                self.client_choice(client)

        except Exception as err:
            print(err)

    def client_choice(self, sms_r):
        with sms_r as c_choice:
            client_input = c_choice.recv(1024)
            client_input = client_input.decode("utf-8").split(":")
            try:
                if len(client_input) > 0:
                    print("Received Data: ", client_input)
                    if client_input[0] == "gad":
                        self.get_all_data(c_choice)
                    elif client_input[0] == "ureg" or len(client_input) == 8:
                        loop = True
                        while loop:
                            if len(client_input) > 7:
                                self.u_register(client_input)
                                loop = False
                            elif len(client_input) == 3:
                                self.user_exist(c_choice, client_input)
                                loop = False
                            else:
                                print("Insufficient data for registration.")
                                loop = False
                    elif client_input[0] == "creg" or len(client_input) == 7:
                        loop = True
                        while loop:
                            if len(client_input) > 6:
                                self.c_register(client_input)
                                loop = False
                            elif len(client_input) == 3:
                                self.user_exist(c_choice, client_input)
                                loop = False
                            else:
                                print("Insufficient data for registration.")
                                loop = False
                    elif client_input[0] == "login":
                        self.login_check(c_choice, client_input)
                    elif client_input[0] == "clogin":
                        self.c_login_check(c_choice, client_input)
                    elif client_input[0] == "up":
                        self.user_update(client_input)
                    elif client_input[0] == "u_p_up":
                        self.user_point_update(client_input)
                    elif client_input[0] == "c_up":
                        self.c_money_update(client_input)
                    elif client_input[0] == "get_udata":
                        self.get_udata(c_choice, client_input)
                    elif client_input[0] == "info_change":
                        self.user_info_change(client_input)
                    elif client_input[0] == "get_cdata":
                        self.get_cdata(c_choice, client_input)
                    elif client_input[0] == "candi_up":
                        self.candidate_update(client_input)
                    elif client_input[0] == "get user data":
                        self.get_all_udata(c_choice)
                    elif client_input[0] == "passcheck":
                        self.pass_check(client_input, c_choice)
                    elif client_input[0] == "del":
                        self.deletion(client_input)
                    else:
                        print("Invalid choice.")
                        print(client_input)
                else:
                    print("Empty client input.")
            except Exception as err:
                print(err)
                self.client_choice(sms_r)

    def get_all_data(self, c_choice):
        data: dict = {}
        for i in col.find({}, {"_id": 1, "name": 1, "v_mark": 1, "v_points": 1, "voter": 1}):
            data_form = {"name": i["name"], "v_mark": i["v_mark"], "v_points": i["v_points"],
                         "voter": i["voter"]}
            data.update({i["_id"]: data_form})
        print(data)
        str_data = json.dumps(data)
        str_data = bytes(str_data, "utf-8")
        c_choice.send(str_data)

    def get_all_udata(self, c_choice):
        data: dict = {}
        _id = 0
        for i in col1.find({}, {"_id": 0, "name": 1, "mail": 1, "points": 1}):
            _id += 1
            data_form = {"name": i["name"], "mail": i["mail"], "points": i["points"]}
            data.update({_id: data_form})
        print(data)
        str_data = json.dumps(data)
        str_data = bytes(str_data, "utf-8")
        c_choice.send(str_data)

    def get_udata(self, c_choice, client_input):
        name = client_input[1]
        print(name)
        for i in col1.find({"name": name}, {"_id": 1, "mail": 1, "name": 1, "password": 1, "money": 1, "points": 1}):
            sms = f"{i['name']},{i['money']},{i['points']},{i['mail']},{i['password']}"
            str_data = bytes(sms, 'utf-8')
            print(str_data)
            c_choice.send(str_data)

    def get_cdata(self, c_choice, client_input):
        name = client_input[1]
        for i in col.find({"name": name}, {"_id": 1, "mail": 1, "name": 1, "password": 1, "money": 1, "v_points": 1}):
            sms = f"{i['name']},{i['money']},{i['v_points']}"
            str_data = bytes(sms, 'utf-8')
            c_choice.send(str_data)

    def c_register(self, client_input):

        c_id = [0]

        for i in col.find({}, {"_id": 1}):
            print(i["_id"])
            c_id.append(i["_id"])
            print(c_id)
        if c_id[-1] == 0:
            _id = 1
        else:
            _id = c_id[-1] + 1

        u_mail = client_input[0]
        u_name = client_input[1]
        u_pass = client_input[2]
        phone = client_input[3]
        age = client_input[4]
        mark = client_input[5]
        points = client_input[6]
        money = 0
        voter = []
        print(client_input)
        db = {"_id": _id, "mail": u_mail, "name": u_name, "password": u_pass, "phone": int(phone),
              "age": int(age), "v_mark": int(mark), "v_points": int(points), "money": int(money), "voter": voter}

        col.insert_one(db)

    def u_register(self, client_input):
        user_id = random.randint(10, 10000)
        u_mail = client_input[0]
        u_name = client_input[1]
        u_pass = client_input[2]
        address = client_input[3]
        phone = client_input[4]
        age = client_input[5]
        money = client_input[6]
        points = client_input[7]
        print(client_input)
        db = {"_id": user_id, "mail": u_mail, "name": u_name, "password": u_pass, "address": address,
              "phone": int(phone),
              "age": int(age), "money": int(money), "points": int(points)}

        col1.insert_one(db)

    def login_check(self, c_choice, client_input):
        print("login checking")
        l_email = client_input[1]
        l_password = client_input[2]
        flag = -1
        sms = ''
        name = ''
        for i in col1.find({}, {"_id": 0, "mail": 1, "name": 1, "password": 1, "money": 1, "points": 1}):
            if i["mail"] == l_email and i["password"] == l_password:
                print('user_found')
                name = f"{i['name']},{i['money']},{i['points']}"
                flag = 1
                break
            else:
                print('user_notfound')
                sms = '1'

        if flag == 1:
            str_data = bytes(name, 'utf-8')
            c_choice.send(str_data)

        else:
            str_data = bytes(sms, 'utf-8')
            c_choice.send(str_data)

    def c_login_check(self, c_choice, client_input):
        print("c_login checking")
        l_email = client_input[1]
        l_password = client_input[2]
        flag = -1
        sms = ''
        name = ''
        for i in col.find({}, {"_id": 0, "mail": 1, "name": 1, "password": 1, "money": 1, "v_points": 1}):
            if i["mail"] == l_email and i["password"] == l_password:
                print('user_found')
                name = f"{i['name']},{i['money']},{i['v_points']}"
                flag = 1
                break
            else:
                print('user_notfound')
                sms = '1'

        if flag == 1:
            str_data = bytes(name, 'utf-8')
            c_choice.send(str_data)

        else:
            str_data = bytes(sms, 'utf-8')
            c_choice.send(str_data)

    def user_update(self, client_input):
        n_money = client_input[1]
        n_points = client_input[2]
        name = client_input[3]
        col1.update_one({"name": name}, {"$set": {"money": int(n_money), "points": int(n_points)}})
        print("u_data updated")

    def user_point_update(self, client_input):
        points = client_input[1]
        upoints = client_input[2]
        name = client_input[3]
        u_name = client_input[4]
        col1.update_one({"name": name}, {"$set": {"points": int(points)}})
        col1.update_one({"name": u_name}, {"$set": {"points": int(upoints)}})

    def pass_check(self, client_input, c_choice):
        n_pass = client_input[1]
        name = client_input[2]
        flag = -1
        for i in col1.find({"name": name}, {"password": 1}):
            if i["password"] == n_pass:
                flag = 1
            else:
                flag = 0

        if flag == 1:
            str_data = bytes("1", 'utf-8')
            c_choice.send(str_data)

        else:
            str_data = bytes("0", 'utf-8')
            c_choice.send(str_data)

    def user_info_change(self, client_input):
        n_name = client_input[1]
        mail = client_input[2]
        password = client_input[3]
        name = client_input[4]
        print(name, mail, password)
        col1.update_one({"name": name}, {"$set": {"mail": mail, "name": n_name, "password": password}})

    def c_money_update(self, client_input):
        n_money = client_input[1]
        n_points = client_input[2]
        name = client_input[3]
        col.update_one({"name": name}, {"$set": {"money": int(n_money), "v_points": int(n_points)}})
        print("u_data updated")

    def candidate_update(self, client_input):
        v_mark = int(client_input[1])
        v_points = int(client_input[2])
        voter = client_input[3]
        v_id = int(client_input[4])
        col.update_one({"_id": v_id}, {"$set": {"v_mark": v_mark, "v_points": v_points}, "$push": {"voter": voter}})
        print("c_data updated")

    def user_exist(self, c_choice, client_input):
        print("testing user exit")
        u_email = client_input[1]
        u_name = client_input[2]
        flag = -1
        if col1.count_documents({}) == 0:
            str_data = bytes("0", 'utf-8')
            c_choice.send(str_data)
        else:
            try:
                for i in col1.find({}, {"_id": 0, "mail": 1, "name": 1}):
                    if i["mail"] == u_email or i["name"] == u_name:
                        flag = 1
                        break
                    else:
                        for j in col.find({}, {"_id": 0, "mail": 1, "name": 1}):
                            if j["mail"] == u_email or j["name"] == u_name:
                                flag = 1
                                break
                if flag == 1:
                    str_data = bytes("1", 'utf-8')
                    c_choice.send(str_data)
                else:
                    str_data = bytes("0", 'utf-8')
                    c_choice.send(str_data)
            except Exception as err:
                err = bytes(str(err), 'utf-8')
                c_choice.send(err)

    def deletion(self, client_input):
        name = client_input[1]
        col1.delete_one({"name":name})


if __name__ == "__main__":
    mongo_server()
