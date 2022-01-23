from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import DriverForm


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
            new_driver.user_id = request.user.user_id
            new_driver.save()
            return redirect('app:index')
    else:
        form = DriverForm()

    return render(request, 'drivers/register.html', {'form': form})

        
