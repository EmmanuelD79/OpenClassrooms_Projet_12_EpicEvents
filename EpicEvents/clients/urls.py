from rest_framework import routers
from .views import ClientViewset


client_urls = routers.SimpleRouter()
client_urls.register(r'clients', ClientViewset, basename='client')

urlpatterns = client_urls.urls
