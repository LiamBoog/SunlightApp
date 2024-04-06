from django.http import HttpResponse
from .models import Program
from django.shortcuts import render

def index(request) -> HttpResponse:
    programs = [program.name for program in Program.objects.all()]
    context = {
        "programs": programs
    }
    return render(request, "sunlight/index.html", context)


def test(request, id: int) -> HttpResponse | Exception:
    return HttpResponse(f"Test {id}")