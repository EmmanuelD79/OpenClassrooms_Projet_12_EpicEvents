from rest_framework import serializers
from .models import Event
from contracts.models import Contract
from django.shortcuts import get_object_or_404


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['contract_id', 'event_status', 'event_date', 'attendees', 'notes', 'support_contact_id']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'support_contact_id': {'read_only': True},
        }

    def create(self, validated_data):
        contract_id = validated_data['contract_id']

        contract = Contract.objects.filter(id=contract_id.id)
        active_contract = get_object_or_404(contract)
        if active_contract.status:
            return Event.objects.create(**validated_data)
        else:
            raise serializers.ValidationError({'contract_id': "Contract isn't valid"})


class EventUpdateSerializer(EventSerializer):

    class Meta:
        model = Event
        fields = ['contract_id', 'event_status', 'event_date', 'attendees', 'notes', 'support_contact_id']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'support_contact_id': {'read_only': True},
            'contract_id': {'read_only': True},
        }
