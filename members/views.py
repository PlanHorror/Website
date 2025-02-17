from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from .decorators import members_required
# Create your views here.
@members_required
def index(request):
    return render(request, 'member/tem/index.html')
@members_required   
def news(request):
    news = News.objects.all().order_by('-created_at')
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
    labels = NewsLabel.objects.all().order_by('-created_at')
    if request.method == 'POST':
        post = dict(request.POST)
        new = News.objects.create(title=post['title'][0], author=request.user)
        label_selected = request.POST.getlist('labels')
        label_selected = NewsLabel.objects.filter(id__in=label_selected)
        new.label.set(label_selected)
        new.save()
        del post['csrfmiddlewaretoken'], post['title']
        for x,y in post.items():
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
def new(request, new_id):
    this_new = News.objects.get(id=new_id)
    this_new_data = list(this_new.image.all()) + list(this_new.content.all())
    this_new_data.sort(key=lambda x: x.num)
    this_new.data = this_new_data
    all_labels = NewsLabel.objects.all()
    if this_new.author != request.user:
        messages.error(request, 'You are not the author of this news')
        return redirect('/members/news')
    if request.method == 'POST':
        post = dict(request.POST)
        this_new.title = post['title'][0]
        label_selected = request.POST.getlist('labels')
        image_not_delete = request.POST.getlist('not-delete')
        label_selected = NewsLabel.objects.filter(id__in=label_selected)
        this_new.label.set(label_selected)
        this_new.save()
        del post['csrfmiddlewaretoken'], post['title']
        try:
            del post['labels'], post['not-delete']
        except:
            pass
        print(image_not_delete)
        a = NewsImage.objects.filter(news=this_new).exclude(num__in=image_not_delete)
        for i in a:
            i.image.delete(save=False)
        # Bulk delete for speed and performance
        a.delete()
        NewsContent.objects.filter(news=this_new).delete()
        for x,y in post.items():
            if y[0]=='image' or y[0]=='change_image':
                image = NewsImage.objects.create(image=request.FILES[x], num=int(y[1]), news=this_new)
                print(image)
                image.save()
            if y[0]=='text':
                content = NewsContent.objects.create(content=y[2], num=int(y[1]), news=this_new)
                print(content)
                content.save()
            if y[0]=='change_num':
                image = NewsImage.objects.get(num=int(y[2]), news=this_new)
                image.num = int(y[1])
                image.save()
        messages.success(request, 'News updated successfully')
        return redirect('/members/news')
    return render(request, 'member/tem/new.html', {'new': this_new, 'all_labels': all_labels})
@members_required
def delete_news_item(request, new_id):
    try:
        new = News.objects.get(id=new_id)
    except News.DoesNotExist:
        messages.error(request, 'News not found')
        return redirect('/members/news')
    if new.author != request.user:
        messages.error(request, 'You are not the author of this news')
        return redirect('/members/news')
    new.delete()
    messages.success(request, 'News deleted successfully')
    return redirect('/members/news')
def translate_news(request, new_id):
    try:
        new = News.objects.get(id=new_id)
    except News.DoesNotExist:
        messages.error(request, 'News not found')
        return redirect('/members/news')
    if new.author != request.user:
        messages.error(request, 'You are not the author of this news')
        return redirect('/members/news')
    # Get news by english, japanese, vietnamese
    new_ja = None
    new_vi = None
    new_en = new.title
    if new.has_translation('ja'):
        new_ja = {
            'title': new.get_translation('ja').title,
        }
    
    if new.has_translation('vi'):
        new_vi = {
            'title': new.get_translation('vi').title,
        }
    contents = new.content.all()
    list_content_en = []
    list_content_ja = []
    list_content_vi = []
    for i in contents:
        list_content_en.append({
            'content': i.get_translation('en').content,
            'num': i.num,
            'id': i.pk
        })
        if i.has_translation('ja'):
            list_content_ja.append({
                'content': i.get_translation('ja').content,
                'num': i.num,
                'id': i.pk
            })
        else:
            list_content_ja.append({
                'content': None,
                'num': i.num,
                'id': i.pk
            })
        if i.has_translation('vi'):
            list_content_vi.append({
                'content': i.get_translation('vi').content,
                'num': i.num,
                'id': i.pk
            })
        else:
            list_content_vi.append({
                'content': None,
                'num': i.num,
                'id': i.pk
            })
    if request.method == 'POST':
        p = dict(request.POST)
        new.title = p['title_en'][0]
        new.save()
        new.set_current_language('ja')
        new.title = p['title_ja'][0]
        new.save()
        new.set_current_language('vi')
        new.title = p['title_vi'][0]
        new.save()
        del p['csrfmiddlewaretoken'], p['title_en'], p['title_ja'], p['title_vi']
        for x,y in p.items():
            if y[0] == 'en':
                content = NewsContent.objects.get(id=y[1])
                content.set_current_language('en')
                content.content = y[2]
                content.save()
            if y[0] == 'ja':
                content = NewsContent.objects.get(id=y[1])
                content.set_current_language('ja')
                content.content = y[2]
                content.save()
            if y[0] == 'vi':
                content = NewsContent.objects.get(id=y[1])
                content.set_current_language('vi')
                content.content = y[2]
                content.save()
        messages.success(request, 'News translated successfully')
        return redirect('/members/news')
    return render(request, 'member/tem/translate_news.html', {'new_en': new_en, 'new_ja': new_ja, 'new_vi': new_vi, 'contents_en': list_content_en, 'contents_ja': list_content_ja, 'contents_vi': list_content_vi})
@members_required
def new_labels(request):
    labels = NewsLabel.objects.all().order_by('-created_at')
    for i in labels:
        if i.has_translation('vi'):
            i.name_vi = i.get_translation('vi').name
        else:
            i.name_vi = None
        if i.has_translation('ja'):
            i.name_ja = i.get_translation('ja').name
        else:
            i.name_ja = None
    if request.method == 'POST':
        if request.POST['submit'] == 'add':
            label = NewsLabel.objects.create(name=request.POST['name'], created_by=request.user)
            label.save()
            messages.success(request, 'Label created successfully')
            return redirect('/members/news/labels')
        if request.POST['submit'] == 'update':
            label = NewsLabel.objects.get(id=request.POST['id'])
            label.name = request.POST['name_en']
            label.save()
            label.set_current_language('ja')
            label.name = request.POST['name_ja']
            label.save()
            label.set_current_language('vi')
            label.name = request.POST['name_vi']
            label.save()
            messages.success(request, 'Label updated successfully')
            return redirect('/members/news/labels')
    return render(request, 'member/tem/new_labels.html', {'labels': labels})
@members_required
def new_label_delete(request, label_id):
    try:
        label = NewsLabel.objects.get(id=label_id)
    except NewsLabel.DoesNotExist:
        messages.error(request, 'Label not found')
        return redirect('/members/news/labels')
    label.delete()
    messages.success(request, 'Label deleted successfully')
    return redirect('/members/news/labels')
@members_required
def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    all_labels = ProjectLabel.objects.all().order_by('-created_at')
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
    labels = ProjectLabel.objects.all().order_by('-created_at')
    for i in labels:
        if i.has_translation('vi'):
            i.name_vi = i.get_translation('vi').name
        else:
            i.name_vi = None
        if i.has_translation('ja'):
            i.name_ja = i.get_translation('ja').name
        else:
            i.name_ja = None
    if request.method == 'POST':
        if request.POST['submit'] == 'add':
            label = ProjectLabel.objects.create(name=request.POST['name'], created_by=request.user)
            label.save()
            messages.success(request, 'Label created successfully')
            return redirect('/members/projects/labels')
        if request.POST['submit'] == 'update':
            label = ProjectLabel.objects.get(id=request.POST['id'])
            label.name = request.POST['name_en']
            label.save()
            label.set_current_language('ja')
            label.name = request.POST['name_ja']
            label.save()
            label.set_current_language('vi')
            label.name = request.POST['name_vi']
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
    module = Module.objects.all().order_by('-created_at')
    all_courses = Course.objects.all().order_by('-created_at')
    usr_courses = all_courses.filter(author=request.user).order_by('-created_at')
    if request.method == 'POST':
        course = Course.objects.create(title=request.POST['title'], url=request.POST['url'], author=request.user)
        module_selected = request.POST.getlist('modules')
        module_selected = Module.objects.filter(id__in=module_selected)
        course.module.set(module_selected)
        course.save()
        messages.success(request, 'Course created successfully')
        return redirect('/members/courses')
    return render(request, 'member/tem/courses.html', {'courses': all_courses, 'usr_courses': usr_courses, 'modules': module})
@members_required
def delete_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, 'Course not found')
        return redirect('/members/courses')
    if course.author != request.user:
        messages.error(request, 'You are not the author of this course')
        return redirect('/members/courses')
    course.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('/members/courses')
@members_required
def course(request, course_id):
    module = Module.objects.all().order_by('-created_at')
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, 'Course not found')
        return redirect('/members/courses')
    if course.author != request.user:
        messages.error(request, 'You are not the author of this course')
        return redirect('/members/courses')
    title_en = None
    title_jp = None
    title_vi = None
    if course.has_translation('en'):
        title_en = course.get_translation('en').title
    if course.has_translation('ja'):
        title_jp = course.get_translation('ja').title
    if course.has_translation('vi'):
        title_vi = course.get_translation('vi').title
    if request.method == 'POST':
        course.title = request.POST['title_en']
        course.url = request.POST['url']
        course.module.clear()
        module_selected = request.POST.getlist('modules')
        module_selected = Module.objects.filter(id__in=module_selected)
        course.module.set(module_selected)
        course.save()
        if request.POST['title_jp']:
            course.set_current_language('ja')
            course.title = request.POST['title_jp']
            course.save()
        if request.POST['title_vi']:
            course.set_current_language('vi')
            course.title = request.POST['title_vi']
            course.save()
        messages.success(request, 'Course updated successfully')
        return redirect('/members/courses')
    return render(request, 'member/tem/course.html', {'course': course, 'modules': module, 'title_en': title_en, 'title_jp': title_jp, 'title_vi': title_vi})
@members_required
def modules(request):
    module = Module.objects.all().order_by('-created_at')
    for i in module:
        if i.has_translation('vi'):
            i.module_vi = i.get_translation('vi').module
        else:
            i.module_vi = None
        if i.has_translation('ja'):
            i.module_ja = i.get_translation('ja').module
        else:
            i.module_ja = None
    if request.method == 'POST':
        if request.POST['submit'] == 'add':
            module = Module.objects.create(module=request.POST['module'], created_by=request.user)
            module.save()
            messages.success(request, 'Module created successfully')
            return redirect('/members/courses/module')
        if request.POST['submit'] == 'update':
            module = Module.objects.get(id=request.POST['id'])
            module.module = request.POST['module_en']
            module.save()
            module.set_current_language('ja')
            module.module = request.POST['module_ja']
            module.save()
            module.set_current_language('vi')
            module.module = request.POST['module_vi']
            module.save()
            messages.success(request, 'Module updated successfully')
            return redirect('/members/courses/module')
    return render(request, 'member/tem/modules.html', {'modules': module})
@members_required
def module_delete(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        messages.error(request, 'Module not found')
        return redirect('/members/courses/module')
    module.delete()
    messages.success(request, 'Module deleted successfully')
    return redirect('/members/courses/module')
@members_required
def profile(request):
    total_projects = Project.objects.filter(author=request.user).count()
    total_news = News.objects.filter(author=request.user).count()
    total_courses = Course.objects.filter(author=request.user).count()
    usr = CustomUser.objects.get(id=request.user.id)
    form = UserChangeForm(request.POST or None, instance=usr)
    error = None
    if request.session.get('error'):
        error = request.session['error']['email'][0]
        request.session['error'] = None
    if request.method == 'POST':
        if request.POST['type'] == 'profile':
            if form.is_valid():
                usr.first_name = form.cleaned_data['first_name']
                usr.last_name = form.cleaned_data['last_name']
                usr.email = form.cleaned_data['email']
                usr.phone_number = form.cleaned_data['phone_number']
                if request.POST.getlist('avatar')[0] == 'remove':
                    usr.reset_avatar()
                elif request.POST.getlist('avatar')[0] == 'changed':
                    usr.avatar = request.FILES['avatar']
                else:
                    pass
                usr.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('/members/profile') 
            else:
                request.session['error'] = form.errors
                return redirect('/members/profile')
        elif request.POST['type'] == 'password':
            if not usr.check_password(request.POST['current_password']):
                messages.error(request, 'Old password is incorrect')
                return redirect('/members/profile')
            if request.POST['new_password'] != request.POST['confirm_password']:
                messages.error(request, 'New password and confirm password do not match')
                return redirect('/members/profile')
            usr.set_password(request.POST['new_password'])
            usr.save()
            auth.login(request, usr)
            messages.success(request, 'Password updated successfully')
            return redirect('/members/profile')
    return render(request, 'member/tem/profile.html', {'total_projects': total_projects, 'total_news': total_news, 'total_courses': total_courses, 'form': form, 'error': error})
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
    all_contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'member/tem/contact.html', {'contacts': all_contacts})
@members_required
def project(request, project_id):
    all_labels = ProjectLabel.objects.all().order_by('-created_at')
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
@members_required
def translate_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('/members/projects')
    if project.author != request.user:
        messages.error(request, 'You are not the author of this project')
        return redirect('/members/projects')
    # Get project by english, japanese, vietnamese
    project_en = None
    project_jp = None
    project_vi = None
    if project.has_translation('en'):
        project_en = {
            'title': project.get_translation('en').title,
            'content': project.get_translation('en').content,
        }
    if project.has_translation('ja'):
        project_jp = {
            'title': project.get_translation('ja').title,
            'content': project.get_translation('ja').content,
        }
    if project.has_translation('vi'):
        project_vi = {
            'title': project.get_translation('vi').title,
            'content': project.get_translation('vi').content,
        }
    if request.method == 'POST':
        project.set_current_language('en')
        project.title = request.POST['title_en']
        project.content = request.POST['content_en']
        project.set_current_language('ja')
        project.title = request.POST['title_jp']
        project.content = request.POST['content_jp']
        project.set_current_language('vi')
        project.title = request.POST['title_vi']
        project.content = request.POST['content_vi']
        project.save()
        messages.success(request, 'Project translated successfully')
        return redirect('/members/projects')
    return render(request, 'member/tem/translate_project.html', {'project_en': project_en, 'project_jp': project_jp, 'project_vi': project_vi})

