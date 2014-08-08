from django.test import Client
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *
from Permission.models import *
import random

def testAddPermissionTemplate():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	# normal case
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/addPermissionTemplate/',{'name':'test12','sharedSection1':'email1','sharedSection2':'phone1'})
	print response.content
	print '---------------'	

	# name exist case	
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/addPermissionTemplate/',{'name':'friend','sharedSection1':'email3','sharedSection2':'phone1'})
	print response.content
	print '---------------'	

	# permission exist case	
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/addPermissionTemplate/',{'name':'test13','sharedSection1':'email1','sharedSection2':'phone1'})
	print response.content
	print '---------------'	


def testUpdatePermissionTemplate():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	permissionTemplate = PermissionTemplate.objects.filter(user=user)[0]
	print 'Template' + str(permissionTemplate.user.username)+' '+str(permissionTemplate.name)

	# normal case update name
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/updatePermissionTemplate/',{'templateID':str(permissionTemplate.id),'name':'updateTest','sharedSection1':'firstName','sharedSection2':'lastName','sharedSection3':'phone1'})
	print response.content
	print '---------------'	


	# normal case update permission
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/updatePermissionTemplate/',{'templateID':str(permissionTemplate.id),'name':'updateTest','sharedSection1':'firstName','sharedSection2':'lastName','sharedSection3':'phone2'})
	print response.content
	print '---------------'	

	# normal case update name and permission
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/updatePermissionTemplate/',{'templateID':str(permissionTemplate.id),'name':'updateTestAll','sharedSection1':'firstName'})
	print response.content
	print '---------------'	

	# boundary case name exist
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/updatePermissionTemplate/',{'templateID':str(permissionTemplate.id),'name':'stranger','sharedSection1':'firstName'})
	print response.content
	print '---------------'		

	# boundary case permission exist
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/updatePermissionTemplate/',{'templateID':str(permissionTemplate.id),'name':'zzz','sharedSection1':'firstName','sharedSection2':'lastName'})
	print response.content
	print '---------------'	


def testDeletePermissionTemplate():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	permissionTemplate = PermissionTemplate.objects.filter(user=user)[0]
	print 'Template' + str(permissionTemplate.user.username)+' '+str(permissionTemplate.name)

	#normal case
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/deletePermissionTemplate/',{'templateID':str(permissionTemplate.id)})
	print response.content
	print '---------------'	

def testPermissionTemplateHtml():
	user = User.objects.order_by('?')[0]
	print 'User' + str(user.username) + ' ' + str(user.id)

	#normal case
	client = Client()
	client.login(username=user.username,password='12345')
	response=client.post('/getPermissionTemplate/',{})
	print response.content
	print '---------------'	