from django.urls import path

from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("pF/", views.pFile, name="pF")
]
