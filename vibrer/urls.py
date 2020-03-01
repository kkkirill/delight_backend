from django.urls import include, path

from apps.media.routers import router

urlpatterns = [
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
]
