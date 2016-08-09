# coding: utf-8
from django.db.transaction import atomic
from rest_framework import serializers
from django.utils.text import ugettext_lazy as _
from backend import models
from core.utils import first
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
    tailoring_time = serializers.SerializerMethodField()

    def get_texture(self, obj):
        if obj.texture:
            return self.context['request'].build_absolute_uri(obj.texture.sample_thumbnail.url)
        return None

    def get_price(self, obj):
        return first(lambda x: x["fabric_category"] == obj.category_id, obj.cached_collection.prices, {}).get('price')

    def get_tailoring_time(self, obj):
        return obj.cached_collection.tailoring_time

    class Meta:
        model = models.Fabric
        fields = ['id', 'fabric_type', 'thickness', 'code', 'short_description', 'long_description', 'texture', 'price',
                  'tailoring_time']


class FabricColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.FabricColor


class FabricDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.FabricDesign



class CollarButtonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.CollarButtons
        exclude = ('types', 'buttons')


class CollarTypeSerializer(serializers.ModelSerializer):
    buttons = CollarButtonsSerializer(many=True)

    class Meta:
        model = dictionaries.CollarType
        fields = ('id', 'title', 'picture', 'buttons')


class CuffRoundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.CuffRounding
        exclude = ('types',)


class CuffTypeSerializer(serializers.ModelSerializer):
    rounding = CuffRoundingSerializer(many=True)

    class Meta:
        model = dictionaries.CuffType
        fields = ('id', 'title', 'picture', 'rounding')


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
    collection = serializers.StringRelatedField(source='collection.title')
    short_description = serializers.StringRelatedField(source='fabric.short_description')

    def get_sex(self, object):
        try:
            return object.collection.get_sex_display()
        except AttributeError:
            return None

    class Meta:
        model = models.TemplateShirt
        fields = ['id', 'url', 'code', 'material', 'showcase_image', 'fabric', 'fabric_type', 'short_description', 'thickness', 'price', 'sex', 'collection']


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


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.Discount
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = dictionaries.FAQ
        fields = ('question', 'answer', )


class ShirtCollarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collar
        fields = ('type', 'hardness', 'size', 'stays')


class ShirtCuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuff
        fields = ('type', 'rounding', 'hardness')


class ShirtDickeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dickey
        fields = ('type', 'fabric')


class ContrastDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContrastDetails
        fields = ('element', 'fabric')


class ContrastStitchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContrastStitch
        fields = ('element', 'color')


class InitialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Initials
        fields = ('font', 'location', 'text', 'color', )


class ShirtDetailsSerializer(serializers.ModelSerializer):
    required_fields = {'collection', 'sleeve', 'fabric'}

    collar = ShirtCollarSerializer()
    cuff = ShirtCuffSerializer()
    dickey = ShirtDickeySerializer(required=False)
    contrast_details = ContrastDetailsSerializer(many=True)
    contrast_stitches = ContrastStitchesSerializer(many=True)
    initials = InitialsSerializer(required=False)

    class Meta:
        model = models.Shirt
        depth = 0
        exclude = ["is_template", "is_standard", "code", "individualization", "showcase_image"]

    def __init__(self, *args, **kwargs):
        super(ShirtDetailsSerializer, self).__init__(*args, **kwargs)
        for field_name in self.required_fields:
            self.fields[field_name].allow_null = False
            self.fields[field_name].required = True


class OrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.OrderDetails
        fields = ('shirt', 'amount', )

    shirt = ShirtDetailsSerializer()

    def create(self, validated_data):
        shirt = validated_data.pop('shirt')
        collar = shirt.pop('collar')
        cuff = shirt.pop('cuff')
        dickey = shirt.pop('dickey', None)
        initials = shirt.pop('initials', None)
        contrast_details = shirt.pop('contrast_details')
        contrast_stitches = shirt.pop('contrast_stitches')
        shirt = models.Shirt.objects.create(**shirt)
        models.Collar.objects.create(shirt=shirt, **collar)
        models.Cuff.objects.create(shirt=shirt, **cuff)

        if dickey:
            models.Dickey.objects.create(shirt=shirt, **dickey)

        if initials:
            shirt.initials = models.Initials.objects.create(**initials)
            shirt.save()

        for contrast_detail in contrast_details:
            models.ContrastDetails.objects.create(shirt=shirt, **contrast_detail)
        for contrast_stitche in contrast_stitches:
            models.ContrastStitch.objects.create(shirt=shirt, **contrast_stitche)

        return checkout.OrderDetails.objects.create(shirt=shirt, price=shirt.price, **validated_data)


class CustomerDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = checkout.CustomerData
        fields = ('name', 'lastname', 'midname', 'phone', 'email', 'type', 'city', 'address', 'index', )


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True, required=True, read_only=False)
    customer_data = CustomerDataSerializer(many=True, required=True, read_only=False)
    amount = serializers.StringRelatedField(source='payment.order_amount')

    class Meta:
        model = checkout.Order
        fields = ('number', 'customer', 'checkout_shop', 'certificate', 'amount', 'order_details', 'customer_data', )

    def validate(self, attrs):
        customer_data = attrs.get('customer_data', [])
        has_customer_address = False
        for data in customer_data:
            if data.get('type') == checkout.CustomerData.ADDRESS_TYPE.customer_address:
                has_customer_address = True
        if not has_customer_address:
            raise serializers.ValidationError(_(u'Данные клиента обязательны'))
        return attrs

    @atomic
    def create(self, validated_data):
        order_details = validated_data.pop('order_details')
        customer_data = validated_data.pop('customer_data')
        order = checkout.Order.objects.create(**validated_data)
        order_details_serializer = OrderDetailsSerializer()
        for detail in order_details:
            detail['order'] = order
            order_details_serializer.create(detail)
        for data in customer_data:
            checkout.CustomerData.objects.create(order=order, **data)
        order.create_payment()
        return order


class OrderDetailSerializer(OrderSerializer):
    class Meta:
        model = checkout.Order
        fields = OrderSerializer.Meta.fields + ('state', 'payment_status', 'full_amount', 'discount_value',
                                                'certificate_value',)

    checkout_shop = ShopSerializer()
    certificate = CertificateSerializer()
    payment_status = serializers.StringRelatedField(source='payment.status')
    full_amount = serializers.StringRelatedField(source='get_full_amount')
