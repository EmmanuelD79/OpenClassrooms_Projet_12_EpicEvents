from django.shortcuts import get_object_or_404

from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response

from permissions.permissions_mixins import GetPermissionMixin

from .filters import ClientFilter
from .models import Client
from .serializers import ClientSerializer


class ClientViewset(GetPermissionMixin, viewsets.ModelViewSet): 
    __basic_fields = ('last_name', 'email')
    queryset = Client.objects.all()    
    serializer_class = ClientSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClientFilter
    search_fields = __basic_fields
    ordering_fields = __basic_fields

    def get_object(self):
        obj = get_object_or_404(self.queryset, id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(sales_contact_id=self.request.user)
        
    def update(self, request, pk=None):
        client = self.get_object()
        serializer = self.serializer_class(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    