from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import run_scraper, pwd

urlpatterns = [
    path('', run_scraper, name='run_scraper'),
    path('pwd/', pwd, name='pwd'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)