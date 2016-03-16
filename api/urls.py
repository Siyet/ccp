from django.conf.urls import url, include
import views

shirt_urls = [
    url(r'^showcase/$', views.TemplateShirtsList.as_view()),
    url(r'^showcase/(?P<pk>[0-9]+)/$', views.TemplateShirtDetails.as_view(), name='templateshirt-detail'),
    url(r'^showcase/filter/$', views.TemplateShirtsFiltersList.as_view()),
]

collection_urls = [
    url(r'^fabric/$', views.CollectionFabricsList.as_view()),
    url(r'^fabric/color/$', views.CollectionFabricColorsList.as_view()),
    url(r'^fabric/design/$', views.CollectionFabricDesignsList.as_view()),
    url(r'^hardness/$', views.CollectionHardnessList.as_view())
]

components = [
    url(r'^collar/$', views.CollarTypeList.as_view()),
    url(r'^cuff/$', views.CuffTypeList.as_view()),
    url(r'^hem/$', views.HemTypeList.as_view()),
    url(r'^back/$', views.BackTypeList.as_view()),
    url(r'^pocket/$', views.PocketTypeList.as_view()),
    url(r'^placket/$', views.PlacketTypeList.as_view()),
    url(r'^sleeve/$', views.SleeveTypeList.as_view()),
    url(r'^yoke/$', views.YokeTypeList.as_view())
]

urlpatterns = [
    url(r'^collection/$', views.CollectionsListView.as_view()),
    url(r'^collection/(?P<pk>[0-9]+)/', include(collection_urls)),
    url(r'^components/', include(components)),
    url(r'^shirt/', include(shirt_urls)),
    url(r'^shirt_info/', views.ShirtInfoListView.as_view()),
    url(r'^size/$', views.SizesList.as_view()),
    url(r'^size/option/$', views.SizeOptionsList.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
