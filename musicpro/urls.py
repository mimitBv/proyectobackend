from django.contrib import admin
from django.urls import include, path

from music_pro.views import admin_dashboard

urlpatterns = [
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/", admin.site.urls),
    path("", include("music_pro.urls")),
]
