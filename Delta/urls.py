# urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # account url
    path('useracc/', include('useracc.urls')),  
   
    # front urls
    path('', include('front.urls')),

    # staff urls
    path('staff/', include('staff.urls', ),),
    
    #checkeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    

    
]



urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    
    
