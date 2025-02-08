from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('news/<slug:title>-<int:news_id>/', views.new, name='new'),
    path('courses/', views.course, name='courses'),
    # path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:title>-<int:project_id>/', views.project, name='project'),
    path('collaboration/', views.collaboration, name='collaboration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    # Path for JSON response
    path('get_projects/', views.get_projects, name='get_projects'),
    path('get_news/', views.get_news, name='get_news'),
    path('get_courses/', views.get_courses, name='get_courses'),
    
] 