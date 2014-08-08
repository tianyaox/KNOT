# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template import *
from django.contrib.auth.models import User
from Permission.models import *
from Friend.models import *
from Card.models import *
from Card.forms import *
from Notification.models import *
from Notification.views import *
import datetime
import json
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from storages import s3
import pdb
import csv
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required
import random
from django.views.decorators.csrf import csrf_exempt



def getCardInternal(request, getType='friends', userID=None):
	#author: wmy
	#description: get cards according to the type given and the permission level, only use by the inner function
	#need request
	#return a list of card object after process by permission

	cards=[]
	if getType=='friends' and request.user.is_anonymous()==False:	
		relations = FriendRelation.objects.order_by('-time').filter(friend=request.user)

		# friend and permission
		friends = [relation.user for relation in relations]
		permissions = [relation.permission for relation in relations]

		rawCards = [card for card in Card.objects.filter(user__in=friends)]

		for rawCard in rawCards:
			for relation in relations:
				if rawCard.user.id == relation.user.id:

					cards.append(rawCard.getCardWithPermission(relation.permission))

	elif getType=='self'and request.user.is_anonymous()==False:
		user = User.objects.filter(id=request.user.id)
		if len(user)>0:
			card = Card.objects.filter(user=user[0])
			if len(card)>0:
				cards.append(card[0])

	elif getType=='other' and request.user.is_anonymous()==False:			
		if str(userID).isdigit():
			otherUser = User.objects.filter(id=int(userID))
			if len(otherUser)>0:
				rawCard = Card.objects.filter(user=otherUser[0])
				if len(rawCard)>0:
					relation = FriendRelation.objects.filter(user=otherUser, friend=request.user)
					rawCard = rawCard[0]
					# if have friend relationip then card should follow permission
					if len(relation)>0:
						relation = relation[0]
						cards.append(rawCard.getCardWithPermission(relation.permission))
					# Stranger, then return defalult permission level
					else:
						cards.append(rawCard.getCardWithPermission(PermissionTemplate.generatePermissionStr('stranger')))

	elif getType=='strangers' and request.user.is_anonymous()==False:
		relations = FriendRelation.objects.order_by('-time').filter(user=request.user)
		friendIDs = [relation.friend.id for relation in relations]
		friendIDs.append(request.user.id)
		strangers = [user for user in User.objects.exclude(id__in=friendIDs)]

		rawCards = [card for card in Card.objects.filter(user__in=strangers)]

		for rawCard in rawCards:
			cards.append(rawCard.getCardWithPermission(PermissionTemplate.generatePermissionStr('stranger')))

	return cards


def getCardPermissionTemplateNamesInternal(request, cards):
	#author: wmy
	#description: get cards template name, only used by the inner function
	#need request and the cards you want to get template names
	#return a list of template names
	permissionTemplateNames=[]
	for card in cards:
		relation = FriendRelation.objects.filter(user=request.user, friend=card.user)
		if(len(relation)>0):
			relation = relation[0]
			permissionTemplateNames.append(PermissionTemplate.getPermissionTemplateName(request.user, relation.permission))
		else:
			permissionTemplateNames = []

	return permissionTemplateNames

@login_required
def myCardHtml(request):
	#author: wmy
	#description: display my card html page
	#need card object
	#return http response to render myCard page

	context = {}


	cards = getCardInternal(request,'self')
	if len(cards)>0:
		context['card']=cards[0]
	else:
		context['card']=None

	return render_to_response('myCard.html',context,context_instance=RequestContext(request))


@login_required
def otherCardHtml(request, id):
	#author: wmy
	#description: display the other card according to the id of the other user
	#need id of the user
	#return http response to render otherCard page

	context = {}

	cards = getCardInternal(request,'other',id)
	if len(cards)>0:
		context['card']=cards[0]
	else:
		context['card']=None

	friendTemplateName = getCardPermissionTemplateNamesInternal(request, cards)
	if len(friendTemplateName)<=0:
		friendTemplateName = 'stranger'
	else:
		friendTemplateName = friendTemplateName[0]

	templates = PermissionTemplate.objects.filter(user=request.user)
	templateNames = [template.name for template in templates]

	context['friendTemplateName'] = friendTemplateName
	context['templateNames'] = templateNames
	return render_to_response('otherCard.html',context,context_instance=RequestContext(request))


@login_required
def contactsHtml(request, permissionTemplateName):
	context={}
	if request.method == "GET":
		cards = getCardInternal(request)

		selectedPermissionTemplate = PermissionTemplate.objects.filter(user=request.user, name=permissionTemplateName)
		
		qualifiedCards = []


		# filter template name
		if permissionTemplateName=='all':
			qualifiedCards = cards
		elif len(selectedPermissionTemplate)>0:
			selectedPermissionTemplate = selectedPermissionTemplate[0]
			for card in cards:
				relation = FriendRelation.objects.filter(user=request.user, friend=card.user)
				if len(relation)>0:
					relation = relation[0]
					if relation.permission == selectedPermissionTemplate.permission:
						qualifiedCards.append(card)
		else:
			qualifiedCards = cards

		# template people number


		context['cards']= qualifiedCards
	
	elif request.method == "POST":

		cards = searchCardInternal(request,'friends',['name'])
		context['cards'] = cards

	#get permission template name and numbers:
	permissionTemplateNames = []
	permissionTemplateStrs = []
	permissionTemplates = PermissionTemplate.objects.filter(user=request.user)
	for permissionTemplate in permissionTemplates:
		permissionTemplateNames.append(permissionTemplate.name)
		permissionTemplateStrs.append(permissionTemplate.permission)

	numberOfMembers = [0 for x in range(len(permissionTemplateNames))]
	relations = FriendRelation.objects.filter(user=request.user)
	for relation in relations:
		index = 0
		for permissionTemplateStr in permissionTemplateStrs:
			if permissionTemplateStr == relation.permission:
				numberOfMembers[index] = numberOfMembers[index] + 1
			index = index + 1


	allFriendNum = 0
	for num in numberOfMembers:
		allFriendNum+=num
	context['permissionTemplateNames'] = permissionTemplateNames
	context['numOfMembers'] = numberOfMembers
	context['allFriendNum'] = allFriendNum
	context['nameAndNumZip'] = zip(permissionTemplateNames,numberOfMembers)


	return render_to_response('contacts.html',context,context_instance=RequestContext(request))


@login_required
def timelineHtml(request, nType):

	context={}
	cards = getCardInternal(request)


	# generate left and righ cards
	leftCards=[]
	rightCards=[]
	index = 0
	for card in cards:
		if index%2 == 0:
			leftCards.append(card)
		else:
			rightCards.append(card)
		index = index + 1


	context['leftCards']=leftCards
	context['rightCards']=rightCards
	context['request']=request


	#generate recommendations
	strangers = getCardInternal(request,'strangers')
	leftStrangers = []
	rightStrangers = []
	index = 0
	for stranger in strangers:
		if index%2 == 0:
			leftStrangers.append(stranger)
		else:
			rightStrangers.append(stranger)
		index = index + 1


	# 1 friend request confirmation
	# 2 card information update
	# 3 tag name update 
	# 4 friend request
	#generate notification
	if nType == 'all':
		notifications = Notification.objects.order_by('-time').filter(toUser=request.user)
	else:
		notifications = Notification.objects.order_by('-time').filter(toUser=request.user, nType=int(nType))
	leftNs = []
	rightNs = []
	index = 0
	for n in notifications:
		if index%2 == 0:
			leftNs.append(n)
		else:
			rightNs.append(n)
		index = index + 1

	context['notifications'] = notifications
	context['leftNs'] = leftNs
	context['rightNs'] = rightNs


	leftItems = leftCards + leftStrangers + leftNs
	rightItems = rightCards + rightStrangers + rightNs
	leftItemTypes = ['friend' for i in range(len(leftCards))] + ['recommendation' for i in range(len(leftStrangers))] + ['notification' for i in range(len(leftNs))]
	rightItemTypes = ['friend' for i in range(len(rightCards))] + ['recommendation' for i in range(len(rightStrangers))] + ['notification' for i in range(len(rightNs))]
	leftItemIndexs = range(len(leftItems))
	rightItemIndexs = range(len(rightItems))
	random.shuffle(leftItemIndexs)
	random.shuffle(rightItemIndexs)

	context['leftItems'] = leftItems
	context['rightItems'] = rightItems
	context['leftItemTypes'] = leftItemTypes
	context['rightItemTypes'] = rightItemTypes
	context['leftItemIndexs'] = leftItemIndexs
	context['rightItemIndexs'] = rightItemIndexs
	context['leftStrangers'] = leftStrangers
	context['rightStrangers'] = rightStrangers

	# loop leftItemIndexs to get leftItems and leftItemTypes to get random items

	context['status'] = 'success'
	return render_to_response('timeline.html',context,context_instance=RequestContext(request))

@login_required
def searchHtml(request):
	context={}
	if request.method == 'POST':
		context['cards']=searchCardInternal(request,'strangers',request.POST.getlist('conditions[]'))
	else:
		context['cards']=searchCardInternal(request,'strangers')


	return render_to_response('search.html',context,context_instance=RequestContext(request))



@login_required
def checkUpdateSection(request):
	#author: wmy
	#description: compare card information and add notification to friends
	#need serialize form
	changeFields = []
	card = Card.objects.get(user=request.user)



	sections = Card.getSections()


	# check which section of card changed
	for section in sections:
		sectionValue = getattr(card,section)
		if section == 'birthday':
			sectionValue = sectionValue.strftime('%Y-%m-%d')
		if request.POST.get(section)!=None and  str(request.POST.get(section)) != str(sectionValue):
			changeFields.append(section)


	relations = FriendRelation.objects.filter(user=request.user)
	extraInformation = ''

	index = 0
	for changeField in changeFields:
		extraInformation = extraInformation + ' '+changeField + ' ' 
		index = index + 1
		if index > 4:
			extraInformation = extraInformation + '...'
			break
	# if some sections changed, then send notification
	if len(changeFields)>0:
		for relation in relations:
			addNotificationInternal(request.user, relation.friend, 2, extraInformation)

@login_required
def getMyCard(request):
	context = {}
	context['status'] = 'Fail'	
	if request.method == 'POST' and request.user:
		user = User.objects.filter(id=request.user.id)
		if len(user)>0:
			card = Card.objects.filter(user=user[0])
			if len(card)>0:
				context['card']=card[0]
				context['status'] = 'Success'
				print card[0]	

	return HttpResponse(json.dumps(context, cls=CardEncoder), content_type="application/json")


@login_required
def updateMyCard(request):
	#author: wmy
	#description: update informaion
	#need serialize form
	#date yyyy-mm-dd

	
	context = {}
	context['status'] = 'Fail'	

	if request.method == 'POST' and request.user:
		cardForm = CardForm(request.POST)
		if cardForm.is_valid():
			# check update section and send notifications
			checkUpdateSection(request)

			card = Card.objects.get(user=request.user)

			sections = Card.getSections()
			for section in sections:
				sectionValue = getattr(card,section)
				if section == 'birthday':
					sectionValue = sectionValue.strftime('%Y-%m-%d')
				if request.POST.get(section)!=None and  str(request.POST.get(section)) != str(sectionValue):
					if section == 'birthday':
						value = datetime.datetime.strptime(request.POST.get(section),"%Y-%m-%d").date()
					else:
						value = request.POST.get(section)
					setattr(card, section, value)			

			card.save()
			context['status'] = 'Success'
		else:
			errors = []
			for error in cardForm.errors.values():
				errors.append(error[0])
			context['errors'] = errors

	return HttpResponse(json.dumps(context), content_type="application/json")



def searchCardInternal(request, searchRange,requiredConditions=[]):
	#author: wmy
	#description: search with conditions
	#need
	# #{
	# 	conditions:['name','age','gender','hometown','currentCity','mutualFriend'];

	# 	name : 'wmy'
	# 	ageMin : 18
	#   ageMax : 30
	# 	gender: 'F'
	# 	...
	# }

	#return {status: "Success" or "Fail", friends:[name1, name2, ....]}	
	#I think this function should  return web page not json

	context = {}
	context['status'] = 'Fail'
	conditions = ['name', 'age', 'gender', 'hometown', 'currentCity', 'mutualFriend','range']


	if request.method == 'GET' and request.user:
		if searchRange == 'friends':
			qualifiedCards = getCardInternal(request, searchRange)
		else:
			qualifiedCards = getCardInternal(request, searchRange)



	if request.method == 'POST' and request.user:



		searchRange = request.POST.get('range')


		if searchRange == 'friends':

			cards = getCardInternal(request,searchRange)
		else:

			cards = getCardInternal(request,searchRange)


		qualifiedCards = cards





		# name
		if conditions[0] in requiredConditions:
			tempCards = qualifiedCards
			qualifiedCards = []

			requiredName = request.POST.get('name').lower()
			for card in tempCards:
				# get friend name card
				if requiredName in card.firstName.lower() or requiredName in card.lastName.lower():
					qualifiedCards.append(card)

		#age
		if conditions[1] in requiredConditions:

			tempCards = qualifiedCards
			qualifiedCards = []

			selectedAgeMin = int(request.POST.get('ageMin'))
			selectedAgeMax = int(request.POST.get('ageMax'))

			for card in tempCards:
				if card.birthday != None:
					age = int((datetime.date.today() - card.birthday).days/365.2425)+1
					if age>=selectedAgeMin and age<=selectedAgeMax:
						qualifiedCards.append(card)
		

		# gender
		if conditions[2] in requiredConditions:

			tempCards = qualifiedCards
			qualifiedCards = []

			requiredGender = request.POST.get('gender')
			for card in tempCards:
				if card.gender == requiredGender:
					qualifiedCards.append(card)


		if conditions[4] in requiredConditions:

			tempCards = qualifiedCards
			qualifiedCards = []

			requiredCurrentCity = request.POST.get('currentCity')
			for card in tempCards:
				if card.city1 == requiredCurrentCity or card.city2 == requiredCurrentCity or card.city3 == requiredCurrentCity or card.city4 == requiredCurrentCity or card.city5 == requiredCurrentCity:
					qualifiedCards.append(card)

		#mutualFriend give the mutual friend A find people who act A as friend,  B A, C A, find C
		# if conditions[5] in requiredConditions:
		# 	print "check mutual friend"

		# 	tempCards = qualifiedCards
		# 	qualifiedCards = []

		# 	requiredMutualFriends = []

		# 	# get mutual friend name from post request
		# 	index = 1
		# 	while True:
		# 		key = 'mutualFriend'+ str(index)
		# 		requiredMutualFriend = request.POST.get(key)
		# 		index = index + 1
		# 		if requiredMutualFriend == None:
		# 			break
		# 		else:
		# 			requiredMutualFriends.append(requiredMutualFriend)

		# 	userFriends = [relation.friend for relation in FriendRelation.objects.filter(user=request.user)]
		# 	for requiredMutualFriend in requiredMutualFriends:
		# 		for card in tempCards:
		# 			# firned's friend List
		# 			friendFriends = FriendRelation.objects.filter(user=card.user).exclude(friend__in=userFriends)
		# 			friendFriendCards = Card.objects.filter(user__in=friendFriends)
		# 			friendFriendNames = [friendFriendCard.firstName+' '+friendFriendCard.lastName for friendFriendCard in friendFriendCards]
		# 			print card.user.username
		# 			print friendFriendNames
		# 			if requiredMutualFriend in friendFriendNames:
		# 				qualifiedCards.append(card)	
		# 		tempCards = qualifiedCards
		# 		qualifiedCards = []

		# 	qualifiedCards = tempCards

		#get qualified name for tet
		# context['status'] = 'Success'
		# qualifiedFriendName = [card.user.username for card in qualifiedCards]
		# context['friendNames'] = qualifiedFriendName

		# return card for real use
		context['cards'] = qualifiedCards
		context['status'] = 'Success'
	
	return qualifiedCards



@login_required
def exportCSV(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
	writer = csv.writer(response)

	sections = PermissionTemplate.getPermissionSections()
	writer.writerow(sections)

	cards = getCardInternal(request,'friends')
	for card in cards:
		row = []
		for section in sections:
			if getattr(card, section) != None:
				if section == 'user':
					continue
				elif section == 'birthday':
					row.append(str(getattr(card, section).strftime('%Y-%m-%d')))
				else:
					row.append(str(getattr(card, section)))
			else:
				row.append("empty")

		writer.writerow(row)
	return response




@login_required
def uploadImageFromCamera(request):
	context = {}
	context['status'] = 'Fail'
	if request.method == 'POST' and request.user:
		imageString = request.POST.get('image')
		imageData = imageString.decode("base64")
		imageName = request.user.username+".jpg"
		content_type = guess_type(imageName)[0]



		imageURL = s3.saveFile(imageName, imageData, content_type)
		card = Card.objects.get(user=request.user)
		card.imageURL = imageURL
		card.save()
		context['status'] = 'Success'
	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def getRecoderWorker(request):
	context={}
	return render_to_response('recorderWorker.js',context,context_instance=RequestContext(request))

@login_required
def uploadAudio(request):
	context={}
	context['status'] = 'Fail'
	if 'audio' in request.FILES and request.user:
		audio =  request.FILES['audio']
		audioData = audio.read()
		audioName = request.user.username+".wav"
		content_type = guess_type(audioName)[0]


		soundURL = s3.saveFile(audioName, audioData, content_type)
		card = Card.objects.get(user=request.user)
		card.soundURL = soundURL
		card.save()
		context['status'] = 'Success'
	return HttpResponse(json.dumps(context), content_type="application/json")



@login_required
@csrf_exempt
def uploadImageFromFile(request):
	context = {}
	context['status'] = 'Fail'
	extensions = ["jpg", "png", "gif", "jpeg"]
	if 'image' in request.FILES and request.user:
		image =  request.FILES['image']
		imageData = image.read()
		imageName = request.FILES['image'].name

		if imageName.split('.')[-1].lower() in extensions:
			content_type = guess_type(imageName)[0]
			newImageName = request.user.username + '.' + imageName.split('.')[-1].lower()

			card = Card.objects.get(user=request.user)
			imageUrl = s3.saveFile(newImageName, imageData, content_type)
			card.imageURL = imageUrl
			card.save()

			context['status'] = 'Success'
	return HttpResponseRedirect('/myCard/')
