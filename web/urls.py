from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="web"

urlpatterns = [
    path('form/', views.form_page, name='form_page'),
    path('work/', views.work_page, name='work_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)