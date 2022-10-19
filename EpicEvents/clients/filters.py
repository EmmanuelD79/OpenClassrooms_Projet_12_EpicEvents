from django_filters import rest_framework as filters
from .models import Client

class ClientFilter(filters.FilterSet):
    """
    Client filter for API search.
    """
    class Meta:
        model = Client
        fields = {
            'last_name': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains', 'istartswith']
        }
        
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        
        if user.is_superuser:
            return parent.all()
        else:
            return parent.filter(sales_contact_id=user) | parent.filter(contract__event__support_contact_id=user)