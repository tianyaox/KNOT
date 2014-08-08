# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from Friend.models import *
from Notification.models import *
import datetime
import json
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


def deleteNotification(request):
	#author: wmy
	#description: delete notification after user check it
	#{notificationID: '123'}

	#return {status: "Success" or "Fail"}	

	context = {}
	context['status'] = 'Fail'

	if request.method == 'POST' and request.user:
		notificationID = request.POST.get('notificationID')
		notification = Notification.objects.filter(id=int(notificationID))
		if(len(notification)>0):
			notification[0].delete()
			context['status'] = 'Success'


	return HttpResponse(json.dumps(context), content_type="application/json")


def notificationHtml(request):
	#author: wmy
	#description: get notification based on date
	#type == 'all' or '1' or '2' or '3'

	#return {status: "Success" or "Fail", notifications:[n1, n2, .....], dates:['2013-1-12','2013-1-3'....]}	

	return render_to_response('notification.html',{},context_instance=RequestContext(request))



def getNotification(request):
	context = {}
	context['status'] = 'Fail'

	if request.user and request.method=='POST':
		nType = request.POST.get('nType')
		if nType == 'all':
			notifications = Notification.objects.order_by('-time').filter(toUser=request.user)
		else:
			notifications = Notification.objects.order_by('-time').filter(toUser=request.user, nType=int(nType))

		notificationDates = [notification.time.strftime('%Y/%m/%d') for notification in notifications]

		dates = []
		index = 0
		for notificationDate in notificationDates:


			if notificationDate not in dates:
				dates.append(notificationDate)

			if notificationDate not in context:
				context[notificationDate]=[]

			context[notificationDate].append(notifications[index])
			index = index + 1

		context['dates'] = dates
		context['status'] = 'Success'
		context['notifications'] = list(notifications)

	
	return HttpResponse(json.dumps(context, cls=NotificationEncoder), content_type="application/json")


def getNotificationInternal(fromUser, toUser, nType, extraInformation=None):
	#author: wmy
	#description: get Notifications 

	# 1 friend request confirmation
	# 2 card information update
	# 3 tag name update 
	# 4 friend request	
	return Notification.objects.filter(fromUser=fromUser, toUser=toUser, nType=nType)


def addNotificationInternal(fromUser, toUser, nType, extraInformation=None):
	#author: wmy
	#description: generate Notification 

	# 1 friend request confirmation
	# 2 card information update
	# 3 tag name update 
	# 4 friend request


	if nType == 1:
		content = " accept your friend request"
	elif nType == 2:
		content = " updated "+extraInformation
	elif nType == 3:
		content = " got a new tag name"+ extraInformation
	elif nType == 4:
		content = " request to be your friend"

	time = datetime.datetime.now()

	notification = Notification(fromUser=fromUser, toUser=toUser, content=content, time=time, nType=nType)
	notification.save()

def deleteNotificationInternal(fromUser, toUser, nType):
	#author: wmy
	#description: delete Notification 

	# 1 friend request confirmation
	# 2 card information update
	# 3 tag name update 
	# 4 friend request

	notifications = Notification.objects.filter(fromUser=fromUser, toUser=toUser, nType=nType)
	if(len(notifications)>0):
		notifications.delete()
