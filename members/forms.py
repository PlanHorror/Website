from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from members.models import *
class UserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', ]
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light border-secondary'
        
