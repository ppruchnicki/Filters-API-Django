from .serializers import FTDSerializer, ProgramySerializer
from .forms import FTDForm, FTD_ELEMENTYForm
from django import forms
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.views.generic import DetailView, CreateView
from .models import FTD, Programy, Osie, Dzialania
from django.db.models import Prefetch
import json


class ProgramyListView(APIView):
    model = Programy

    # can be displayed in pure django without using DRF, but of course it is safer way to used common and well-tested code to do so

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


class FiltryListCreateView(CreateAPIView):
    model = FTD
    serializer_class = FTDSerializer

    """ def format_data(self, obj):
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
            return obj
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

    def get_serializer(self, *args, **kwargs):
        # leave this intact
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        # Intercept the request and see if it needs tweaking

        if (self.request.data["ftd"]):
            # Copy and manipulate the request
            draft_request_data = self.request.data.copy()
            ftd_data = draft_request_data['ftd']
            # Additionaly check if ftd structure is correct
            serializer = ProgramySerializer(data=ftd_data, many=True)
            if serializer.is_valid():
                dzl_list = []
                for program in ftd_data:
                    for os in program['osie']:
                        for dzl in os['dzialania']:
                            dzl_list.append(dzl)
                ftd_data = draft_request_data.pop('ftd')
                draft_request_data['ftd'] = dzl_list
            print(draft_request_data)
            kwargs["data"] = draft_request_data
            return serializer_class(*args, **kwargs)
        """
        If there is no ftd in json
        """
        return serializer_class(*args, **kwargs)

        # TODO try to use for loops to obtain id_dzl
        # TODO try to move it to to_internal and modify json there
        # TODO add update method

    def get(self, request):
        ftd = FTD.objects.all()
        serializer = FTDSerializer(ftd, many=True)
        return Response(serializer.data)

    """ def post(self, request, format=None):
        #serializer = FTDSerializer(data=self.format_data(request.data))
        serializer = FTDSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """


class FiltryUpdateDeleteView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = FTD.objects.all()
    serializer_class = FTDSerializer

    def get_serializer(self, *args, **kwargs):
        # leave this intact
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        # Intercept the request and see if it needs tweaking

        if (self.request.data["ftd"]):
            # Copy and manipulate the request
            draft_request_data = self.request.data.copy()
            ftd_data = draft_request_data['ftd']
            # Additionaly check if ftd structure is correct
            serializer = ProgramySerializer(data=ftd_data, many=True)
            if serializer.is_valid():
                dzl_list = []
                for program in ftd_data:
                    for os in program['osie']:
                        for dzl in os['dzialania']:
                            dzl_list.append(dzl)
                ftd_data = draft_request_data.pop('ftd')
                draft_request_data['ftd'] = dzl_list
            print('to jest draft request data/////////////')
            print(draft_request_data)
            kwargs["data"] = draft_request_data
            print(kwargs["data"])
            return serializer_class(*args, **kwargs)
        """
        If there is no ftd in json
        """
        return serializer_class(*args, **kwargs)

    """ def format_data(self, obj):
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
            return obj
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

    def put(self, request, *args, **kwargs):
        # print(request.data)
        #request.data = self.format_data(request.data)
        return self.update(request, *args, **kwargs)


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
