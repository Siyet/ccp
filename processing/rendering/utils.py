import OpenEXR

import numpy
import Imath
import os
from PIL import Image

FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

CHANNELS = ('R', 'G', 'B', 'A')

class Repickable(object):
    def repick(self, bbox):
        self.bbox = bbox
        (x, y, x1, y1) = bbox
        self.values = self._source[x: x1, y: y1]

class Matrix(Repickable):
    def __init__(self, arr):
        size = arr.shape[:2]
        self.values = arr
        self.bbox = (0, 0, size[0], size[1])
        self._source = arr


class Submatrix(Repickable):
    def __init__(self, arr, mask=None):
        if mask is None:
            if len(arr.shape) > 2:
                mask = arr[..., arr.shape[2] - 1]
            else:
                mask = arr > 0
        indices = numpy.where(mask)
        x = [indices[0].min(), indices[0].max() + 1]
        y = [indices[1].min(), indices[1].max() + 1]
        # Using the smallest and largest x and y indices of nonzero elements,
        # we can find the desired rectangular bounds.
        # And don't forget to add 1 to the top bound to avoid the fencepost problem.
        self.values = arr[x[0]:x[1], y[0]:y[1]]
        self.bbox = (x[0], y[0], x[1], y[1])
        self._source = arr



def load_image(filename):
    extension = os.path.split(filename)[1]
    if extension in '.png':
        return Image.open(filename)
    elif extension in ('.npy', '.exr'):
        array = exr_to_array(filename)
        return image_from_array(array)
    else:
        return None


def image_from_array(array, channels=None):
    array = array * 255.0
    channels_count = len(channels) if channels else array.shape[2]
    real_channels = channels if channels else CHANNELS[:channels_count]
    if channels_count == 1:
        array = array.reshape(array.shape[:2])
        real_channels = ['L']
    else:
        array = array[..., :channels_count]
    return Image.fromarray(array.astype('uint8'), ''.join(real_channels))


def exr_to_array(exrfile, channels=None):
    global CHAN

    extension = os.path.splitext(exrfile)[1]
    if extension == '.npy':
        return numpy.load(exrfile)

    file = OpenEXR.InputFile(exrfile)
    dw = file.header()['dataWindow']

    channels = file.header()['channels'].keys() if channels is None else channels

    channels_list = list()
    for c in CHANNELS:
        if c in channels:
            channels_list.append(c)

    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    color_channels = file.channels(channels_list, FLOAT)

    channels_tuple = [numpy.fromstring(channel, dtype='f') for channel in color_channels]
    res = numpy.dstack(channels_tuple)
    res = res.reshape(size + (len(channels_tuple),))

    return res



def uv_to_image(arr):
    result = extend_uv_with_blue(arr) * 255.0
    return Image.fromarray(result.astype('uint8'), "RGB")


def extend_uv_with_blue(arr):
    sz = arr.shape[:2]
    blue = numpy.zeros(sz + (1,))
    result = numpy.dstack((arr, blue))
    return result


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))