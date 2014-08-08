# Create your views here.
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
import pdb

def saveFile(fileName, fileContent, fileContentType):

	accessKey = getattr(settings, 'AWS_ACCESS_KEY_ID')
	secretKey = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
	bucketName = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
	connection = S3Connection(accessKey, secretKey)

	knotBucket = connection.get_bucket(bucketName)
	k = Key(knotBucket)
	k.key = fileName
	k.content_type=fileContentType
	k.set_contents_from_string(fileContent, policy='public-read')
	url =  k.generate_url(0, 'GET', None, False, None, False)
	return url

def loadFile(fileName):
	accessKey = getattr(settings, 'AWS_ACCESS_KEY_ID')
	secretKey = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
	bucketName = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
	connection = S3Connection(accessKey, secretKey)

	knotBucket = connection.get_bucket(bucketName)
	k = knotBucket.get_key(fileName)
	fileContent = None
	if k:
		fileContent = k.get_contents_as_string()
	return fileContent