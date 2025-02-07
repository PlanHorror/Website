from django.shortcuts import render
from members.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _, get_language, activate
from django.shortcuts import redirect
# Import login_required decorator, login, logout, authenticate functions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from .forms import *
# Create your views here.
def index(request):
    # Print template root directory
    # print('Template root directory:', request.templates.dirs)
    return render(request, 'app/tem/index.html')
def login(request):
    if request.user.is_authenticated:
        messages.error(request, _('You are already logged in'))
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, _('Login successfully'))
            return redirect('index')
        else:
            print('Invalid username or password')
            messages.error(request, _('Invalid username or password'))
            return redirect('login')
    return render(request, 'app/tem/login.html')
def register(request):
    print(request)
    form = UserRegisterForm()
    error = None
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Register successfully'))
            return redirect('login')
        else:
            error = form.errors
    return render(request, 'app/tem/register.html', {'form': form, 'error': error})
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, _('Logout successfully'))
    return redirect('index')
def about(request):
    return render(request, 'app/tem/about.html')
def contact(request):
    return render(request, 'app/tem/contact.html')
def news(request):
    # news = News.objects.all()
    # # Select image have num min of each news
    # for n in news:
    #     image = NewsImage.objects.filter(news=n).order_by('num').first()
    #     if image:
    #         n.image = image.image
    return render(request, 'app/tem/news.html', {'ns': news})
def new(request, title ,news_id):
    news = News.objects.get(id=news_id)
    image = NewsImage.objects.filter(news=news)
    content = NewsContent.objects.filter(news=news)
    # Merge image and content to a list then sort by num
    combine = list(image) + list(content)
    combine.sort(key=lambda x: x.num)
    for i in combine:
        if isinstance(i, NewsImage):
            i.type = 'image'
        else:
            i.type = 'content'
    news.combine = combine
    return render(request, 'app/tem/new.html', {'n': news})
def course(request):
    courses = Course.objects.all()
    paginator = Paginator(courses, 6)
    page = request.GET.get('page') or 1
    try:
        paginator.validate_number(page)
    except EmptyPage :
        page = 1
        messages.error(request, _('Page not found'))
    except PageNotAnInteger:
        page = 1
        messages.error(request, _('Page invalid'))
    project = paginator.get_page(page)
    return render(request, 'app/tem/course.html', {'cr': courses})
def projects(request):
    sort = request.GET.get('sort', None)
    print(sort)
    search = request.GET.get('search', None)
    print(search)
    default_sort = sort
    project = Project.objects.all().order_by('-created_at')
    if sort:
        if sort == 'newest':
            project = Project.objects.all().order_by('-created_at')
        elif sort == 'oldest':
            project = Project.objects.all().order_by('created_at')
    if search:
        project = Project.objects.filter(Q(translation__title__icontains=search) | Q(translation__content__icontains=search))
    paginator = Paginator(project, 6)
    page = request.GET.get('page') or 1
    try:
        paginator.validate_number(page)
    except EmptyPage :
        page = 1
        messages.error(request, _('Page not found'))
    except PageNotAnInteger:
        page = 1
        messages.error(request, _('Page invalid'))
    project = paginator.get_page(page)
    labels = Label.objects.all()
    
    return render(request, 'app/tem/projects.html', {'pr': project, 'labels': labels, 'sort': default_sort, 'search': search})
def project(request, title, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'app/tem/project.html', {'p': project})
def collaboration(request):
    return render(request, 'app/tem/collab.html')
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, _('You must login to view this page'))
        return redirect('login') 
    return render(request, 'app/tem/profile.html')