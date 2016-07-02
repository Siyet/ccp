from process import create, compose
from PIL import Image
from time import time

import numpy

arr = numpy.load('media/composecache/uv/cache_uv_26ad9ae0-af73-4980-880c-fb8e7880daf3')
print(arr.shape)
exit()




texture = "B4382_blur_CC_noAO.jpg"

text_img = Image.open(texture)
compose(exr_to_array("BODY/BODY_UV_01.exr"), text_img, AA=True).save("comp.body.png")
exit()


front = {
    "textures": [texture],
    "tiling": 4,
    "uv" : ["BODY/BODY_UV_01.exr", "COLLAR/COLLAR_UV_10.exr", "CUFF/CUFF_UV_09.exr"],
    "lights" : ["BODY/BODY_LIGHT_01_v3.exr", "COLLAR/COLLAR_LIGHT_10_v3a.exr", "CUFF/CUFF_LIGHT_09_v3.exr"],
    "pre_shadows": [], #["BODY/BODY_AO_01_v3.exr", "COLLAR/COLLAR_AO_10_v3a.exr", "CUFF/CUFF_AO_09_v3.exr"],
    "post_shadows": [],
    "AA": True
}

body = {
    "textures": ["textures/F4140.png"],
    "tiling": 4,
    "uv" : ["BODY/BODY_UV_01.exr"],
    "lights" : ["BODY/BODY_LIGHT_01_v3.exr", "COLLAR/COLLAR_LIGHT_10_v3a.exr"],
    "pre_shadows": ["BODY/BODY_AO_01.exr", "COLLAR/COLLAR_AO_10_v3a.exr"],
    "post_shadows": [],
    "AA": True
}

cuff = {
    "textures": ["textures/F3543.png"],
    "tiling": 4,
    "uv" : ["CUFF/CUFF_UV_09.exr"],
    "lights" : ["CUFF/CUFF_LIGHT_09_v3.exr"],
    "pre_shadows": ["CUFF/CUFF_AO_09_v3.exr"],
    "post_shadows": [],
    "AA": True
}

collar = {
    "textures": ["textures/A4236.png"],
    "tiling": 8,
    "uv" : ["COLLAR/COLLAR_UV_10.exr"],
    "lights" : ["COLLAR/COLLAR_LIGHT_10_v3a.exr"],
    "pre_shadows": ["COLLAR/COLLAR_AO_10_v3a.exr"],
    "post_shadows": [],
    "AA": True
}

elems = [
    ('body', body),
    ('collar', collar),
    ('cuff', cuff)
]


for (title, elem) in elems:
     start = time()
     create(**elem)[0].save("%s.png" % title)
     print(title, time() - start)


body = Image.open("body.png")
collar = Image.open("collar.png")
cuff = Image.open("cuff.png")
body.paste(collar, mask=collar)
body.paste(cuff, mask=cuff)
body.save("diff.png")