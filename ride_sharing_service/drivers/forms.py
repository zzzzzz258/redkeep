from django.forms import ModelForm
from .models import Driver


"""
   Form of registering a user
"""


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        exclude = ['user', 'driver_id']
        widgets = {
        }
