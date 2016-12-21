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
        fields = ('id', 'title', 'text', 'image', 'tailoring_time',)


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
    title = serializers.ReadOnlyField()
    id = serializers.IntegerField(required=False)

    class Meta:
        fields = ['id', 'title', 'show_sizes']
        read_only_fields = ('title', 'show_sizes')
        model = dictionaries.SizeOptions


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.Size


class BaseFabricSerializer(serializers.ModelSerializer):
    texture = serializers.SerializerMethodField()

    def get_texture(self, obj):
        if obj.texture:
            return self.context['request'].build_absolute_uri(obj.texture.sample_thumbnail.url)
        return None

    class Meta:
        model = models.Fabric
        fields = ['id', 'code', 'texture']


class FabricSerializer(BaseFabricSerializer):
    type = serializers.StringRelatedField()
    thickness = serializers.StringRelatedField(source='thickness.title')
    price = serializers.SerializerMethodField()
    tailoring_time = serializers.SerializerMethodField()

    def get_price(self, obj):
        return first(lambda x: x["fabric_category"] == obj.category_id, obj.cached_collection.prices, {}).get('price')

    def get_tailoring_time(self, obj):
        return obj.cached_collection.tailoring_time

    class Meta(BaseFabricSerializer.Meta):
        fields = ['id', 'type', 'thickness', 'code', 'short_description', 'long_description', 'texture', 'price',
                  'tailoring_time']


class FabricColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.FabricColor
        exclude = ('order',)


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
        model = dictionaries.YokeType


class DickeyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.DickeyType


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


class ShirtCollectionSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='__unicode__')
    production = serializers.CharField(source='about_shirt_title')

    class Meta:
        model = models.Collection
        fields = ('id', 'title', 'production',)


class TemplateShirtListSerializer(serializers.HyperlinkedModelSerializer):
    fabric = serializers.StringRelatedField()
    fabric_type = serializers.StringRelatedField(source='fabric.type')
    collection = ShirtCollectionSerializer()
    thickness = serializers.StringRelatedField(source='fabric.thickness.title')
    showcase_image = serializers.ImageField(source='showcase_image_list')
    sex = serializers.SerializerMethodField()
    material = serializers.StringRelatedField(source='fabric.material')
    short_description = serializers.StringRelatedField(source='fabric.short_description')

    def get_sex(self, object):
        try:
            return object.collection.get_sex_display()
        except AttributeError:
            return None

    class Meta:
        model = models.TemplateShirt
        fields = ['id', 'url', 'code', 'material', 'showcase_image', 'fabric', 'fabric_type', 'short_description',
                  'thickness', 'price', 'sex', 'collection']


class ShirtImageSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True, source='image.url')

    class Meta:
        model = models.ShirtImage
        fields = ['url']


class TemplateShirtDetailsSerializer(serializers.ModelSerializer):
    shirt_images = serializers.SerializerMethodField()
    country = serializers.StringRelatedField(source='collection.storehouse.country')
    short_description = serializers.StringRelatedField(source='fabric.short_description')
    long_description = serializers.StringRelatedField(source='fabric.long_description')
    tailoring_time = serializers.ReadOnlyField(source='collection.tailoring_time')

    def get_shirt_images(self, object):
        return [self.context['view'].request.build_absolute_uri(shirt_image.image.url) for shirt_image in
                object.shirt_images.all()]

    class Meta:
        model = models.TemplateShirt
        fields = ['individualization', 'short_description', 'long_description', 'shirt_images',
                  'country', 'tailoring_time']


class TemplateShirtSerializer(TemplateShirtListSerializer):
    showcase_image_hd = serializers.ImageField(source='showcase_image')
    showcase_image = serializers.ImageField(source='showcase_image_detail')
    details = serializers.SerializerMethodField()

    def get_details(self, object):
        return TemplateShirtDetailsSerializer(instance=object, context=self.context).data

    class Meta(TemplateShirtListSerializer.Meta):
        fields = TemplateShirtListSerializer.Meta.fields + ['showcase_image_hd', 'details']


class HardnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hardness
        fields = ['id', 'title']


class StaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stays
        fields = ['id', 'title']


class TuckSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.TuckType
        fields = ['id', 'title', 'picture']


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
        fields = ('question', 'answer',)


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


class NullableListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        res = super(NullableListSerializer, self).to_representation(data)
        return res if res else None


class ContrastDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContrastDetails
        fields = ('element', 'fabric')
        list_serializer_class = NullableListSerializer


class ContrastStitchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContrastStitch
        fields = ('element', 'color')


class InitialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Initials
        fields = ('font', 'location', 'text', 'color',)


class ShirtSerializer(serializers.ModelSerializer):
    required_fields = {'collection', 'sleeve', 'fabric'}

    collar = ShirtCollarSerializer()
    cuff = ShirtCuffSerializer()
    dickey = ShirtDickeySerializer(required=False, allow_null=True)
    contrast_details = ContrastDetailsSerializer(many=True, allow_null=True)
    contrast_stitches = ContrastStitchesSerializer(many=True)
    initials = InitialsSerializer(required=False, allow_null=True)
    fabric_code = serializers.ReadOnlyField(source='fabric.code')
    size_option = SizeOptionSerializer()

    class Meta:
        model = models.Shirt
        depth = 0
        exclude = ["is_template", "is_standard", "code", "individualization", "showcase_image"]

    def __init__(self, *args, **kwargs):
        super(ShirtSerializer, self).__init__(*args, **kwargs)
        for field_name in self.required_fields:
            self.fields[field_name].allow_null = False
            self.fields[field_name].required = True


class ShirtDetailsSerializer(ShirtSerializer):
    fit = serializers.StringRelatedField(source='fit.title')
    sleeve_length = serializers.StringRelatedField(source='sleeve_length.title')
    tailoring_time = serializers.ReadOnlyField(source='collection.tailoring_time')


class OrderItemSerializer(serializers.ModelSerializer):
    shirt = ShirtSerializer()

    class Meta:
        model = checkout.OrderItem
        fields = ('shirt', 'amount',)

    def create(self, validated_data):
        shirt = validated_data.pop('shirt')
        collar = shirt.pop('collar')
        cuff = shirt.pop('cuff')
        dickey = shirt.pop('dickey', None)
        initials = shirt.pop('initials', None)
        contrast_details = shirt.pop('contrast_details', None)
        contrast_stitches = shirt.pop('contrast_stitches')
        shirt['size_option_id'] = shirt.pop('size_option')['id']
        shirt = models.Shirt.objects.create(**shirt)
        models.Collar.objects.create(shirt=shirt, **collar)
        models.Cuff.objects.create(shirt=shirt, **cuff)

        if dickey:
            models.Dickey.objects.create(shirt=shirt, **dickey)

        if initials:
            models.Initials.objects.create(shirt=shirt, **initials)

        if contrast_details is not None:
            if shirt.collection.contrast_details:
                for contrast_detail in contrast_details:
                    models.ContrastDetails.objects.create(shirt=shirt, **contrast_detail)
            else:
                for element in models.ContrastDetails.ELEMENTS:
                    models.ContrastDetails.objects.create(shirt=shirt, element=element, fabric=shirt.collection.white_fabric)

        for contrast_stitche in contrast_stitches:
            models.ContrastStitch.objects.create(shirt=shirt, **contrast_stitche)

        return checkout.OrderItem.objects.create(shirt=shirt, price=shirt.price, **validated_data)


class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = checkout.CustomerData
        fields = ('name', 'lastname', 'midname', 'phone', 'email', 'type', 'city', 'address', 'index',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=True, read_only=False)
    customer_data = CustomerDataSerializer(many=True, required=True, read_only=False)
    amount = serializers.StringRelatedField(source='payment.order_amount')

    class Meta:
        model = checkout.Order
        fields = ('number', 'customer', 'checkout_shop', 'certificate', 'amount', 'items', 'customer_data',)

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
        order_items = validated_data.pop('items')
        customer_data = validated_data.pop('customer_data')
        order = checkout.Order.objects.create(**validated_data)
        order_item_serializer = OrderItemSerializer()
        for item in order_items:
            item['order'] = order
            order_item_serializer.create(item)
        for data in customer_data:
            checkout.CustomerData.objects.create(order=order, **data)
        order.create_payment()
        return order


class OrderDetailsSerializer(OrderSerializer):
    class Meta:
        model = checkout.Order
        fields = OrderSerializer.Meta.fields + ('state', 'payment_status', 'full_amount', 'discount_value',
                                                'certificate_value',)

    checkout_shop = ShopSerializer()
    certificate = CertificateSerializer()
    payment_status = serializers.StringRelatedField(source='payment.status')
    full_amount = serializers.StringRelatedField(source='get_full_amount')


class ThicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.Thickness
        fields = '__all__'


class FabricTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = dictionaries.FabricType
        fields = '__all__'


class FitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fit
        fields = ('id', 'picture', 'title', 'sizes',)

    sizes = SizeSerializer(many=True)
