from rest_framework import serializers
from backend import models
from backend.models import FabricPrice
from dictionaries import models as dictionaries


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Collection
        fields = ('id', 'title', 'text', 'image')


class CollectionSexSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField()

    def get_sex(self, object):
        try:
            return models.SEX[object.get('sex')]
        except KeyError:
            return object.get('sex')

    class Meta:
        model = models.Collection
        fields = ('sex', )


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


class TemplateShirtListSerializer(serializers.HyperlinkedModelSerializer):
    fabric = serializers.StringRelatedField()
    showcase_image = serializers.ImageField(source='showcase_image_list')
    sex = serializers.SerializerMethodField()

    def get_sex(self, object):
        try:
            return object.collection.get_sex_display()
        except AttributeError:
            return None

    class Meta:
        model = models.TemplateShirt
        fields = ['id', 'url', 'code', 'material', 'showcase_image', 'fabric', 'price', 'sex']


class ShirtImageSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True, source='image.url')

    class Meta:
        model = models.ShirtImage
        fields = ['url']


class TemplateShirtDetailsSerializer(serializers.ModelSerializer):

    shirt_images = serializers.SerializerMethodField()
    collection = CollectionSerializer()
    country = serializers.SerializerMethodField()

    def get_shirt_images(self, object):
        return [self.context['view'].request.build_absolute_uri(shirt_image.image.url) for shirt_image in object.shirt_images.all()]

    def get_country(self, object):
        try:
            return object.collection.storehouse.country
        except AttributeError:
            return None

    class Meta:
        model = models.TemplateShirt
        fields = ['individualization', 'description', 'shirt_images', 'collection', 'country']

class TemplateShirtSerializer(TemplateShirtListSerializer):

    showcase_image = serializers.ImageField(source='showcase_image_detail')
    details = serializers.SerializerMethodField()

    def get_details(self, object):
        return TemplateShirtDetailsSerializer(instance=object, context=self.context).data

    class Meta(TemplateShirtListSerializer.Meta):
        fields = TemplateShirtListSerializer.Meta.fields + ['details']
