from .serializers import FTDSerializer, ProgramySerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.views.generic import DetailView, CreateView
from .models import FTD, Programy, Osie, Dzialania
from django.db.models import Prefetch


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
        if programy:
            serializer = ProgramySerializer(programy, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FiltryListCreateView(CreateAPIView):
    model = FTD
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
                kwargs["data"] = draft_request_data
                return serializer_class(*args, **kwargs)
            # return (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """
        If there is no ftd in json
        """
        return serializer_class(*args, **kwargs)

    def get(self, request):
        ftd = FTD.objects.all()
        if ftd:
            serializer = FTDSerializer(ftd, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FiltryUpdateDeleteView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
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
            kwargs["data"] = draft_request_data
            return serializer_class(*args, **kwargs)
        """
        If there is no ftd in json
        """
        return serializer_class(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        ftd = FTD.objects.filter(pk=pk)
        if ftd:
            serializer = FTDSerializer(ftd, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
