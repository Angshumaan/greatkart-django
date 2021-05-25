from django.http.response import HttpResponse
from accounts.models import Account
from django.shortcuts import render, redirect
from . forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# verification send emial
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
            # User activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email]
                                      )
            send_email.send()
            # messages.success(
            #     request, 'Thank you for registering with us.We have sent you an verification email.Please Verify it')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # this will return the user object
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
# After getting userobject in try block
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


# @login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
