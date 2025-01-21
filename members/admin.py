from django.contrib import admin
from .models import CustomUser, Project, Comment, Label, News, NewsContent, NewsImage, Course, CourseContent, CourseImage
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Label)
admin.site.register(News)
admin.site.register(NewsContent)
admin.site.register(NewsImage)
admin.site.register(Course)
admin.site.register(CourseContent)
admin.site.register(CourseImage)
# Make CustomUser at Authentication and Authorization in the admin site

