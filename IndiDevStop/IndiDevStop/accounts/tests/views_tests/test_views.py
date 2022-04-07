from django.test import TestCase

class UserRegisterViewTests(TestCase):

    def test_register_view_status_code(self):
        response = self.client.get('/accounts/register/')
        self.assertEquals(response.status_code, 200)

    def test_register_view_template(self):
        response = self.client.get('/accounts/register/')
        self.assertTemplateUsed(response, 'register.html')