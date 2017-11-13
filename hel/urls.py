from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from project_manager import urls as pm_urls
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth', obtain_jwt_token),
    url(r'^api-token-verify', verify_jwt_token),
    url(r'^api/', include('hel.api_urls')),

    url(r'^', views.index),
]\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

