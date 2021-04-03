from .models import Programy, Osie, Dzialania, FTD, FTD_ElEMENTY
from rest_framework import serializers


class FTD_ElementySerializer(serializers.ModelSerializer):

    class Meta:
        model = FTD_ElEMENTY
        #fields = ["id_ftd", "id_dzl"]
        fields = ["id_dzl"]


class FTDSerializer(serializers.ModelSerializer):
    ftd = FTD_ElementySerializer(many=True)

    def create(self, validated_data):
        ftd_data = validated_data.pop('ftd')
        ftd = FTD.objects.create(**validated_data)
        for ftd_data in ftd_data:
            FTD_ElEMENTY.objects.create(id_ftd=ftd, **ftd_data)
        print(ftd)
        return ftd

    class Meta:
        model = FTD
        fields = ["id_ftd", "nazwa", "opis", "ftd"]


class DzialaniaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dzialania
        fields = ["id_dzl", "nazwa"]


class OsieSerializer(serializers.ModelSerializer):
    dzialania = DzialaniaSerializer(many=True)

    class Meta:
        model = Osie
        fields = ["id_os", "nazwa", "dzialania"]


class ProgramySerializer(serializers.ModelSerializer):
    osie = OsieSerializer(many=True)

    class Meta:
        model = Programy
        fields = ["id_program", "nazwa", "osie"]
