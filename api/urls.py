from django.conf.urls import url, include
from api.views import CollectionsListView, ShirtInfoListView, SizeOptionsList, SizesList
from api.views import CollectionFabricDesignsList, CollectionFabricColorsList, CollectionFabricsList
from api.views import CollarTypeList, CuffTypeList, HemTypeList
from api.views import HemTypeList, BackTypeList, PocketTypeList, PlacketTypeList, SleeveTypeList


collection_urls = [
    url(r'^fabric/$', CollectionFabricsList.as_view()),
    url(r'^fabric/color/$', CollectionFabricColorsList.as_view()),
    url(r'^fabric/design/$', CollectionFabricDesignsList.as_view())
]

components = [
    url(r'^collar/$', CollarTypeList.as_view()),
    url(r'^cuff/$', CuffTypeList.as_view()),
    url(r'^hem/$', HemTypeList.as_view()),
    url(r'^back/$', BackTypeList.as_view()),
    url(r'^pocket/$', PocketTypeList.as_view()),
    url(r'^placket/$', PlacketTypeList.as_view()),
    url(r'^sleeve/$', SleeveTypeList.as_view()),
]

urlpatterns = [
    url(r'^collection/$', CollectionsListView.as_view()),
    url(r'^collection/(?P<pk>[0-9]+)/', include(collection_urls)),
    url(r'^components/', include(components)),
    url(r'^shirt_info/', ShirtInfoListView.as_view()),
    url(r'^size/$', SizesList.as_view()),
    url(r'^size/option/$', SizeOptionsList.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
