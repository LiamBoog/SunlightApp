from django.http import HttpResponse, HttpResponseRedirect
from .models import Program
from django.shortcuts import render
import random
from django.urls import reverse


def index(request, colour="#ffffff") -> HttpResponse:
    programs = [program.name for program in Program.objects.all()]
    context = {
        "programs": programs,
        "colour": colour
    }
    return render(request, "sunlight/index.html", context)


def get_sunlight_colour(request):
    colour = "#" + "".join((hex(random.randint(0, 255))[2:] for _ in range(3)))
    print(colour)
    return index(request, colour)
