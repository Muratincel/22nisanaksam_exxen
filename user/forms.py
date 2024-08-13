from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            field.help_text = ""


class ConfirmDeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(label="Are you sure you want to delete your account?")
