from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from web import s3_interface
from web.forms import CreateUserForm

import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_file', path = '')
        else:
            return render(request, 'registration/index.html',{'some_flag':True})

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
	    ##########
            _ip = get_client_ip(request)
            url = "http://whois.kisa.or.kr/openapi/ipascc.jsp?query=" + _ip + "&key=2019061018312567743339&answer=json"
            res = requests.get(url)
            country = res.json()['whois']['countryCode']
	    ############
            print(res.json(), _ip)

            if country == 'KR':
                s3_interface.make_bucket(user.username)
                s3_interface.make_directory(user.username, 'waste/')
            else:
                s3_interface.make_bucket(user.username, 'us-west-1')
                s3_interface.make_directory(user.username, 'waste/')
     


            return redirect('user_file', path = '')
        else:
            return render(request, 'registration/index.html', {'some_flag_1':True})

@login_required
def delete_account(request):
    if request.method == 'GET':
        return render(request, 'registration/delete_account.html')
    elif request.method == 'POST':
        if request.POST.get('yes'):
            return redirect('delete_account_success')
        else:
            return redirect('/')

@login_required
def delete_account_success(request):
    if request.method == 'GET':
        # delete account
        u = User.objects.get(username = request.user.username)
        u.delete()
        # logout
        logout(request)
        return render(request, 'registration/delete_account_success.html')

