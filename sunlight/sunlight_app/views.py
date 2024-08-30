from django.http import HttpResponse, HttpRequest
from .models import Program
from django.shortcuts import render, redirect
import random
from . import spectral_colour, urls


INDEX_TEMPLATE = "sunlight/index.html"


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "programs": [program.name for program in Program.objects.all()]
    }
    return render(request, INDEX_TEMPLATE, context)


def get_random_colour(_: HttpRequest):
    colour = "".join((hex(random.randint(0, 15))[2:] for _ in range(6)))
    return redirect(urls.COLOURED_INDEX, colour=colour)


def get_sunlight_colour(_: HttpRequest):
    colour = spectral_colour.get_sunlight_colour()
    return redirect(urls.COLOURED_INDEX, colour=colour[1:])


def coloured_index(request: HttpRequest, colour: str):
    context = {
        "programs": [program.name for program in Program.objects.all()],
        "colour": f"#{colour}",
        "random_colour_url": urls.GET_RANDOM_COLOUR,
        "sunlight_colour_url": urls.GET_SUNLIGHT_COLOUR,
    }
    return render(request, INDEX_TEMPLATE, context)


def render_blackbody(_: HttpRequest, temperature: int):
    colour = spectral_colour.blackbody_temperature_to_srgb(float(temperature))[1:]
    return redirect(urls.COLOURED_INDEX, colour=colour)
