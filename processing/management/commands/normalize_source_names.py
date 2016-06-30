import re

from django.core.management import BaseCommand

from processing.models import ComposeSource, ButtonsSource


class Command(BaseCommand):
    def handle(self, *args, **options):
        compose_regexp = re.compile(r'(.+\_(%s)\_\d+)\_[^\.]+.exr' % "|".join(("AO", "UV", "LIGHTS")), re.I)
        buttons_regexp = re.compile(r'(.+(\d{2}|BODY(_SHADOW)?))\_((?!SHADOW).)*.exr', re.I)

        self.process_models(ComposeSource, ('ao', 'uv', 'light'), compose_regexp)
        self.process_models(ButtonsSource, ('ao', 'image'), buttons_regexp)


    def process_models(self, model, field_names, regexp, dry=False):
        for source in model.objects.all():
            changes = False
            for field_name in field_names:
                field = getattr(source, field_name)
                match = regexp.match(field.name)
                if match:
                    field.name = u'%s.EXR' % match.groups()[0]
                    changes = True

            if changes:
                source.save()

