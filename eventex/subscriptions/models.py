from django.db import models
from django.shortcuts import resolve_url as r
from eventex.subscriptions.validators import validate_cpf


class Subscription(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=100)
    cpf = models.CharField(verbose_name='CPF', max_length=11,
                           validators=[validate_cpf])
    email = models.EmailField(verbose_name='E-mail', max_length=75, blank=True)
    phone = models.CharField(verbose_name='Telefone', max_length=20, blank=True)
    created_at = models.DateTimeField(verbose_name='Criado em',
                                      auto_now_add=True)
    paid = models.BooleanField(verbose_name='Pago', default=False)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('subscriptions:detail', self.pk)
