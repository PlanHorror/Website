from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# CustomUser model is created by extending AbstractUser model
class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)
    def __str__(self):
        return self.username
# Label model is created to store the labels created by the user
class Label(models.Model):
    name = models.TextField(unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
# Project model is created to store the projects created by the user
class Project(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.TextField()
    label = models.ManyToManyField(Label, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
# News model is created to store the news created by the user
class News(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.TextField()
    label = models.ManyToManyField(Label)   
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
# NewsContent model is created to store the content of the news
class NewsContent(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    num = models.IntegerField()
    def __str__(self):
        return self.content
# NewsImage model is created to store the images of the news
class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    num = models.IntegerField()
    def __str__(self):
        return self.image
# Comment model is created to store the comments created by the user
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
# Course model is created to store the courses created by the user
class Course(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.TextField()
    label = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
# CourseContent model is created to store the content of the course
class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    num = models.IntegerField()
    def __str__(self):
        return self.content
# CourseImage model is created to store the images of the course
class CourseImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    num = models.IntegerField()
    def __str__(self):
        return self.image