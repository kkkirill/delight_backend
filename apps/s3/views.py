from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.s3.models import File
from apps.s3.serializers import FileSerializer
from utils.permission_tools import ActionBasedPermission


class S3View(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    http_method_names = ('get', 'post', 'put', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsAuthenticated: ('create',),
        IsAdminUser: ('update', 'destroy'),
    }
