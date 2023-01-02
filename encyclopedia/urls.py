from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("<str:title>".lower(), views.search, name="entry"),
]

