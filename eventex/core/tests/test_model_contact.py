from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Luca Bezerra',
            slug='luca-bezerra',
            photo='http://hbn.link/hb-pic'
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker,
                                         kind=Contact.EMAIL,
                                         value='lucabezerra@gmail.com')
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker,
                                         kind=Contact.PHONE,
                                         value='987654321')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """ Contact kind should be limited to E or P """
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact.objects.create(speaker=self.speaker,
                                         kind=Contact.EMAIL,
                                         value='lucabezerra@gmail.com')
        self.assertEqual('lucabezerra@gmail.com', str(contact))
