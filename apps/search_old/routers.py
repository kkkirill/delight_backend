from rest_framework import routers

from apps.search_old.view import GlobalDocumentViewSet

router = routers.DefaultRouter()
router.register('search_old', GlobalDocumentViewSet, basename='search_old')

