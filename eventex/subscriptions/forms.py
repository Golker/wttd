from django import forms
from django.core.exceptions import ValidationError
from eventex.subscriptions.models import Subscription
from eventex.subscriptions.validators import validate_cpf


class SubscriptionFormOld(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11, validators=[validate_cpf])
    email = forms.EmailField(label='Email', max_length=75, required=False)
    phone = forms.CharField(label='Telefone', max_length=20, required=False)


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'cpf', 'email', 'phone']

    # every field in a form has a method called clean_<field_name>
    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

    # the 'clean' method refers to the form as a whole;
    # must return a dictionary with all the form's data even if no data has
    # changed, otherwise, it'll replace cleaned_data with None
    def clean(self):
        # the father's clean() must be called because
        # it does other things as well
        self.cleaned_data = super().clean()
        if not self.cleaned_data.get('email') and \
           not self.cleaned_data.get('phone'):
            raise ValidationError('Informe seu e-mail ou telefone.')

        return self.cleaned_data
