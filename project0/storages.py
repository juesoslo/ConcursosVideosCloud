from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_S3_CUSTOM_DOMAIN
        super(StaticStorage, self).__init__(*args, **kwargs)
