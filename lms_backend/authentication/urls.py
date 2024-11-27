from django.contrib import admin
from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    # path('forgotten_password/', views.forgotten_password, name='forgotten_password'),
    # path('reset_password/<uidb64>/<token>/', views.reset_password, name="reset_password")
]
