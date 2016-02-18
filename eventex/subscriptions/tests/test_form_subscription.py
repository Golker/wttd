from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """ CPF must accept digits only """
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, code='digits', field='cpf')

    def test_cpf_has_11_digits(self):
        """ CPF must have 11 digits """
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, code='length', field='cpf')

    def test_name_must_be_capitalized(self):
        """ Name must have all words starting with a capital letter """
        form = self.make_validated_form(name='LUCA bezerra')

        self.assertEqual('Luca Bezerra', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """ Email is an optional field """
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """ Phone is an optional field """
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """ Email and phone are optional, but one must be informed """
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFormErrorCode(self, form, code, field):
        errors_list = form.errors.as_data()[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Luca Bezerra', cpf='12345678901',
                     email='lucabezerra@gmail.com', phone='987654321')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
