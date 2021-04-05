from django.db.models.query import Prefetch
from django.test import TestCase
from rest_framework import serializers
from ..models import Programy, Osie, Dzialania, FTD, FTD_ElEMENTY
from ..serializers import ProgramySerializer, OsieSerializer, DzialaniaSerializer, FTDSerializer, FTD_ElementySerializer


class ModelsTest(TestCase):

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
        ftd_1 = FTD.objects.create(nazwa="filtr testowy", opis="testowy_opis")
        ftd_2 = FTD.objects.create(nazwa="filtr pusty", opis="testowy_opis")
        FTD_ElEMENTY.objects.create(id_ftd=ftd_1, id_dzl=dzl_1)
        FTD_ElEMENTY.objects.create(id_ftd=ftd_1, id_dzl=dzl_2)

    def test_get_all_programs(self):
        self.assertEqual(Programy.objects.count(), 2)
        self.assertEqual(Osie.objects.count(), 2)
        self.assertEqual(Dzialania.objects.count(), 2)
        self.assertEqual(
            Programy.objects.prefetch_related('osie').count(), 2
        )
        self.assertEqual(
            Programy.objects.prefetch_related(
                Prefetch('osie', queryset=Osie.objects.prefetch_related('dzialania'))).count(), 2
        )

    def test_get_all_filters(self):
        self.assertEqual(FTD.objects.count(), 2)
        self.assertEqual(FTD_ElEMENTY.objects.count(), 2)
        self.assertEqual(
            FTD.objects.prefetch_related('ftd').count(), 2
        )
