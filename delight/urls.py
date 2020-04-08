from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from apps.media.routers import router as me_router
from apps.user import urls as user_urls
from apps.user.routers import router as us_router


class ApiRouter(routers.DefaultRouter):

    def extend(self, router):
        self.registry.extend(router.registry)


schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API', default_version='v1',
        description='This endpoint shows the API of all RESTful endpoints in '
                    '`delight` application',
    ),
    public=True, permission_classes=(permissions.AllowAny,)
)

router = ApiRouter()
router.extend(me_router)
router.extend(us_router)

urlpatterns = (
    path('api/', include(router.urls)),
    path('auth/', include(user_urls)),
    path('swagger.json', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc')
)
