from rest_framework import serializers

from .models import Userdb


class DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userdb
        fields = '__all__'
