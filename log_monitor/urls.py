from django.contrib import admin
from django.urls import path, include
from logs.views import home

urlpatterns = [
    # Home / landing page
    path("", home, name="home"),

    # Admin
    path("admin/", admin.site.urls),

    # Logs app (API + HTML)
    path("api/", include("logs.urls")),   # API base
    path("logs/", include("logs.urls")),  # HTML pages
]
