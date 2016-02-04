# coding: UTF-8

from django.db import models

class ComposingSource(models.Model):

    type = models.CharField(u'Тип', max_length=10, choices=(
        ('EXR', u'UV (в формате EXR)'),
        ('LIGHT', u'Свет (png)'),
        ('SHADOW', u'Тень (png)'),
        ('TEXTURE', u'Текстура')
    ))
    file = models.FileField(u'Файл', upload_to='sources')

    class Meta:
        verbose_name = u'Исходник'
        verbose_name_plural = u'Исходники для композа'

    def __unicode__(self):
        return self.get_type_display()
