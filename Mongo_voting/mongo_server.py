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
                    print("Received Data: ", client_input[0])
                    if client_input[0] == "gad":
                        self.get_all_data(c_choice)
                    elif client_input[0] == "reg" or len(client_input) == 8:
                        loop = True
                        while loop:
                            if len(client_input) > 7:
                                self.register(client_input)
                                loop = False
                            elif len(client_input) == 3:
                                self.user_exist(c_choice, client_input)
                                loop = False
                            else:
                                print("Insufficient data for registration.")
                                loop = False
                    elif client_input[0] == "login":
                        self.login_check(c_choice, client_input)
                    elif client_input[0] == "up":
                        self.user_update(client_input)
                    elif client_input[0] == "get_udata":
                        self.get_udata(c_choice, client_input)
                    elif client_input[0] == "candi_up":
                        self.candidate_update(client_input)
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
        for i in col.find({}, {"_id": 0, "name": 1, "v_mark": 1, "v_points": 1, "voter": 1}):
            _id = len(data) + 1
            data_form = {"name": i.get("name"), "v_mark": i.get("v_mark"), "v_points": i.get("v_points"),
                         "voter": i.get("voter")}
            data.update({_id: data_form})
        print(data)
        str_data = json.dumps(data)
        str_data = bytes(str_data, "utf-8")
        c_choice.send(str_data)

    def get_udata(self, c_choice, client_input):
        name = client_input[1]
        for i in col1.find({"name": name}, {"_id": 1, "mail": 1, "name": 1, "password": 1, "money": 1, "points": 1}):
            sms = f"{i['name']},{i['money']},{i['points']}"
            str_data = bytes(sms, 'utf-8')
            c_choice.send(str_data)

    def register(self, client_input):
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
        db = {"_id": user_id, "mail": u_mail, "name": u_name, "password": u_pass, "address": address, "phone": phone,
              "age": age, "money": money, "points": points}

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

    def user_update(self, client_input):
        n_money = client_input[1]
        n_points = client_input[2]
        name = client_input[3]
        col1.update_one({"name": name}, {"$set": {"money": n_money, "points": n_points}})
        print("u_data updated")

    def candidate_update(self, client_input):
        v_mark = int(client_input[1])
        v_points = int(client_input[2])
        voter = client_input[3]
        voter = eval(voter)
        v_id = int(client_input[4])
        col.update_one({"_id": v_id}, {"$set": {"v_mark": v_mark, "v_points": v_points, "voter": voter}})
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
                if flag == 1:
                    str_data = bytes("1", 'utf-8')
                    c_choice.send(str_data)
                else:
                    str_data = bytes("0", 'utf-8')
                    c_choice.send(str_data)
            except Exception as err:
                err = bytes(str(err), 'utf-8')
                c_choice.send(err)


if __name__ == "__main__":
    mongo_server()
