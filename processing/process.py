from time import time
import os

from PIL import Image, ImageChops, ImageOps
import numpy
import numexpr as ne
from scipy.misc import imresize
from utils import exr_to_array


def compose(source, texture_arr, AA):
    size = source.shape[:2]

    # TODO: ensure cache
    source[..., 0] %= texture_arr.shape[0]
    source[..., 1] %= texture_arr.shape[1]

    start = time()
    source = source.astype('uint16')  # TODO: store cache in uint16
    print('astype', time() - start)
    # one-line mapping!
    start = time()

    result = texture_arr[source[..., 0], source[..., 1]]
    print("mapping", time() - start)
    result = Image.fromarray(result, "RGB")
    if AA:
        start = time()
        result = result.resize(tuple(x / 2 for x in result.size), Image.LANCZOS)
        print("resize", time() - start)

    return result


def overlay_arrays(A, B):
    start = time()
    res = ne.evaluate("""where(
                            B < 0.5,
                            2. * A * B,
                            1.0 - 2.0 * (1. - A) * (1. - B)
                         )""")

    print("overlay", time() - start)
    return res


def overlay(a, b):
    # convert to arrays
    A = numpy.asarray(a).astype(numpy.float32) / 255.0
    B = numpy.asarray(b).astype(numpy.float32) / 255.0
    result = overlay_arrays(A, B) * 255.0
    # convert back to image
    return Image.fromarray(result.astype('uint8'), a.mode)


def compose_uv(*args):
    if len(args) == 0:
        return None
    result = exr_to_array(args[0], channels=('R', 'G'))
    if len(args) > 1:
        for arg in args[1:]:
            arg_array = exr_to_array(arg, channels=('R', 'G'))
            arg_mask = numpy.logical_or(arg_array[..., 0] > 0, arg_array[..., 1] > 0)
            result[arg_mask] = arg_array[arg_mask]

    return result





def uv_to_image(arr):
    result = extend_uv_with_blue(arr) * 255.0
    return Image.fromarray(result.astype('uint8'), "RGB")


def extend_uv_with_blue(arr):
    sz = arr.shape[:2]
    blue = numpy.zeros(sz + (1,))
    result = numpy.dstack((arr, blue))
    return result


def exr_to_srgb(array):
    array = encode_to_srgb(array) * 255.
    present_channels = ["R", "G", "B", "A"][:array.shape[2]]
    channels = "".join(present_channels)
    return Image.fromarray(array.astype('uint8'), channels)


def encode_to_srgb(x):
    a = 0.055
    return ne.evaluate("""where(
                            x <= 0.0031308,
                            x * 12.92,
                            (1 + a) * (x ** (1 / 2.4)) - a
                          )""")


def apply_srgb(img):
    arr = numpy.asarray(img).astype('float32') / 255.0
    res = exr_to_srgb(arr)
    return res


def load_texture(texture):
    img = load_image(texture)

    arr = numpy.asarray(img).transpose(1, 0, 2)
    return arr[..., :3]

def load_image(image):

    if isinstance(image, basestring):
        extension = os.path.splitext(image)[1]
        if extension == '.npy':
            return numpy.load(image)

        result = Image.open(image)
    else:
        result = image

    if result.mode != "RGB":
        result = result.convert("RGB")
    return result


def load_uv(uv):
    if isinstance(uv, numpy.ndarray):
        return uv

    return numpy.load(uv)

def create(texture, full_uv, full_light, full_shadow, post_shadows=[], alpha=None, buttons=[], base_layer=[], AA=True):
    full_light = load_image(full_light)
    # op6
    texture_arr = load_texture(texture)

    # op7: op1+op6
    result = compose(full_uv, texture_arr, AA)
    # op8: op1+op6+op7
    if full_shadow is not None:
        result = ImageChops.multiply(result, load_image(full_shadow))

    result = overlay(full_light, result)
    # op10: op9 + op2
    result = apply_srgb(result)
    if alpha:
        result.putalpha(alpha)

    for button in buttons:
        button_image = Image.open(button['image'])
        result.paste(button_image, button['position'], mask=button_image)

    for shadow in post_shadows:
        shadow_image = Image.open(shadow['image'])
        result.paste(shadow_image, shadow['position'], mask=shadow_image)

    if base_layer:
        mask = result.split()[-1]
        mask = ImageOps.invert(mask)
        for layer in base_layer:
            result.paste(layer, (0,0), mask=mask)

    return result
