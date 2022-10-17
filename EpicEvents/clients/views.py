from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Client, ClientStatus
from .serializers import ClientSerializer


class ClientViewset(viewsets.ViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_object(self):
        obj = get_object_or_404(Client.objects.all(), id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action in ['create''retrieve', 'destroy', 'update']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list']:
            self.permission_classes = []
        return super().get_permissions()
    
    def get_queryset(self):
        return Client.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        client = self.get_object()
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(sales_contact_id=self.request.user)
        
    def update(self, request, pk=None):
        client = self.get_object()
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
