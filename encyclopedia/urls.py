from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newpage", views.new, name="new"),
    path("save", views.save, name="save"),
]
