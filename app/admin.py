from django.contrib import admin

from app.models import Comment, EmailSend, Post, ProfileUser

# Register your models here.

admin.site.register(ProfileUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(EmailSend)