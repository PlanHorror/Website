from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='mindex'),
    path('login/', views.login, name='mlogin'),
    path('logout/', views.logout, name='mlogout'),
    path('projects/', views.projects, name='mprojects'),
    path('projects/<int:project_id>/', views.project, name='mproject'),
    # path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='del_project'),
    path('projects/labels', views.project_labels, name='mproject_labels'),
    path('projects/labels/<int:label_id>/delete/', views.project_label_delete, name='del_project_label'),
    path('news/', views.news, name='mnews'),
    path('news/create/', views.create_news, name='mcreate_news'),
    # path('news/<int:news_id>/', views.news_item, name='news_item'),
    # path('news/<int:news_id>/edit/', views.edit_news_item, name='edit_news_item'),
    # path('news/<int:news_id>/delete/', views.delete_news_item, name='delete_news_item'),
    path('courses/', views.courses, name='mcourses'),
    # path('courses/<int:course_id>/', views.course, name='course'),
    # path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    # path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('contact/', views.contact, name='mcontact'),
]