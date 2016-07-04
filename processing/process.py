from time import time
import os

from PIL import Image, ImageChops
import numpy
import numexpr as ne

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
    result = exr_to_array(args[0], channels=('R', 'G', 'B', 'A'))
    if len(args) > 1:
        for arg in args[1:]:
            arg_array = exr_to_array(arg, channels=('R', 'G', 'B', 'A'))
            arg_mask = numpy.logical_or(arg_array[..., 0] > 0, arg_array[..., 1] > 0)
            result[arg_mask] = arg_array[arg_mask]

    return result


def compose_light(*sources):
    if len(sources) == 0:
        return None
    result = sources[0]
    for source in sources[1:]:
        result = Image.alpha_composite(result, source)
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
    img = None
    if isinstance(texture, basestring):
        extension = os.path.splitext(texture)[1]
        if extension == '.npy':
            return numpy.load(texture)

        img = Image.open(texture)
    else:
        img = texture

    arr = numpy.asarray(img).transpose(1, 0, 2)
    return arr[..., :3]


def create(texture, uv, lights, pre_shadows, tiling, post_shadows=[], buttons=None, buttons_shadow=None, AA=True):
    start = time()
    # op3
    lights_images = [Image.open(light) for light in lights]
    full_light = compose_light(*lights_images)

    # op4
    pre_shadow_images = [Image.open(shadow) for shadow in pre_shadows]
    full_shadow = compose_light(*pre_shadow_images)

    # op5: op4
    post_shadow_images = [Image.open(shadow) for shadow in post_shadows]
    for shadow in post_shadow_images:
        full_shadow = ImageChops.multiply(full_shadow, shadow)

    # op1
    full_uv = compose_uv(*uv)

    # op2: op1
    # uv = Image.fromarray((full_uv * 255.0).astype('uint8'), "RGBA")
    # if AA:
    #     size = uv.size
    #     uv = uv.resize((size[0] / 2, size[1] / 2), Image.LANCZOS)
    # alpha = uv.split()[-1]

    # op6
    texture_arr = load_texture(texture)

    # op7: op1+op6
    result = compose(full_uv, texture_arr, AA)

    # op8: op1+op6+op7
    if full_shadow is not None:
        result = ImageChops.multiply(result, full_shadow)

    result = overlay(full_light, result)

    # op9: op8
    if buttons is not None and buttons_shadow is not None:
        buttons_image = Image.open(buttons)
        buttons_shadow_image = Image.open(buttons_shadow)

        result.paste(buttons_image, mask=buttons_image)
        result.paste(buttons_shadow_image, mask=buttons_shadow_image)

    # op10: op9 + op2
    result = apply_srgb(result)
    # result.putalpha(alpha)
    print('renedered in %s' % (time() - start))
    return result
