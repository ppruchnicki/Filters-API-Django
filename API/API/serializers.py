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
        fields = ["id_dzl"]


class FTDSerializer(serializers.ModelSerializer):
    ftd = FTD_ElementySerializer(many=True)

    def create(self, validated_data):
        ftd_data = validated_data.pop('ftd')
        ftd = FTD.objects.create(**validated_data)
        for dzialania in ftd_data:
            FTD_ElEMENTY.objects.create(
                id_ftd=ftd, **dzialania)
        return ftd

    def update(self, instance, validated_data):
        instance.nazwa = validated_data.get('nazwa', instance.nazwa)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.save()

        # TODO test if it possible to compare what is in db vs in json and only add new and remove old ftd
        # theoritically I should query db and get all ftds, than compare it with jsons ftds and save only new ones and delete old ones

        """ ftd_data = validated_data.pop('ftd')
        print("to jest ftd_data//////////////////////////")
        print(ftd_data)

        print(instance.id_ftd)
        data_test = FTD.objects.filter(
            id_ftd=instance.id_ftd).prefetch_related('ftd')
        #data_test = FTD_ElEMENTY.objects.filter(id_ftd=instance)
        print("query///////////////////////")
        print(data_test)
        for ftd_element in data_test:
            print(ftd_element)
            for dzl in ftd_element.ftd.all():
                print(dzl) """
        ftd_data = validated_data.pop('ftd')
        FTD_ElEMENTY.objects.filter(id_ftd=instance.id_ftd).delete()
        for dzialania in ftd_data:
            FTD_ElEMENTY.objects.create(id_ftd=instance, **dzialania)

        return instance

    class Meta:
        model = FTD
        fields = ["id_ftd", "nazwa", "opis", "ftd"]
