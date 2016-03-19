from django.conf.urls import url
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    url(r'^content-type-objects/$', staff_member_required(views.ContentTypeObjectList.as_view()), name='content_type_object_list'),
]
