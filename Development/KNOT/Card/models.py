import json
from django.db import models
from django.contrib.auth.models import User
import pdb
# Create your models here.


class Card(models.Model):
	user = models.ForeignKey(User)
	firstName = models.CharField(max_length=42, blank=True)
	lastName = models.CharField(max_length=42, blank=True)
	gender = models.CharField(max_length=42, blank=True)
	title = models.CharField(max_length=200, blank=True)
	birthday = models.DateField(blank=True)
	citizenship = models.CharField(max_length=42, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	phone1 = models.CharField(max_length=42, blank=True)
	phone2 = models.CharField(max_length=42, blank=True)
	email1 = models.CharField(max_length=200, blank=True)
	email2 = models.CharField(max_length=200, blank=True)
	blog = models.CharField(max_length=200, blank=True)
	# It is planned to use facebook and twitter API to link them
	# How can facebook and twitter be stored is still not decided
	# Currently CharField is used




	#invisible section
	address3 = models.CharField(max_length=200, blank=True)
	address4 = models.CharField(max_length=200, blank=True)
	address5 = models.CharField(max_length=200, blank=True)
	phone3 = models.CharField(max_length=42, blank=True)
	phone4 = models.CharField(max_length=42, blank=True)
	phone5 = models.CharField(max_length=42, blank=True)
	email3 = models.CharField(max_length=200, blank=True)
	email4 = models.CharField(max_length=200, blank=True)
	email5 = models.CharField(max_length=200, blank=True)


	# Last modified time
	time = models.DateTimeField(auto_now=False)

	#city
	city1 = models.CharField(max_length=100, blank=True)
	city2 = models.CharField(max_length=100, blank=True)
	city3 = models.CharField(max_length=100, blank=True)
	city4 = models.CharField(max_length=100, blank=True)
	city5 = models.CharField(max_length=100, blank=True)


	#sns
	facebook = models.CharField(max_length=100, blank=True)
	twitter = models.CharField(max_length=100, blank=True)
	skype = models.CharField(max_length=100, blank=True)
	linkedin = models.CharField(max_length=200, blank=True)
	googlePlus = models.CharField(max_length=100, blank=True)	
	instagram = models.CharField(max_length=100, blank=True)
	vimeo = models.CharField(max_length=100, blank=True)
	github = models.CharField(max_length=100, blank=True)
	tumblr = models.CharField(max_length=100, blank=True)	


	#sound and avatar
	soundURL = models.CharField(max_length=200, blank=True)
	imageURL = models.CharField(max_length=200, blank=True)


	def __unicode__(self):
		return self.firstName + " " + self.lastName+" "+self.gender+" "+self.title+" "+str(self.birthday)

	@staticmethod
	def getSections():
		return ['firstName','lastName','gender','title','birthday','citizenship', 'blog',\
	'email1','email2','email3','email4','email5',\
	'address1','address2','address3','address4','address5',\
	'phone1','phone2','phone3','phone4','phone5',\
	'city1','city2','city3','city4','city5',\
	'facebook','twitter','skype','linkedin',\
	'googlePlus','instagram','vimeo','github','tumblr',\
	'soundURL','imageURL']

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
	def getPermissionSectionNames(permission):
		names=[]
		permissionSections=Card.getSections()
		for i in range(len(permissionSections)):
			if permission[i]=='+':
				names.append(permissionSections[i])
		return names

	def getCardWithPermission(self, permission):
		card = Card()
		card.user = self.user
		permissionSections=Card.getSections()

		for i in range(len(permissionSections)):
			if permission[i]=='+':
				setattr(card, permissionSections[i], getattr(self,permissionSections[i]))

		return card





class SelfDefCardColumn(models.Model):
	# allow user to add some profiles he wants
	user = models.ForeignKey(User)
	name = models.CharField(max_length=200, blank=True)
	content = models.CharField(max_length=200, blank=True)
	validate = models.BooleanField(default=True)

	# Last modified time
	time = models.DateTimeField(auto_now=False)

	def __unicode__(self):
		return self.user.username+ " " + self.name + " " + self.content



class CardEncoder(json.JSONEncoder):
	def default(self, obj):
		dic={}
		try:
			if isinstance(obj, Card):

				sections = Card.getSections()

				for section in sections:
					if getattr(obj, section)!=None:
						if section == 'user':
							dic[section]=getattr(obj, section).username
						elif section == 'birthday':
							dic[section]=getattr(obj, section).strftime('%Y-%m-%d')
						else:
							dic[section]=getattr(obj, section)

				return dic
			else:
				print 'EncoderError'
		except Exception, e:
			print str(e)
