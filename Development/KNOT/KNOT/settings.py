# Django settings for KNOT project.
import os



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.andrew.cmu.edu'
EMAIL_PORT=587
EMAIL_HOST_USER='mengyanw'
EMAIL_HOST_PASSWORD='Wmy@19901212'
EMAIL_USE_TLS = True


DEBUG = True
TEMPLATE_DEBUG = DEBUG
APP_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(APP_ROOT, os.pardir)

ADMINS = (
    ('Wenbing Bai', 'wbai@andrew.cmu.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'knot',                      # Or path to database file if using sqlite3.
        'USER': 'WEBTEAM16',
        'PASSWORD': '15637',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT+'/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT,'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_0!k1rg3io5euygpv4%j-d%&amp;8zgk3&amp;nem^%3u#&amp;8f$b1^$86@p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_HOST = 'smtp.andrew.cmu.edu'
# EMAIL_HOST_USER = 'wbai'
# EMAIL_HOST_PASSWORD = 'Sand1990!'
# EMAIL_USE_TLS = True

# To enable real email-sending, you should uncomment and 
# configure the settings below.
# EMAIL_HOST = 'Your-SMTP-host'               # perhaps 'smtp.andrew.cmu.edu'
# EMAIL_HOST_USER = 'Your-SMTP-username'      # perhaps your Andrew ID
# EMAIL_HOST_PASSWORD = 'Your-SMTP-password'
# EMAIL_USE_TLS = True

ROOT_URLCONF = 'KNOT.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'KNOT.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT,'templates').replace('\\','/'),
)

# for getting url in templates(used in timeline)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Card',
    'Friend',
    'Notification',
    'UserManagement',
    'Permission',
    'SNS',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = '/timeline/1'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#storage system
# DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_ACCESS_KEY_ID = 'AKIAI7BF6L4ALOFHDCPA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'knot'
# from S3 import CallingFormat
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN 
# AWS_HEADERS = {
#     'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT', # see http://developer.yahoo.com/performance/rules.html#expires
#     'Cache-Control': 'max-age=86400',
#     }



#SNS
TWITTER_CONSUMER_KEY = 'hHsmT6Oao2hRCfzlPM8QqQ'
TWITTER_CONSUMER_SECRET = 'GBATDdIMxsIfVIYzNfWvw32cIWGnbDiCCgslVSKasZw'
GITHUB_CLIENT_ID = 'aee026b30d39b09b279e'
GITHUB_CLIENT_SECRET = '235e79785078e5528cea0280c8829961fc5628a4'
TUMBLR_CONSUMER_KEY = 'IGKfkfYPlDhZTXjDuUH18E9VkAUXGM3nns6f2uRTjg8WW6HCOq'
TUMBLR_CONSUMER_SECRET = 'l6QekOfnH8SDrMZ6JTLtHK5JH9UEtwLHA5UABILKAOhpwdV5xt'
LINKEDIN_API_KEY = '77wfsejely7l93'
LINKEDIN_SECRET_KEY = 'a8HSfMu0D9rZDnDa'
INSTAGRAM_CLIENT_ID = '8a9c84de5b2f494d9d3f99e400d20b73'
INSTAGRAM_CLIENT_SECRET = '6a35b50faa5b423e9e8e602d5d87778a'
VIMEO_CLIENT_ID = 'a04ea982eafb40aa256891e0bfc809519dcac607'
VIMEO_CLIENT_SECRET = '5d29621be0ebe205ec01f9c68891c9828ccc82c3'
GOOGLE_CLIENT_ID = '985774456109.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'yIcynp2Ii1KZx_irrr3lTLAQ'
FACEBOOK_APP_ID = '702950619717607'
FACEBOOK_APP_SECRET = '4481c7e0830f2f8b87a0fe3e9adefb41'

#root url
# ROOT_URL = 'http://127.0.0.1:8000/'
ROOT_URL = 'http://localhost:8000/'