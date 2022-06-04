from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    Post creation/modification form
    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'summary')

        widgets={
            "title":forms.TextInput(attrs={
                "id":"title",
                "placeholder":"Title",
                "name":"title",
                "class":'form-control',
            }),
            "content":forms.TextInput(attrs={
                "id":"content",
                "placeholder":"Your text",
                "name":"username",
                "class":'form-control',
                "style":'height:250px;',
            }),
            "summary":forms.TextInput(attrs={
                "id":"summary",
                "placeholder":"Your summary text (250 symbols)",
                "name":"summary",
                "class":'form-control',
                "style":'height:100px;',
            }),
        }