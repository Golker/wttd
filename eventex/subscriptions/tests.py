from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """ GET /inscricao/ must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use subscriptions/subscription_form.html """
        self.assertTemplateUsed(self.response,
                                'subscriptions/subscription_form.html')

    def test_html(self):
        """ HTML must contain input tags """
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)  # one extra due to csrf
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """ HTML must contain CSRF token """
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have subscription form """
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'],
                                 list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Luca Bezerra', cpf='12345678901',
                    email='lucabezerra@gmail.com', phone='987654321')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """ Valid POST should redirect to /inscricao/ """
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        """ Email should be sent on clicking the submit button """
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        """ Email subject should match 'Confirmação de inscrição' """
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        """ Email sender should match 'contato@eventex.com.br' """
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        """
            Email recipient should match 'lucabezerra@gmail.com' and
            'contato@eventex.com.br'
        """
        email = mail.outbox[0]
        expect = ['lucabezerra@gmail.com', 'contato@eventex.com.br']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Luca Bezerra', email.body)


class SubscribeInvalidPost(TestCase):

    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response,
                                'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = dict(name='Luca Bezerra', cpf='12345678901',
                    email='lucabezerra@gmail.com', phone='987654321')
        self.response = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')
