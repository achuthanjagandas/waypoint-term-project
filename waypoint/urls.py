from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("report/", views.report_trail, name="report"),
    path("search/", views.search_trails, name="search"),
]