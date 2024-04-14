from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .models import Program
from django.shortcuts import render, redirect
import random
from django.urls import reverse


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
