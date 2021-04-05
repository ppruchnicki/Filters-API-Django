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
        # fields = ["id_ftd", "id_dzl"]
        fields = ["id_dzl"]
        # fields = ["dzialania"]


class FTDSerializer(serializers.ModelSerializer):
    ftd = FTD_ElementySerializer(many=True)

    # TODO check if that can work somehow

    """ def to_internal_value(self, data):
        ftd_data = data['ftd']
        serializer = ProgramySerializer(data=ftd_data, many=True)
        if serializer.is_valid():
            dzl_list = []
            for program in ftd_data:
                for os in program['osie']:
                    for dzl in os['dzialania']:
                        dzl_list.append(dzl)
            ftd_data = data.pop('ftd')
            data['ftd'] = dzl_list
            print(data)

        return data """

    def create(self, validated_data):
        print("to jest validated_data//////////////////")
        print(validated_data)
        ftd_data = validated_data.pop('ftd')
        ftd = FTD.objects.create(**validated_data)
        for dzialania in ftd_data:
            FTD_ElEMENTY.objects.create(
                id_ftd=ftd, **dzialania)
        return ftd

    def update(self, instance, validated_data):
        print("to jest validated_data ////////////")
        print(validated_data)
        instance.nazwa = validated_data.get('nazwa', instance.nazwa)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.save()  # TODO IMPORTANT TO UNCOMMENT

        # TODO test if it possible to compare what is in db vs in json and only add new and remove old ftd
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
