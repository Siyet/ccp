from rest_framework import serializers
from backend.models import Collection
from dictionaries.models import ShirtInfo, ShirtInfoImage, SizeOptions, Size


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('title', 'text', 'image')


class ShirtInfoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShirtInfoImage
        fields = ('text', 'image')


class ShirtInfoSerializer(serializers.ModelSerializer):
    images = ShirtInfoImageSerializer(many=True)
    class Meta:
        model = ShirtInfo
        fields = ('title', 'text', 'images')


class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOptions


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size