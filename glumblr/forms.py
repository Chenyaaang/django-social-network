from django import forms
from django.contrib.auth.models import User
from glumblr.models import *


# form 是接收用户输入的
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not cleaned_data.get('username'):
            raise forms.ValidationError('Please enter username')
        if not cleaned_data.get('password'):
            raise forms.ValidationError('Please enter password')
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username')
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')
    email = forms.CharField(max_length=50, label='Email')
    password1 = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password did not match')
        return cleaned_data
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User_profile.objects.filter(username=username).count()>0:
            raise forms.ValidationError('Username %s has already exists' % username)
        return username
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User_profile.objects.filter(email=email).count()>0:
    #         raise forms.ValidationError('email %s has already been used' % email)
    #     return email
class ForgetPasswordForm(forms.Form):
    email = forms.CharField(max_length=50, label='Email')

    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()
        email = self.cleaned_data.get('email')
        if not email or len(email) == 0:
            raise forms.ValidationError('Type in an email')
        return cleaned_data

class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(max_length=100, label='New Password', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('password did not match')
        return cleaned_data

class MessageForm(forms.Form):
    message = forms.CharField(max_length=42)
    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        message = self.cleaned_data.get('message')
        if not message or len(message) == 0:
            raise forms.ValidationError('Type in a message')
        if len(message) > 42:
            raise forms.ValidationError('The message should not be longer than 42 characters')
        return cleaned_data


# class Edit_profileForm(forms.Form):
#     username = forms.CharField(max_length=50, label='Username')
#     first_name = forms.CharField(max_length=50, label='First Name')
#     last_name = forms.CharField(max_length=50, label='Last Name')
#     age = forms.CharField(max_length=10, label='Age')
#     location = models.CharField(max_length=50)
#     job = models.CharField(max_length=50)
#     img_url = models.CharField(max_length=50)
#
#     self_intro = models.CharField(max_length=420)
#     def clean(self):
#         cleaned_data = super(Edit_profileForm, self).clean()
#
#         return cleaned_data


class User_profileForm(forms.ModelForm):
    class Meta:
        model = User_profile
        # fields = '__all__'
        exclude = ('friends', 'confirm', 'token_reg', 'password', 'token_reset', 'email')
        widgets = {'picture': forms.FileInput()}
