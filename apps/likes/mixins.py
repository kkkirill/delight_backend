from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.openapi import Response as SwaggerResponse

from apps.likes import mixin_tools
from apps.likes.serializers.like import FanSerializer, LikeSerializer
from apps.user.models import User


class LikedMixin:
    @swagger_auto_schema(
        method='post',
        operation_description='# Create like',
        responses={
            '200': SwaggerResponse(
                'Like has been created successfully',
                FanSerializer()
            ),
            '400': 'Bad request',
            '409': 'Multiple user like',
            '401': 'Unauthorized',
            '403': 'Permission denied'
        }
    )
    @swagger_auto_schema(
        method='delete',
        operation_description='# Delete like',
        responses={
            '204': SwaggerResponse(
                'Like has been deleted successfully',
                LikeSerializer()
            ),
            '401': 'Unauthorized',
            '403': 'Permission denied'
        }
    )
    @action(methods=['POST', 'DELETE'], detail=True, )
    def like(self, request, pk=None, **kwargs):
        if self.request.method == 'POST':
            obj = self.get_object()
            if mixin_tools.is_fan(obj, request.user):
                return Response(status=status.HTTP_409_CONFLICT)
            if isinstance(obj, User):
                mixin_tools.add_follower(obj, request.user)
            mixin_tools.add_like(obj, request.user)
            return Response()
        elif self.request.method == 'DELETE':
            obj = self.get_object()
            if not mixin_tools.is_fan(obj, request.user):
                return Response(status=status.HTTP_404_NOT_FOUND)
            if isinstance(obj, User):
                mixin_tools.remove_follower(obj, request.user)
            mixin_tools.remove_like(obj, request.user)
            return Response()

    @method_decorator(name='fans', decorator=swagger_auto_schema(
        operation_description='# Returns the list of users following current object',
        responses={
            '200': 'List of fans received'
        }
    ))
    @action(methods=['GET'], detail=True, )
    def fans(self, request, pk=None, **kwargs):
        obj = self.get_object()
        fans = mixin_tools.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
