from core.constants import SEX
from backend.models import Collection
from .male import MaleShirtBuilder

from processing.models import CACHE_RESOLUTION

class ShirtBuilderFactory(object):
    @staticmethod
    def get_builder_for_shirt(shirt, projection, resolution=CACHE_RESOLUTION.full):
        try:
            collection_id = shirt['collection']
            collection = Collection.objects.get(pk=collection_id)
            sex = collection.sex
        except:
            sex = SEX.male

        if sex == SEX.male:
            return MaleShirtBuilder(shirt, projection, resolution)

        raise Exception("Builder not found for sex: %s" % sex)
