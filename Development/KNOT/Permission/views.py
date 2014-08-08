# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from Friend.models import *
from Card.models import *
from Notification.models import *
from Permission.models import *
from Permission.forms import *
import datetime
import json
import pdb
from django.contrib.auth.decorators import login_required

@login_required
def addPermissionTemplate(request):
	#author: wmy
	#description: add Permission 
	#{name:'classmate', sharedSection1:'firstName', sharedSection2:'lastName' .........}


	context = {}
	context['status'] = 'Fail'	


	if request.method == 'POST' and request.user:
		# get sharedSections from POST
		index = 1 
		# default share image and sound
		sharedSections = ['soundURL', 'imageURL']
		while True:
			key = 'sharedSection' + str(index)
			sharedSection = request.POST.get(key)
			index = index + 1
			if sharedSection == None:
				break
			elif 'address' in sharedSection:
				sharedSections.append('city'+ str(sharedSection[-1]))
				sharedSections.append('address' + str(sharedSection[-1]))
			else:
				sharedSections.append(sharedSection)

		#get permission str
		permissionStr = PermissionTemplate.generatePermissionStr('custom',sharedSections)
		#get template name
		name = request.POST.get('name')

		# check unique template name
		permissionTemplate = PermissionTemplate.objects.filter(user=request.user, name=name)
		if len(permissionTemplate)>0:
			context['errors']='Name has already existed'

		# chekc unique permission 
		permissionTemplate = PermissionTemplate.objects.filter(user=request.user, permission=permissionStr)
		if len(permissionTemplate)>0:
			context['errors']='Permission has already existed'

		# chekc not All friend 
		if name.lower() == 'friend' or name.lower() =='all':
			context['errors']='Default Permission level can not be added'

		#save template
		if 'errors' not in context:
			template = PermissionTemplate(user=request.user, name= name, permission=permissionStr, time=datetime.datetime.now())
			template.save()
			context['status'] = 'Success'
			context['name'] = name


	return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def updatePermissionTemplate(request):
	#author: wmy
	#description: update Permission template
	#{templateID:'123', sharedSection1:'firstName', sharedSection2:'lastName' .........}	
	context = {}
	context['status'] = 'Fail'	


	if request.method == 'POST' and request.user:
		# get sharedSections from POST
		index = 1 
		sharedSections = ['soundURL', 'imageURL']
		while True:
			key = 'sharedSection' + str(index)
			sharedSection = request.POST.get(key)
			index = index + 1
			if sharedSection == None:
				break
			elif 'address' in sharedSection:
				sharedSections.append('city'+ str(sharedSection[-1]))
				sharedSections.append('address' + str(sharedSection[-1]))
			else:
				sharedSections.append(sharedSection)

		#get permission str
		permissionStr = PermissionTemplate.generatePermissionStr('custom',sharedSections)
		#get template id
		templateID = str(request.POST.get('templateID'))
		#get template name
		name = request.POST.get('name')


		#get template
		if templateID.isdigit():
			template = PermissionTemplate.objects.filter(id=int(templateID))
			if len(template)>0:
				template = template[0]

				# chekc unique permission 
				repeatTemplates = PermissionTemplate.objects.filter(user=request.user, permission=permissionStr).exclude(id=int(templateID))
				if len(repeatTemplates)>0:
						context['errors']='This template has same permission level with '+repeatTemplates[0].name

				#check unique name
				repeatTemplates = PermissionTemplate.objects.filter(user=request.user, name=name).exclude(id=int(templateID))
				if len(repeatTemplates)>0:
						context['errors']='Template name has already existed'

				# chekc not All friend 
				if name.lower() =='all':
					context['errors']='Default Permission level can not be changed'
				#update friend and save template
				if 'errors' not in context:
					#update friend
					oldPermissionStr = template.permission
					relations = FriendRelation.objects.filter(user=request.user, permission=oldPermissionStr)
					for relation in relations:
						relation.permission = permissionStr
						relation.save()

					#save template
					template.name = request.POST.get('name')
					template.permission = permissionStr
					template.datetime = datetime.datetime.now()
					template.save()
					context['status'] = 'Success'
					context['name'] = request.POST.get('name')

	return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def deletePermissionTemplate(request):
	#author: wmy
	#description: delete Permission template, friends who belong to this template will become the lowest permission
	#{templateID:'123', sharedSection1:'firstName', sharedSection2:'lastName' .........}
	#maybe should return html
	context = {}
	context['status'] = 'Fail'	

	if request.method == 'POST' and request.user:
		#get template id
		templateID = str(request.POST.get('templateID'))
		templateNum = len(PermissionTemplate.objects.all())

		#get template
		if templateID.isdigit() and templateNum > 1:
			template = PermissionTemplate.objects.filter(id=int(templateID))
			if len(template)>0:
				template = template[0]

				# chekc not All friend 
				if template.name.lower() == 'friend':
					context['errors']='Default Permission level can not be deleted'

				# friends who belong to this template the permission will become lowest
				if 'errors' not in context:
					relations = FriendRelation.objects.filter(user=request.user)
					for relation in relations:
						if relation.permission == template.permission:

							friendPermissionStr = PermissionTemplate.objects.get(user=request.user, name='friend').permission	
							relation.permission = friendPermissionStr
							relation.save()

					#delete template
					template.delete()
					context['status'] = 'Success'

	return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def getPermissionTemplateHtml(request,templateName):
	#author: wmy
	#description: delete Permission template, friends who belong to this template will become the lowest permission
	#{templateID:'123', sharedSection1:'firstName', sharedSection2:'lastName' .........}
	context = {}
	context['status'] = 'Fail'	

	if request.method == 'GET' and request.user:
		templates = PermissionTemplate.objects.filter(user=request.user)

		#store template id 
		ids = [template.id for template in templates]
		context['templateIDs']=ids
		# store template names
		names = [template.name for template in templates]
		context['templateNames'] = names


		# add new template
		if (templateName=="addNewTemplate"):
			context['selectedTemplateSections'] = []
			context['selectedTemplateName'] = ""
		else:
			#store sections according to name
			for template in templates:
				if template.name == templateName:
					sections = PermissionTemplate.getPermissionSectionNames(template.permission)
					context['selectedTemplateSections'] = sections
					context['selectedTemplateName'] = template.name
					context['selectedTemplateID'] = template.id

					relations = FriendRelation.objects.filter(user=request.user)
					for relation in relations:
						if relation.permission == template.permission:
							if not 'friendsWithSelectedPermission' in context:
								context['friendsWithSelectedPermission']=[]
							card = Card.objects.get(user = relation.friend)
							context['friendsWithSelectedPermission'].append(card)

		# no one found then return the first one
		if 'selectedTemplateSections' not in context:
			template = templates[0]
			sections = PermissionTemplate.getPermissionSectionNames(template.permission)
			context['selectedTemplateSections'] = sections		
			context['selectedTemplateName'] = template.name
			context['selectedTemplateID'] = template.id


	# real use should revise html page information
	return render_to_response('permission.html',context,context_instance=RequestContext(request))
