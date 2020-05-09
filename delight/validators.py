from django.core.validators import URLValidator

from delight.settings import STATIC_CLOUDFRONT_DOMAIN


class CustomURLValidator(URLValidator):
    def __call__(self, value):
        return STATIC_CLOUDFRONT_DOMAIN in value and super().__call__(value)
