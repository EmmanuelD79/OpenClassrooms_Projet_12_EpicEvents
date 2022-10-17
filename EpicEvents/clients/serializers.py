from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'status', 'sales_contact_id']
        extra_kwargs = {
            'id': {'read_only': True},
            'sales_contact_id': {'read_only': True},
        }
        