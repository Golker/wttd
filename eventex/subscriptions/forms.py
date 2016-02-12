from django import forms


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11)
    email = forms.EmailField(label='Email', max_length=75)
    phone = forms.CharField(label='Telefone', max_length=20)
