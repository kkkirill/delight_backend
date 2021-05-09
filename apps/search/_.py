# from django.utils.decorators import method_decorator
# from drf_yasg.openapi import Response as SwaggerResponse
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.permissions import (
#     AllowAny)
# from rest_framework.viewsets import ModelViewSet
#
# from utils.permission_tools import ActionBasedPermission
#
#
# @method_decorator(name='list', decorator=swagger_auto_schema(
#     operation_description='# Get list of all albums',
#     responses={
#         '200': SwaggerResponse(
#             'The list of albums has been retrieved successfully',
#             'SERIALIZER'
#         )
#     }
# ))
# class AlbumView(ModelViewSet):
#     queryset = 'DOCUMENT_CLASS'
#     http_method_names = ('get',)
#     permission_classes = (ActionBasedPermission,)
#     action_permissions = {
#         AllowAny: ('list',),
#     }
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET' and self.action == 'list':
#             return 'SERIALIZER'
#
#         return super().get_serializer_class()
