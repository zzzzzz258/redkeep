from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.core.mail import send_mail

from .forms import DriverForm, SearchFormSet, SearchForm
from .models import Driver
import sys
sys.path.append("..")
from riders.models import Ride, Ride_Owner, Ride_Sharer

"""
   Index page of driver information
"""


@login_required
def index(request):
    drivers = Driver.objects.filter(user = request.user)
    if (drivers.exists()):
        driver = drivers.get()
        confirmed_rides = Ride.objects.filter(driver = driver, status='c')
        complete_rides = Ride.objects.filter(driver = driver, status='t')
    else:
        driver = None
        complete_rides = None
        confirmed_rides = None
    context = {'user': request.user,
               'driver': driver,
               'confirmed_rides': confirmed_rides,
               'complete_rides': complete_rides,
               }
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
        form = DriverForm(request.POST,
                          instance = Driver.objects.get(user = request.user))
        if form.is_valid():
            form.save()
            return redirect('zber:drivers:index')
    else:
        form = DriverForm(instance = Driver.objects.get(user = request.user))
    return render(request, 'drivers/register.html', {'form' : form})


"""
   Ride view in driver app
"""


def ride(request, ride_owner_id):
    driver = Driver.objects.get(user = request.user)
    ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
    ride = Ride.objects.get(ride_owner = ride_owner)    
    ride_sharers = Ride_Sharer.objects.filter(ride = ride)
    context = {'driver': driver,
               'ride': ride,
               'ride_owner': ride_owner,
               'ride_sharers': ride_sharers
               }
    return render(request, 'drivers/ride.html', context)


"""
   Completes a ride. Only allow POST request, raise 404 error for GET request
"""


def ride_complete(request, ride_owner_id):
    if request.method == 'POST':
        ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
        ride = Ride.objects.get(ride_owner = ride_owner)
        ride.status = 't'
        ride.save()
        return redirect('zber:drivers:index')
    else:
        raise Http404("Page Not Found")


"""
   Display all search results to driver user
"""


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            max_passengers = form.cleaned_data['max_passengers']
            vehicle_type = form.cleaned_data['vehicle_type']
            special_request_info = form.cleaned_data['special_request_info']
            raw_url = reverse('zber:drivers:search_results')+'?'
            if max_passengers is not None:
                raw_url += ('max_passengers='+str(max_passengers))
            if len(vehicle_type) == 1:
                raw_url += ('&vehicle_type='+vehicle_type[0])
            if special_request_info is not None:
                raw_url += ('&special_request_info='+special_request_info)
            return redirect(raw_url)
    else:
        form = SearchForm()
    return render(request, 'drivers/search.html', {'form': form})


"""
   Show the results of seaching in driver search
"""


def search_results(request):
    results = Ride.objects.filter(status='o')
    
    max_passengers = request.GET.get('max_passengers')
    if max_passengers is not None:
        results = results.filter(sum_passengers__range=(1, max_passengers))

    vehicle_type = request.GET.get('vehicle_type')
    if vehicle_type is not None:
        results = results.filter(ride_owner__specific_type=vehicle_type)

    special_request_info = request.GET.get('special_request_info')
    if special_request_info is not None:
        results = results.filter(ride_owner__special_requests=special_request_info)

    context = {'result_rides': results, 'form': SearchForm()}
    return render(request, 'drivers/search.html', context)


"""
   Confirm a ride
"""


def ride_confirm(request, ride_owner_id):
    if request.method == 'POST':
        ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
        ride = Ride.objects.get(ride_owner = ride_owner)
        ride.driver = Driver.objects.get(user = request.user)
        ride.status = 'c'
        # send email to owner and sharers, not sending to sharers yet
        send_mail(
            'Ride Confirmation',
            'This is a confirmation to let you know that your ride request has been confirmed!',
            'zber568@outlook.com',
            [ride.ride_owner.user.email],
            fail_silently=False,
        )
        ride.save()
        return redirect('zber:drivers:index')
    else:
        raise Http404("Page Not Found")
    
