from django.urls import path, register_converter
from . import views, converters

register_converter(converters.HexadecimalConverter, "hex")

urlpatterns = [
    path("", views.index, name="index"),
    path("get_colour", views.get_sunlight_colour, name="get_sunlight_colour"),
    path("<hex:colour>", views.coloured_index, name="coloured_index"),
]