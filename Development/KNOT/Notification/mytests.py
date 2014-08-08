from django.test import Client
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *
import random

def testGetNotification():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')

	response=client.get('/getNotification/all')
	print response.content	
	print '------------------'

	response=client.get('/getNotification/2')
	print response.content	
	print '------------------'

 


def testDeleteNotification():
	user = User.objects.order_by('?')[0]
	print 'User ' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')	

	notification = Notification.objects.order_by('?')[0]

	print 'Notification ' + str(notification.id) + str(notification.toUser.username)

	response=client.post('/deleteNotification/',{'notificationID':notification.id})
	print response.content	
	print '------------------'