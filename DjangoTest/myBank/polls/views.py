from django.http import HttpResponse


def home(request):
    return HttpResponse("hi welcome to mybank")


# Create your views here.
def pFile(request):
    return HttpResponse("Welcome to polls' profile!")
