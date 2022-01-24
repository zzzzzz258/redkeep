from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import DriverForm
from .models import Driver


"""
   Index page of driver information
"""


@login_required
def index(request):
    drivers = Driver.objects.filter(user = request.user)
    if (drivers.exists()):
        driver = drivers.get()
    else:
        driver = None            
    context = {'user': request.user, 'driver': driver}
    return render(request, 'drivers/index.html', context)


"""
   Register as a driver
"""


@login_required
def register(request):
    if request.method == 'POST':
        # create a driver and back to index page
        form = DriverForm(request.POST)
        if form.is_valid():
            new_driver = form.save(commit = False)
            new_driver.user = request.user
            new_driver.save()
            return redirect('zber:drivers:index')
    else:
        form = DriverForm()

    return render(request, 'drivers/register.html', {'form': form})


"""
   Edit driver information
"""


def edit(request):
    if request.method == 'POST':        
        form = DriverForm(request.POST, instance = Driver.objects.get(user = request.user))
        if form.is_valid():
            form.save()
            return redirect('zber:drivers:index')
    else:
        form = DriverForm(instance = Driver.objects.get(user = request.user))
    return render(request, 'drivers/register.html', {'form' : form})
