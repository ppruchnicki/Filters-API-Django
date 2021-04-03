from .serializers import ProgramySerializer
from .forms import FTDForm, FTD_ELEMENTYForm
from django import forms
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from django.views.generic import DetailView, CreateView
from .models import FTD, Programy, Osie, Dzialania
from django.db.models import Prefetch
import json


class ProgramyListView(APIView):
    model = Programy

    """ def get(self, request, *args, **kwargs):
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

        return JsonResponse(programy, status=200, safe=False) """

    def get(self, request):
        programy = Programy.objects.all()
        serializer = ProgramySerializer(programy, many=True)
        return Response(serializer.data)


""" class FiltryCreateView(CreateView):
    model = FTD
    form_class = FTDForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.save()

        return JsonResponse(FTD.toJson(obj), status=200, safe=False)

    def post(self, request):
        if request.POST:
            form = FTDForm(request.POST)
        else:
            body = json.loads(request.body.decode('utf-8'))
            form = FTDForm(body)
            if body['struktura']:
                print(body['struktura'])
            print(body['nazwa'])
        if form.is_valid():
            return self.form_valid(form)
        return JsonResponse(form.errors, status=400, safe=False) """
