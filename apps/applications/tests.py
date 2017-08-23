from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class ApplicationUnitTest(TestCase):
    def test_send_mail(self):
        from django.contrib.auth import get_user_model
        from django.conf import settings
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        user = get_user_model().objects.create_user('tst')
        self.client.force_login(user)
        self.client.get(reverse('applications:terminal-restart'))
