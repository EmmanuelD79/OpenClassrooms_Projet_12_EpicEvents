from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'client_id', 'name', 'status', 'payment_due', 'amount_float']
        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True}
        }
        