from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.shortcuts import redirect
from .models import *
from django.shortcuts import get_object_or_404
from .decorators import members_required
# Create your views here.
@members_required
def index(request):
    return render(request, 'member/tem/index.html')
@members_required   
def news(request):
    news = News.objects.all()
    return render(request, 'member/tem/news.html', {'news': news})
@members_required
def projects(request):
    projects = Project.objects.all()
    usr_projects = projects.filter(author=request.user)
    if request.method == 'POST':
        project = Project.objects.create(title=request.POST['title'], content=request.POST['content'], image = request.FILES['image'], author=request.user)
        project.save()
        messages.success(request, 'Project created successfully')
        return redirect('/members/projects')
    return render(request, 'member/tem/projects.html', {'projects': projects, 'usr_projects': usr_projects})
@members_required
def courses(request):
    return render(request, 'member/tem/courses.html')
@members_required
def profile(request):
    return render(request, 'member/tem/profile.html')
def login(request):
    if request.user.is_authenticated and (request.user.is_member or request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You are already logged in')
        return redirect('/members')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_member == False and user.is_staff == False and user.is_superuser == False:
                messages.error(request, 'You are not a members')
                return redirect('/members/login')
            else:
                auth.login(request, user)
                messages.success(request, 'Login successfully')
                return redirect('/members')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/members/login')
    return render(request, 'member/tem/login.html')
@members_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('/members/login')
@members_required
def contact(request):
    return render(request, 'member/tem/contact.html')
@members_required
def project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('/members/projects')
    if project.author != request.user:
        messages.error(request, 'You are not the author of this project')
        return redirect('/members/projects')
    if not project:
        messages.error(request, 'Project not found')
        return redirect('/members/projects')
    if request.method == 'POST':
        if request.FILES:
            project.image = request.FILES['image']
        project.title = request.POST['title']
        project.content = request.POST['content']
        project.save()
        messages.success(request, 'Project updated successfully')
        return redirect('/members/projects')
    return render(request, 'member/tem/project.html', {'p': project})
@members_required  
def delete_project(request, project_id):
    print(project_id)
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('/members/projects')
    if project.author != request.user:
        messages.error(request, 'You are not the author of this project')
        return redirect('/members/projects')
    project.delete()
    messages.success(request, 'Project deleted successfully')
    return redirect('/members/projects')