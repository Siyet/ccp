from PIL import Image, ImageOps, ImageColor

class MapIconProcessor(object):

    def __init__(self, *args, **kwargs):
        self.color = ImageColor.getrgb(kwargs.get("color", "#FF0000"))
        self.alpha = kwargs.get("alpha", 1.0)

    def process(self, image):
        source = image.getdata()
        gs = ImageOps.grayscale(image)
        data = gs.getdata()
        extrema = gs.getextrema()
        multiplier = 255.0/(extrema[1]-extrema[0])
        result = list()
        for i in range(len(data)):
            pixel = list()
            for j in range(3):
                color = 255.0 -multiplier*(255.0-data[i])/255.0*(255.0-self.color[j])
                pixel.append(int(color))

            result.append(tuple(pixel + [int(source[i][3]*self.alpha)]))

        res = Image.new("RGBA", image.size)
        res.putdata(result)
        return res