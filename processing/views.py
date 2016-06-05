from django.views.generic import View
from django.http.response import HttpResponse

def image(request):
    # ... create/load image here ...
    # serialize to HTTP response
    response = HttpResponse(content_type="image/png")
    return response