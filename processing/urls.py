from django.conf.urls import url
from django.views.generic import TemplateView

from .views import image

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^image/$', image, name='image')
]