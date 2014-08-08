import csv
from collections import defaultdict
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *
from Permission.models import *
import datetime
import random
import string


fileName = 'dummyData.csv'


dummyFile=open(fileName,'rU')
reader = csv.DictReader(dummyFile, delimiter='|')

infoDict=defaultdict(list)

index=0;
for row in reader:
	for (k,v) in row.items():
		infoDict[k].append(v)
dummyFile.close()



def generateRandomString(length):
	char_set = string.ascii_uppercase + string.digits
 	return ''.join(random.choice(char_set) for x in range(length))



def generateUser(num):
	if num >=100:
		num = 100
	User.objects.all().delete()
	nameIndexs=random.sample(range(0,99),num)

	for nameIndex in nameIndexs:
		newUser = User.objects.create_user(username=infoDict['firstName'][nameIndex], password='12345')
		newUser.save()

def generateFriend(relationNum):
	FriendRelation.objects.all().delete()
	
	for  x in range(relationNum):
		user = User.objects.order_by('?')[0]
		friendIDsSoFar = [relation.friend.id for relation in FriendRelation.objects.filter(user=user)]
		friend = User.objects.order_by('?').exclude(id__in=friendIDsSoFar).exclude(id=user.id)

		if len(friend)==0:
			continue
		else:
			friend = friend[0]

		permission = ''


		# permission ="++"
		# for y in range(30):
		# 	if random.randint(0,100)%2 == 0:
		# 		permission = permission + '+'
		# 	else:
		# 		permission = permission + '-'
		permissions = PermissionTemplate.objects.filter(user=user)
		permissionStr = permissions[random.randint(0,3)].permission

		currentTime = datetime.datetime.now()
		delta = datetime.timedelta(random.randint(0,500))
		time = currentTime - delta


		relation = FriendRelation(user=user, friend=friend, permission=permissionStr, time=time)
		relation.save()

		relation = FriendRelation(user=friend, friend=user, permission=permissionStr, time=time)
		relation.save()

def generateCard():
	Card.objects.all().delete()


	indexs=random.sample(range(0,99),len(User.objects.all()))

	i = 0
	for user in User.objects.all():
		firstName = user.username.split(' ')[0]
		lastName = user.username.split(' ')[1]

		if(random.randint(0,100)%2==0):
			gender='F'
		else:
		 	gender='M'

		title=infoDict['title'][indexs[i]]

		today = datetime.date.today()
		delta = datetime.timedelta(random.randint(5000,20000))
		birthday = today - delta

		citizenship = infoDict['citizenship'][indexs[i]]



		address1 = infoDict['address'][indexs[i]]
		address2 = infoDict['address'][indexs[i]]
		address3 = infoDict['address'][indexs[i]]
		address4 = infoDict['address'][indexs[i]]
		address5 = infoDict['address'][indexs[i]]
		phone1 = infoDict['phone'][indexs[i]]
		phone2 = infoDict['phone'][indexs[i]]
		phone3 = infoDict['phone'][indexs[i]]
		phone4 = infoDict['phone'][indexs[i]]
		phone5 = infoDict['phone'][indexs[i]]
		email1 = infoDict['email'][indexs[i]]
		email2 = infoDict['email'][indexs[i]]
		email3 = infoDict['email'][indexs[i]]
		email4 = infoDict['email'][indexs[i]]
		email5 = infoDict['email'][indexs[i]]


		user.email = email1
		user.save()
		
		city = None
		if(random.randint(0,100)%2==0):
			city='Washington, D.C., DC, United States'
		else:
		 	city='Peking, Beijing, China'

		city1 = city
		city2 = city
		city3 = city
		city4 = city
		city5 = city

		imageURL = 'https://s3.amazonaws.com/knot/default.jpg'
		soundURL = 'https://s3.amazonaws.com/knot/Tyrone+Tillman.wav'


		currentTime = datetime.datetime.now()
		delta = datetime.timedelta(random.randint(0,500))
		time = currentTime - delta

		card = Card(user=user,firstName=firstName, lastName=lastName, gender=gender, title=title, birthday=birthday, citizenship=citizenship, \
					address1=address1, phone1=phone1, email1=email1, city1=city1,\
					address2=address2, phone2=phone2, email2=email2, city2=city2,\
					address3=address3, phone3=phone3, email3=email3, city3=city3,\
					address4=address4, phone4=phone4, email4=email4, city4=city4,\
					address5=address5, phone5=phone5, email5=email5, city5=city5,\
					imageURL=imageURL, soundURL=soundURL,\
					time=time)
		card.save()

		i=i+1


def generateFriendRequest(requestNum):
	for  x in range(requestNum):
		user = User.objects.order_by('?')[0]

		friendList = [relation.friend.id for relation in FriendRelation.objects.filter(user=user)]
		requestList = [notification.toUser.id for notification in Notification.objects.filter(fromUser=user, nType=4)]
		toUser = User.objects.order_by('?').exclude(id__in=friendList).exclude(id__in=requestList)

		if len(toUser)==0:
			continue
		else:
			toUser = toUser[0]
			
		currentTime = datetime.datetime.now()
		delta = datetime.timedelta(random.randint(0,500))
		time = currentTime - delta

		# friendRequest = FriendRequest(fromUser=fromUser, toUser=user, confirmation=False, time=time)
		# friendRequest.save()
		# friendRequest = Notification(fromUser=)
		nType = 4
		content = " request to be your friend"
		notification = Notification(fromUser=user, toUser=toUser, content=content, time=time, nType=nType)	
		notification.save()	


def generateTagName(tagNum):
	SelfDefCardColumn.objects.filter(name='tag').delete()

	for x in range(tagNum):
		user = User.objects.order_by('?')[0]
		name = 'tag'
		validate = True
		content = infoDict['lastName'][random.randint(0,99)]

		currentTime = datetime.datetime.now()
		delta = datetime.timedelta(random.randint(0,500))
		time = currentTime - delta

		tag = SelfDefCardColumn(user=user, name = name, validate = validate, content = content, time=time)
		tag.save()


def generateNotification(notificationNum):
	Notification.objects.all().delete()
	for x in range(notificationNum):
		toUser = User.objects.order_by('?')[0]
		fromUser = User.objects.order_by('?').exclude(id=toUser.id).exclude()[0]

		nType = random.randint(0,99)%3+1
		cardList = ["email","address","phone"];
		if nType==2:
			content = " update his "+cardList[random.randint(0,99)%3]
		elif nType==3 and len(SelfDefCardColumn.objects.filter(name='tag').filter(user = fromUser))>0:
			content = " got a new tag name "+str(SelfDefCardColumn.objects.filter(name='tag').filter(user = fromUser).order_by('?')[0].content)
		else:
			content = " update his "+cardList[random.randint(0,99)%3]

		currentTime = datetime.datetime.now()
		delta = datetime.timedelta(random.randint(0,500))
		time = currentTime - delta

		notification = Notification(fromUser=fromUser, toUser=toUser, content=content, time=time, nType=nType)	
		notification.save()	

def generatePermissionTemplate():
	users = User.objects.all()

	for user in users:

		currentTime = datetime.datetime.now()
		delta = datetime.timedelta(random.randint(0,500))
		time = currentTime - delta

		
		name = 'friend'
		permissionStr = PermissionTemplate.generatePermissionStr(name)
		permission = PermissionTemplate(user=user,name=name,permission=permissionStr, time=time)
		permission.save()

		name = 'classmate'
		permissionStr = PermissionTemplate.generatePermissionStr(name)
		permission = PermissionTemplate(user=user,name=name,permission=permissionStr, time=time)
		permission.save()

		name = 'family'
		permissionStr = PermissionTemplate.generatePermissionStr(name)
		permission = PermissionTemplate(user=user,name=name,permission=permissionStr, time=time)
		permission.save()

		# name = 'god'
		# permissionStr = PermissionTemplate.generatePermissionStr(name)
		# permission = PermissionTemplate(user=user,name=name,permission=permissionStr, time=time)
		# permission.save()

		name = 'custom'
		permissionStr ="++"
		for i in range(len(PermissionTemplate.getPermissionSections())-2):
			if random.randint(0,100)%2 == 0:
				permissionStr = permissionStr + '+'
			else:
				permissionStr = permissionStr + '-'	


		permission = PermissionTemplate(user=user,name=name,permission=permissionStr, time=time)
		permission.save()


def generateDummyData(userNum=15, relationNum=100, notificationNum=200, tagNum=100):
	generateUser(userNum)
	generatePermissionTemplate();
	generateFriend(relationNum)
	generateCard()
	generateNotification(notificationNum)
	generateFriendRequest(relationNum)
	# generateTagName(tagNum)