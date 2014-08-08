 # Create your views here.
import oauth2 as oauth
import urlparse
import urllib
import httplib2
import time
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import RequestContext
from django.conf import settings
from Card.models import *
import pdb
import json
from xml.dom import minidom
from django.db.models import Q
from Card.models import *
from Permission.models import *
from django.contrib.auth.decorators import login_required
import certifi
from django.views.decorators.csrf import csrf_exempt
from Friend.models import *
from Notification.views import *

twitterRequestTokenURL = 'https://api.twitter.com/oauth/request_token'
twitterAuthorizeURL = 'https://api.twitter.com/oauth/authenticate'
twitterAccessTokenURL = 'https://api.twitter.com/oauth/access_token'


githubAuthenticationURL = 'https://github.com/login/oauth/authorize'
githubAccessTokenURL = 'https://github.com/login/oauth/access_token'
githubUserInfoURL = 'https://api.github.com/user'

tumblrRequestTokenURL = 'http://www.tumblr.com/oauth/request_token'
tumblrAuthorizeURL = 'http://www.tumblr.com/oauth/authorize'
tumblrAccessTokenURL = 'http://www.tumblr.com/oauth/access_token'
tumblrUserInfoURL = 'http://api.tumblr.com/v2/user/info'

linkedinAuthorizeURL = 'https://www.linkedin.com/uas/oauth2/authorization'
linkedinAccessTokenURL = 'https://www.linkedin.com/uas/oauth2/accessToken'
linkedinUserInfoURL = 'https://api.linkedin.com/v1/people/~'
linkedinUserBasicProfileURL = 'https://api.linkedin.com/v1/people/url'

instagramAuthorizeURL = 'https://api.instagram.com/oauth/authorize/'
instagramAccessTokenURL = 'https://api.instagram.com/oauth/access_token'
instagramUserInfoURL = 'https://api.linkedin.com/v1/people/~'

vimeoRequestTokenURL = 'https://vimeo.com/oauth/request_token'
vimeoAuthorizeURL = 'https://vimeo.com/oauth/authorize'
vimeoAccessTokenURL = 'https://vimeo.com/oauth/access_token'
vimeoUserInfoURL = 'http://vimeo.com/api/rest/v2?method=vimeo.test.login&format=json'

facebookAuthorizeURL = 'https://www.facebook.com/dialog/oauth'
facebookAccessTokenURL = 'https://graph.facebook.com/oauth/access_token'
facebookUserInfoURL = 'https://graph.facebook.com/me'

googleAuthorizeURL = 'https://accounts.google.com/o/oauth2/auth'
googleAccessTokenURL = 'https://accounts.google.com/o/oauth2/token'
googleUserInfoURL = 'https://www.googleapis.com/oauth2/v2/userinfo'
googleContactListURL = 'https://www.google.com/m8/feeds/contacts/default/full/'

rootURL = getattr(settings, 'ROOT_URL')

@login_required
def apiTest(request, name):
	context={}
	return render_to_response('apiTest.html',context,context_instance=RequestContext(request))

@login_required
def sendUpdateNotification(request, name):
	relations = FriendRelation.objects.filter(user=request.user)
	for relation in relations:
		addNotificationInternal(request.user, relation.friend, 2, name)

@login_required
def connectTwitter(request):
	twitterConsumerKey = getattr(settings, 'TWITTER_CONSUMER_KEY')
	twitterConsumerSecret = getattr(settings, 'TWITTER_CONSUMER_SECRET')
	consumer = oauth.Consumer(twitterConsumerKey, twitterConsumerSecret)
	client = oauth.Client(consumer)
	client.ca_certs = certifi.where()
	resp, content = client.request(twitterRequestTokenURL, "POST", body=urllib.urlencode({"oauth_callback" : rootURL + "twitterCallback"}))

	if resp['status'] != '200':
	    raise Exception("Invalid response %s." % resp['status'])

	requestToken = dict(urlparse.parse_qsl(content))
	redirectURL = twitterAuthorizeURL + '?oauth_token='+requestToken['oauth_token']

	request.session['twitterRequestToken'] = requestToken

	return HttpResponseRedirect(redirectURL)

@login_required
def twitterCallback(request):
	twitterConsumerKey = getattr(settings, 'TWITTER_CONSUMER_KEY')
	twitterConsumerSecret = getattr(settings, 'TWITTER_CONSUMER_SECRET')


	consumer = oauth.Consumer(twitterConsumerKey, twitterConsumerSecret)


	#cancel handle
	if 'oauth_verifier' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	oauthVerifier = request.GET['oauth_verifier']
	token = oauth.Token(request.session['twitterRequestToken']['oauth_token'], request.session['twitterRequestToken']['oauth_token_secret'])
	token.set_verifier(oauthVerifier)
	client = oauth.Client(consumer, token)
	client.ca_certs = certifi.where()
	resp, content = client.request(twitterAccessTokenURL, "POST")
	if resp['status'] != '200':
	    raise Exception("Invalid response from Twitter.")

	accessToken = dict(urlparse.parse_qsl(content))

	#save account
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.twitter = 'https://twitter.com/'+ accessToken['screen_name']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'twitter')

	return HttpResponseRedirect('/myCard/')

@login_required
def connectGithub(request):
	#get application indentification
	githubClientID = getattr(settings, 'GITHUB_CLIENT_ID')

	redirectURL = githubAuthenticationURL + '?client_id='+ githubClientID + '&redirect_uri='+ rootURL +'githubCallback'

	return HttpResponseRedirect(redirectURL)

@login_required
def githubCallback(request):
	githubClientID = getattr(settings, 'GITHUB_CLIENT_ID')
	githubClientSecret = getattr(settings, 'GITHUB_CLIENT_SECRET')


	#cancel handle
	if 'code' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	code = request.GET['code']

	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = githubAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'client_id': githubClientID, 'client_secret': githubClientSecret, 'code':code}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	#use access token to get message
	accessToken = dict(urlparse.parse_qsl(content))
	url = githubUserInfoURL+ '?access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	userInformation = json.loads(content)

	#save account
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.github = userInformation['html_url']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'github')

	return HttpResponseRedirect('/myCard/')


@login_required
def connectTumblr(request):
	tumblrConsumerKey = getattr(settings, 'TUMBLR_CONSUMER_KEY')
	tumblrConsumerSecret = getattr(settings, 'TUMBLR_CONSUMER_SECRET')
	consumer = oauth.Consumer(tumblrConsumerKey, tumblrConsumerSecret)
	client = oauth.Client(consumer)
	client.ca_certs = certifi.where()
	resp, content = client.request(tumblrRequestTokenURL, "POST", body=urllib.urlencode({"oauth_callback" : rootURL + "tumblrCallback"}))

	requestToken = dict(urlparse.parse_qsl(content))
	redirectURL = tumblrAuthorizeURL + '?oauth_token='+requestToken['oauth_token']

	request.session['tumblrRequestToken'] = requestToken

	return HttpResponseRedirect(redirectURL)

@login_required
def tumblrCallback(request):
	tumblrConsumerKey = getattr(settings, 'TUMBLR_CONSUMER_KEY')
	tumblrConsumerSecret = getattr(settings, 'TUMBLR_CONSUMER_SECRET')

	consumer = oauth.Consumer(tumblrConsumerKey, tumblrConsumerSecret)

	#cancel handle
	if 'oauth_verifier' not in request.GET:
		return HttpResponseRedirect('/myCard/')


	oauthVerifier = request.GET['oauth_verifier']
	token = oauth.Token(request.session['tumblrRequestToken']['oauth_token'], request.session['tumblrRequestToken']['oauth_token_secret'])
	token.set_verifier(oauthVerifier)
	client = oauth.Client(consumer, token)
	client.ca_certs = certifi.where()
	resp, content = client.request(tumblrAccessTokenURL, "POST")
	if resp['status'] != '200':
	    raise Exception("Invalid response from Tumblr.")

	accessToken = dict(urlparse.parse_qsl(content))

	#use accesstoken to get user information
	consumer = oauth.Consumer(tumblrConsumerKey, tumblrConsumerSecret)
	token = oauth.Token(accessToken['oauth_token'], accessToken['oauth_token_secret'])
	client = oauth.Client(consumer, token)
	client.ca_certs = certifi.where()
	resp, content = client.request(tumblrUserInfoURL, "GET")
	#save account
	userInformation = json.loads(content)['response']['user']['blogs'][0]

	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.tumblr = userInformation['url']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'tumblr')

	return HttpResponseRedirect('/myCard/')

@login_required
def connectLinkedin(request):
	linkedinAPIKey = getattr(settings, 'LINKEDIN_API_KEY')

	redirectURL = linkedinAuthorizeURL + '?response_type=code&client_id='+ linkedinAPIKey+'&state=DCEEFWF45453sdffef424&redirect_uri='+ rootURL +'linkedinCallback'
	return HttpResponseRedirect(redirectURL)

@login_required
def linkedinCallback(request):
	linkedinAPIKey = getattr(settings, 'LINKEDIN_API_KEY')
	linkedinSecretKey = getattr(settings, 'LINKEDIN_SECRET_KEY')


	#cancel handle
	if 'code' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	code = request.GET['code']

	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = linkedinAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'grant_type': 'authorization_code', 'code':code, 'redirect_uri':rootURL+'linkedinCallback', 'client_id':linkedinAPIKey,'client_secret': linkedinSecretKey}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
	
	#use api to get person information
	accessToken = json.loads(content)
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = linkedinUserInfoURL+ '?oauth2_access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))
	
	#save account
	xmldoc = minidom.parseString(content)
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.linkedin = xmldoc.getElementsByTagName('url')[0].firstChild.nodeValue
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'linkedin')

	return HttpResponseRedirect('/myCard/')

@login_required
def connectInstagram(request):
	instagramClientID = getattr(settings, 'INSTAGRAM_CLIENT_ID')

	redirectURL = instagramAuthorizeURL + '?response_type=code&client_id='+ instagramClientID+'&redirect_uri=' + rootURL +'instagramCallback'
	return HttpResponseRedirect(redirectURL)

@login_required
def instagramCallback(request):
	instagramClientID = getattr(settings, 'INSTAGRAM_CLIENT_ID')
	instagramClientSecret = getattr(settings, 'INSTAGRAM_CLIENT_SECRET')

	#cancel handle
	if 'code' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	code = request.GET['code']
	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = instagramAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'client_id':instagramClientID,'client_secret': instagramClientSecret,'grant_type': 'authorization_code','redirect_uri':rootURL+'instagramCallback','code':code}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	
	#save account
	userInformation = json.loads(content)['user']
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.instagram = 'http://instagram.com/'+userInformation['username']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'instragram')

	return HttpResponseRedirect('/myCard/')

@login_required
def connectVimeo(request):
	vimeoClientID = getattr(settings, 'VIMEO_CLIENT_ID')
	vimeoClientSecret = getattr(settings, 'VIMEO_CLIENT_SECRET')
	consumer = oauth.Consumer(vimeoClientID, vimeoClientSecret)
	client = oauth.Client(consumer)
	client.ca_certs = certifi.where()
	resp, content = client.request(vimeoRequestTokenURL, "POST", body=urllib.urlencode({"oauth_callback" : rootURL +"vimeoCallback"}))

	if resp['status'] != '200':
	    raise Exception("Invalid response %s." % resp['status'])

	requestToken = dict(urlparse.parse_qsl(content))
	redirectURL = vimeoAuthorizeURL + '?oauth_token='+requestToken['oauth_token']

	request.session['vimeoRequestToken'] = requestToken
	return HttpResponseRedirect(redirectURL)

@login_required
def vimeoCallback(request):
	vimeoClientID = getattr(settings, 'VIMEO_CLIENT_ID')
	vimeoClientSecret = getattr(settings, 'VIMEO_CLIENT_SECRET')

	consumer = oauth.Consumer(vimeoClientID, vimeoClientSecret)


	#cancel handle
	if 'oauth_verifier' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	oauthVerifier = request.GET['oauth_verifier']
	token = oauth.Token(request.session['vimeoRequestToken']['oauth_token'], request.session['vimeoRequestToken']['oauth_token_secret'])
	token.set_verifier(oauthVerifier)
	client = oauth.Client(consumer, token)
	client.ca_certs = certifi.where()
	resp, content = client.request(vimeoAccessTokenURL, "POST")
	if resp['status'] != '200':
	    print content
	    raise Exception("Invalid response from Vimeo.")

	accessToken = dict(urlparse.parse_qsl(content))

	#get user information
	consumer = oauth.Consumer(vimeoClientID, vimeoClientSecret)
	token = oauth.Token(accessToken['oauth_token'], accessToken['oauth_token_secret'])
	client = oauth.Client(consumer, token)
	client.ca_certs = certifi.where()
	resp, content = client.request(vimeoUserInfoURL, "GET")
	userInformation = json.loads(content)['user']

	#save account
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.vimeo = 'https://vimeo.com/'+ userInformation['username']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'vimeo')

	return HttpResponseRedirect('/myCard/')

@login_required
def connectFacebook(request):
	facebookAppID = getattr(settings, 'FACEBOOK_APP_ID')

	redirectURL = facebookAuthorizeURL + '?client_id='+ facebookAppID+'&redirect_uri='+ rootURL +'facebookCallback'
	return HttpResponseRedirect(redirectURL)

@login_required
def facebookCallback(request):
	facebookAppID = getattr(settings, 'FACEBOOK_APP_ID')
	facebookAppSecret = getattr(settings, 'FACEBOOK_APP_SECRET')

	#cancel handle
	if 'code' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	code = request.GET['code']

	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = facebookAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'client_id':facebookAppID,'client_secret': facebookAppSecret,'redirect_uri':rootURL + 'facebookCallback','code':code}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	#use api to get person information
	accessToken = dict(urlparse.parse_qsl(content))
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = facebookUserInfoURL+ '?access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	#save account
	userInformation = json.loads(content)
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.facebook = userInformation['link']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'vimeo')

	return HttpResponseRedirect('/myCard/')


@login_required
def connectGoogle(request):
	googleClientID = getattr(settings, 'GOOGLE_CLIENT_ID')

	redirectURL = googleAuthorizeURL + '?client_id='+ googleClientID+'&response_type=code&scope=https://www.googleapis.com/auth/plus.me+https://www.google.com/m8/feeds/&redirect_uri=' + rootURL +'googleCallback'
	return HttpResponseRedirect(redirectURL)

@login_required
def googleCallback(request):
	googleClientID = getattr(settings, 'GOOGLE_CLIENT_ID')
	googleClientSecret = getattr(settings, 'GOOGLE_CLIENT_SECRET')



		#cancel handle
	if 'code' not in request.GET:
		return HttpResponseRedirect('/myCard/')

	code = request.GET['code']

	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = googleAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'code':code,'client_id':googleClientID,'client_secret': googleClientSecret,'redirect_uri':rootURL + 'googleCallback','grant_type':'authorization_code'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	#use api to get person information
	accessToken = json.loads(content)
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = googleUserInfoURL+ '?access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	#save account
	userInformation = json.loads(content)
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.googlePlus = 'https://plus.google.com/' + userInformation['id']
	card.save()

	#send notification to friends
	sendUpdateNotification(request,'google plus')

	return HttpResponseRedirect('/myCard/')

def connectLinkedinGetContactInfo(request):
	linkedinAPIKey = getattr(settings, 'LINKEDIN_API_KEY')

	redirectURL = linkedinAuthorizeURL + '?response_type=code&client_id='+ linkedinAPIKey+'&state=DCEEFWF45453sdffef424&redirect_uri='+ rootURL +'linkedinGetContactInfoCallback'
	return HttpResponseRedirect(redirectURL)

def linkedinGetContactInfoCallback(request):
	context = {}
	linkedinAPIKey = getattr(settings, 'LINKEDIN_API_KEY')
	linkedinSecretKey = getattr(settings, 'LINKEDIN_SECRET_KEY')

	#cancel handle
	if 'code' not in request.GET:
		return HttpResponseRedirect('/guide/3')

	code = request.GET['code']
	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = linkedinAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'grant_type': 'authorization_code', 'code':code, 'redirect_uri':rootURL+'linkedinGetContactInfoCallback', 'client_id':linkedinAPIKey,'client_secret': linkedinSecretKey}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
	

	#use api to get basic profile information
	accessToken = json.loads(content)
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = linkedinUserInfoURL+ ':(phone-numbers,email-address,headline)?format=json&oauth2_access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	#save account
	userInformation = json.loads(content)
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")

	card = card[0]
	#title
	if userInformation['headline']!='':
		context['title'] = userInformation['headline']
		card.title = userInformation['headline']
	#email
	if userInformation['emailAddress']!='':
		context['email'] = userInformation['emailAddress']
		card.email1 = userInformation['emailAddress']
	#phone number
	if(userInformation['phoneNumbers']['_total']>0):
		context['phone'] = userInformation['phoneNumbers']['values'][0]['phoneNumber']
		card.phone1 = userInformation['phoneNumbers']['values'][0]['phoneNumber']


	card.save()

		#use api to get person information
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = linkedinUserInfoURL+ '?oauth2_access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))
	
	#save account
	xmldoc = minidom.parseString(content)
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]
	card.linkedin = xmldoc.getElementsByTagName('url')[0].firstChild.nodeValue
	card.save()
	context['linkedin'] = True
	return render(request,'guide3.html',context)

@csrf_exempt
def connectFacebookGetBasicInfo(request):
	facebookAppID = getattr(settings, 'FACEBOOK_APP_ID')
	redirectURL = facebookAuthorizeURL + '?client_id='+ facebookAppID+'&redirect_uri='+ rootURL +'facebooketGetBasicInfoCallback'
	return HttpResponseRedirect(redirectURL)

@csrf_exempt
def facebooketGetBasicInfoCallback(request):
	context={}
	facebookAppID = getattr(settings, 'FACEBOOK_APP_ID')
	facebookAppSecret = getattr(settings, 'FACEBOOK_APP_SECRET')

	if 'code' not in request.GET:
		HttpResponseRedirect('/guide/2')

	code = request.GET['code']

	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = facebookAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'client_id':facebookAppID,'client_secret': facebookAppSecret,'redirect_uri':rootURL + 'facebooketGetBasicInfoCallback','code':code}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	#use api to get person information
	accessToken = dict(urlparse.parse_qsl(content))
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = facebookUserInfoURL+ '?access_token=' + accessToken['access_token']
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	#save account
	userInformation = json.loads(content)
	card = Card.objects.filter(user=request.user)
	if len(card)<=0:
	    raise Exception("Can not find card")
	card = card[0]

	if 'first_name' in userInformation and userInformation['first_name']!='':
		card.firstName = userInformation['first_name']
		context['firstName'] = userInformation['first_name']
	if 'last_name' in userInformation and userInformation['last_name']!='':
		card.lastName = userInformation['last_name']
		context['lastName'] = userInformation['last_name']
	if 'gender' in userInformation and userInformation['gender']!='':
		if userInformation['gender']=='male':
			context['gender'] = 'Male'
			card.gender = 'M'
		else:
			context['gender'] = 'Female'
			card.gender = 'F'
			
	card.facebook = userInformation['link']
	card.save()
	context['facebook'] = True 
	return render(request,'guide2.html',context)

def connectGoogleGetEmailList(request):
	googleClientID = getattr(settings, 'GOOGLE_CLIENT_ID')

	redirectURL = googleAuthorizeURL + '?client_id='+ googleClientID+'&response_type=code&scope=https://www.googleapis.com/auth/plus.me+https://www.google.com/m8/feeds/&redirect_uri=' + rootURL +'googleGetEmailListCallback'
	return HttpResponseRedirect(redirectURL)

def googleGetEmailListCallback(request):
	googleClientID = getattr(settings, 'GOOGLE_CLIENT_ID')
	googleClientSecret = getattr(settings, 'GOOGLE_CLIENT_SECRET')

	#cancel handle
	if 'code' not in request.GET:
		HttpResponseRedirect('/guide/5')

	code = request.GET['code']
	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = googleAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'code':code,'client_id':googleClientID,'client_secret': googleClientSecret,'redirect_uri':rootURL + 'googleGetEmailListCallback','grant_type':'authorization_code'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	#use api to get person information
	accessToken = json.loads(content)
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = googleContactListURL+ '?access_token=' + accessToken['access_token'] +'&alt=json'
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	# search friends
	contactEmails = []
	contactInfos = json.loads(content)['feed']['entry']
	for i in range(len(contactInfos)):
		email = contactInfos[i]['gd$email'][0]['address']
		contactEmails.append(email)

	print contactEmails
	relations = FriendRelation.objects.filter(user=request.user)
	friends = [relation.friend for relation in relations]
	friends.append(request.user)
	rawCards = Card.objects.exclude(user__in=friends).filter(Q(email1__in=contactEmails) | Q(email2__in=contactEmails) | Q(email3__in=contactEmails) | Q(email4__in=contactEmails) | Q(email5__in=contactEmails))

	cards=[]
	for rawCard in rawCards:
		cards.append(rawCard.getCardWithPermission(PermissionTemplate.generatePermissionStr('stranger')))

	context = {}
	context['friends'] = cards
	context['guide'] = True
	return render(request,'guide5.html',context)

def connectGoogleSearchEmailList(request):
	googleClientID = getattr(settings, 'GOOGLE_CLIENT_ID')

	redirectURL = googleAuthorizeURL + '?client_id='+ googleClientID+'&response_type=code&scope=https://www.googleapis.com/auth/plus.me+https://www.google.com/m8/feeds/&redirect_uri=' + rootURL +'googleSearchEmailListCallback'
	return HttpResponseRedirect(redirectURL)

def googleSearchEmailListCallback(request):
	googleClientID = getattr(settings, 'GOOGLE_CLIENT_ID')
	googleClientSecret = getattr(settings, 'GOOGLE_CLIENT_SECRET')

	if 'code' not in request.GET:
		HttpResponseRedirect('/search/')

	code = request.GET['code']
	# get access token
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = googleAccessTokenURL
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {'code':code,'client_id':googleClientID,'client_secret': googleClientSecret,'redirect_uri':rootURL + 'googleSearchEmailListCallback','grant_type':'authorization_code'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))

	#use api to get person information
	accessToken = json.loads(content)
	http = httplib2.Http(disable_ssl_certificate_validation=True)
	url = googleContactListURL+ '?access_token=' + accessToken['access_token'] +'&alt=json'
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	body = {}
	response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

	# search friends
	contactEmails = []
	contactInfos = json.loads(content)['feed']['entry']
	for i in range(len(contactInfos)):
		email = contactInfos[i]['gd$email'][0]['address']
		contactEmails.append(email)

	relations = FriendRelation.objects.filter(user=request.user)
	friends = [relation.friend for relation in relations]
	friends.append(request.user)
	rawCards = Card.objects.exclude(user__in=friends).filter(Q(email1__in=contactEmails) | Q(email2__in=contactEmails) | Q(email3__in=contactEmails) | Q(email4__in=contactEmails) | Q(email5__in=contactEmails))

	cards=[]
	for rawCard in rawCards:
		cards.append(rawCard.getCardWithPermission(PermissionTemplate.generatePermissionStr('stranger')))

	context = {}
	context['cards'] = cards
	context['guide'] = True
	return render(request,'search.html',context)