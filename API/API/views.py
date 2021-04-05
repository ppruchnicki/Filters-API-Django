from .serializers import FTDSerializer, ProgramySerializer
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


class ProgramyList(APIView):
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


class FiltryList(APIView):
    model = FTD

    def format_data(self, obj):
        ftd_data = obj['ftd']
        serializer = ProgramySerializer(data=ftd_data, many=True)
        if serializer.is_valid():
            dzl_list = []
            for program in ftd_data:
                for os in program['osie']:
                    for dzl in os['dzialania']:
                        dzl_list.append(dzl)
            ftd_data = obj.pop('ftd')
            obj['ftd'] = dzl_list
            # print(obj)

        return obj

        # 1 try to use for loops to obtain id_dzl
        # 2 try to move it to to_internal and modify json there
        # 3 add update method

        """ programy = []
        for program in queryset:
            osie = []
            for os in program.osie.all():
                dzialania = []
                for dzialanie in os.dzialania.all():
                    dzialania.append(Dzialania.toJson(dzialanie))
                osie.append(Osie.toJson(os, dzialania))
            programy.append(
                Programy.toJson(program, osie)) """

    def get(self, request):
        ftd = FTD.objects.all()
        serializer = FTDSerializer(ftd, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FTDSerializer(data=self.format_data(request.data))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
