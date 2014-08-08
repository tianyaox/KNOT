from django.test import Client
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *
from Permission.models import *
import random




def testSearchHtml():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)


	relations = FriendRelation.objects.order_by('time').filter(user=user)
	friends = [relation.friend for relation in relations]
	print friends

	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/search/',{})
	print response.content
	print '---------------'		


def testContactsHtml():
	# user = User.objects.order_by('?')[0]
	user = User.objects.get(id=488)
	print 'User ' + str(user.username) + ' ' + str(user.id)


	permissionTemplate = PermissionTemplate.objects.filter(user=user)[random.randint(0,3)]

	print 'PermissionTemplate ' + str(permissionTemplate.name) + ' ' + str(permissionTemplate.id)

	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/contacts/'+permissionTemplate.name,{})
	print response.content
	print '---------------'		


def testOtherHtml():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')


	print 'getFriendTestCase'	
	print '---------------'	
	relation = FriendRelation.objects.filter(user=user)[0]
	print relation.permission
	print relation.friend
	print PermissionTemplate.getPermissionSectionNames(relation.permission)
	content={}
	response=client.post('/otherCard/'+str(relation.friend.id),content)
	print response.content
	print '---------------'	

	print 'getStrangerTestCase'	
	print '---------------'	
	relations = FriendRelation.objects.order_by('time').filter(user=user)
	friendIDs = [relation.friend.id for relation in relations]
	stranger = User.objects.order_by('?').exclude(id__in=friendIDs)[0]
	content={}
	response=client.post('/otherCard/'+str(stranger.id),content)
	print response.content
	print '---------------'	



def testMyCardHtml():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')


	content={}
	response=client.post('/myCard/',content)
	print response.content
	print '---------------'	


def testSearchCard(name='A', gender='F'):
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	client = Client()
	client.login(username=user.username,password='12345')


	conditions = ['name', 'age', 'mutualFriend']


	relations = FriendRelation.objects.filter(user=user)

	cards = []
	for relation in relations:
		friend = relation.friend
		card = Card.objects.get(user=friend)
		card = card.getCardWithPermission(relation.permission)
		cards.append(card)


	testName
	relations = FriendRelation.objects.filter(user=user)
	for relation in relations:
		print 'Friend '+ str(relation.friend.username)+' '+ str(relation.friend.id)

	condition1 = ['name']
	response=client.post('/searchCard/',{'conditions':condition1, 'name':name, 'range':'friends'})
	print response.content
	print '---------------'	

	#testGender
	condition2 = ['gender']
	if random.randint(0,99)%2==0:
		gender='F'
	else:
		gender='M'

	relations = FriendRelation.objects.filter(user=user)

	cards = []
	for relation in relations:
		friend = relation.friend
		card = Card.objects.get(user=friend)
		card = card.getCardWithPermission(relation.permission)
		cards.append(card)

	for card in cards:
		print 'Friend '+ str(card.firstName)+' '+ str(card.lastName)+' '+str(card.gender)


	response=client.post('/searchCard/',{'conditions':condition2, 'gender':gender, 'range':'friends'})
	print response.content
	print '---------------'	

	# #testMutualFriend
	condition3 = ['mutualFriend']
	user1 = FriendRelation.objects.filter(user=user)[0].friend
	user2 = FriendRelation.objects.filter(user=user)[1].friend


	for card in cards:
		print 'Friend '+ str(card.firstName)+' '+ str(card.lastName)+' '+str(card.birthday)
	print 'Mutual Friend ' + str(user1.username) + ' ' + str(user1.id)
	print 'Mutual Friend ' + str(user2.username) + ' ' + str(user2.id)
	# print response.content


	response=client.post('/searchCard/',{'conditions':condition3, 'mutualFriend1':user1.username, 'mutualFriend2':user2.username, 'range':'friends'})
	print response.content
	print '---------------'	

	#testAge
	condition4 = ['age']
	ageMin = 30
	ageMax = 50

	for card in cards:
		print 'Friend '+ str(card.firstName)+' '+ str(card.lastName)+' '+str(card.birthday)

	response=client.post('/searchCard/',{'conditions':condition4, 'ageMin':ageMin, 'ageMax':ageMax, 'range':'friends'})
	print response.content
	print '---------------'	





def testCheckUpdateCard():
	user = User.objects.order_by('?')[0]
	card = Card.objects.get(user=user)

	client = Client()
	client.login(username=user.username,password='12345')

	print 'User ' + str(user.username) + ' ' + str(user.id)
	relations = FriendRelation.objects.filter(user=user)
	for relation in relations:
		print 'Friend '+ str(relation.friend.username)+' '+ str(relation.friend.id)


	content = {}
	sections = Card.getSections()
	for section in sections:
		content[section] = getattr(card, section)

	content['title'] = content['title']+'123'

	response=client.post('/updateMyCard/',content)
	print response.content
	print '---------------'		