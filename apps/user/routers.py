from rest_framework import routers

from apps.user.views.user import UserView


router = routers.DefaultRouter()
router.register('user', UserView)
