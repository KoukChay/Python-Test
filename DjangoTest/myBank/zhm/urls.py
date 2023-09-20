from django.urls import path

from . import views

urlpatterns = [
    path("", views.zHM, name="zHM")
]
