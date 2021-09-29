from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .forms import *
from .models import *


def signup(request):
    if request.user.is_authenticated: # 이미 로그인된 상태면 다른 곳으로 보냄
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'account/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # print(request.user.is_info_set)
            if request.user.is_info_set:
                if request.user.type == 'school':
                    return redirect(request.GET.get('next') or 'school:dash')
                elif request.user.type == 'teacher':
                    return redirect(request.GET.get('next') or 'teacher:dash')
                elif request.user.type == 'student':
                    return redirect(request.GET.get('next') or 'student:dash')
                elif request.user.type == 'superadmin':
                    return redirect('superadmin:dash')
            else:
                if request.user.type == 'school':
                    return redirect('school:signup_info')
                elif request.user.type == 'teacher':
                    return redirect('teacher:signup_info')
                elif request.user.type == 'student':
                    return redirect('student:signup_info')
                elif request.user.is_admin:
                    request.user.is_info_set = True
                    request.user.type = 'superadmin'
                    request.user.user_name = 'admin'
                    request.user.save()
            return redirect('/')
        else:
            return render(request, 'account/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'account/login.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def detail(request):
    return render(request, 'account/account_detail.html')


def update(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'account/account_update.html', context)
