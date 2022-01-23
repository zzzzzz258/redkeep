from django.urls import path

from .import views

app_name = 'drivers'
urlpatterns = [
    path("register", views.register, name = 'register'), 
]
