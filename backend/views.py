import json
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse, Http404, HttpResponse
from django.views.generic import View


class ContentTypeObjectList(View):

    def get(self, request, *args, **kwargs):
        try:
            content_type = ContentType.objects.get(pk=request.GET.get('pk'))
        except ContentType.DoesNotExist:
            raise Http404('DoesNotExist')
        result = [(x.pk, unicode(x)) for x in content_type.model_class().objects.all()]
        return HttpResponse(json.dumps(result), content_type='application/json')
