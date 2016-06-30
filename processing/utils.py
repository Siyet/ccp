import numpy
import OpenEXR
import Imath

FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

class Submatrix(object):
    def __init__(self, arr):
        mask = arr[..., 3] > 0
        indices = numpy.where(mask)
        x = [indices[0].min(), indices[0].max()]
        y = [indices[1].min(), indices[1].max()]
        # Using the smallest and largest x and y indices of nonzero elements,
        # we can find the desired rectangular bounds.
        # And don't forget to add 1 to the top bound to avoid the fencepost problem.
        self.values = arr[x[0]:x[1], y[0]:y[1]]
        self.bbox = (x[0], y[0], x[1]-x[0], y[1] - y[0])


def exr_to_array(exrfile, channels=None):
    global CHAN

    file = OpenEXR.InputFile(exrfile)
    dw = file.header()['dataWindow']

    channels = file.header()['channels'].keys() if channels is None else channels

    channels_list = list()
    for c in ('R', 'G', 'B', 'A'):
        if c in channels:
            channels_list.append(c)

    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    color_channels = file.channels(channels_list, FLOAT)

    channels_tuple = [numpy.fromstring(channel, dtype='f') for channel in color_channels]
    res = numpy.dstack(channels_tuple)
    res = res.reshape(size + (len(channels_tuple),))

    return res
