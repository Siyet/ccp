from time import time

from process import create, uv_to_image, exr_to_array
from utils import image_from_array
import numpy as np
from PIL import Image
from scipy import ndimage

# uv = np.load('/Users/cloud/dev/django/costumecode/media/composecache/uv/composesource_103_uv.npy')
# uv = ndimage.zoom(uv, [3./8, 3./8, 1], order=1)
# np.save('/Users/cloud/dev/django/costumecode/media/composecache/uv/composesource_103_uv_z.npy', uv)
# exit()

settings = {'AA': True, 'buttons_shadow': None,
            'uv': [u'/Users/cloud/dev/django/costumecode/media/composecache/uv/composesource_103_uv_z.npy'],
            'texture': u'/Users/cloud/dev/django/costumecode/media/textures/cache/A4631.jpg.npy',
            'buttons': None,
            'lights': [u'/Users/cloud/dev/django/costumecode/media/composecache/light/composesource_103_light_z.png'],
            'pre_shadows': [u'/Users/cloud/dev/django/costumecode/media/composecache/ao/composesource_103_ao_z.png'],
            'post_shadows': [],
            'tiling': 8L}
start = time()
res = create(**settings)
print(time() - start)
res.save("/tmp/result.png")
exit()
