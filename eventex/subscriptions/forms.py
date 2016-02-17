from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'digits')

    if len(value) != 11:
        raise ValidationError('CPF deve conter 11 números', 'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11, validators=[validate_cpf])
    email = forms.EmailField(label='Email', max_length=75)
    phone = forms.CharField(label='Telefone', max_length=20)
