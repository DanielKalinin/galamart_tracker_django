from django.conf.urls import url

from project_manager import urls as pm_urls
from user_profile import urls as user_urls

urlpatterns = [
    *pm_urls.urlpatterns,
    *user_urls.urlpatterns,
]
