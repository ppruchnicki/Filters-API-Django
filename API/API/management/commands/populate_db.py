from django.core.management.base import BaseCommand
from API.models import Dzialania, Programy, Osie
from pathlib import Path
import csv


class Command(BaseCommand):

    def get_path(self, filename):
        path = Path(__file__).resolve().parents[4].joinpath(
            "Files/" + filename)
        return path

    def handle(self, *args, **options):
        with open(self.get_path("programy.csv")) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                obj, created = Programy.objects.update_or_create(
                    id_program=row['ID_PROGRAM'],
                    nazwa=row['NAZWA'],
                )
            f.close()
        with open(self.get_path("osie.csv")) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                obj, created = Osie.objects.update_or_create(
                    #  other possibility to write this id_program_id=row['ID_PROGRAM']the _id allows you to assign the foreign key (= the primary key of the referred object) directly.
                    id_program=Programy.objects.get(
                        id_program=row['ID_PROGRAM']),
                    id_os=row['ID_OS'],
                    nazwa=row['NAZWA'],
                )
            f.close()
        with open(self.get_path("dzialania.csv")) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                obj, created = Dzialania.objects.update_or_create(
                    id_os=Osie.objects.get(id_os=row['ID_OS']),
                    id_dzl=row['ID_DZL'],
                    nazwa=row['NAZWA'],
                )
            f.close()
