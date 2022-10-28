from rest_framework import serializers
from .models import Contract
from clients.models import Client, ClientStatus
from django.shortcuts import get_object_or_404


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'client_id', 'name', 'status', 'payment_due', 'amount_float']
        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data = self.check_is_client(validated_data)
        return Contract.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        validated_data = self.check_is_client(validated_data)
        return super().update(instance, validated_data)
    
    def check_is_client(self, validated_data):
        client_id = validated_data['client_id']
        client = Client.objects.filter(id=client_id.id)
        active_client = get_object_or_404(client)
        if active_client.status.status != "Client":
            raise serializers.ValidationError({'client_id': "Status client isn't Client"})
        return validated_data
