from django_filters import rest_framework as filters
from .models import Event

class EventFilter(filters.FilterSet):
    """
    Event filter for API search.
    """
    class Meta:
        model = Event
        fields = {
            'contract_id__client_id__last_name': ['exact', 'icontains'],
            'contract_id__client_id__email': ['exact', 'icontains'],
            'event_date': ['exact'],
        }

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        
        if user.is_superuser:
            return parent.all()
        else:
            return parent.filter(contract_id__client_id__sales_contact_id=user) | parent.filter(support_contact_id=user)
