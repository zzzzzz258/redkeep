from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import UserManager, User
from .forms import LogupForm

"""
   Log up surface to create a user
"""


def log_up(request):
    if request.method == 'POST':
        # create a user and back to login page
        form = LogupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            return redirect('login')
    else:
        form = LogupForm()

    return render(request, 'registration/logup.html', {'form': form})


"""
   Index view to display basic user info
"""


@login_required
def index(request):
    user = request.user
    context = {'user': user}
    return render(request, 'app/index.html', context)
