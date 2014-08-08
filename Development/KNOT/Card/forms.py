from django import forms
from django.contrib.auth.models import User
from Card.models import *
import pdb

class CardForm(forms.Form):
	firstName = forms.CharField(label='firstName', required=False)
	lastName = forms.CharField(label='lastName', required=False)
	gender = forms.CharField(label='gender', required=False)
	title = forms.CharField(label='title', required=False)
	birthday = forms.DateField(label='birthday', required=False)
	citizenship = forms.CharField(label='citizenship', required=False)


	address1 = forms.CharField(label='address1', required=False)
	address2 = forms.CharField(label='address2', required=False)
	address3 = forms.CharField(label='address3', required=False)
	address4 = forms.CharField(label='address4', required=False)
	address5 = forms.CharField(label='address5', required=False)

	#city
	city1 = forms.CharField(label='city1', required=False)
	city2 = forms.CharField(label='city2', required=False)
	city3 = forms.CharField(label='city3', required=False)
	city4 = forms.CharField(label='city4', required=False)
	city5 = forms.CharField(label='city5', required=False)

	phone1 = forms.CharField(label='phone1', required=False)
	phone2 = forms.CharField(label='phone2', required=False)
	phone3 = forms.CharField(label='phone3', required=False)
	phone4 = forms.CharField(label='phone4', required=False)
	phone5 = forms.CharField(label='phone5', required=False)


	email1 = forms.EmailField(label='email1', required=False, error_messages = {'invalid': 'Work email address is not vaild'})
	email2 = forms.EmailField(label='email2', required=False, error_messages = {'invalid': 'Private email address is not vaild'})
	email3 = forms.EmailField(label='email3', required=False, error_messages = {'invalid': 'Email3 address is not vaild'})
	email4 = forms.EmailField(label='email4', required=False, error_messages = {'invalid': 'Email4 email address is not vaild'})
	email5 = forms.EmailField(label='email5', required=False, error_messages = {'invalid': 'Email5 email address is not vaild'})

	blog = forms.CharField(label='blog', required=False)

	def clean(self):
		cleanDatas = super(CardForm, self).clean()
		for key, value in cleanDatas.iteritems():
			if key == 'birthday':
				continue
			if '<script>' in value:
				raise forms.ValidationError(key + ' contains illegal content javascript code')

