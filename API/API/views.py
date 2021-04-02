from django import forms
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from .models import Programy, Osie, Dzialania
from django.db.models import Prefetch


class ProgramyListView(ListView):
    model = Programy

    def get(self, request, *args, **kwargs):
        queryset = Programy.objects.prefetch_related(
            Prefetch('osie', queryset=Osie.objects.prefetch_related('dzialania')))
        programy = []
        for program in queryset:
            osie = []
            for os in program.osie.all():
                dzialania = []
                for dzialanie in os.dzialania.all():
                    dzialania.append(Dzialania.toJson(dzialanie))
                osie.append(Osie.toJson(os, dzialania))
            programy.append(
                Programy.toJson(program, osie))

        return JsonResponse(programy, status=200, safe=False)
