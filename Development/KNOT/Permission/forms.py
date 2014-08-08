from django import forms
from django.contrib.auth.models import User
from Permission.models import *

class PermissionTemplateForm(forms.Form):
	name = forms.CharField(label='name', error_messages={'required':'Template name is reqiured'})
	permission = forms.CharField(label='permission', error_messages={'required':'Permission is reqiured'})


	def __init__(self, user, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self._user=user;


	def clean_name(self):
		user = self._user
		name = self.cleaned_data['name']
		permissionTemplate = PermissionTemplate.objects.filter(user=user, name=name)

		if len(permissionTemplate)>0:
			raise forms.ValidationError("Name has already existed")
		return userName

	def clean_permission(self):
		user = self._user
		permission = self.cleaned_data['permission']
		permissionTemplate = PermissionTemplate.objects.filter(user=user, permission=permission)

		if len(permissionTemplate)>0:
			raise forms.ValidationError("Permission level has already existed")
		return userName
