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
    usr_news = []
    for i in news:
        if len(i.image.all().order_by('num')) > 0:
            i.imagef = i.image.all().order_by('num')[0].image
        else:
            i.imagef = None
        if len(i.content.all().order_by('num')) > 0:
            i.contentf = i.content.all().order_by('num')[0].content
        else:
            i.contentf = None
        if i.author == request.user:
            usr_news.append(i)
    return render(request, 'member/tem/news.html', {'news': news, 'usr_news': usr_news})
@members_required
def create_news(request):
    labels = NewsLabel.objects.all()
    if request.method == 'POST':
        post = dict(request.POST)
        new = News.objects.create(title=post['title'][0], author=request.user)
        label_selected = request.POST.getlist('label')
        label_selected = NewsLabel.objects.filter(id__in=label_selected)
        new.label.set(label_selected)
        new.save()
        print(new)
        del post['csrfmiddlewaretoken'], post['title']
        for x,y in post.items():
            print(x,y)
            if y[0]=='image':
                image = NewsImage.objects.create(image=request.FILES[x], num=int(y[1]), news=new)
                print(image)
                image.save()
            if y[0]=='text':
                content = NewsContent.objects.create(content=y[2], num=int(y[1]), news=new)
                print(content)
                content.save()
        messages.success(request, 'News created successfully')
        return redirect('/members/news')
    return render(request, 'member/tem/new_create.html', {'all_labels': labels})
@members_required
def projects(request):
    projects = Project.objects.all()
    all_labels = ProjectLabel.objects.all()
    usr_projects = projects.filter(author=request.user)
    if request.method == 'POST':
        label_selected = request.POST.getlist('labels')
        label_selected = ProjectLabel.objects.filter(id__in=label_selected)
        project = Project.objects.create(title=request.POST['title'], content=request.POST['content'], image = request.FILES['image'], author=request.user)
        project.label.set(label_selected)
        project.save()
        messages.success(request, 'Project created successfully')
        return redirect('/members/projects')
    return render(request, 'member/tem/projects.html', {'projects': projects, 'usr_projects': usr_projects, 'all_labels': all_labels})
@members_required
def project_labels(request):
    labels = ProjectLabel.objects.all()
    if request.method == 'POST':
        if request.POST['submit'] == 'add':
            label = ProjectLabel.objects.create(name=request.POST['name'], created_by=request.user)
            label.save()
            messages.success(request, 'Label created successfully')
            return redirect('/members/projects/labels')
        if request.POST['submit'] == 'update':
            label = ProjectLabel.objects.get(id=request.POST['id'])
            label.name = request.POST['name']
            label.save()
            messages.success(request, 'Label updated successfully')
            return redirect('/members/projects/labels')
    return render(request, 'member/tem/project_labels.html', {'labels': labels})
@members_required
def project_label_delete(request, label_id):
    try:
        label = ProjectLabel.objects.get(id=label_id)
    except ProjectLabel.DoesNotExist:
        messages.error(request, 'Label not found')
        return redirect('/members/projects/labels')
    label.delete()
    messages.success(request, 'Label deleted successfully')
    return redirect('/members/projects/labels')
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
    all_labels = ProjectLabel.objects.all()
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
        project.label.clear()
        label_selected = request.POST.getlist('labels')
        label_selected = ProjectLabel.objects.filter(id__in=label_selected)
        project.label.set(label_selected)
        project.title = request.POST['title']
        project.content = request.POST['content']
        project.save()
        messages.success(request, 'Project updated successfully')
        return redirect('/members/projects')
    return render(request, 'member/tem/project.html', {'p': project, 'all_labels': all_labels})
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