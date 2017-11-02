from django.conf.urls import url
from . import apis 

urlpatterns = [
    url(
        regex="^users/(?P<pk>\d+)/$",
        view=apis.UsersApiDetailView.as_view(),
        name='users',
    ),
    url(
        regex="^users/~native/$",
        view=apis.UsersNativeApiListView.as_view(),
        name='users_native',
    ),
    url(
        regex="^users/~learn/$",
        view=apis.UsersLearnApiListView.as_view(),
        name='users_learn',
    ),    
]