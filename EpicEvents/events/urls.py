from rest_framework import routers
from .views import EventViewset


event_urls = routers.SimpleRouter()
event_urls.register(r'events', EventViewset, basename='event')

urlpatterns = event_urls.urls
