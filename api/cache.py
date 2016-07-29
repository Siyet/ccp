import os

from backend.models import Fabric, FabricPrice
from processing.models import Texture


class TempFileToken(object):
    def __init__(self, path):
        self.path = path

    def __del__(self):
        if os.path.isfile(self.path):
            os.remove(self.path)


def get_latest_date(model):
    latest = model.objects.values_list('modified').latest('modified')
    return latest[0] if latest else None


def fabric_last_modified(*args, **kwargs):
    dates = map(lambda model: get_latest_date(model), [Fabric, FabricPrice, Texture])
    return max(dates)
