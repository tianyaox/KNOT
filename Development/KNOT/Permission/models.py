from django.db import models
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *

# Create your models here.
class PermissionTemplate(models.Model):
	user = models.ForeignKey(User,related_name="permissionUser")

	name =  models.CharField(max_length=100)

	permission = models.CharField(max_length=100)

	time = models.DateTimeField(auto_now=False)

	def __unicode__(self):
		return self.user.username +" --> "+self.name+ ": "+self.permission

	#permission meanging
	# 0 firstName
	# 1 lastName
	# 2 gender
	# 3 title
	# 4 birthday
	# 5 citizenship
	# 6 - 10 email
	# 11 - 15 address
	# 16 - 20 telephone
	# .... social network TBD

	@staticmethod
	def getPermissionSections():
		return Card.getSections()

	@staticmethod
	def getPermissionSectionNames(permission):
		names=[]
		permissionSections=PermissionTemplate.getPermissionSections()
		for i in range(len(permissionSections)):
			if permission[i]=='+':
				names.append(permissionSections[i])
		return names

	@staticmethod
	def generatePermissionStr(pType, allowedSections=None):
		permissionSections=PermissionTemplate.getPermissionSections()


		# only use for friend not use in friendrelationship
		if pType=='stranger':
			allowedSections=['firstName','lastName','gender','birthday','city1','imageURL','soundURL']
		elif pType=='friend':
			allowedSections=['firstName','lastName','gender','birthday','city1','email1','phone1','address1','facebook','twitter','imageURL','soundURL']
		elif pType=='classmate':
			allowedSections=['firstName','lastName','gender','birthday','city1','email1','imageURL','soundURL']
		elif pType=='family':
			allowedSections=['firstName','lastName','gender','birthday','city1','email1','phone1','address1','imageURL','soundURL']
		elif pType=='god':
			allowedSections=PermissionTemplate.getPermissionSections()
		elif pType == 'custom':
			allowedSections=allowedSections

		permissionStr = ''
		for section in permissionSections:
			if section in allowedSections:
				permissionStr = permissionStr + '+'
			else:
				permissionStr = permissionStr + '-'

		return permissionStr

	@staticmethod
	def getPermissionTemplateName(user, permission):
		templateName = 'unknown'
		permissionTemplates = PermissionTemplate.objects.filter(user=user)
		for permissionTemplate in permissionTemplates:
			if permissionTemplate.permission == permission:
				templateName = permissionTemplate.name
				break

		return templateName


class PermissionTemplateEncoder(json.JSONEncoder):
	def default(self, obj):
		dic={}
		try:
			if isinstance(obj, PermissionTemplate):
				dic['id'] = obj.id
				dic['user'] = obj.user.username
				dic['name'] = obj.name
				dic['permission'] = PermissionTemplate.getPermissionSectionNames(obj.permission)
				return dic
			else:
				print 'EncoderError'
		except Exception, e:
			print str(e)
