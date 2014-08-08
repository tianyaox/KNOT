from django.test import Client
from django.contrib.auth.models import User
from Friend.models import *
from Notification.models import *
from Permission.models import *
import random



def testRecommendFriend():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')

	# normal case
	relations = FriendRelation.objects.filter(user=user)
	for relation in relations:
		print relation.friend.username
		
	response=client.post('/recommendFriend/'+user.username,{})
	print response.content
	print '---------------'	

	# user not exist


def testAddFriend():
	toUser = None
	fromUser = None
	while True:
		toUser = User.objects.order_by('?')[0]
		if(len(Notification.objects.filter(toUser=toUser, nType=4))>0):
			fromUser = Notification.objects.filter(toUser=toUser, nType=4)[0].fromUser
			break


	print 'FromUser ' + str(fromUser.username) + ' ' + str(fromUser.id)
	print 'ToUser ' + str(toUser.username) + ' ' + str(toUser.id)

	client = Client()
	client.login(username=toUser.username,password='12345')

	# normal case
	response=client.post('/addFriend/',{'friendID':fromUser.id})
	print response.content
	print '---------------'

	# user not exist case


	# friend not exist case
	response=client.post('/addFriend/',{'friendID':'qqq'})
	print response.content
	print '---------------'

	# both not exist case

def testDeleteFriend():
	user = None
	friend = None

	while True:
		user = User.objects.order_by('?')[0]
		if(len(FriendRelation.objects.filter(user=user))>0):
			friend = FriendRelation.objects.filter(user=user)[0].friend
			break	

	print 'User' + str(user.username) + ' ' + str(user.id)
	print 'Friend' + str(friend.username) + ' ' + str(friend.id)

	client = Client()
	client.login(username=user.username,password='12345')

	# normal case
	response=client.post('/deleteFriend/',{'friendID':friend.id})
	print response.content
	print '---------------'

	#friend not exist
	response=client.post('/deleteFriend/',{'friendID':"AAA"})
	print response.content
	print '---------------'	

def testGetFriendList():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')

	# normal case
	response=client.post('/getFriendList/'+user.username,{})
	print response.content
	print '---------------'	

	# user not exist


def testSearchFriend(name='A', gender='F'):
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')


	conditions = ['name', 'age', 'mutualFriend']

	# testName
	response=client.post('/getFriendList/'+user.username,{})
	print response.content	

	condition1 = ['name']
	response=client.post('/searchUser/',{'conditions':condition1, 'name':name, 'range':'friend'})
	print response.content
	print '---------------'	

	#testGender
	condition2 = ['gender']
	if random.randint(0,99)%2==0:
		gender='F'
	else:
		gender='M'
	response=client.post('/searchUser/',{'conditions':condition2, 'gender':gender, 'range':'friend'})
	print response.content
	print '---------------'	

	#testMutualFriend
	condition3 = ['mutualFriend']
	user1 = FriendRelation.objects.filter(user=user)[0].friend

	response=client.post('/getFriendList/'+user.username,{})
	print 'User' + str(user.username) + ' ' + str(user.id)
	print response.content
	# response=client.post('/getFriendList/'+user1.username,{})
	print 'User1' + str(user1.username) + ' ' + str(user1.id)
	# print response.content


	response=client.post('/searchUser/',{'conditions':condition3, 'mutualFriend':user1.username, 'range':'stranger'})
	print response.content
	print '---------------'	


def testAddFriendRequest():
	user = User.objects.order_by('?')[0]

	client = Client()
	client.login(username=user.username,password='12345')

	toUser = User.objects.exclude(id = user.id)[0]

	print 'fromUser ' + str(user.username) + ' ' + str(user.id)
	print 'toUser ' + str(toUser.username) + ' ' + str(toUser.id)

	response=client.post('/addFriendRequest/',{'friendID':toUser.id})
	print response.content
	print '---------------'	


def testUpdateFriendPermission():
	user = User.objects.order_by('?')[0]
	print 'User ' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')

	relations = FriendRelation.objects.filter(user=user)
	relation = relations[0]
	friend = relation.friend
	print 'Friend ' + str(friend.username) + ' ' + str(friend.id)
	print 'TemplateName '+ str(PermissionTemplate.getPermissionTemplateName(user,relation.permission))

	response=client.post('/updateFriendPermission/',{'friendID':friend.id, \
	'permissionName':PermissionTemplate.getPermissionTemplateName(user,relation.permission)})
	print response.content
	print '---------------'		


