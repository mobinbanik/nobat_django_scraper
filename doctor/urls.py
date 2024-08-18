from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import run_scraper, pwd, doctor_profile, doctors_list

urlpatterns = [
    path('', run_scraper, name='run_scraper'),
    path('pwd/', pwd, name='pwd'),
    path('doctor/<int:doctor_id>/', doctor_profile, name='doctor_profile'),
     path('doctors/', doctors_list, name='doctors_list'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)