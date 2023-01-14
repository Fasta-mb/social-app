

from argparse import _ExtendAction
from django import forms

from app.models import Comment, EmailSend, Post, ProfileUser
from django.utils.translation import gettext_lazy as _



class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ('image', 'description',)
        widgets = {
            'description': forms.Textarea(attrs={'maxlength': '200'})
        }
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'title', 'description')
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': _("")}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['placeholder'] = 'Add a comment'
        self.fields['body'].widget.attrs['class'] = 'form-control'
        
class ReportForm(forms.ModelForm):
    class Meta:
        model = EmailSend
        fields = '__all__'