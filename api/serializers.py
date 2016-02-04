from rest_framework import serializers
from backend import models
from dictionaries import models as dictionaries


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ('title', 'text', 'image')


class ShirtInfoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.ShirtInfoImage
        fields = ('text', 'image')


class ShirtInfoSerializer(serializers.ModelSerializer):
    images = ShirtInfoImageSerializer(many=True)
    class Meta:
        model = dictionaries.ShirtInfo
        fields = ('title', 'text', 'images')


class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.SizeOptions


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.Size


class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fabric
        fields = ['id', 'code', 'description', 'texture']


class FabricColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.FabricColor


class FabricDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.FabricDesign



class CollarButtonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.CollarButtons


class CollarTypeSerializer(serializers.ModelSerializer):
    buttons = CollarButtonsSerializer(many=True)
    class Meta:
        model = dictionaries.CollarType
        fields = ('id', 'title', 'picture', 'buttons')


class CuffRoundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.CuffRounding


class CuffTypeSerializer(serializers.ModelSerializer):
    rounding = CuffRoundingSerializer(many=True)

    class Meta:
        model = dictionaries.CuffType
        fields = ('title', 'picture', 'rounding')


class HemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.HemType


class SleeveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.SleeveType


class BackTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.BackType


class PlacketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.PlacketType


class PocketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.PocketType