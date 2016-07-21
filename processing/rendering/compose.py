from time import time
import os

from PIL import Image, ImageChops, ImageOps
import numpy as np
import numexpr as ne


def STMap(source, texture_arr, AA):
    # TODO: ensure cache
    source[..., 0] %= texture_arr.shape[0]
    source[..., 1] %= texture_arr.shape[1]

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
    A = np.asarray(a).astype(np.float32) / 255.0
    B = np.asarray(b).astype(np.float32) / 255.0
    result = overlay_arrays(A, B) * 255.0
    # convert back to image
    return Image.fromarray(result.astype('uint8'), a.mode)


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
    arr = np.asarray(img).astype('float32') / 255.0
    res = exr_to_srgb(arr)
    return res


def load_texture(texture):
    img = load_image(texture)
    arr = np.asarray(img)
    return arr[..., :3]


def load_image(image):
    if isinstance(image, basestring):
        extension = os.path.splitext(image)[1]
        if extension == '.npy':
            return np.load(image)

        result = Image.open(image)
    elif isinstance(image, np.ndarray):
        return image
    else:
        result = image

    if result.mode != "RGB":
        result = result.convert("RGB")
    return result


def load_uv(uv):
    if isinstance(uv, np.ndarray):
        return uv

    return np.load(uv)


def paste(source, image_info):
    if not image_info:
        return
    image = image_info['image']
    if not isinstance(image, Image.Image):
        image = Image.open(image)

    source.paste(image, image_info['position'], mask=image)


class Composer(object):
    @staticmethod
    def compose_uv(sources):
        base = np.load(sources[0].file.path)
        for source in sources[1:]:
            (x0, y0) = source.position[::-1]
            array = np.load(source.file.path)
            (x1, y1) = array.shape[:2]
            mask = np.logical_or(array[..., 0] > 0, array[..., 1] > 0)
            base[x0: x0 + x1, y0:y0 + y1][mask] = array[mask]
        return base

    @staticmethod
    def compose_light(sources):
        base = Image.open(sources[0].file.path)
        for source in sources[1:]:
            source_img = Image.open(source.file.path)
            base.paste(source_img, source.position, mask=source_img)

        return base.convert("RGB")

    @staticmethod
    def compose_alpha(sources):
        from PIL import ImageChops
        base = Image.open(sources[0].file.path)
        for source in sources[1:]:
            source_img = Image.open(source.file.path)
            layer = Image.new("L", base.size, 0)
            layer.paste(source_img, source.position)
            base = ImageChops.add(base, layer)

        return base

    @staticmethod
    def create(texture, uv, light=None, shadow=None, post_shadows=[], alpha=None, buttons=[], lower_stitches=[],
               upper_stitches=[], dickey=None, extra_details=[], base_layer=[], AA=True):

        texture_arr = load_texture(texture)

        result = STMap(uv, texture_arr, AA)

        paste(result, dickey)

        if shadow is not None:
            result = ImageChops.multiply(result, load_image(shadow))

        if light is not None:
            light = load_image(light)
            result = overlay(light, result)

        result = apply_srgb(result)

        for detail in extra_details:
            paste(result, detail)

        if alpha:
            result.putalpha(alpha)

        for stitches in lower_stitches:
            paste(result, stitches)

        for button in buttons:
            paste(result, button)

        for stitches in upper_stitches:
            paste(result, stitches)

        for shadow in post_shadows:
            paste(result, shadow)

        if base_layer:
            mask = result.split()[-1]
            mask = ImageOps.invert(mask)
            for layer in base_layer:
                result.paste(layer, (0, 0), mask=mask)

        return result
