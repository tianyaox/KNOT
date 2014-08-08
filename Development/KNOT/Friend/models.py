from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FriendRelation(models.Model):
	#user
	user = models.ForeignKey(User,related_name="user")
	#friend
	friend = models.ForeignKey(User,related_name="friend")
	# Used to define the permission from user1 to user2
	permission = models.CharField(max_length=100)
	# time = models.DateTimeField(auto_now=True)
	time = models.DateTimeField(auto_now=False)

	def __unicode__(self):
		return self.user.username +" --> "+self.friend.username+ ": "+self.permission



#permission meanging
# 1 name
# 2 gender
# 3 title
# 4 birthday
# 5 citizenship
# 6 - 10 email
# 11 - 15 address
# 16 - 20 telephone
# .... social network TBD




class FriendRequest(models.Model):
	fromUser = models.ForeignKey(User,related_name="friendReqFrom")
	toUser = models.ForeignKey(User,related_name="friendReqTo")
	confirmation = models.BooleanField(default=False)
	time = models.DateTimeField(auto_now_add=False)

	def __unicode__(self):
		return "From " + self.fromUser.username +\
			" to " + self.toUser.username