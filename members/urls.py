from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('projects/', views.projects, name='projects'),
    # path('projects/<int:project_id>/', views.project, name='project'),
    # path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    # path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('news/', views.news, name='news'),
    # path('news/<int:news_id>/', views.news_item, name='news_item'),
    # path('news/<int:news_id>/edit/', views.edit_news_item, name='edit_news_item'),
    # path('news/<int:news_id>/delete/', views.delete_news_item, name='delete_news_item'),
    path('courses/', views.courses, name='courses'),
    # path('courses/<int:course_id>/', views.course, name='course'),
    # path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    # path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('message/', views.message, name='messages'),
]