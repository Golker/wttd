from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Luca Bezerra', cpf='12345678901',
                    email='lucabezerra@gmail.com', phone='987654321')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """ Email subject should match 'Confirmação de inscrição' """
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """ Email sender should match 'lucabezerra@gmail.com' """
        expect = 'lucabezerra@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        """
        Email recipient should match 'lucabezerra@gmail.com' twice, as 'from'
         and 'to' roles.
        """
        expect = ['lucabezerra@gmail.com', 'lucabezerra@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Luca Bezerra', '12345678901', 'lucabezerra@gmail.com',
                    '987654321']

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
