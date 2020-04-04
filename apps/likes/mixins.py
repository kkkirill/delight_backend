from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.likes import mixin_tools
from apps.likes.serializers.like import FanSerializer


class LikedMixin:

    @action(methods=['POST', 'DELETE'], detail=True, )
    def like(self, request, pk=None, **kwargs):
        if self.request.method == 'POST':
            obj = self.get_object()
            if mixin_tools.is_fan(obj, request.user):
                return Response(status=status.HTTP_409_CONFLICT)
            mixin_tools.add_like(obj, request.user)
            return Response()
        elif self.request.method == 'DELETE':
            obj = self.get_object()
            if not mixin_tools.is_fan(obj, request.user):
                return Response(status=status.HTTP_404_NOT_FOUND)
            mixin_tools.remove_like(obj, request.user)
            return Response()

    @action(methods=['GET'], detail=True,)
    def fans(self, request, pk=None, **kwargs):
        obj = self.get_object()
        fans = mixin_tools.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
