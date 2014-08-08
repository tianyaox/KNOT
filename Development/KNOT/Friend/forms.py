from django import forms
from django.contrib.auth.models import User
from Friend.models import *


class FriendForm(forms.Form):
	userName = forms.CharField(label='userName', error_messages={'required':'User name is reqiured'})
	friendName = forms.CharField(label='friendName', error_messages={'required':'Friend name is reqiured'})

	def clean_userName(self):
		userName=self.cleaned_data['userName']
		if len(User.objects.filter(username=userName))==0:
			raise forms.ValidationError("User does not exist")
		return userName

	def clean_friendName(self):
		friendName=self.cleaned_data['friendName']
		if len(User.objects.filter(username=friendName))==0:
			raise forms.ValidationError("Friend does not exist")
		return friendName