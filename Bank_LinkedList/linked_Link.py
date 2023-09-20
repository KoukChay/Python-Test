import pymongo

connection = pymongo.MongoClient("localhost", 27017)
Bank_db = connection["Bank_db"]
users = Bank_db["users"]


class UserLinkedList:
    def __init__(self):
        self.head = None

    def add_old_user(self, old_user):
        current_user = self.head
        if self.head is None:
            self.head = old_user
        else:
            while current_user.next is not None:
                current_user = current_user.next
            current_user.next = old_user

    def money_update(self, t_user, t_amount, user, user_amount):
        current_user = self.head
        while current_user is not None:
            if current_user.name == t_user.name:
                current_user.amount = t_amount
                break
            else:
                current_user = current_user.next

        while current_user is not None:
            if current_user.name == user.name:
                current_user.amount = user_amount
                break
            else:
                current_user = current_user.next

    def add_user(self, new_user):
        current_user = self.head

        if current_user is None:
            self.head = new_user
        else:
            while current_user.next is not None:
                current_user = current_user.next
            current_user.next = new_user

    def save_user(self):
        _id = 1
        current_user = self.head
        while current_user is not None:
            print(f"Uploading user '{current_user.name}' to database....")
            u_info = {"_id": _id, "name": current_user.name, "mail": current_user.mail, "pass": current_user.password,
                      "amount": current_user.amount,
                      "phone": current_user.phone}
            _id += 1
            users.insert_one(u_info)
            current_user = current_user.next

    def check_user(self, mail, name,phone):
        current_user = self.head
        if current_user is None:
            return None
        else:
            while current_user is not None:
                if current_user.mail == mail or current_user.name == name or current_user.phone == phone:
                    return current_user
                else:
                    current_user = current_user.next
            return None

    def get_user(self, you):
        current_user = self.head
        other_users = []
        if current_user is None:
            return None
        else:
            while current_user is not None:
                if current_user.name != you:
                    other_user = {"name": current_user.name, "mail": current_user.mail, "amount": current_user.amount}
                    other_users.append(other_user)
                    current_user = current_user.next
                else:
                    current_user = current_user.next
                    pass
            return other_users
