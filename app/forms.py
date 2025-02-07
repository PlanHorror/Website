from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from members.models import *
# Create a form for user registration with CustomUser model
class UserRegisterForm(UserCreationForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2','avatar']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'
            if field_name != 'avatar' and field_name != 'first_name' and field_name != 'last_name':
                print(field_name)
                field.required = True
            if field_name == 'avatar':
                field.widget.attrs['class'] = 'custom-file-input'
            
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        