from django.contrib import admin
from django.urls import path,include
import base


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('base.urls')),
    path("room/ ", include('base.urls')),
    path("home/ ", include('base.urls')),

] 
