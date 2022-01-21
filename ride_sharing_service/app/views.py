from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from .forms import LoginForm

"""
   Log_in view to handle request to login or submitted login form
"""


def log_in(request):
    if request.method == 'POST':
        # post request, check username and password and redirect
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,
                                username = username,
                                password = password)
            if user is not None:
                # log in successfully, redirect to index page
                login(request, user)
                # TODO
                return redirect('/app/')
            else:
                # log in failed, redirect to log in page with message
                # TODO: add sm message to this
                return redirect('/app/login')
    else:
        # get request, display login page info
        # TODO
        form = LoginForm()
        return render(request, 'app/login.html', {'form': form})


"""
   Log out current user, and return to login page
"""


@login_required
def log_out(request):
    logout(request)
    return redirect('/app/login')


"""
   Index view to display basic user info
"""


@login_required
def index(request):    
    return HttpResponse("Hello, " + request.user.get_username())


