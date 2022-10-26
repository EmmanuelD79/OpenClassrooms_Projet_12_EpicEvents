from rest_framework import routers
from .views import ContratViewset


contrat_urls = routers.DefaultRouter()
contrat_urls.register(r'contracts', ContratViewset, basename='contract')

urlpatterns = contrat_urls.urls
