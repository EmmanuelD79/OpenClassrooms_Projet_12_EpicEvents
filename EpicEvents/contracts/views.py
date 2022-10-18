from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from permissions.permissions import HasGroupPerms
from .models import Contract
from .serializers import ContractSerializer


class ContratViewset(viewsets.ViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def get_object(self):
        obj = get_object_or_404(Contract.objects.all(), id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy', 'update', 'retrieve']:
            self.permission_classes = [HasGroupPerms]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_queryset(self):
        return Contract.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        client = self.get_object()
        serializer = ContractSerializer(client)
        return Response(serializer.data)

    def create(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        client = self.get_object()
        serializer = ContractSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
