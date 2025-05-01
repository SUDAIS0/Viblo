from django import forms
from .models import Video, User, Comment

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Video Description'}),
        }

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email                                                                                ', 'password']:
            self.fields[fieldname].help_text = None

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'oninput': 'autoResize(this)', 'style': 'overflow:hidden; resize:none;'})
        }