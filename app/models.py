from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class ProfileUser(models.Model):
    image = models.ImageField(upload_to='images', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    image = models.ImageField(upload_to='images', null=False, blank=False)
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(max_length=120, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    picuser = models.ForeignKey(ProfileUser,on_delete=models.SET_NULL, related_name='profile', blank=True, null=True)
    
    class Meta:
        ordering = ('-created', '-updated',)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post =  models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pic = models.ForeignKey(ProfileUser,on_delete=models.SET_NULL, related_name='pic', blank=True, null=True)
    
    def __str__(self):
        return self.author.username
    
class EmailSend(models.Model):
    subject = models.CharField(max_length=120)
    message = models.CharField(max_length=320)
    email = models.EmailField()
