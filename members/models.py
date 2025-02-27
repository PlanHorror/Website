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
    phone_number = models.CharField(max_length=15, blank=True, unique=True, null=True)
    def __str__(self):
        return "User id: " + str(self.pk) + " - Username: " + self.username + " - Email: " + self.email
    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = CustomUser.objects.get(pk=self.pk)
            if orig.avatar != self.avatar and orig.avatar != 'user-avatars/default.jpg':
                orig.avatar.delete(save=False)
        super().save(*args, **kwargs)
    def reset_avatar(self):
        if self.avatar != 'user-avatars/default.jpg':
            self.avatar.delete()
            self.avatar = 'user-avatars/default.jpg'
            self.save()
        else:
            pass
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
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Project.objects.get(pk=self.pk)
            if orig.image != self.image:
                orig.image.delete(save=False)
        super().save(*args, **kwargs)
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
    def delete(self, *args, **kwargs):
        for img in self.image.all():
            img.delete()
        super().delete(*args, **kwargs)
# NewsContent model is created to store the content of the news
class NewsContent(TranslatableModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='content')
    translation = TranslatedFields(
        content = models.TextField()
    )
    num = models.IntegerField()
    def __str__(self):
        return  "News id: " + str(self.news.pk) + " - Num: "+ str(self.num)
    class Meta:
        unique_together = ('news', 'num')
# NewsImage model is created to store the images of the news
class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='news-images/')
    num = models.IntegerField()
    def __str__(self):
        return "News id: " + str(self.news.pk) + " - Num: "+ str(self.num) + " - Image: " + self.image.url
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = NewsImage.objects.get(pk=self.pk)
            if orig.image != self.image:
                orig.image.delete(save=False)
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ('news', 'num')
    
# Comment model is created to store the comments created by the user
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Comment id: " + str(self.pk) + " - Author: " + self.author.username + " - News id: " + str(self.news.pk)
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