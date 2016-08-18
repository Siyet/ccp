from django.http.response import HttpResponse

from processing.rendering.builder import ShirtBuilder
from models import PROJECTION, CACHE_RESOLUTION
from api.serializers import ShirtDetailsSerializer
from backend.models import Shirt


def shirt(request, pk, *args, **kwargs):
    data = ShirtDetailsSerializer(instance=Shirt.objects.get(pk=pk)).data
    initials = data.get('initials', None)
    projection = request.GET.get("projection") or PROJECTION.front
    resolution = request.GET.get("resolution") or CACHE_RESOLUTION.preview
    bldr = ShirtBuilder(data, projection, resolution=resolution)
    response = HttpResponse(content_type="image/png")
    image = bldr.build_shirt()
    if initials:
        ShirtBuilder.add_initials(image, initials, projection, data['pocket'])
    image.save(response, "PNG")
    return response
