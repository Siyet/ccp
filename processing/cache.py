from .utils import Submatrix, exr_to_array
from tempfile import TemporaryFile

class CacheBuilder(object):
    def create_cache(self, instance, fields, cache_model):
        for field in fields:
            image = getattr(instance, field, None)
            if not image:
                continue
            array = exr_to_array(image.file)
            submatrix = Submatrix(array)
            cache = cache_model(bounding_box=submatrix.bbox, source_field=field)
            outfile = TemporaryFile()
            submatrix.values.save.tofile(outfile)
            

