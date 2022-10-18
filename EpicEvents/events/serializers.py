from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['contract_id', 'event_status' , 'event_date', 'attendees', 'notes', 'support_contact_id']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'support_contact_id': {'read_only': True},
        }

class EventUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ['contract_id', 'event_status' , 'event_date', 'attendees', 'notes', 'support_contact_id']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'support_contact_id': {'read_only': True},
            'contract_id': {'read_only': True},
        }
    