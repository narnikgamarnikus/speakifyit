from rest_framework import viewsets, status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from annoying.functions import get_object_or_None


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = []

    @list_route(methods=['POST'])
    def is_read(self, request):
    	pk = request.data.get('id', None)
    	print(pk)
    	notification = get_object_or_None(Notification, id=pk)
    	print(notification)
    	if notification:
    		notification.is_read = True
    		return Response(status=status.HTTP_200_OK)
    	return Response(status=status.HTTP_404_NOT_FOUND)