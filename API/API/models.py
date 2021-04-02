from django.db import models
from django.db.models.fields.related import ForeignKey


class Programy(models.Model):
    id_program = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=1000)

    def __str__(self):
        return '%s %s' % (self.id_program, self.nazwa)

    def toJson(obj, list):
        program = {
            "id_program": obj.id_program,
            "nazwa": obj.nazwa,
            "osie": list
        }
        return program


class Osie(models.Model):
    id_program = models.ForeignKey(
        Programy, related_name='osie', on_delete=models.CASCADE)
    id_os = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=1000)

    def __str__(self):
        return '%s %s %s' % (self.id_program, self.id_os, self.nazwa)

    def toJson(obj, list):
        os = {
            'id_os': obj.id_os,
            'nazwa': obj.nazwa,
            'dzialania': list
        }
        return os


class Dzialania(models.Model):
    id_dzl = models.AutoField(primary_key=True)
    id_os = models.ForeignKey(
        Osie, related_name='dzialania', on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=1000)

    def __str__(self):
        return '%s %s %s' % (self.id_dzl, self.id_os, self.nazwa)

    def toJson(obj):
        dzialanie = {
            'id_dzl': obj.id_dzl,
            'nazwa': obj.nazwa
        }
        return dzialanie


class FTD(models.Model):
    id_ftd = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    opis = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.id_ftd, self.nazwa, self.opis)


class FTD_ElEMENTY(models.Model):
    id_ftd_element = models.AutoField(primary_key=True)
    id_ftd = models.ForeignKey(FTD, on_delete=models.CASCADE)
    id_dzl = models.ForeignKey(Dzialania, on_delete=models.CASCADE)
