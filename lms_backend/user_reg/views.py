from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
# from settings import EXTERNAL_URL
# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'