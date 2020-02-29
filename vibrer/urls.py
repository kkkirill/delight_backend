from django.conf.urls.static import static
from django.urls import path, include

from apps.media.routers import router
from vibrer.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
