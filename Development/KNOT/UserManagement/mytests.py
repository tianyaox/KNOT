from django.test import Client
from django.contrib.auth.models import User
import random

def testRegister():
	#normal case
	client = Client()
	response=client.post('/register/',{'username':'wenbingBAI','email':'email@gmail.com','password1':'12345','password2':'12345'})
	print response.content
	print '---------------'

	#username has been taken
	client = Client()
	response=client.post('/register/',{'username':'wenbingBAI','email':'email@gmail.com','password1':'12345','password2':'12345'})
	print response.content
	print '---------------'

	#invalid email address
	client = Client()
	response=client.post('/register/',{'username':'BAI','email':'email','password1':'12345','password2':'12345'})
	print response.content
	print '---------------'

	#password does not match
	client = Client()
	response=client.post('/register/',{'username':'BAI','email':'email@gmail.com','password1':'1234','password2':'12345'})
	print response.content
	print '---------------'
	