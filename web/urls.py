from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="web"

urlpatterns = [
    path("", views.test, name='test'),
    path('form/', views.form_page, name='form'),
    path('home', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)