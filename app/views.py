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
from django.http import JsonResponse, HttpResponse
from .forms import *
from django.utils import translation
# Create your views here.
def index(request):
    # Create 16 News objects
    # for i in range(1, 19):
    #     ns = News.objects.create(title='News ' + str(i), author=CustomUser.objects.get(id=1))
    #     if i%6 < 5:
    #         ns.label.set(NewsLabel.objects.filter(id__in=[i%6, i%6+1, i%6+2]))
    #     elif i%6 == 5:
    #         ns.label.set(NewsLabel.objects.filter(id__in=[5, 6, 7]))
    #     else:
    #         ns.label.set(NewsLabel.objects.filter(id__in=[6,7,1]))
    #     ns.set_current_language('en')
    #     ns.save()
    #     ns_image = NewsImage.objects.create(news=ns, image='news-images/download_jtR0orR.avif', num=1)
    #     ns_content = NewsContent.objects.create(news=ns, content='Content ' + str(i), num=2)
    #     ns_content.set_current_language('en')
    #     ns_image.save()
    #     ns_content.save()
    #     ns.set_current_language('vi')
    #     ns.title = 'Tin tức ' + str(i)
    #     ns_content.content = 'Nội dung ' + str(i)   
    #     ns_content.save()
    #     ns.save()
 

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
    news = News.objects.all()
    labels = NewsLabel.objects.all()
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    label = request.GET.get('topic', None)
    if search and label:
        news = News.objects.filter(Q(translation__title__icontains=search) & Q(label=label)).distinct()
        label = int(label)
    else:
        if search:
            news = News.objects.filter(Q(translation__title__icontains=search)).distinct()
        if label:
            label = int(label)
            news = news.filter(label=label)
    if sort == 'time2':
        news = news.order_by('created_at')
    else:
        news = news.order_by('-created_at')
    paginator = Paginator(news, 6)
    page = request.GET.get('page') or 1
    try:
        paginator.validate_number(page)
    except EmptyPage :
        page = 1
        messages.error(request, _('Page not found'))
    except PageNotAnInteger:
        page = 1
        messages.error(request, _('Page invalid'))
    news = paginator.get_page(page)
    for i in news:
        i.imagef= NewsImage.objects.filter(news=i).order_by('num').first().image or None
        i.contentf= NewsContent.objects.filter(news=i).order_by('num').first() or None
    return render(request, 'app/tem/news.html', {'n': news, 'labels': labels, 'sort': sort, 'search': search, 'topic': label})
def new(request, title ,news_id):
    news = News.objects.get(id=news_id)
    image = NewsImage.objects.filter(news=news)
    content = NewsContent.objects.filter(news=news)
    all_comments = Comment.objects.filter(news=news)
    # Merge image and content to a list then sort by num
    combine = list(image) + list(content)
    combine.sort(key=lambda x: x.num)
    for i in combine:
        if isinstance(i, NewsImage):
            i.type = 'image'
        else:
            i.type = 'content'
    news.combine = combine
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': _('You need to login to comment'), 'url': '/login'})
        comment = request.POST.get('comment', None)
        if comment:
            a = Comment.objects.create(author=request.user, news=news, comment=comment)
            a.save()
            return JsonResponse({'status': 'success', 'comment_time' : a.created_at.strftime('%B %d, %Y - %I:%M %p')})
    return render(request, 'app/tem/new.html', {'n': news, 'comments': all_comments})
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
@login_required(login_url='login')
def profile(request):
    form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
    error = None
    if request.method == 'POST':
        
        if form.is_valid():
            form.save()
            messages.success(request, _('Update profile successfully'))
            return redirect('profile')
        else:
            error = form.errors
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'app/tem/profile.html', {'form': form, 'error': error})
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