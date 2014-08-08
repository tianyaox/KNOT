from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.
class Notification(models.Model):
	fromUser = models.ForeignKey(User, related_name="fromUser")
	toUser = models.ForeignKey(User, related_name="toUser")
	content = models.CharField(max_length=200)
	time = models.DateTimeField(auto_now_add=False)
	nType = models.IntegerField(default=0)
	# 1 friend request confirmation
	# 2 card information update
	# 3 tag name update 
	# 4 friend request

	def __unicode__(self):
		return str(self.id)+' '+self.fromUser.username +": "+self.content

class NotificationEncoder(json.JSONEncoder):
	def default(self, obj):
		dic={}
		try:
			if isinstance(obj, Notification):
				dic['id']=obj.id
				dic['fromUser']=obj.fromUser.username
				dic['fromUserID']=obj.fromUser.id
				dic['toUser']=obj.toUser.username
				dic['content']=obj.content
				dic['date']=obj.time.strftime('%Y/%m/%d')
				dic['nType']=str(obj.nType)

				return dic
			else:
				print 'EncoderError'
		except Exception, e:
			print str(e)