from django.db import models
from django.contrib.auth.models import AbstractUser
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
# Create your models here.
# CustomUser model is created by extending AbstractUser model
class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='user-avatars/', default='user-avatars/default.jpg')
    email = models.EmailField(unique=True, blank=False)
    def __str__(self):
        return "User id: " + str(self.pk) + " - Username: " + self.username + " - Email: " + self.email
# Label model is created for projects to store the labels created by the user
class ProjectLabel(TranslatableModel):
    translation = TranslatedFields(
        name = models.TextField(_('Name'), unique=True)
    )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Label id: " + str(self.pk) + " - Name: " + self.name + " - Created by: " + self.created_by.username
# Label model is created for news to store the labels created by the user
class NewsLabel(TranslatableModel):
    translation = TranslatedFields(
        name = models.TextField(_('Name'), unique=True)
    )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Label id: " + str(self.pk) + " - Name: " + self.name + " - Created by: " + self.created_by.username
# Project model is created to store the projects created by the user
class Project(TranslatableModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    label = models.ManyToManyField("ProjectLabel", blank=True, related_name='plabel')
    translation = TranslatedFields(
        title = models.TextField(_('Title')),
        content = models.TextField(_('Content'))
    )
    image = models.ImageField(upload_to='pj-images/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Project id: " + str(self.pk) + " - Title: " + self.title + "- Author: " + self.author.username
# News model is created to store the news created by the user
class News(TranslatableModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    label = models.ManyToManyField("NewsLabel", blank=True, related_name='nlabel')
    translation = TranslatedFields(
        title = models.TextField(),  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "News id: " + str(self.pk) + " - Title: " + self.title
# NewsContent model is created to store the content of the news
class NewsContent(TranslatableModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    translation = TranslatedFields(
        content = models.TextField()
    )
    num = models.IntegerField()
    def __str__(self):
        return  "News id: " + str(self.news.pk) + " - Num: "+ str(self.num)
# NewsImage model is created to store the images of the news
class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news-images/')
    num = models.IntegerField()
    def __str__(self):
        return "News id: " + str(self.news.pk) + " - Num: "+ str(self.num) + " - Image: " + self.image.url
# Comment model is created to store the comments created by the user
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Comment id: " + str(self.pk) + " - Author: " + self.author.username + " - News id: " + self.news.pk
# Course model is created to store the courses created by the user
class Course(TranslatableModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    translation = TranslatedFields(
        title = models.TextField()
    )
    url = models.URLField()
    module = models.ManyToManyField('Module', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Course id: " + str(self.pk) + " - Title: " + self.title + "- Author: " + self.author.username
# Module model is created to store the modules created by the user, modules are the labels of the courses
class Module(TranslatableModel):
    translation = TranslatedFields(
        module = models.TextField(unique=True)
    )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Module id: " + str(self.pk) + " - Module: " + self.module + " - Created by: " + self.created_by.username
class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    c_type = models.CharField(max_length=20, choices=[('project', 'Project'), ('news', 'News'), ('course', 'Course'), ('other', 'Other')])
    project_obj = models.ManyToManyField(Project, blank=True)
    news_obj = models.ManyToManyField(News, blank=True)
    course_obj = models.ManyToManyField(Course, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Contact id: " + str(self.pk) + " - Name: " + self.user.username + " - Type: " + self.c_type 