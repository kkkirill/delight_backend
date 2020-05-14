from storages.backends.s3boto3 import S3Boto3Storage

from delight import settings
from delight.settings import AWS_STATIC_BUCKET_NAME


class StaticStorage(S3Boto3Storage):
    bucket_name = AWS_STATIC_BUCKET_NAME

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.STATIC_CLOUDFRONT_DOMAIN.replace('https://', '')

        super().__init__(*args, **kwargs)
