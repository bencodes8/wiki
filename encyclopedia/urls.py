from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("<str:title>".lower(), views.entry, name="entry"),
]

