from .models import Programy, Osie, Dzialania, FTD, FTD_ElEMENTY
from rest_framework import serializers


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


class FTD_ElementySerializer(serializers.ModelSerializer):

    class Meta:
        model = FTD_ElEMENTY
        #fields = ["id_ftd", "id_dzl"]
        fields = ["id_dzl"]
        #fields = ["dzialania"]


class FTDSerializer(serializers.ModelSerializer):
    ftd = FTD_ElementySerializer(many=True)

    def create(self, validated_data):
        ftd_data = validated_data.pop('ftd')
        ftd = FTD.objects.create(**validated_data)
        # print(ftd_data)
        """ for programy in ftd_data:
            print(programy)
            ftd_data_programy = ftd_data.pop('osie')
            print(ftd_data_programy)
            for osie in ftd_data_programy:
                ftd_data_programy_osie = ftd_data_programy.pop('dzialania')
                for dzialania in ftd_data_programy_osie:
                    pass
                    #FTD_ElEMENTY.objects.create(id_ftd=ftd, **dzialania) """
        for dzialania in ftd_data:
            FTD_ElEMENTY.objects.create(
                id_ftd=ftd, **dzialania)
        print(ftd_data)
        return ftd

    class Meta:
        model = FTD
        fields = ["id_ftd", "nazwa", "opis", "ftd"]
