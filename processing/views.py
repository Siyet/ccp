from django.views.generic import View
from django.http.response import HttpResponse
from process import compose_shirt

def image(request):
    # ... create/load image here ...
    # serialize to HTTP response
    response = HttpResponse(content_type="image/png")
    image = compose_shirt()
    image.save(response, "PNG")
    return response