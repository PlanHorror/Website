from django.db import models
from django.contrib.auth.models import AbstractUser
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
# Create your models here.
# CustomUser model is created by extending AbstractUser model
class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)
    def __str__(self):
        return self.username
# Label model is created to store the labels created by the user
class Label(TranslatableModel):
    translation = TranslatedFields(
        name = models.TextField(_('Name'), unique=True)
    )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
# Project model is created to store the projects created by the user
class Project(TranslatableModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    label = models.ManyToManyField(Label, blank=True, null=True)
    translation = TranslatedFields(
        title = models.TextField(_('Title')),
        content = models.TextField(_('Content'))
    )
    image = models.ImageField(upload_to='pj-images/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
# News model is created to store the news created by the user
class News(TranslatableModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    label = models.ManyToManyField(Label)
    translation = TranslatedFields(
        title = models.TextField(),  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
# NewsContent model is created to store the content of the news
class NewsContent(TranslatableModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    translation = TranslatedFields(
        content = models.TextField()
    )
    num = models.IntegerField()
    def __str__(self):
        return self.content
# NewsImage model is created to store the images of the news
class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news-images/')
    num = models.IntegerField()
    def __str__(self):
        return self.image.name
# Comment model is created to store the comments created by the user
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
# Course model is created to store the courses created by the user
class Course(TranslatableModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    translation = TranslatedFields(
        title = models.TextField()
    )
    module = models.ManyToManyField('Module', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Module(TranslatableModel):
    translation = TranslatedFields(
        module = models.TextField(unique=True)
    )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.module