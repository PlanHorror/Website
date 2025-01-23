from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    # path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('courses/', views.course, name='courses'),
    # path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('projects/', views.project, name='projects'),
    # path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('collaboration/', views.collaboration, name='collaboration'),
    
] 