from django.conf.urls import url
from . import apis 

urlpatterns = [
    url(
        regex="^rooms/$",
        view=apis.RoomsApiListView.as_view(),
        name='rooms',
    ),
    url(
        regex="^rooms/(?P<pk>\d+)/messages/$",
        view=apis.MessagesApiListView.as_view(),
        name='messages',
    ),
]