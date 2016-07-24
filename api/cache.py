from backend.models import Fabric, FabricPrice
from processing.models import Texture


def get_latest_date(model):
    latest = model.objects.values_list('modified').latest('modified')
    return latest[0] if latest else None


def fabric_last_modified(*args, **kwargs):
    dates = map(lambda model: get_latest_date(model), [Fabric, FabricPrice, Texture])
    return max(dates)
