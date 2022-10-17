from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'client_id', 'status', 'payment_due', 'amount_float', 'sales_contact_id']
        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'sales_contact_id': {'read_only': True},
        }
        