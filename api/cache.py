# coding: utf-8

import os

from backend.models import Fabric, FabricPrice
from processing.models import Texture
from rest_framework_extensions.key_constructor.constructors import DefaultListKeyConstructor
from rest_framework_extensions.key_constructor.bits import QueryParamsKeyBit

class TempFileToken(object):
    def __init__(self, path):
        self.path = path

    def __del__(self):
        if os.path.isfile(self.path):
            os.remove(self.path)


class ListKeyConstructor(DefaultListKeyConstructor):
    query_params = QueryParamsKeyBit()


def get_latest_date(model):
    try:
        latest = model.objects.values_list('modified').latest('modified')
        return latest[0] if latest else None
    except:
        return None


def fabric_last_modified(*args, **kwargs):
    dates = map(lambda model: get_latest_date(model), [Fabric, FabricPrice, Texture])
    dates = filter(None, dates)
    return max(dates)
