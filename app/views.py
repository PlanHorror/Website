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
from django.http import JsonResponse
from .forms import *
from django.utils import translation
# Create your views here.
def index(request):
    # Create 16 Course objects
    # for i in range(1, 17):
    #     cr = Course.objects.create(title='Course ' + str(i), url='course-' + str(i), author=CustomUser.objects.get(id=1))
    #     m1 = Module.objects.get(id=(i % 4) + 1)
    #     try:
    #         m2 = Module.objects.get(id=(i % 4) + 2)
    #     except Module.DoesNotExist:
    #         cr.module.add(m1)
    #     else:
    #         cr.module.add(m1, m2)
    #     cr.set_current_language('en')
    #     cr.save()
    #     cr.set_current_language('vi')
    #     cr.title = 'Khoá học ' + str(i)
    #     cr.save()
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
            messages.error(request, _('Invalid username or password'))
            return redirect('login')
    return render(request, 'app/tem/login.html')
def register(request):
    if request.user.is_authenticated:
        messages.error(request, _('You are already logged in'))
        return redirect('index')
    form = UserRegisterForm()
    error = None
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
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
def news(request):
    # news = News.objects.all()
    # # Select image have num min of each news
    # for n in news:
    #     image = NewsImage.objects.filter(news=n).order_by('num').first()
    #     if image:
    #         n.image = image.image
    return render(request, 'app/tem/news.html')
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
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    module = request.GET.get('module', None)
    courses = Course.objects.all()
    modules = Module.objects.all()
    if search and module:
        courses = Course.objects.filter(Q(translation__title__icontains=search) & Q(module=module)).distinct()
        module = int(module)
    else:
        if search:
            courses = Course.objects.filter(Q(translation__title__icontains=search)).distinct()
        if module:
            module = int(module)
            courses = courses.filter(module=module)
    if sort == 'time2':
        courses = courses.order_by('created_at')
    else:
        courses = courses.order_by('-created_at')
    paginator = Paginator(courses, 4)
    page = request.GET.get('page') or 1
    try:
        paginator.validate_number(page)
    except EmptyPage :
        page = 1
        messages.error(request, _('Page not found'))
    except PageNotAnInteger:
        page = 1
        messages.error(request, _('Page invalid'))
    courses = paginator.get_page(page)
    return render(request, 'app/tem/course.html', {'cr': courses, 'sort': sort, 'search': search, 'module': module, 'modules': modules})
def projects(request):
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    default_sort = sort
    project = Project.objects.all()
    if search:
        project = Project.objects.filter(Q(translation__title__icontains=search) | Q(translation__content__icontains=search))
    if sort == 'time2':
        project = project.order_by('created_at')
    else:
        project = project.order_by('-created_at')

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

    pLabels = ProjectLabel.objects.all()
    
    return render(request, 'app/tem/projects.html', {'pr': project, 'pl': pLabels, 'sort': default_sort, 'search': search})
def project(request, title, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'app/tem/project.html', {'p': project})
@login_required(login_url='login')
def collaboration(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            c_type = request.POST['interest']
            obj = request.POST.getlist('title')
            if c_type == 'project':
                obj = Project.objects.filter(id__in=obj)
                ct = Contact.objects.create(user=request.user, phone_number=phone_number, c_type=c_type, message=message)
                ct.project_obj.set(obj)
                ct.save()
            elif c_type == 'news':
                obj = News.objects.filter(id__in=obj)
                ct = Contact.objects.create(user=request.user, phone_number=phone_number, c_type=c_type, message=message)
                ct.news_obj.set(obj)
                ct.save()
            messages.success(request, _('Send message successfully'))
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'app/tem/collab.html', {'form': form})
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, _('You must login to view this page'))
        return redirect('login') 
    return render(request, 'app/tem/profile.html')
# JSON response for AJAX request
def get_projects(request):
    # Take current language
    lang = request.GET.get('lang', 'en')
    # Get all projects
    activate(lang)
    projects = Project.objects.values_list('translation__title', 'pk')
    # Return JSON response
    return JsonResponse({'projects': list(projects)})
def get_news(request):
    # Take current language
    lang = request.GET.get('lang', 'en')
    # Get all news
    activate(lang)
    news = News.objects.values_list('translation__title', 'pk')
    # Return JSON response
    return JsonResponse({'news': list(news)})
def get_courses(request):
    # Take current language
    lang = request.GET.get('lang', 'en')
    # Get all courses
    activate(lang)
    courses = Course.objects.values_list('translation__title', 'pk')
    # Return JSON response
    return JsonResponse({'courses': list(courses)})