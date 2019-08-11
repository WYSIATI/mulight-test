from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from watch.models import Watch


import json


class WatchFunctionTests(APITestCase):
    def setUp(self):
        self.rolex = Watch.objects.create(name='Rolex', price=100,
                                          discount_base=3, discount_amount=200)
        self.mc = Watch.objects.create(name='Michael Kors', price=80,
                                       discount_base=2, discount_amount=120)
        self.swatch = Watch.objects.create(name='Swatch', price=50)
        self.casio = Watch.objects.create(name='Casio', price=30)

    def test_do_checkout(self):
        """Test do_checkout() api_view.
        """
        url = reverse('do_checkout')

        # empty list
        d1 = []
        response = self.client.post(url, d1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('price'), 0)

        # no discount condition triggered
        d2 = ['001', '001', '002', '003', '004']
        response = self.client.post(url, d2, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('price'), 360)

        # trigger one discount condition
        d3 = ['001', '001', '001', '003', '004']
        response = self.client.post(url, d3, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('price'), 280)

        # trigger one discount condition with module discount combination
        # number greater than one.
        d4 = ['001', '001', '001', '001', '004']
        response = self.client.post(url, d4, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('price'), 330)

        # two discount condition triggered
        d4 = ['001', '001', '001', '001', '002', '002']
        response = self.client.post(url, d4, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('price'), 420)

        # non-existing id
        d5 = ['005', '002']
        response = self.client.post(url, d5, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(json.loads(response.content).get('err_msg'))
