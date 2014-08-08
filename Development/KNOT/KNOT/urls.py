from django.conf.urls import patterns, include, url
from KNOT.views import *

from Friend.views import *

from Card.views import *
from Notification.views import *
from Permission.views import *

from UserManagement.views import *
from UserManagement.forms import *

from SNS.views import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'KNOT.views.home', name='home'),
    # url(r'^KNOT/', include('KNOT.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),


    #url return html
    url(r'^myCard/$',myCardHtml, name='myCard'),
    url(r'^otherCard/(.+)$',otherCardHtml, name='otherCard'),
    url(r'^timeline/(.+)$',timelineHtml, name='timeline'),
    url(r'^notification/$',notificationHtml, name='notification'),
    url(r'^search/$',searchHtml, name='search'),
    url(r'^contacts/(.+)$',contactsHtml, name='contacts'),
    url(r'^getPermissionTemplate/(.+)$',getPermissionTemplateHtml, name='getPermissionTemplate'),


    #user account html and ajax
    # url(r'^$', 'django.contrib.auth.views.login', {'template_name':'login.html','authentication_form':MyAuthenticationForm},name='login'),
    url(r'^$',login,name='login'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^register/$',register, name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'UserManagement.views.confirm_registration', name='confirm'),
    url(r'^forget/$','UserManagement.views.forget_password',name='forget'),
    url(r'^reset_password/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$','UserManagement.views.reset_password1',name='reset_password1'),
    url(r'^reset/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)/(?P<token>[a-z0-9\-]+)$', 'UserManagement.views.reset_password', name='reset'),
    url(r'^account/(.+)$','UserManagement.views.accountSetting',name='account'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^guide/(.+)$','UserManagement.views.guide',name='guide'),
    # url(r'^guideRedirect/$','UserManagement.views.guideRedirect',name='guideRedirect'),
    # url(r'^guideRedirectGmail/$','UserManagement.views.guideRedirectGmail',name='guideRedirectGmail'),
    # url(r'^guideRedirectLinkedIn/$','UserManagement.views.guideRedirectLinkedIn',name='guideRedirectLinkedIn'),
    url(r'^confirmEmail/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$','UserManagement.views.confirmEmail',name='confirmEmail'),


    #notification ajax
    url(r'^getNotification/', getNotification, name='getNotification'),
    url(r'^deleteNotification/', deleteNotification, name='deleteNotification'),

    #my card ajax
    url(r'^updateMyCard/', updateMyCard, name='updateMyCard'),
    url(r'^getMyCard/', getMyCard, name='getMyCard'),

    #friend ajax
    url(r'^recommendFriend/',recommendFriend, name=recommendFriend),
    url(r'^addFriend/$', addFriend, name='addFriend'),
    url(r'^deleteFriend/$', deleteFriend, name='deleteFriend'),
    url(r'^getFriendList/(.+)$', getFriendList, name='getFriendList'),
    url(r'^addFriendRequest/', addFriendRequest, name='addFriendRequest'),
    url(r'^getFriendLocation/$', getFriendLocation, name='getFriendLocation'),


    #permission template ajax
    url(r'^addPermissionTemplate/', addPermissionTemplate, name='addPermissionTemplate'),
    url(r'^updatePermissionTemplate/',updatePermissionTemplate, name='updatePermissionTemplate'),
    url(r'^deletePermissionTemplate/',deletePermissionTemplate, name='deletePermissionTemplate'),
    url(r'^updateFriendPermission',updateFriendPermission, name='updateFriendPermission'),

    #CSV ajax
    url(r'^exportCSV/',exportCSV, name='exportCSV'),

    #media image and audio ajax
    # url(r'^captureAudioAndSnapShot/',captureAudioAndSnapShot, name='captureAudioAndSnapShot'),
    url(r'^uploadImageFromCamera/', uploadImageFromCamera, name='uploadImageFromCamera'),
    url(r'^uploadImageFromFile/', uploadImageFromFile, name='uploadImageFromFile'),
    url(r'^getRecoderWorker/$', getRecoderWorker, name='getRecoderWorker'),
    url(r'^uploadAudio/$', uploadAudio, name='uploadAudio'),

    #for connect SNS account all ajax
    url(r'^connectTwitter/$', connectTwitter, name='connectTwitter'),
    url(r'^twitterCallback/$', twitterCallback, name='twitterCallback'),
    url(r'^connectGithub/$', connectGithub, name='connectGithub'),
    url(r'^githubCallback/$', githubCallback, name='githubCallback'),
    url(r'^connectTumblr/$', connectTumblr, name='connectTumblr'),
    url(r'^tumblrCallback/$', tumblrCallback, name='tumblrCallback'),
    url(r'^connectLinkedin/$', connectLinkedin, name='connectLinkedin'),
    url(r'^linkedinCallback/$', linkedinCallback, name='linkedinCallback'),
    url(r'^connectInstagram/$', connectInstagram, name='connectInstagram'),
    url(r'^instagramCallback/$', instagramCallback, name='instagramCallback'),
    url(r'^connectInstagram/$', connectInstagram, name='connectInstagram'),
    url(r'^instagramCallback/$', instagramCallback, name='instagramCallback'),
    url(r'^connectVimeo/$', connectVimeo, name='connectVimeo'),
    url(r'^vimeoCallback/$', vimeoCallback, name='vimeoCallback'),
    url(r'^connectFacebook/$', connectFacebook, name='connectFacebook'),
    url(r'^facebookCallback/$', facebookCallback, name='facebookCallback'),
    url(r'^connectGoogle/$', connectGoogle, name='connectGoogle'),
    url(r'^googleCallback/$', googleCallback, name='googleCallback'),


    #linkedin get title email and phone ajax
    url(r'^connectLinkedinGetContactInfo/$', connectLinkedinGetContactInfo, name='connectLinkedinGetContactInfo'),
    url(r'^linkedinGetContactInfoCallback/$', linkedinGetContactInfoCallback, name='linkedinGetContactInfoCallback'),
    #facebook get  firstName, lastName, gender ajax
    url(r'^connectFacebookGetBasicInfo/$', connectFacebookGetBasicInfo, name='connectFacebookGetBasicInfo'),
    url(r'^facebooketGetBasicInfoCallback/$', facebooketGetBasicInfoCallback, name='facebooketGetBasicInfoCallback'),
    #google get contact info ajax
    url(r'^connectGoogleGetEmailList/$', connectGoogleGetEmailList, name='connectGoogleGetEmailList'),
    url(r'^googleGetEmailListCallback/$', googleGetEmailListCallback, name='googleGetEmailListCallback'),
    url(r'^connectGoogleSearchEmailList/$', connectGoogleSearchEmailList, name='connectGoogleSearchEmailList'),
    url(r'^googleSearchEmailListCallback/$', googleSearchEmailListCallback, name='googleSearchEmailListCallback'),

    #backend test
    url(r'^apiTest/$', apiTest, name='apiTest'),

    
    
)
