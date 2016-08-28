import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from .models import PageURL, Token

# Create your tests here.


class PageURLAPITests(TestCase):

    def setUp(self):
        self.factory = RequestFactory
        self.user = User.objects.create_user(
            username='tester', email='tester@example.com', password='mypass')
        self.token = Token.objects.create(user=self.user).uuid
        self.url = "http://google.com"
        self.create_url = reverse('api-create')


    def test_create_url(self):
        api_req = {"long_url": self.url, "apikey": self.token}
        response = self.client.post(self.create_url, api_req)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)


    def test_create_pageurl(self):
        pageurl = PageURL.objects.create(
            long_url=self.url,
            author=self.user,
        )
        self.assertIsInstance(pageurl.__str__(), str)
