import OpenEXR
import Imath
from PIL import Image, ImageChops
import array

from .models import ComposingSource

FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

def to_png(exrfile, pngfile):
    file = OpenEXR.InputFile(exrfile)
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    (R, G, B, A) = [array.array('f', file.channel(Chan, FLOAT)).tolist() for Chan in ("R", "G", "B", "A")]
    bytes = [(int(round(255*r)),int(round(255*g)),int(round(255*b)),int(round(255*a))) for (r, g, b, a) in zip(R,G,B,A)]
    img = Image.new('RGBA', size)
    img.putdata(bytes)

    img.save(pngfile)


def to_jpg(exrfile, jpgfile):
    file = OpenEXR.InputFile(exrfile)
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    rgbf = [Image.fromstring("F", size, file.channel(c, pt)) for c in "RGB"]

    extrema = [im.getextrema() for im in rgbf]
    darkest = min([lo for (lo, hi) in extrema])
    lighest = max([hi for (lo, hi) in extrema])
    scale = 255 / (lighest - darkest)

    def normalize_0_255(v):
        return (v * scale) + darkest

    rgb8 = [im.point(normalize_0_255).convert("L") for im in rgbf]
    Image.merge("RGB", rgb8).save(jpgfile)

def compose_shirt():

    source_file = ComposingSource.objects.filter(type='EXR').first().file
    source = OpenEXR.InputFile(source_file.path)

    shadow_file = ComposingSource.objects.filter(type='SHADOW').first().file
    shadow = Image.open(shadow_file.path)

    light_file = ComposingSource.objects.filter(type='LIGHT').first().file
    light = Image.open(light_file.path)

    texture_file = ComposingSource.objects.filter(type='TEXTURE').first().file
    texture = Image.open(texture_file.path)

    dw = source.header()['dataWindow']
    sz = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    (R, G, A) = [array.array('f', source.channel(Chan, FLOAT)).tolist() for Chan in ("R", "G", "A")]
    zipped = zip(R,G,A)

    texture_pxls = texture.load()
    texture_sz = texture.size

    result = Image.new("RGBA", sz, (0, 0, 0, 1))
    result_pxls = result.load()

    for (i, (r, g, a)) in enumerate(zipped):
        if a == 0:
            continue
        x, y = round(r * texture_sz[0]), round((1.0 - g) * texture_sz[1] - 1)
        px = texture_pxls[x, y]
        result_pxls[i % sz[0], i / sz[0]] = (px[0], px[1], px[2], int(round(a * 255)))

    result = ImageChops.multiply(result, shadow)
    result = ImageChops.add(result, light)
    return result