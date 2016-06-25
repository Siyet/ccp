from rest_framework import serializers
from backend import models
from dictionaries import models as dictionaries
from checkout import models as checkout


class CollectionSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='__unicode__')
    class Meta:
        model = models.Collection
        fields = ('id', 'title', 'text', 'image', 'tailoring_time', )


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
    fabric_type = serializers.StringRelatedField(source='fabric_type.title')
    thickness = serializers.StringRelatedField(source='thickness.title')
    price = serializers.SerializerMethodField()
    texture = serializers.SerializerMethodField()

    def get_texture(self, obj):
        if obj.texture:
            return self.context['request'].build_absolute_uri(obj.texture.sample_thumbnail.url)
        return None

    def get_price(self, object):
        for price_info in object.cached_collection.prices:
            if price_info["fabric_category"] == object.category_id:
                return price_info["price"]
        return None


    class Meta:
        model = models.Fabric
        fields = ['id', 'fabric_type', 'thickness', 'code', 'short_description', 'long_description', 'texture', 'price']


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


class YokeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.PocketType


class CustomButtonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomButtons
        fields = ['id', 'title', 'picture', ]


class CustomButtonsTypeSerializer(serializers.ModelSerializer):
    buttons = CustomButtonsSerializer(many=True)

    class Meta:
        model = dictionaries.CustomButtonsType
        fields = ['id', 'title', 'extra_price', 'buttons', ]


class ShawlOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShawlOptions


class TemplateShirtListSerializer(serializers.HyperlinkedModelSerializer):
    fabric = serializers.StringRelatedField()
    fabric_type = serializers.StringRelatedField(source='fabric.fabric_type.title')
    thickness = serializers.StringRelatedField(source='fabric.thickness.title')
    showcase_image = serializers.ImageField(source='showcase_image_list')
    sex = serializers.SerializerMethodField()
    material = serializers.StringRelatedField(source='fabric.material')

    def get_sex(self, object):
        try:
            return object.collection.get_sex_display()
        except AttributeError:
            return None

    class Meta:
        model = models.TemplateShirt
        fields = ['id', 'url', 'code', 'material', 'showcase_image', 'fabric', 'fabric_type', 'thickness', 'price', 'sex']


class ShirtImageSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True, source='image.url')

    class Meta:
        model = models.ShirtImage
        fields = ['url']


class TemplateShirtDetailsSerializer(serializers.ModelSerializer):
    shirt_images = serializers.SerializerMethodField()
    collection_title = serializers.StringRelatedField(source='collection')
    country = serializers.StringRelatedField(source='collection.storehouse.country')
    short_description = serializers.StringRelatedField(source='fabric.short_description')
    long_description = serializers.StringRelatedField(source='fabric.long_description')

    def get_shirt_images(self, object):
        return [self.context['view'].request.build_absolute_uri(shirt_image.image.url) for shirt_image in object.shirt_images.all()]

    class Meta:
        model = models.TemplateShirt
        fields = ['individualization', 'short_description', 'long_description', 'shirt_images', 'collection_title', 'country']


class TemplateShirtSerializer(TemplateShirtListSerializer):
    showcase_image = serializers.ImageField(source='showcase_image_detail')
    details = serializers.SerializerMethodField()

    def get_details(self, object):
        return TemplateShirtDetailsSerializer(instance=object, context=self.context).data

    class Meta(TemplateShirtListSerializer.Meta):
        fields = TemplateShirtListSerializer.Meta.fields + ['details']


class HardnessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hardness
        fields = ['id', 'title']


class StaysSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stays
        fields = ['id', 'title']


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.Shop
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.Certificate
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = dictionaries.FAQ
        fields = ('question', 'answer', )


class ShirtDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Shirt
        exclude = ["is_template", "is_standard", "code", "individualization", "showcase_image"]


class OrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.OrderDetails
        fields = ('order', 'shirt', 'amount', )


class OrderAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.OrderAddress
        fields = ('name', 'lastname', 'midname', 'phone', 'city', 'address', 'index', 'email')


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True, required=True)
    addresses = OrderAddressSerializer(many=True, required=True)

    class Meta:
        model = checkout.Order
        fields = ('number', 'customer', 'checkout_shop', 'name', 'lastname', 'midname', 'phone', 'city', 'address',
                  'index', 'email', 'order_details', 'addresses')
