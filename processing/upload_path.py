from django.utils.deconstruct import deconstructible


@deconstructible
class UploadComposingSource(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        return (self.path % (instance._meta.model_name, filename)).encode('utf-8')


@deconstructible
class UploadComposeCache(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        return (self.path % (instance.field_name, filename)).encode('utf-8')
