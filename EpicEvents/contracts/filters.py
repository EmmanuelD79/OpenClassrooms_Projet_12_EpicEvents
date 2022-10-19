from django_filters import rest_framework as filters
from .models import Contract


class ContractFilter(filters.FilterSet):
    """
    Contract filter for API search.
    """
    class Meta:
        model = Contract
        fields = {
            'client_id__last_name': ['exact', 'icontains'],
            'client_id__email': ['exact', 'icontains'],
            'date_created': ['exact'],
            'amount_float': ['exact'],
        }
    
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        
        if user.is_superuser:
            return parent.all()
        else:
            return parent.filter(client_id__sales_contact_id=user)| parent.filter(event__support_contact_id=user)