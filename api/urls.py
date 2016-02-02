from django.conf.urls import url, include
from api.views import CollectionsListView, ShirtInfoListView, SizeOptionsList, SizesList

urlpatterns = [
    url(r'^collection/', CollectionsListView.as_view()),
    url(r'^shirt_info/', ShirtInfoListView.as_view()),
    url(r'^size/', SizesList.as_view()),
    url(r'^size_option/', SizeOptionsList.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
