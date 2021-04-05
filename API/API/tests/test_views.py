import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import FTD, FTD_ElEMENTY, Programy, Osie, Dzialania
from ..serializers import FTDSerializer, FTD_ElementySerializer, ProgramySerializer


# initialize the APIClient app
client = Client()


class GetAllAndSingleTests(TestCase):

    def setUp(self):
        program_1 = Programy.objects.create(
            nazwa="testowy"
        )
        program_2 = Programy.objects.create(
            nazwa="The ENI Cross-border Cooperation Programme Poland-Russia 2014-2020"
        )
        os_1 = Osie.objects.create(id_program=program_1,
                                   nazwa="Promotion of local culture and preservation of historical heritage (TO3)")
        os_2 = Osie.objects.create(id_program=program_1,
                                   nazwa="Improvement of accessibility to the regions, development of sustainable and climate-proof transport and communication networks and systems (TO7)")
        dzl_1 = Dzialania.objects.create(id_os=os_1,
                                         id_dzl=4702, nazwa="Promotion of local culture and history")
        dzl_2 = Dzialania.objects.create(id_os=os_1,
                                         id_dzl=4703, nazwa="Promotion and preservation of natural heritage")
        self.ftd_1 = FTD.objects.create(
            nazwa="filtr testowy", opis="testowy_opis")
        self.ftd_2 = FTD.objects.create(
            nazwa="filtr pusty", opis="testowy_opis")
        FTD_ElEMENTY.objects.create(id_ftd=self.ftd_1, id_dzl=dzl_1)
        FTD_ElEMENTY.objects.create(id_ftd=self.ftd_1, id_dzl=dzl_2)

    """ Test module for GET all programs API """

    def test_get_all_programs(self):
        # get API response
        response = client.get(reverse('programy-list'))
        # get data from db
        programy = Programy.objects.all()
        serializer = ProgramySerializer(programy, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_filters(self):
        # get API response
        response = client.get(reverse('filtry-list-create'))
        # get data from db
        filtry = FTD.objects.all()
        serializer = FTDSerializer(filtry, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def test_get_valid_filter(self):
        response = client.get(
            reverse('filtry-update-delete', kwargs={'pk': self.ftd_1.pk}))
        ftd = FTD.objects.filter(pk=self.ftd_1.pk)
        serializer = FTDSerializer(ftd, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_filter(self):
        response = client.get(
            reverse('filtry-update-delete', kwargs={'pk': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FiltryCreateTest(TestCase):

    def test_create_valid_filter(self):
        pass

    def test_create_invalid_filter(self):
        pass


class FiltryUpdateTest(TestCase):

    def test_update_valid_filter(self):
        pass

    def test_update_invalid_filter(self):
        pass


class FiltryDeleteTest(TestCase):

    def test_delete_valid_filter(self):
        pass

    def test_delete_invalid_filter(self):
        pass
