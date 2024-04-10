from django.http import HttpResponse, HttpResponseRedirect
from .models import Program
from django.shortcuts import render
import random
from django.urls import reverse


def index(request) -> HttpResponse:
    context = {
        "programs": [program.name for program in Program.objects.all()]
    }
    print("index")
    return render(request, "sunlight/index.html", context)


def get_sunlight_colour(request):
    colour = "".join((hex(random.randint(0, 255))[2:] for _ in range(3)))
    return coloured_index(request, colour)


def coloured_index(request, colour):
    context = {
        "programs": [program.name for program in Program.objects.all()],
        "colour": f"#{colour}"
    }
    return render(request, "sunlight/index.html", context)

