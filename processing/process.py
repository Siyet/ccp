import OpenEXR
import Imath
from PIL import Image, ImageChops
import numpy
from time import time


def compose_arrays(source, texture_arr, AA):
    start = time()
    size = source.shape[:2]
    # add blue channel

    source[..., 0] = (source[..., 0] * size[0]) % texture_arr.shape[0]
    source[..., 1] = (source[..., 1] * size[1]) % texture_arr.shape[1]
    print("adjust", time()-start)
    source = source.astype('uint16')
    print("astype", time()-start)
    # one-line mapping!
    result = texture_arr[source[..., 0], source[..., 1]]
    print("mapping", time()-start)
    result = Image.fromarray(result, "RGB")
    print("image", time()-start)
    if AA:
        result = result.resize(tuple(x / 2 for x in result.size), Image.LANCZOS)
        print("resize", time()-start)

    return result

def compose(source, texture, AA):
    texture_arr = numpy.array(texture).transpose(1, 0, 2)
    return compose_arrays(source, texture_arr, AA)

def overlay_arrays(A, B):
    return numpy.where(B< 0.5,
                       2. * A* B,
                       1.0 - 2.0 * (1. - A) * (1. - B))


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


def gamma(src, value=2.2):
    src_array = numpy.asarray(src).astype('float32') / 255.
    src_array = numpy.power(src_array, value) * 255.0
    return Image.fromarray(src_array.astype('uint8'), src.mode)


def ungamma(src, value=2.2):
    src_array = numpy.asarray(src).astype('float32') / 255.
    src_array = numpy.power(src_array, 1.0 / value) * 255.0
    return Image.fromarray(src_array.astype('uint8'), src.mode)


def uv_to_image(arr):
    result = extend_uv_with_blue(arr) * 255.0
    return Image.fromarray(result.astype('uint8'), "RGB")

def extend_uv_with_blue(arr):
    sz = arr.shape[:2]
    blue = numpy.zeros(sz + (1,))
    result = numpy.dstack((arr, blue))
    return result


def image_from_exr(file, channels=('R', 'G', 'B', 'A')):
    array = exr_to_array(file, channels)
    array = array * 255.0
    return Image.fromarray(array.astype('uint8'), ''.join(channels))

def save_array_as_exr(image_array, filename, size=None):
    size = image_array.shape[:2] if size is None else size
    channels = (image_array[..., 0].ravel(), image_array[..., 1].ravel(), image_array[..., 2].ravel())
    (Rs, Gs, Bs) = [chan.tostring() for chan in channels]
    out = OpenEXR.OutputFile(filename, OpenEXR.Header(size[0], size[1]))
    out.writePixels({'R': Rs, 'G': Gs, 'B': Bs})

def save_image_as_exr(image, filename):
    image_array = numpy.asarray(image).astype('float32') / 255.
    save_array_as_exr(image_array, filename)


def exr_to_srgb(array):
    array = encode_to_srgb(array) * 255.
    present_channels = ["R", "G", "B", "A"][:array.shape[2]]
    channels = "".join(present_channels)
    return Image.fromarray(array.astype('uint8'), channels)


def encode_to_srgb(x):
    a = 0.055
    return numpy.where(x <= 0.0031308,
                 x * 12.92,
                 (1 + a) * pow(x, 1 / 2.4) - a)

def add_alpha_array(source, alpha_arr):
    source_arr = numpy.asarray(source)
    result = numpy.dstack((source_arr, alpha_arr))
    return Image.fromarray(result, "RGBA")

def add_alpha(source, alpha_donor):
    alpha_arr = numpy.asarray(alpha_donor)[..., 3]
    return add_alpha_array(source, alpha_arr)


def create(textures, uv, lights, pre_shadows, tiling, post_shadows=[], buttons=None, buttons_shadow=None, AA=True):

     # op3
    lights_images = [image_from_exr(light) for light in lights]
    full_light = compose_light(*lights_images )

    # op4
    pre_shadow_images = [image_from_exr(shadow) for shadow in pre_shadows]
    full_shadow = compose_light(*pre_shadow_images)

    # op5: op4
    post_shadow_images = [image_from_exr(shadow) for shadow in post_shadows]
    for shadow in post_shadow_images:
        full_shadow = ImageChops.multiply(full_shadow, shadow)


    # op1
    full_uv = compose_uv(*uv)

    # op2: op1
    uv = Image.fromarray((full_uv * 255.0).astype('uint8'), "RGBA")
    if AA:
        size = uv.size
        uv = uv.resize((size[0]/2, size[1]/2), Image.LANCZOS)
    alpha = uv.split()[-1]

    results = list()
    # op6
    for texture in textures:
        texture_img = Image.open(texture).convert("RGB")
        if tiling > 4: # TODO: proper resizing
            texture_img = texture_img.resize((texture_img.size[0] / 2, texture_img.size[1] / 2), Image.LANCZOS)

        # op7: op1+op6
        result = compose(full_uv, texture_img, AA)

        # op8: op1+op6+op7
        if full_shadow is not None:
            result = ImageChops.multiply(result, full_shadow.convert("RGB"))

        result = overlay(full_light.convert("RGB"), result)

        # op9: op8
        if buttons is not None and buttons_shadow is not None:
            buttons_image = Image.open(buttons)
            buttons_shadow_image = Image.open(buttons_shadow)

            result.paste(buttons_image, mask=buttons_image)
            result.paste(buttons_shadow_image, mask=buttons_shadow_image)

        # op10: op9 + op2
        result_array = numpy.asarray(result).astype('float32') / 255.
        result = exr_to_srgb(result_array)
        result.putalpha(alpha)
        results.append(result)

    return results