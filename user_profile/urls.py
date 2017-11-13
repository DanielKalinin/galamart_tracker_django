from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^user/create$', UserViewSet.as_view({'post': 'create'})),
    url(r'^user/confirm$', UserViewSet.as_view({'post': 'confirm'})),
    url(r'^user/get$', UserViewSet.as_view({'get': 'retrieve'})),
    url(r'^user/personal$', UserViewSet.as_view({'get': 'personal'})),
]
