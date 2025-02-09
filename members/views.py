from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.shortcuts import redirect
from .models import *
from django.template import Library
register = Library()
# Create your views here.
@login_required(login_url='members/login')
def index(request):
    messages.error(request, 'You are already logged in')
    return render(request, 'member/tem/index.html')
@login_required(login_url='members/login')
def news(request):
    news = News.objects.all()
    return render(request, 'member/tem/news.html', {'news': news})
@login_required(login_url='members/login')
def projects(request):
    projects = Project.objects.all()
    return render(request, 'member/tem/projects.html', {'projects': projects})
@login_required(login_url='members/login')
def courses(request):
    return render(request, 'member/tem/courses.html')
@login_required(login_url='members/login')
def profile(request):
    return render(request, 'member/tem/profile.html')
def login(request):
    if request.user.is_authenticated and request.user.is_member:
        messages.error(request, 'You are already logged in')
        return redirect('members/index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_member == False:
                messages.error(request, 'You are not a members')
                return redirect('members/login')
            else:
                auth.login(request, user)
                messages.success(request, 'Login successfully')
                return redirect('members/index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'member/tem/login.html')
@login_required(login_url='members/login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('login')
@login_required(login_url='members/login')
def message(request):
    return render(request, 'member/tem/message.html')
