from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView,  RedirectView
from .views import *

urlpatterns = [
    path('', student_main_page, name='student_main_page'),
]