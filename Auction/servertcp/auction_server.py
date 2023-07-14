import json
import random
import socket

import ob
import s_encrypt_and_decrypt
from DBModel import AuctionModel


class Server:

    def __init__(self):

        self.decrypt = s_encrypt_and_decrypt.A3Decryption()
        self.encrypt = s_encrypt_and_decrypt.A3Encryption()
        self.server_ip = "localhost"
        self.server_port = 9190
        self.DB: DB_call = DB_call()
        self.ob = ob.Ob()

    def main(self):

        auction_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auction_server.bind((self.server_ip, self.server_port))

        auction_server.listen()

        print("\nServer listen on port: {} and ip: {}".format(self.server_port, self.server_ip))

        try:
            while True:
                client, address = auction_server.accept()
                print("\nAccepted Connection from - {} : {}".format(address[0], address[1]))

                self.client_control(client)

        except Exception as err:
            print(err)

    def client_control(self, client):

        with client as sock:

            from_client = sock.recv(1024)

            data_list = from_client.decode("utf-8")

            decrypted = self.decrypt.startDecryption(data_list)
            print("\nReceived From Client :", decrypted)
            decrypted_list = decrypted.split(':')
            self.ob.get_received(decrypted_list)
            collection = self.DB.AuctModel.User_req()
            collection.insert_one({"User Request": decrypted_list[0]})

            if decrypted_list[0] == 'info':

                data_dict = self.DB.info()
                data_str = json.dumps(data_dict)
                encrypted = self.encrypt.start_encryption(data_str, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(data_str)

            elif decrypted_list[0] == "Bidder_reg" or len(decrypted_list) == 6:

                if len(decrypted_list) > 5:

                    ob_sent = self.DB.b_register(decrypted_list)
                    encrypted = self.encrypt.start_encryption(ob_sent, 'server_key')
                    sock.send(bytes(encrypted, "utf-8"))
                    self.ob.send_data(ob_sent)

                elif len(decrypted_list) == 3:
                    flag = self.DB.user_exit(decrypted_list)
                    encrypted = self.encrypt.start_encryption(flag, 'server_key')
                    sock.send(bytes(encrypted, "utf-8"))
                    self.ob.send_data(flag)
                else:

                    print("Insufficient data for registration.")

            elif decrypted_list[0] == 'login':
                data_str = self.DB.login(decrypted_list)
                encrypted = self.encrypt.start_encryption(data_str, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(data_str)

            elif decrypted_list[0] == 'get_money':
                data_str = self.DB.m_up(decrypted_list)
                encrypted = self.encrypt.start_encryption(data_str, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(data_str)

            elif decrypted_list[0] == "get user data":
                data_dict = self.DB.get_udata()
                data_str = json.dumps(data_dict)
                encrypted = self.encrypt.start_encryption(data_str, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(data_str)

            elif decrypted_list[0] == "money_transfer":
                data_str = self.DB.user_money_update(decrypted_list)
                encrypted = self.encrypt.start_encryption(data_str, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(data_str)
                # data_list = data_str.split(":")
                # t_money = data_list[2]
                # u_name = data_list[3]
                # name = data_list[4]
                # self.ob.send_data(f"{name} transferred ${t_money} to {u_name}")

            elif decrypted_list[0] == "info_change":
                data_str = self.DB.user_info_change(decrypted_list)
                encrypted = self.encrypt.start_encryption(data_str, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(data_str)

            elif decrypted_list[0] == "pass_check":
                flag = self.DB.pass_check(decrypted_list)
                encrypted = self.encrypt.start_encryption(flag, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(flag)

            elif decrypted_list[0] == "Account_delete":
                respond = self.DB.Acc_deletion(decrypted_list)
                encrypted = self.encrypt.start_encryption(respond, 'server_key')
                sock.send(bytes(encrypted, "utf-8"))
                self.ob.send_data(respond)


class DB_call:
    def __init__(self):
        self.AuctModel = AuctionModel()

    def info(self):
        collection = self.AuctModel.item_Price()
        data_dict = {}
        for i in collection.find({}, {"_id": 1, "Item": 1, "Price": 1}):
            data = {i["_id"]: {"Item": i["Item"], "Price": i["Price"]}}
            data_dict.update(data)
        return data_dict

    def b_register(self, decrypted_list):
        b_id = random.randint(1, 100)
        collection = self.AuctModel.Bidder()
        b_mail = decrypted_list[1]
        b_name = decrypted_list[2]
        b_pass = decrypted_list[3]
        phone = decrypted_list[4]
        money = decrypted_list[5]
        n_bidder = {"_id": b_id, "mail": b_mail, "name": b_name, "pass": b_pass, "phone": int(phone),
                    "money": int(money)}
        collection.insert_one(n_bidder)
        return "New Bidder Registered!"

    def login(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        l_mail = decrypted_list[1]
        l_pass = decrypted_list[2]
        for i in collection.find({}, {"_id": 1, "mail": 1, "pass": 1, "name": 1, "money": 1}):
            if i["mail"] == l_mail and i["pass"] == l_pass:
                return f'{i["name"]}:{i["money"]}:{i["mail"]}:{i["pass"]}'
        return "Login Fail"

    def m_up(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        b_name = decrypted_list[1]
        n_money = int(decrypted_list[2])
        for i in collection.find({"name": b_name}, {"money": 1}):
            n_money += i["money"]
        collection.update_one({"name": b_name}, {"$set": {"money": n_money}})
        return f'{b_name}:{n_money}'

    def get_udata(self):
        collection = self.AuctModel.Bidder()
        data_dict = {}
        for i in collection.find({}, {"_id": 1, "name": 1, "money": 1, "mail": 1}):
            data = {i["_id"]: {"name": i["name"], "money": i["money"], "mail": i["mail"]}}
            data_dict.update(data)
        return data_dict

    def user_money_update(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        u_money = 0
        money = int(decrypted_list[1])
        t_money = int(decrypted_list[2])
        name = decrypted_list[3]
        u_name = decrypted_list[4]
        u_money += t_money
        money -= t_money
        collection.update_one({"name": name}, {"$set": {"money": money}})
        collection.update_one({"name": u_name}, {"$set": {"money": u_money}})
        return f"{money}:{u_money}:{t_money}:{u_name}:{name}"

    def user_info_change(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        n_name = decrypted_list[1]
        mail = decrypted_list[2]
        password = decrypted_list[3]
        name = decrypted_list[4]
        collection.update_one({"name": name}, {"$set": {"mail": mail, "name": n_name, "pass": password}})
        return "Info Changed"

    def user_exit(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        b_mail = decrypted_list[1]
        b_name = decrypted_list[2]
        if collection.count_documents({}) == 0:
            return "Email Added"
        else:
            try:
                for i in collection.find({}, {"_id": 0, "mail": 1, "name": 1}):
                    if i["mail"] == b_mail:
                        return "Email Already Existed"
                    elif i["name"] == b_name:
                        return "Name Already Existed"

                return "Email Accepted"
            except Exception as err:
                print(str(err))
                return str(err)

    def pass_check(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        n_pass = decrypted_list[1]
        name = decrypted_list[2]
        flag = -1
        for i in collection.find({"name": name}, {"pass": 1}):
            if i["pass"] == n_pass:
                flag = 1
            else:
                flag = 0

        if flag == 1:
            return "Same Password"

        else:
            return n_pass

    def Acc_deletion(self, decrypted_list):
        collection = self.AuctModel.Bidder()
        name = decrypted_list[1]
        collection.delete_one({"name": name})
        return "Account Deleted!"


class Data:
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    auction: Server = Server()
    auction.main()
