from django import forms
from .models import User

class UserForm(forms.ModelForm):
    """

    User registration/login form

    """
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

        widgets={
            "email":forms.EmailInput(attrs={
                "id":"email",
                "placeholder":"Email",
                "name":"email",
                "class":'form-control',
            }),
            "username":forms.TextInput(attrs={
                "id":"username",
                "placeholder":"Username",
                "name":"username",
                "class":'form-control',
            }),
            "password":forms.PasswordInput(attrs={
                "id":"password",
                "placeholder":"Password",
                "name":"password",
                "class":'form-control',
            }),
        }