from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='mindex'),
    path('login/', views.login, name='mlogin'),
    path('logout/', views.logout, name='mlogout'),
    path('projects/', views.projects, name='mprojects'),
    path('projects/<int:project_id>/', views.project, name='mproject'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='del_project'),
    path('projects/labels', views.project_labels, name='mproject_labels'),
    path('projects/labels/<int:label_id>/delete/', views.project_label_delete, name='del_project_label'),
    path('news/', views.news, name='mnews'),
    path('news/create/', views.create_news, name='mcreate_news'),
    path('news/<int:new_id>/', views.new, name='mnew'),
    path('news/<int:new_id>/delete/', views.delete_news_item, name='del_news'),
    path('news/labels', views.new_labels, name='mnews_labels'),
    path('news/labels/<int:label_id>/delete/', views.new_label_delete, name='del_new_label'),
    path('courses/', views.courses, name='mcourses'),
    path('courses/module', views.modules, name='mmodule'),
    path('courses/module/<int:module_id>/delete/', views.module_delete, name='del_module'),
    path('courses/<int:course_id>/', views.course, name='mcourse'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='del_course'),
    path('contact/', views.contact, name='mcontact'),
]