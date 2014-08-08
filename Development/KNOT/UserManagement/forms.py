from django import forms
from Card.models import *
from django.db.models import Q
import pdb


class RegisterForm(forms.Form):
	username=forms.CharField(label='User Name', error_messages={'required':'User name is required'})
	email=forms.EmailField(label='Email', error_messages={'required':'Email is required'})
	password1=forms.CharField(label='Password1', error_messages={'required':'Password is required'})
	password2=forms.CharField(label='Password2', error_messages={'required':'Confirm password is required'})

	def clean_email(self):
		email=self.cleaned_data['email']
		if len(User.objects.filter(email = email))>0:
			raise forms.ValidationError("Email has already been taken")
		return email

	def clean_username(self):
		username=self.cleaned_data['username']
		if len(User.objects.filter(username=username))>=1:
			raise forms.ValidationError("Username has already been taken")
		if ' ' in username:
			raise forms.ValidationError("Username cannot contain space")
		return username

	def clean_password2(self):
		password1=None
		if 'password1' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			
		password2=self.cleaned_data['password2']
		if(password1!=password2):
			raise forms.ValidationError("Passwords are not match")
		return password1

class GuideEmailForm(forms.Form):
	email = forms.EmailField(label='Email', required=False)

class ChangePwForm(forms.Form):
	password0=forms.CharField(label='Password0', error_messages={'required':'Current Password is required'})
	password1=forms.CharField(label='Password1', error_messages={'required':'Password is required'})
	password2=forms.CharField(label='Password2', error_messages={'required':'Confirm password is required'})

	def __init__(self, user, *args, **kwargs):
		super(ChangePwForm, self).__init__(*args, **kwargs)
		self._user=user;

	def clean_password2(self):
		password1=None
		if 'password1' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			
		password2 = self.cleaned_data['password2']
		if password1!=password2:
			raise forms.ValidationError("Passwords are not match")
		return password1

	def clean_password0(self):
		password=self.cleaned_data['password0']
		if self._user.check_password(password)!=True:
			raise forms.ValidationError("Current Password is not correct")
		return password
