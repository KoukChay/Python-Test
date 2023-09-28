from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("userpf/", views.userpf, name='userpf'),
    path("login/", views.login, name='login'),
    path("rstpass/", views.rstpass, name='rstpass'),
    path("delacc/", views.delacc, name='delacc'),
    path("deposit/", views.deposit, name='deposit'),
    path("transfer/", views.transfer, name='transfer'),
]
