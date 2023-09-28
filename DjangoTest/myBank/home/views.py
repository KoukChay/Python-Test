from django.shortcuts import render
import pymongo

connection = pymongo.MongoClient('localhost',27017)
database = connection['Django_Server']
collection = database['infos']

def home(request):
    smail = request.POST.get('semail')
    print(smail)
    spass = request.POST.get('spass1')
    print(spass)
    user = {'mail':smail,'password':spass}
    collection.insert_one(user)
    return render(request,'home.html',{'email':smail,'password':spass})

def userpf(request):
    return render(request,'userpf.html')
# Create your views here.
