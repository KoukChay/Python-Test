import socket



class TCP_server:
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9998
        self.db = {}
        self.recording_all_data()

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("Server listen on port:{} and ip {}".format(self.server_port, self.server_ip))
        try:
            while True:
                client, address = server.accept()
                print("Accepted Connection from - {} : {} ".format(address[0], address[1]))
                self.handle_client(client)
        except Exception as err:
            print(err)

    def handle_client(self, client_socket):
        with client_socket as sock:
            from_client = sock.recv(1024)
            received_data = from_client.decode("utf-8")
            print("Running Command : ", received_data)

            try:
                if received_data == "gad":
                    data = self.loading_all_data()
                    print(data)

            except Exception as err:
                print(err)

            # self.toSave.update(received_data)
            message = "server got it:>" + received_data
            to_send = bytes(message, 'utf-8')
            sock.send(to_send)

    def recording_all_data(self):
        with open("u_data.txt", 'w') as file:
            file.writelines("""Zas Ass,z@gmail.com,zpass,92373,21,
Zaw Hein,zaw@gmail.com,zpass,91233,23,
Kouk Chay,zz@gmail.com,zpass,12321,12,
Kouk Chay ,@gmail.com,12231,12231,12,""")

    def loading_all_data(self):
        try:
            with open("u_data.txt", 'r') as file:
                lines = file.readlines()
                i = 0
                for line in lines:
                    line = line[:len(line) - 1]
                    if line == "":
                        continue
                    line_items = line.split(',')
                    self.db[i] = {"name": line_items[0],
                                  "email": line_items[1],
                                  "password": line_items[2],
                                  "phone": line_items[3],
                                  "age": line_items[4], }
                    i += 1
        except FileNotFoundError:
            pass
        return self.db


if __name__ == '__main__':
    tcpserver = TCP_server()
    tcpserver.main()
