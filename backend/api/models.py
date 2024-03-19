from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# class Interest(models.TextChoices):
#     sports = 'sports'
#     food_delivery = 'Food and Delivery'
#     tech = 'Technology'
#     fashion = 'Fashion'
#     health = 'Health'
#     gaming = 'Gaming'
#     music = 'Music'
#     books = 'Books'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    verified = models.BooleanField(default=False)
    image = models.ImageField(null=True)
    bio = models.CharField(max_length=255, null=True)
    # interest = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

class Post(models.Model):
    class DescCategory(models.TextChoices):
        edu = 'education'
        leaening = 'Learning'
        health = 'General Health'
        aka = 'Ask For Advise'
        discuss = 'General discussion'
        memes = 'Memes'
        interview = 'Interview Reviews'
        win = 'Wins'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(null=True)
    description = models.CharField(max_length=255, choices=DescCategory.choices)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post_author.title}'
    
