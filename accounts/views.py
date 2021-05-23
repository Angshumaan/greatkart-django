from accounts.models import Account
from django.shortcuts import render, redirect
from . forms import RegistrationForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == "POST":
        # request.post will contain all the field values
        form = RegistrationForm(request.POST)
        if form.is_valid():  # if form has all the required field and validations
            # fetching all field from request.pOSt
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            # if email is basu@gmail.com we will get only basu coz indexing is 0
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email,  username=username, password=password)
            # we did like this coz phone_number argument is not specified in create_user
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return
