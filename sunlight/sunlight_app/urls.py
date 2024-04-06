from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/get_colour", views.get_sunlight_colour, name="get_sunlight_colour")
]