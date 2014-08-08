from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
	user = models.ForeignKey(User)
	firstName = models.CharField(max_length=42)
	lastName = models.CharField(max_length=42)
	gender = models.CharField(max_length=42)
	title = models.CharField(max_length=42)
	birthday = models.DateField()
	citizenship = models.CharField(max_length=42)
	picture = models.ImageField(upload_to="user-profile-picture",\
		blank=True,null=True)
	address1 = models.CharField(max_length=200)
	address2 = models.CharField(max_length=200)
	phone1 = models.CharField(max_length=42)
	phone2 = models.CharField(max_length=42)
	email1 = models.CharField(max_length=42)
	email2 = models.CharField(max_length=42)
	blog = models.CharField(max_length=200)
	# It is planned to use facebook and twitter API to link them
	# How can facebook and twitter be stored is still not decided
	# Currently CharField is used
	facebook = models.CharField(max_length=42)
	twitter = models.CharField(max_length=42)

	# Last modified time
	time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.firstName + " " + self.lastName

class SelfDefProfile(models.Model):
	# allow user to add some profiles he wants
	user = models.ForeignKey(User)
	# Self-defined jsonfield as shown at last
	""" The three rows are for 
		"the list of names of the added profile"
		"the list of contents of the added profile"
		"the list of validations of the added profile".
		When a profile is deleted, its corresponding validation 
		will be set to False.
	"""
	nameList = JSONField();
	contentList = JSONField();
	validationList = JSONField();


class FriendRequest(models.Model):
	fromUser = models.ForeignKey(User,related_name="friendReqFrom")
	toUser = models.ForeignKey(User,related_name="friendReqTo")
	confirmation = models.BooleanField(default=False)
	time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "From " + self.fromUser.username +\
			" to " + self.toUser.username

class FriendRelation(models.Model):
	fromUser = models.ForeignKey(User,related_name="friendFrom")
	toUser = models.ForeignKey(User,related_name="friendTo")
	# Used to define the permission from user1 to user2
	permission = models.CharField(max_length=10)
	time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.fromUser.usernmae +" --> "self.toUser.username\
			 + ": "+self.permission


class Notification(models.Model):
	user = models.ForeignKey(User)
	content = models.CharField(max_length=200)
	time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username +": "+self.content



# Following codes are from
# https://djangosnippets.org/snippets/1478/
class JSONField(models.TextField): 
	"""JSONField is a generic textfield that neatly 
	serializes/unserializes JSON objects seamlessly"""

	# Used so to_python() is called
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
	    """Convert our string value to JSON after 
	    we load it from the DB"""

	    if value == "":
	        return None

	    try:
	        if isinstance(value, basestring):
	            return json.loads(value)
	    except ValueError:
	        pass

	    return value

	def get_prep_value(self, value):
	    """Convert our JSON object to a string before we save"""
	    if value == "":
	        return None
	    if isinstance(value, dict) or isinstance(value, dict):
	        value = json.dumps(value, cls=DjangoJSONEncoder)
	    return super(JSONField, self).get_prep_value(value)

	def value_to_string(self, obj):
	    """ called by the serializer.
	    """
	    value = self._get_val_from_obj(obj)
	    return self.get_db_prep_value(value)


