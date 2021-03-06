from django.conf.urls import url, include
import views

checkout_urls = [
    url(r'^shop/$', views.ShopListView.as_view()),
    url(r'^order/$', views.OrderCreateView.as_view()),
    url(r'^order/(?P<number>[0-9a-f-]+)/$', views.OrderDetailView.as_view()),
    url(r'^order/(?P<number>[0-9a-f-]+)/payment/$', views.OrderPaymentData.as_view()),
    url(r'^cert/(?P<pk>[0-9-]+)/$', views.CertificateDetailView.as_view()),
    url(r'^discount/(?P<pk>[0-9-]+)/$', views.DiscountDetailView.as_view()),
]

shirt_urls = [
    url(r'^showcase/$', views.ShowcaseShirtsListView.as_view()),
    url(r'^showcase/(?P<pk>[0-9]+)/$', views.TemplateShirtDetails.as_view(), name='templateshirt-detail'),
    url(r'^showcase/filter/$', views.TemplateShirtsFiltersList.as_view()),
    url(r'^image/(?P<projection>front|side|back)/(?P<resolution>full|preview)/$', views.ShirtImage.as_view()),
    url(r'^image/(?P<projection>front|side|back)/$', views.ShirtImage.as_view()),
    url(r'^price/$', views.ShirtPrice.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.ShirtDetails.as_view()),
]

collection_urls = [
    url(r'^fabric/$', views.CollectionFabricsList.as_view()),
    url(r'^fabric/color/$', views.CollectionFabricColorsList.as_view()),
    url(r'^fabric/design/$', views.CollectionFabricDesignsList.as_view()),
    url(r'^fabric/thickness/$', views.CollectionThicknessList.as_view()),
    url(r'^fabric/fabric_type/$', views.CollectionFabricTypeList.as_view()),
    url(r'^hardness/$', views.CollectionHardnessList.as_view()),
    url(r'^stays/$', views.CollectionStaysList.as_view()),
    url(r'^tuck/$', views.CollectionTuckList.as_view()),
    url(r'^stitches/$', views.CollectionStitchesList.as_view()),
    url(r'^fit/$', views.CollectionFitList.as_view()),
]

components = [
    url(r'^collar/$', views.CollarTypeList.as_view()),
    url(r'^cuff/$', views.CuffTypeList.as_view()),
    url(r'^hem/$', views.HemTypeList.as_view()),
    url(r'^back/$', views.BackTypeList.as_view()),
    url(r'^pocket/$', views.PocketTypeList.as_view()),
    url(r'^placket/$', views.PlacketTypeList.as_view()),
    url(r'^sleeve/$', views.SleeveTypeList.as_view()),
    url(r'^yoke/$', views.YokeTypeList.as_view()),
    url(r'^button/$', views.CustomButtonsTypeList.as_view()),
    url(r'^shawl/$', views.ShawlOptionsList.as_view()),
    url(r'^clasp/$', views.ClaspOptionsList.as_view()),
    url(r'^stitch/$', views.StitchOptionsList.as_view()),
    url(r'^initials/$', views.TemplateInitialsList.as_view()),
    url(r'^dickey/$', views.DickeyList.as_view()),
    url(r'^prices/$', views.PricesList.as_view())
]

urlpatterns = [
    url(r'^checkout/', include(checkout_urls)),
    url(r'^collection/(?P<pk>[0-9]+)/', include(collection_urls)),
    url(r'^components/', include(components)),
    url(r'^shirt/', include(shirt_urls)),
    url(r'^size/$', views.SizesList.as_view()),
    url(r'^size/option/$', views.SizeOptionsList.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
