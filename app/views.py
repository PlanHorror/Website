from django.shortcuts import render
from members.models import *
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
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, _('Login successfully'))
                return redirect('index')
            else:
                print('Invalid username or password')
                messages.error(request, _('Invalid username or password'))
                return redirect('login')
        else:
            messages.error(request, _('Invalid username or password'))
            return redirect('login')
    return render(request, 'app/tem/login.html', {'form': form})
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
    news = News.objects.all()
    # Select image have num min of each news
    for n in news:
        image = NewsImage.objects.filter(news=n).order_by('num').first()
        if image:
            n.image = image.image
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
    return render(request, 'app/tem/course.html', {'cr': courses})
def projects(request):
    projects = Project.objects.all()
    return render(request, 'app/tem/projects.html', {'pr': projects})
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'app/tem/project_detail.html', {'p': project})
def collaboration(request):
    return render(request, 'app/tem/collab.html')
def profile(request):
    return render(request, 'app/tem/profile.html')