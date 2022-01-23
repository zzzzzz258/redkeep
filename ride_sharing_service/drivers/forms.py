from django.forms import ModelForm, PasswordInput
from .models import Driver


"""
   Form of registering a user
"""


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        exclude = ['user_id', 'driver_id']
        widgets = {
        }
