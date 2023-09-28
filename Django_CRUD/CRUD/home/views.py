import pymongo
from django.shortcuts import render, redirect

connection = pymongo.MongoClient('localhost', 27017)
database = connection['Django_Server']
collection = database['infos']


def signup(request):
    data_list = []

    for document in collection.find():
        mail = document.get('mail', '')
        password = document.get('password', '')
        data_list.append({"mail": mail, "password": password})
    print(data_list)

    if request.method == "POST":
        mail = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password == c_password:
            for i in data_list:
                print('data', i)
                print("find mail:", i['mail'])
                if i['mail'] == mail:
                    print('existed mail: ', i['mail'])
                    exist = "Email Already Exist!"
                    return render(request, 'signup.html', {"exist": exist})

            user = {"mail": mail, 'password': password, 'money': 0}
            collection.insert_one(user)
            done = "You are Signed Up!"
            return render(request, 'signup.html', {"done": done})
        else:
            exist = "Passwords do not match!"
            return render(request, 'signup.html', {"exist": exist})

    return render(request, 'signup.html')


def login(request):
    data_list = []

    for document in collection.find():
        mail = document.get('mail', '')
        password = document.get('password', '')
        money = document.get('money', '')
        data_list.append({"mail": mail, "password": password,"money":money})

    if request.method == "POST":
        mail = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Received data: mail={mail}, password={password}")
        for i in data_list:
            if i['mail'] == mail and i['password'] == password:
                l_user = {"mail": i['mail'], "password": i['password'],"money":i['money']}
                request.session['l_user'] = l_user
                return redirect('userpf')

        exist = "Email or Password Incorrect!"
        return render(request, 'login.html', {"exist": exist})
    return render(request, 'login.html')


def userpf(request):
    l_user = request.session.get('l_user', None)

    if request.method == "POST":
        opt = request.POST.get('opt')
        if opt == "Reset Password":
            return redirect('rstpass')
        elif opt == "Delete Account":
            return redirect('delacc')
        elif opt == "Transfer Point":
            return redirect('transfer')
        elif opt == "Deposit":
            return redirect('deposit')

    return render(request, 'userpf.html', {"l_user": l_user})


def rstpass(request):
    l_user = request.session.get('l_user', None)
    user_mail = l_user["mail"]
    user_pass = l_user["password"]
    if request.method == "POST":
        old_pass = request.POST.get('oldpass')
        new_pass = request.POST.get('newpass')
        if user_pass == old_pass:
            print(user_pass == old_pass)
            for i in collection.find():
                if i['mail'] == user_mail:
                    collection.update_one({"mail":user_mail}, {"$set": {"password": new_pass}})
                    print("pass reseted")
                    return redirect('login')
        else:
            exist = "Please Enter correct Old Password!"
            return render(request, 'rstpass.html', {"exist": exist})
    return render(request, 'rstpass.html')


def delacc(request):
    l_user = request.session.get('l_user', None)
    user_mail = l_user["mail"]
    user_pass = l_user["password"]
    if request.method == "POST":
        c_pass = request.POST.get('cpass')
        if user_pass == c_pass:
            for i in collection.find():
                if i['mail'] == user_mail:
                    collection.delete_one({})
                    return redirect('login')
        else:
            exist = "Incorrect Password!"
            return render(request, 'delacc.html', {"exist": exist})
    return render(request, 'delacc.html')

def deposit(request):
    l_user = request.session.get('l_user', None)
    user_mail = l_user["mail"]
    user_pass = l_user['password']
    user_money = int(l_user["money"])
    if request.method == "POST":

        add_money = int(request.POST.get('add_money'))
        for i in collection.find():
            if i['mail'] == user_mail:
                user_money += add_money
                collection.update_one({"mail": user_mail}, {"$set": {"money": user_money}})
                l_user = {"mail": user_mail, "password": user_pass, "money": user_money}
                request.session['l_user'] = l_user
                return redirect( 'userpf')

    return render(request, 'deposit.html')

def transfer(request):
    data_list =[]
    l_user = request.session.get('l_user', None)
    your_mail = l_user["mail"]
    your_password = l_user["password"]
    your_money = l_user['money']
    for document in collection.find():
        mail = document.get('mail', '')
        if your_mail != mail:
            data_list.append({"mail": mail})
    if request.method == "POST":
        t_user = request.POST.get("opt")
        t_money = int(request.POST.get("t_money"))
        if your_money >= t_money:
            for i in collection.find():
                if t_user == i['mail']:
                    user_money = i['money']
                    your_money-=t_money
                    user_money+=t_money
                    collection.update_one({"mail": t_user}, {"$set": {"money": user_money}})
                    collection.update_one({"mail": your_mail}, {"$set": {"money": your_money}})
                    l_user = {"mail": your_mail, "password": your_password, "money": your_money}
                    request.session['l_user'] = l_user
                    return redirect( 'userpf')
        else:
            err = "Not Enough Money to Tansfer"
            return render(request, 'transfer.html', {"err": err,"data_list":data_list})

    return render(request,'transfer.html',{"data_list":data_list})