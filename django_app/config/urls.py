"""URL routing for the face analysis application."""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
]