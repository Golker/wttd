from django.db import models
from django.shortcuts import resolve_url as r
from eventex.core.managers import KindQuerySet, PeriodManager


class Speaker(models.Model):
    name = models.CharField('Nome', max_length=255)
    slug = models.SlugField('Slug')
    photo = models.URLField('Foto')
    website = models.URLField('Website', blank=True)
    description = models.TextField('Descrição', blank=True)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)


class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'

    KINDS = (
        (EMAIL, 'Email'),
        (PHONE, 'Phone'),
    )
    speaker = models.ForeignKey('Speaker', verbose_name='palestrante')
    kind = models.CharField(verbose_name='tipo', max_length=1, choices=KINDS)
    value = models.CharField(verbose_name='valor', max_length=255)

    objects = KindQuerySet.as_manager()

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return self.value


class Talk(models.Model):
    title = models.CharField(verbose_name='Título', max_length=200)
    start = models.TimeField(verbose_name='Início', blank=True, null=True)
    description = models.TextField(verbose_name='Descrição', blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name='palestrantes',
                                      blank=True)

    objects = PeriodManager()

    class Meta:
        verbose_name = 'palestra'
        verbose_name_plural = 'palestras'

    def __str__(self):
        return self.title
