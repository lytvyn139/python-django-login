from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('registred', views.registred),
    path('login', views.login),
    path('success', views.success),    
]
