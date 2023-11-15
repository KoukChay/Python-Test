from rest_framework import viewsets
from .models import Userdb
from . import serializers


class DbViewset(viewsets.ModelViewSet):
    queryset = Userdb.objects.all()
    serializer_class = serializers.DbSerializer
