from django.shortcuts import get_object_or_404

from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from permissions.permissions import HasGroupPerms

from .filters import EventFilter
from .models import Event
from .serializers import EventSerializer, EventUpdateSerializer


class EventViewset(viewsets.ModelViewSet):
    __basic_fields = ('contract_id__client_id__last_name', 'contract_id__client_id__email', 'event_date')   
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = __basic_fields
    ordering_fields = __basic_fields
    
    def get_object(self):
        obj = get_object_or_404(Event.objects.all(), contract_id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy', 'update', 'retrieve']:
            self.permission_classes = [HasGroupPerms]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(support_contact_id=self.request.user)
        
    def update(self, request, pk=None):
        event = self.get_object()
        serializer = EventUpdateSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
