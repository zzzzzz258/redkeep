from django.urls import path

from . import views


app_name = 'app'
urlpatterns = [
    path("", views.index, name = 'index'),
    path("register", views.log_up, name = 'logup'),
]
    
