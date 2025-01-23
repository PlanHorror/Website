from django.shortcuts import render
from members.models import *
from django.utils.translation import gettext as _, get_language, activate
# Create your views here.
def index(request):
    # Print template root directory
    # print('Template root directory:', request.templates.dirs)
    return render(request, 'app/tem/index.html')
def about(request):
    return render(request, 'app/tem/about.html')
def contact(request):
    return render(request, 'app/tem/contact.html')
def news(request):
    news = News.objects.all()
    # Select image have num min of each news
    for n in news:
        image = NewsImage.objects.filter(news=n).order_by('num').first()
        n.image = image
    return render(request, 'app/tem/news.html', {'ns': news})
def course(request):
    courses = Course.objects.all()
    return render(request, 'app/tem/course.html', {'cr': courses})
def project(request):
    projects = Project.objects.all()
    return render(request, 'app/tem/project.html', {'pr': projects})
def collaboration(request):
    return render(request, 'app/tem/collab.html')