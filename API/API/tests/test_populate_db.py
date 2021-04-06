from django.core.management import call_command
from django.test import TestCase
from ..models import Programy, Osie, Dzialania, FTD, FTD_ElEMENTY


class CommandsTestCase(TestCase):
    def test_populate_db(self):
        " Test my custom command."

        call_command('populate_db')
        self.assertEqual(Programy.objects.count(), 27)
        self.assertEqual(Osie.objects.count(), 239)
        self.assertEqual(Dzialania.objects.count(), 831)
        # Some Asserts.
