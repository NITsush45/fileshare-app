from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the File Share App!")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include(('fileshare.urls', 'fileshare'), namespace='fileshare')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
