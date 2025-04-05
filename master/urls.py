from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('utilisateurs.urls')),  
    path('geospatial/',include('UL.urls')),  
  
  ]
  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# #pour l'hebergement les static
# urlpatterns +=staticfiles_urlpatterns()
