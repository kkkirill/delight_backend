from rest_framework import routers

from apps.s3.views import S3View

router = routers.DefaultRouter()
router.register('', S3View)
