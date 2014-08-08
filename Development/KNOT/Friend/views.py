# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Friend.forms import *
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *
from Notification.views import *
from Permission.models import *
from Card.views import *
import datetime
import json
import pdb
from django.contrib.auth.decorators import login_required
import urllib2




@login_required
def addFriendRequest(request):
	#author: wmy
	#description: generate friend request to another user

	#need json {friendID : "123"}
	#return {status: "Success" or "Fail"}
	context={}
	context['status'] = "Fail"

	if request.method == 'POST' and request.user:
		toUserID = request.POST.get('friendID')

		toUser = []
		if toUserID.isdigit():
			toUser = User.objects.filter(id=int(toUserID))
		if len(toUser)>0:
			toUser = toUser[0]
			fromUser = request.user
			confirmation = False
			time = datetime.datetime.now()

			# no request then generate request, 
			request = FriendRequest.objects.filter(fromUser=fromUser, toUser=toUser)
			if(len(request)==0):
				request = FriendRequest(fromUser=fromUser, toUser=toUser, confirmation=confirmation, time=time)
				request.save()

			if(len(getNotificationInternal(fromUser, toUser, 4))==0):
				addNotificationInternal(fromUser, toUser, 4, None)
			context['status'] = "Success"

	return HttpResponse(json.dumps(context), content_type="application/json")




@login_required
def deleteFriend(request):
	#author: wmy
	#description: delete a user's friend

	#need json {notificationID : "123"}
	#return {status: "Success" or "Fail" or "..."}
	context={}
	context['status'] = "Fail"

	if request.method == 'POST' and request.user:

		friendID = request.POST['friendID']
		friend = User.objects.filter(id = int(friendID))

		if(len(friend)>0):
			friend = friend[0]

			relation = FriendRelation.objects.filter(user=request.user, friend=friend)
			relation1 = FriendRelation.objects.filter(user=friend, friend=request.user)

			if(len(relation)==1 and len(relation1)==1):
				relation.delete()
				relation1.delete()
				context['status'] = "Success"
			else:
				context['status'] = "Relation not exist or multiply exist"

	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def addFriend(request):
	# author: wmy
	# description: add frend to friend list, then delete friend request and generate a notification


	# need json {notificationID : 123}
	# return {status:"Success" or "Fail"}
	context={}
	context['status']='Fail'


	if request.method == 'POST' and request.user:

		userName = request.user.username
		notificationID = request.POST.get('notificationID')
		friend=[]
		if notificationID.isdigit():
			norification = Notification.objects.filter(id=int(notificationID))
			if(len(norification)>0):
				friend.append(norification[0].fromUser)

		#after validate save friend relationship and delete friend request and generate a notification
		if(len(friend)>0):
			user = request.user
			friend = friend[0]

			#friend template always exist 
			permission = PermissionTemplate.objects.get(user=user, name='friend').permission

			# relation A to B
			if(len(FriendRelation.objects.filter(user=user,friend=friend))==0):
				relation = FriendRelation(user=user,friend=friend,permission=permission,time=datetime.datetime.now())
				relation.save()
				
			#friend template always exist 
			permission = PermissionTemplate.objects.get(user=friend, name='friend').permission

			#relation B to A
			if(len(FriendRelation.objects.filter(user=friend,friend=user))==0):
				relation = FriendRelation(user=friend,friend=user,permission=permission,time=datetime.datetime.now())
				relation.save()
			
			#delete friend request notification
			deleteNotificationInternal(friend, user, 4)
			deleteNotificationInternal(user, friend, 4)

			#generate a notification
			addNotificationInternal(user, friend, 1)

			context['status']='Success'


	return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def getFriendList(request, name):
	#author: wmy
	#description: get the friendlist of a user

	#need json null
	#return {status: "Success" or "Fail", friends:[name1, name2, ....], ids:[1,32,...]}
	context = {}
	context['status'] = 'Fail'

	if request.method == 'POST':
		if len(User.objects.filter(username=name))>0:
			user = User.objects.get(username=name)
			relations = FriendRelation.objects.filter(user=user)
			context['friends'] = [relation.friend.username for relation in relations]
			context['ids'] = [relation.friend.id for relation in relations]
			context['status'] = 'Success'

	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def updateFriendPermission(request):
	#author: wmy
	#description: chage a friend's permission type
	#need {friendID:'123', permissionName:'friend'}
	context = {}
	context['status'] = 'Fail'

	if request.method == 'POST':
		friend = User.objects.filter(id=(int)(request.POST.get('friendID')))
		if len(friend)>0:
			relation = FriendRelation.objects.filter(user=request.user, friend=friend[0])[0]


			permissionTemplate = PermissionTemplate.objects.filter(user=request.user, name=request.POST.get('permissionName'))
			if len(permissionTemplate)>0:
				permissionTemplate = permissionTemplate[0]
				relation.permission = permissionTemplate.permission
				relation.save()
				context['status'] = 'Success'
	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def recommendFriend(request):
	#author: wmy
	#description: recommed friends to user
	#need {request.user}

	context = {}
	context['status'] = 'Fail'

	if request.method == 'POST':
		strangers = getCardInternal(request,'strangers')
		context['strangers'] = strangers
		context['status'] = 'success'

	return HttpResponse(json.dumps(context, cls=CardEncoder), content_type="application/json")

@login_required
def getFriendLocation(request):
	#author: wb
	#description: get the friendlocationlist of a user

	#need json null
	#return {status: "Success" or "Fail", friends:[name1, name2, ....], locations:[location1,location2]}
	context = {}
	context['status'] = 'Fail'
	friends = []
	locations = []
	
	name = request.user.username

	if request.method == 'POST':
		if len(User.objects.filter(username=name))>0:
			user = User.objects.get(username=name)
			relations = FriendRelation.objects.filter(user=user)
			for relation in relations:
				location = ""
				friends.append(relation.friend.username)
				if relation.permission[11] == '+':
					location += Card.objects.get(id=relation.friend.id).address1
				if relation.permission[21] == '+':
					location += " "
					location += Card.objects.get(id=relation.friend.id).city1

				location = location.replace(" ","+")
				response = urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?address='+location+'&sensor=true')
				json_response = json.loads(response.read())
				if (json_response['status'] =='OK'):
					locEntry = []
					locEntry.append(relation.friend.username)
					locEntry.append(json_response['results'][0]['geometry']['location']['lat'])
					locEntry.append(json_response['results'][0]['geometry']['location']['lng'])
					locations.append(locEntry)
				context['status'] = 'Success'

	context['locations'] = locations

	return HttpResponse(json.dumps(context), content_type="application/json")


