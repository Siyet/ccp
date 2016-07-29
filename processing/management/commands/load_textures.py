# coding: utf-8

import sys

from django.core.management import BaseCommand
from django.core.files.base import ContentFile

from os import listdir, path
from os.path import isfile, join

from PIL import Image

from processing.models import Texture
from backend.models import Fabric
from io import BytesIO

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('folder', type=str)

    def handle(self, *args, **options):
        folder = options['folder']
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        i = 0
        count = len(files)
        sys.stdout.write('\n')
        for texture_file in files:
            i += 1
            texture_name, extension = path.splitext(texture_file)
            if not texture_name or not extension:
                continue

            texture = Texture(
                tiling=Texture.TILING.frequent,
                needs_shadow=True
            )
            buffer = BytesIO()

            image = Image.open(path.join(folder, texture_file))
            image.save(buffer, 'png')
            buffer.flush()

            texture.texture.save(texture_name + '.png', ContentFile(buffer.getvalue()))
            fabric = Fabric.objects.filter(code=texture_name).first()
            if fabric:
                fabric.texture = texture
                fabric.save()
            sys.stdout.write("\rprocessed (%s/%s)" % (i, count))
            sys.stdout.flush()
        sys.stdout.write('\n')
        sys.stdout.flush()
        print("cleanup...")
        Texture.objects.filter(fabric=None).delete()




