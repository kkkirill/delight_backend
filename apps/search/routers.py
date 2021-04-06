from rest_framework import routers

router = routers.DefaultRouter()
router.register('search', views.SKUSearchViewSet, base_name='global_search')
