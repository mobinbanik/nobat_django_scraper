from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import run_scraper

urlpatterns = [
    path('', run_scraper, name='run_scraper'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)