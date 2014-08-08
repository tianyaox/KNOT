# Create your views here.
from django.shortcuts import render_to_response, render, redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email

from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import login, authenticate

from django.contrib.auth.tokens import default_token_generator

from UserManagement.forms import *
from Card.models import *
from Permission.models import *
from django.core.mail import send_mail
import json
import pdb
import datetime
from mimetypes import guess_type
from storages import s3
import pdb

def login(request):

    context={}
    if request.user.is_authenticated():
        return HttpResponseRedirect('/timeline/1')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username, password=password)


        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/timeline/1")
        elif user is not None and not user.is_active:
            context['username'] = user.username
            context['email'] = user.email
            return render_to_response('guide.html',context,context_instance=RequestContext(request))
        else:
            context['error'] = 'Username or password is not correct'
            return render_to_response('login.html',context,context_instance=RequestContext(request))
    else:
        return render_to_response('login.html',context,context_instance=RequestContext(request))

@login_required
def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")

@transaction.commit_on_success
def register(request):
    # pdb.set_trace()
    context = {}
    errors = []
    # pdb.set_trace()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
            new_user.is_active = False
            new_user.save()

            new_card = Card(user=new_user,time=datetime.datetime.now(), birthday=datetime.date.today(), imageURL='https://s3.amazonaws.com/knot/default.jpg')
            new_card.save()

            name = 'friend'
            permissionStr = PermissionTemplate.generatePermissionStr(name)
            permission = PermissionTemplate(user=new_user,name=name,permission=permissionStr, time=datetime.datetime.now())
            permission.save()

            name = 'classmate'
            permissionStr = PermissionTemplate.generatePermissionStr(name)
            permission = PermissionTemplate(user=new_user,name=name,permission=permissionStr, time=datetime.datetime.now())
            permission.save()   

            name = 'family'
            permissionStr = PermissionTemplate.generatePermissionStr(name)
            permission = PermissionTemplate(user=new_user,name=name,permission=permissionStr, time=datetime.datetime.now())
            permission.save()  

            token = default_token_generator.make_token(new_user) 


            email_body = """
        Welcome to the KNOT.  Please click the link below to
        verify your email address and complete the registration of your account:

          http://%s%s
        """ % (request.get_host(), 
               reverse('confirm', args=(new_user.username, token)))

            send_mail(subject="Verify your email address",
                      message= email_body,
                      from_email="mengyanw@andrew.cmu.edu",
                      recipient_list=[new_user.email])

            context['email'] = request.POST['email']
            context["message"] = "A confirmation email has been sent to " + request.POST['email'] + ".  Please click the link in that email to confirm your email address and complete your registation your KNOT."
        
        else:
            errors = []
            for error in form.errors.values():
                errors.append(error[0])
            context['errors'] = errors

        return HttpResponse(json.dumps(context), content_type="application/json")

@transaction.commit_on_success
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request,user)
    
    return render(request,'guide.html',{'username':username})

@transaction.commit_on_success
def forget_password(request):
    errors = []
    context = {}
    if request.method == 'GET':
        return render(request, 'forget.html', {})

    if not 'email' in request.POST or not request.POST['email']:
        errors.append('please enter your email')
        return render(request, 'forget.html',{'errors':errors})

    try:
        user = User.objects.get(email=request.POST['email'])
    except ObjectDoesNotExist:
        errors.append('Wrong email address')
        return render(request, 'forget.html',{'errors':errors})

    token = default_token_generator.make_token(user)

    email_body = """
Welcome to the Knot.  Please click the link below to
reset your password:

  http://%s%s
""" % (request.get_host(), 
       reverse('reset', args=(request.POST['email'], token)))

    send_mail(subject="reset your password",
              message= email_body,
              from_email="mengyanw@andrew.cmu.edu",
              recipient_list=[user.email])

    context['email'] = request.POST['email']
    return render(request, 'reset_confirmation.html', context)

@transaction.commit_on_success
def reset_password(request, email, token):
    context = {}
    user = get_object_or_404(User, email=email)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    context['email'] = email
    return render(request, 'reset.html', context)

@transaction.commit_on_success
def reset_password1(request, email):
    context = {}
    errors = []

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    context['errors'] = errors
    context['email'] = email
    
    if errors:
        return render(request, 'reset.html', context)

    user = User.objects.get(email=email)

    user.set_password(request.POST['password1'])
    user.save()

    context['success'] = 'Change Password Successfully!'
    return render(request,'login.html',context)


@login_required
@csrf_exempt
def accountSetting(request, type):
    context={}
    errors=[]
    

    if request.method == 'GET':
        context['email'] = request.user.email
        return render(request, 'accountSetting.html', context)

    if type == '1':
        context['email'] = request.user.email
        form = ChangePwForm(request.user,request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(request.POST['password1'])
            user.save()
            context['success1'] = "Save password changes successfully!"

            return render(request, 'accountSetting.html', context)
        else:
            for error in form.errors.values():
                errors.append(error[0])
            context['errors'] = errors
            return render(request, 'accountSetting.html', context)
    else:
        user = User.objects.get(username=request.user.username)
        if not 'email' in request.POST or not request.POST['email']:
            errors.append('Cannot Save')
            context['email'] = user.email
            context['errors2'] = errors
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            try:
                validate_email(request.POST.get("email", ""))

                token = default_token_generator.make_token(request.user) 

                email_body = """
            Dear KNOT user, you need to click the link below to update your confirmation email address:

              http://%s%s
            """ % (request.get_host(), 
                   reverse('confirmEmail', args=(request.user.username, token, request.POST['email'])))

                send_mail(subject="Verify your email address",
                          message= email_body,
                          from_email="mengyanw@andrew.cmu.edu",
                          recipient_list=[request.user.email])
                context['message'] = "Dear " + user.username + ", an email for updating your account email has been sent to your original email address"
                return HttpResponse(json.dumps(context), content_type="application/json")
            except forms.ValidationError:
                context['email'] = user.email
                errors.append('Not an valid email address.')
                context['errors2'] = errors
                return HttpResponse(json.dumps(context), content_type="application/json")

@transaction.commit_on_success
def confirmEmail(request, username, token, email):
    context = {}
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    user.email = email
    user.save()
    context['email'] = email
    context['message'] = "Update account email address successfully!"
    return render(request,'confirmEmail.html',context)
           
@login_required
@csrf_exempt
def guide(request,type):
    context={}
    errors=[]

    request.user.is_active = True

    if request.method == 'GET' and type == '0':
        return render(request, 'guide.html',{})

    if request.method == 'GET' and type == '2':
        return render(request, 'guide2.html',{})

    if request.method == 'GET' and type == '3':
        context['email'] = request.user.email
        return render(request, 'guide3.html',context)

    if request.method == 'GET' and type == '5':
        context['email'] = request.user.email
        return render(request, 'guide5.html',context)

    if request.method == 'POST' and type == '2':
        card = Card.objects.filter(user=request.user)
        if len(card)<=0:
            raise Exception("Can not find card")
        card = card[0]

        if 'firstname' in request.POST and request.POST['firstname']!='':
            card.firstName = request.POST['firstname']
        if 'lastname' in request.POST and request.POST['lastname']!='':
            card.lastName = request.POST['lastname']

        card.save()
        context['email'] = request.user.email
        return render(request, 'guide3.html',context)

    if request.method == 'POST' and type == '3':
        card = Card.objects.filter(user=request.user)
        if len(card)<=0:
            raise Exception("Can not find card")
        card = card[0]

        form = GuideEmailForm(request.POST)
        if form.is_valid():
            card.email1 = request.POST['email']
            if 'title' in request.POST and request.POST['title']!='':
                card.title = request.POST['title']
            if 'phone' in request.POST and request.POST['phone']!='':
                card.phone1 = request.POST['phone']
            card.save()
            return render(request,'guide4.html',{})
        else:
            errors = []
            for error in form.errors.values():
                errors.append(error[0])
            context['errors'] = errors
            return render(request,'guide3.html',context)       

    if request.method == 'POST' and type == '4':
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
                return render(request,'guide5.html',context)
            else:
                errors.append("Wrong image type.")
                context['errors'] = errors
                return render(request,'guide4.html',context)
        else:
            return render(request,'guide5.html',context)

