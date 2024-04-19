from django.http import HttpResponse, HttpRequest
from .models import Program
from django.shortcuts import render, redirect
import random
from . import spectral_colour


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "programs": [program.name for program in Program.objects.all()]
    }
    return render(request, "sunlight/index.html", context)


def get_sunlight_colour(request: HttpRequest):
    colour = "".join((hex(random.randint(0, 15))[2:] for _ in range(6)))
    return redirect("coloured_index", colour=colour)


def coloured_index(request: HttpRequest, colour: str):
    context = {
        "programs": [program.name for program in Program.objects.all()],
        "colour": f"#{colour}"
    }
    return render(request, "sunlight/index.html", context)


def render_blackbody(request: HttpRequest, temperature: int):
    colour = spectral_colour.custom_sd_to_srgb(float(temperature))[1:]
    return redirect("coloured_index", colour=colour)
