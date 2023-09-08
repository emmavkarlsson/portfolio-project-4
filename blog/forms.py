from .models import Comment, Post, Profile
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    """
    Form for users to add comments on posts
    """
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    """
    Form for users to post their own photos
    """
    class Meta:
        model = Post
        fields = ('title', 'photopost', 'description')


class ProfilePictureForm(forms.ModelForm):
    """
    Form for name and profile image update
    """
    class Meta:
        model = Profile
        fields = ['profile_picture', ]