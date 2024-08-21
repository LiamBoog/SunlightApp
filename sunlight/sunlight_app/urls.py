from django.urls import path, register_converter
from . import views, converters


GET_RANDOM_COLOUR = views.get_random_colour.__name__
GET_SUNLIGHT_COLOUR = views.get_sunlight_colour.__name__
COLOURED_INDEX = views.coloured_index.__name__
RENDER_BLACKBODY = views.render_blackbody.__name__

register_converter(converters.HexadecimalConverter, "hex")

urlpatterns = [
    path("", views.index, name="index"),
    path("get_colour", views.get_random_colour, name=GET_RANDOM_COLOUR),
    path("get_sunlight_colour", views.get_sunlight_colour, name=GET_SUNLIGHT_COLOUR),
    path("<hex:colour>", views.coloured_index, name=COLOURED_INDEX),
    path("<int:temperature>", views.render_blackbody, name=RENDER_BLACKBODY),
]